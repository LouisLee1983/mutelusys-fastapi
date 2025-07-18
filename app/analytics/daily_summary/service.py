from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, text
from decimal import Decimal
import json

from .models import (
    DailySalesSummary, 
    DailyAdPerformance, 
    DailyUserBehavior, 
    DailyProductPerformance
)
from app.order.models import Order, OrderItem, OrderPayment
from app.customer.models import Customer
from app.product.models import Product, ProductCategory
from app.analytics.user_behavior_log.models import UserBehaviorLog
from app.payment.transaction.models import PaymentTransaction


class DailySummaryService:
    """每日数据汇总服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_daily_sales_summary(self, target_date: date) -> DailySalesSummary:
        """生成每日销售汇总数据"""
        
        # 检查是否已存在该日期的数据
        existing = self.db.query(DailySalesSummary).filter(
            DailySalesSummary.report_date == target_date
        ).first()
        
        if existing:
            # 更新现有数据
            self._update_sales_summary(existing, target_date)
            return existing
        
        # 创建新的汇总数据
        summary = DailySalesSummary(report_date=target_date)
        self._calculate_sales_metrics(summary, target_date)
        
        self.db.add(summary)
        self.db.commit()
        self.db.refresh(summary)
        
        return summary
    
    def _calculate_sales_metrics(self, summary: DailySalesSummary, target_date: date):
        """计算销售指标"""
        
        # 获取当日订单数据
        start_date = datetime.combine(target_date, datetime.min.time())
        end_date = datetime.combine(target_date, datetime.max.time())
        
        # 基础订单统计
        orders_query = self.db.query(Order).filter(
            and_(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['PAID', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'COMPLETED'])
            )
        )
        
        orders = orders_query.all()
        
        # 计算基础指标
        summary.total_orders = len(orders)
        summary.total_revenue = sum(order.total_amount or 0 for order in orders)
        summary.total_items_sold = sum(
            self.db.query(func.sum(OrderItem.quantity)).filter(
                OrderItem.order_id == order.id
            ).scalar() or 0 
            for order in orders
        )
        
        if summary.total_orders > 0:
            summary.avg_order_value = summary.total_revenue / summary.total_orders
        
        # 客户统计
        customer_ids = {order.customer_id for order in orders if order.customer_id}
        summary.total_customers = len(customer_ids)
        
        # 新客户统计 (注册日期在目标日期)
        new_customers = self.db.query(Customer).filter(
            and_(
                func.date(Customer.created_at) == target_date,
                Customer.id.in_(customer_ids)
            )
        ).count()
        summary.new_customers = new_customers
        summary.returning_customers = summary.total_customers - new_customers
        
        # 退款统计
        refund_data = self.db.query(
            func.count(Order.id).label('refund_orders'),
            func.sum(Order.total_amount).label('refund_amount')
        ).filter(
            and_(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status == 'REFUNDED'
            )
        ).first()
        
        summary.refund_orders = refund_data.refund_orders or 0
        summary.refund_amount = refund_data.refund_amount or 0
        
        # 按维度分组统计
        summary.by_currency = self._get_sales_by_currency(orders)
        summary.by_country = self._get_sales_by_country(orders)
        summary.by_payment_method = self._get_sales_by_payment_method(orders)
        
        # 计算转化率 (需要结合用户行为数据)
        total_sessions = self.db.query(func.count(func.distinct(UserBehaviorLog.session_id))).filter(
            func.date(UserBehaviorLog.created_at) == target_date
        ).scalar() or 0
        
        if total_sessions > 0:
            summary.conversion_rate = Decimal(summary.total_orders) / Decimal(total_sessions)
    
    def _get_sales_by_currency(self, orders: List[Order]) -> Dict[str, Any]:
        """按货币统计销售数据"""
        currency_stats = {}
        for order in orders:
            currency = order.currency_code or 'USD'
            if currency not in currency_stats:
                currency_stats[currency] = {
                    'orders': 0,
                    'revenue': 0,
                    'avg_order_value': 0
                }
            currency_stats[currency]['orders'] += 1
            currency_stats[currency]['revenue'] += float(order.total_amount or 0)
        
        # 计算平均值
        for currency, stats in currency_stats.items():
            if stats['orders'] > 0:
                stats['avg_order_value'] = stats['revenue'] / stats['orders']
        
        return currency_stats
    
    def _get_sales_by_country(self, orders: List[Order]) -> Dict[str, Any]:
        """按国家统计销售数据"""
        country_stats = {}
        for order in orders:
            country = order.shipping_country or 'Unknown'
            if country not in country_stats:
                country_stats[country] = {
                    'orders': 0,
                    'revenue': 0,
                    'customers': set()
                }
            country_stats[country]['orders'] += 1
            country_stats[country]['revenue'] += float(order.total_amount or 0)
            if order.customer_id:
                country_stats[country]['customers'].add(str(order.customer_id))
        
        # 转换set为count
        for country, stats in country_stats.items():
            stats['customers'] = len(stats['customers'])
        
        return country_stats
    
    def _get_sales_by_payment_method(self, orders: List[Order]) -> Dict[str, Any]:
        """按支付方式统计销售数据"""
        payment_stats = {}
        
        for order in orders:
            # 获取订单的支付方式
            payment = self.db.query(OrderPayment).filter(
                OrderPayment.order_id == order.id
            ).first()
            
            payment_type = payment.payment_type if payment else 'Unknown'
            
            if payment_type not in payment_stats:
                payment_stats[payment_type] = {
                    'orders': 0,
                    'revenue': 0,
                    'success_rate': 0
                }
            payment_stats[payment_type]['orders'] += 1
            payment_stats[payment_type]['revenue'] += float(order.total_amount or 0)
        
        return payment_stats
    
    def generate_daily_user_behavior(self, target_date: date) -> DailyUserBehavior:
        """生成每日用户行为汇总数据"""
        
        # 检查是否已存在
        existing = self.db.query(DailyUserBehavior).filter(
            DailyUserBehavior.report_date == target_date
        ).first()
        
        if existing:
            self._update_user_behavior_summary(existing, target_date)
            return existing
        
        # 创建新的汇总数据
        behavior = DailyUserBehavior(report_date=target_date)
        self._calculate_user_behavior_metrics(behavior, target_date)
        
        self.db.add(behavior)
        self.db.commit()
        self.db.refresh(behavior)
        
        return behavior
    
    def _calculate_user_behavior_metrics(self, behavior: DailyUserBehavior, target_date: date):
        """计算用户行为指标"""
        
        # 获取当日行为日志
        logs_query = self.db.query(UserBehaviorLog).filter(
            func.date(UserBehaviorLog.created_at) == target_date
        )
        
        # 基础统计
        behavior.total_sessions = self.db.query(
            func.count(func.distinct(UserBehaviorLog.session_id))
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date
        ).scalar() or 0
        
        behavior.unique_visitors = self.db.query(
            func.count(func.distinct(UserBehaviorLog.customer_id))
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.customer_id.isnot(None)
        ).scalar() or 0
        
        behavior.page_views = logs_query.filter(
            UserBehaviorLog.behavior_type == 'VIEW'
        ).count()
        
        behavior.cart_additions = logs_query.filter(
            UserBehaviorLog.behavior_type == 'ADD_TO_CART'
        ).count()
        
        # 热门内容统计
        behavior.top_viewed_products = self._get_top_viewed_products(target_date)
        behavior.top_search_keywords = self._get_top_search_keywords(target_date)
        behavior.top_pages = self._get_top_pages(target_date)
        
        # 按维度分组
        behavior.by_device_type = self._get_behavior_by_device(target_date)
        behavior.by_traffic_source = self._get_behavior_by_source(target_date)
        behavior.by_country = self._get_behavior_by_country(target_date)
    
    def _get_top_viewed_products(self, target_date: date, limit: int = 10) -> List[Dict]:
        """获取热门浏览商品"""
        result = self.db.query(
            UserBehaviorLog.object_id,
            func.count(UserBehaviorLog.id).label('view_count')
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.behavior_type == 'VIEW',
            UserBehaviorLog.object_type == 'product'
        ).group_by(
            UserBehaviorLog.object_id
        ).order_by(
            func.count(UserBehaviorLog.id).desc()
        ).limit(limit).all()
        
        top_products = []
        for item in result:
            product = self.db.query(Product).filter(Product.id == item.object_id).first()
            if product:
                top_products.append({
                    'product_id': str(item.object_id),
                    'product_name': product.name,
                    'view_count': item.view_count
                })
        
        return top_products
    
    def _get_top_search_keywords(self, target_date: date, limit: int = 10) -> List[Dict]:
        """获取热门搜索词"""
        # 从行为日志的action_details中提取搜索词
        search_logs = self.db.query(UserBehaviorLog).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.behavior_type == 'SEARCH'
        ).all()
        
        keyword_counts = {}
        for log in search_logs:
            if log.action_details and isinstance(log.action_details, dict):
                keyword = log.action_details.get('keyword', '').strip()
                if keyword:
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # 排序并取前N个
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        return [{'keyword': k, 'count': v} for k, v in sorted_keywords]
    
    def _get_top_pages(self, target_date: date, limit: int = 10) -> List[Dict]:
        """获取热门页面"""
        result = self.db.query(
            UserBehaviorLog.page_url,
            func.count(UserBehaviorLog.id).label('view_count')
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.behavior_type == 'VIEW'
        ).group_by(
            UserBehaviorLog.page_url
        ).order_by(
            func.count(UserBehaviorLog.id).desc()
        ).limit(limit).all()
        
        return [{'page_url': item.page_url, 'view_count': item.view_count} for item in result]
    
    def _get_behavior_by_device(self, target_date: date) -> Dict[str, Any]:
        """按设备类型统计行为"""
        result = self.db.query(
            UserBehaviorLog.device_type,
            func.count(func.distinct(UserBehaviorLog.session_id)).label('sessions'),
            func.count(UserBehaviorLog.id).label('total_actions')
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date
        ).group_by(
            UserBehaviorLog.device_type
        ).all()
        
        device_stats = {}
        for item in result:
            device_type = item.device_type or 'Unknown'
            device_stats[device_type] = {
                'sessions': item.sessions,
                'total_actions': item.total_actions
            }
        
        return device_stats
    
    def _get_behavior_by_source(self, target_date: date) -> Dict[str, Any]:
        """按流量来源统计行为"""
        result = self.db.query(
            UserBehaviorLog.referrer_url,
            func.count(func.distinct(UserBehaviorLog.session_id)).label('sessions')
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date
        ).group_by(
            UserBehaviorLog.referrer_url
        ).all()
        
        source_stats = {}
        for item in result:
            # 简单分类流量来源
            referrer = item.referrer_url or 'Direct'
            if 'google' in referrer.lower():
                source = 'Google'
            elif 'facebook' in referrer.lower():
                source = 'Facebook'
            elif 'instagram' in referrer.lower():
                source = 'Instagram'
            elif referrer == 'Direct':
                source = 'Direct'
            else:
                source = 'Other'
            
            source_stats[source] = source_stats.get(source, 0) + item.sessions
        
        return source_stats
    
    def _get_behavior_by_country(self, target_date: date) -> Dict[str, Any]:
        """按国家统计行为 (基于IP地址解析)"""
        # 这里需要实现IP地址到国家的映射
        # 暂时返回空数据，实际使用时需要集成IP地理位置服务
        return {}
    
    def generate_daily_product_performance(self, target_date: date) -> List[DailyProductPerformance]:
        """生成每日商品表现汇总数据"""
        
        # 获取所有有活动的商品ID
        product_ids = set()
        
        # 从用户行为日志中获取有浏览的商品
        viewed_products = self.db.query(
            func.distinct(UserBehaviorLog.object_id)
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.behavior_type == 'VIEW',
            UserBehaviorLog.object_type == 'product'
        ).all()
        
        product_ids.update([str(p[0]) for p in viewed_products if p[0]])
        
        # 从订单中获取有销售的商品
        sold_products = self.db.query(
            func.distinct(OrderItem.product_id)
        ).join(Order).filter(
            func.date(Order.created_at) == target_date,
            Order.status.in_(['PAID', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'COMPLETED'])
        ).all()
        
        product_ids.update([str(p[0]) for p in sold_products if p[0]])
        
        # 为每个商品生成表现数据
        performances = []
        for product_id in product_ids:
            performance = self._generate_product_performance(product_id, target_date)
            if performance:
                performances.append(performance)
        
        return performances
    
    def _generate_product_performance(self, product_id: str, target_date: date) -> Optional[DailyProductPerformance]:
        """生成单个商品的表现数据"""
        
        # 检查是否已存在
        existing = self.db.query(DailyProductPerformance).filter(
            DailyProductPerformance.report_date == target_date,
            DailyProductPerformance.product_id == product_id
        ).first()
        
        if existing:
            return self._update_product_performance(existing, target_date)
        
        # 获取商品信息
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        
        performance = DailyProductPerformance(
            report_date=target_date,
            product_id=product_id,
            product_name=product.name,
            sku_code=product.sku_code
        )
        
        # 计算各项指标
        self._calculate_product_metrics(performance, target_date)
        
        self.db.add(performance)
        self.db.commit()
        self.db.refresh(performance)
        
        return performance
    
    def _calculate_product_metrics(self, performance: DailyProductPerformance, target_date: date):
        """计算商品指标"""
        
        product_id = performance.product_id
        
        # 浏览数据
        performance.views = self.db.query(UserBehaviorLog).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.behavior_type == 'VIEW',
            UserBehaviorLog.object_type == 'product',
            UserBehaviorLog.object_id == product_id
        ).count()
        
        performance.unique_views = self.db.query(
            func.count(func.distinct(UserBehaviorLog.customer_id))
        ).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.behavior_type == 'VIEW',
            UserBehaviorLog.object_type == 'product',
            UserBehaviorLog.object_id == product_id
        ).scalar() or 0
        
        # 加购数据
        performance.cart_additions = self.db.query(UserBehaviorLog).filter(
            func.date(UserBehaviorLog.created_at) == target_date,
            UserBehaviorLog.behavior_type == 'ADD_TO_CART',
            UserBehaviorLog.object_type == 'product',
            UserBehaviorLog.object_id == product_id
        ).count()
        
        # 销售数据
        sales_data = self.db.query(
            func.count(OrderItem.id).label('purchases'),
            func.sum(OrderItem.quantity).label('quantity_sold'),
            func.sum(OrderItem.final_price).label('revenue')
        ).join(Order).filter(
            func.date(Order.created_at) == target_date,
            OrderItem.product_id == product_id,
            Order.status.in_(['PAID', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'COMPLETED'])
        ).first()
        
        performance.purchases = sales_data.purchases or 0
        performance.quantity_sold = int(sales_data.quantity_sold or 0)
        performance.revenue = sales_data.revenue or 0
        
        if performance.quantity_sold > 0:
            performance.avg_selling_price = performance.revenue / performance.quantity_sold
        
        # 转化率计算
        if performance.views > 0:
            performance.view_to_cart_rate = Decimal(performance.cart_additions) / Decimal(performance.views)
            performance.overall_conversion_rate = Decimal(performance.purchases) / Decimal(performance.views)
        
        if performance.cart_additions > 0:
            performance.cart_to_purchase_rate = Decimal(performance.purchases) / Decimal(performance.cart_additions)
    
    def _update_sales_summary(self, summary: DailySalesSummary, target_date: date):
        """更新现有销售汇总数据"""
        self._calculate_sales_metrics(summary, target_date)
        summary.updated_at = datetime.utcnow()
        self.db.commit()
    
    def _update_user_behavior_summary(self, behavior: DailyUserBehavior, target_date: date):
        """更新现有用户行为汇总数据"""
        self._calculate_user_behavior_metrics(behavior, target_date)
        behavior.updated_at = datetime.utcnow()
        self.db.commit()
    
    def _update_product_performance(self, performance: DailyProductPerformance, target_date: date):
        """更新现有商品表现数据"""
        self._calculate_product_metrics(performance, target_date)
        performance.updated_at = datetime.utcnow()
        self.db.commit()
        return performance
    
    def generate_all_daily_summaries(self, target_date: Optional[date] = None):
        """生成所有日常汇总数据"""
        if target_date is None:
            target_date = date.today() - timedelta(days=1)  # 默认生成昨天的数据
        
        try:
            # 生成销售汇总
            sales_summary = self.generate_daily_sales_summary(target_date)
            print(f"Generated sales summary for {target_date}")
            
            # 生成用户行为汇总
            behavior_summary = self.generate_daily_user_behavior(target_date)
            print(f"Generated user behavior summary for {target_date}")
            
            # 生成商品表现汇总
            product_performances = self.generate_daily_product_performance(target_date)
            print(f"Generated {len(product_performances)} product performance records for {target_date}")
            
            return {
                'date': target_date,
                'sales_summary': sales_summary,
                'behavior_summary': behavior_summary,
                'product_performances': len(product_performances)
            }
            
        except Exception as e:
            print(f"Error generating daily summaries for {target_date}: {e}")
            self.db.rollback()
            raise