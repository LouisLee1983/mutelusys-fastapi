from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from app.core.dependencies import get_db
from app.admin.dependencies import get_current_admin_user
from app.security.models import User
from .models import (
    DailySalesSummary, 
    DailyAdPerformance, 
    DailyUserBehavior, 
    DailyProductPerformance
)
from .schema import (
    DailySalesSummaryResponse,
    DailyAdPerformanceResponse,
    DailyUserBehaviorResponse,
    DailyProductPerformanceResponse,
    DailySummaryRequest,
    DailySummaryResponse,
    DateRangeRequest,
    SalesReportResponse,
    UserBehaviorReportResponse,
    ProductPerformanceReportResponse,
    AdPerformanceReportResponse,
    DashboardSummaryResponse
)
from .service import DailySummaryService

router = APIRouter(prefix="/daily-summary")


@router.post("/generate", response_model=DailySummaryResponse)
async def generate_daily_summary(
    request: DailySummaryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """生成每日数据汇总"""
    service = DailySummaryService(db)
    target_date = request.target_date or (date.today() - timedelta(days=1))
    
    try:
        result = service.generate_all_daily_summaries(target_date)
        
        # 获取生成的数据
        sales_summary = db.query(DailySalesSummary).filter(
            DailySalesSummary.report_date == target_date
        ).first()
        
        behavior_summary = db.query(DailyUserBehavior).filter(
            DailyUserBehavior.report_date == target_date
        ).first()
        
        if not sales_summary or not behavior_summary:
            raise HTTPException(status_code=500, detail="Failed to generate summary data")
        
        return DailySummaryResponse(
            date=target_date,
            sales_summary=DailySalesSummaryResponse.from_orm(sales_summary),
            behavior_summary=DailyUserBehaviorResponse.from_orm(behavior_summary),
            product_performances_count=result['product_performances'],
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating daily summary: {str(e)}")


@router.get("/sales", response_model=SalesReportResponse)
async def get_sales_report(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取销售报表"""
    
    # 获取日期范围内的销售汇总数据
    summaries = db.query(DailySalesSummary).filter(
        and_(
            DailySalesSummary.report_date >= start_date,
            DailySalesSummary.report_date <= end_date
        )
    ).order_by(DailySalesSummary.report_date).all()
    
    if not summaries:
        raise HTTPException(status_code=404, detail="No sales data found for the specified date range")
    
    # 计算汇总指标
    total_orders = sum(s.total_orders for s in summaries)
    total_revenue = sum(s.total_revenue for s in summaries)
    total_customers = sum(s.total_customers for s in summaries)
    avg_conversion_rate = sum(s.conversion_rate for s in summaries) / len(summaries) if summaries else 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # 计算趋势数据
    trends = _calculate_sales_trends(summaries)
    
    return SalesReportResponse(
        date_range={"start_date": start_date, "end_date": end_date},
        total_orders=total_orders,
        total_revenue=total_revenue,
        avg_order_value=avg_order_value,
        total_customers=total_customers,
        conversion_rate=avg_conversion_rate,
        daily_data=[DailySalesSummaryResponse.from_orm(s) for s in summaries],
        trends=trends
    )


@router.get("/user-behavior", response_model=UserBehaviorReportResponse)
async def get_user_behavior_report(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取用户行为报表"""
    
    behaviors = db.query(DailyUserBehavior).filter(
        and_(
            DailyUserBehavior.report_date >= start_date,
            DailyUserBehavior.report_date <= end_date
        )
    ).order_by(DailyUserBehavior.report_date).all()
    
    if not behaviors:
        raise HTTPException(status_code=404, detail="No behavior data found for the specified date range")
    
    # 计算汇总指标
    total_sessions = sum(b.total_sessions for b in behaviors)
    unique_visitors = sum(b.unique_visitors for b in behaviors)
    page_views = sum(b.page_views for b in behaviors)
    avg_session_duration = sum(b.avg_session_duration for b in behaviors) / len(behaviors) if behaviors else 0
    
    # 汇总热门内容
    top_products = _aggregate_top_products(behaviors)
    top_keywords = _aggregate_top_keywords(behaviors)
    
    return UserBehaviorReportResponse(
        date_range={"start_date": start_date, "end_date": end_date},
        total_sessions=total_sessions,
        unique_visitors=unique_visitors,
        page_views=page_views,
        avg_session_duration=int(avg_session_duration),
        daily_data=[DailyUserBehaviorResponse.from_orm(b) for b in behaviors],
        top_products=top_products,
        top_keywords=top_keywords
    )


@router.get("/product-performance", response_model=ProductPerformanceReportResponse)
async def get_product_performance_report(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    limit: int = Query(50, description="返回商品数量限制"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取商品表现报表"""
    
    # 获取商品表现数据并按收入排序
    performances = db.query(DailyProductPerformance).filter(
        and_(
            DailyProductPerformance.report_date >= start_date,
            DailyProductPerformance.report_date <= end_date
        )
    ).order_by(desc(DailyProductPerformance.revenue)).limit(limit).all()
    
    if not performances:
        raise HTTPException(status_code=404, detail="No product performance data found")
    
    # 获取库存预警
    stock_alerts = db.query(DailyProductPerformance).filter(
        and_(
            DailyProductPerformance.report_date >= start_date,
            DailyProductPerformance.report_date <= end_date,
            DailyProductPerformance.stock_level <= DailyProductPerformance.low_stock_alert
        )
    ).all()
    
    total_products = len(set(p.product_id for p in performances))
    
    return ProductPerformanceReportResponse(
        date_range={"start_date": start_date, "end_date": end_date},
        total_products=total_products,
        top_performers=[DailyProductPerformanceResponse.from_orm(p) for p in performances[:20]],
        category_performance=_calculate_category_performance(performances),
        stock_alerts=[
            {
                "product_id": str(p.product_id),
                "product_name": p.product_name,
                "stock_level": p.stock_level,
                "low_stock_alert": p.low_stock_alert
            }
            for p in stock_alerts
        ]
    )


@router.get("/ad-performance", response_model=AdPerformanceReportResponse)
async def get_ad_performance_report(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取广告表现报表"""
    
    ads = db.query(DailyAdPerformance).filter(
        and_(
            DailyAdPerformance.report_date >= start_date,
            DailyAdPerformance.report_date <= end_date
        )
    ).order_by(DailyAdPerformance.report_date).all()
    
    if not ads:
        raise HTTPException(status_code=404, detail="No ad performance data found")
    
    # 计算汇总指标
    total_cost = sum(a.cost for a in ads)
    total_conversions = sum(a.conversions for a in ads)
    avg_roi = sum(a.roi for a in ads) / len(ads) if ads else 0
    
    # 按渠道分组性能
    channel_performance = _calculate_channel_performance(ads)
    
    return AdPerformanceReportResponse(
        date_range={"start_date": start_date, "end_date": end_date},
        total_cost=total_cost,
        total_conversions=total_conversions,
        avg_roi=avg_roi,
        daily_data=[DailyAdPerformanceResponse.from_orm(a) for a in ads],
        channel_performance=channel_performance
    )


@router.get("/dashboard", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取仪表板汇总数据"""
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # 获取今日和昨日数据
    today_summary = db.query(DailySalesSummary).filter(
        DailySalesSummary.report_date == today
    ).first()
    
    yesterday_summary = db.query(DailySalesSummary).filter(
        DailySalesSummary.report_date == yesterday
    ).first()
    
    # 如果今日数据不存在，生成一个空的
    if not today_summary:
        today_summary = DailySalesSummary(
            report_date=today,
            total_orders=0,
            total_revenue=0,
            total_customers=0,
            conversion_rate=0
        )
    
    if not yesterday_summary:
        yesterday_summary = DailySalesSummary(
            report_date=yesterday,
            total_orders=0,
            total_revenue=0,
            total_customers=0,
            conversion_rate=0
        )
    
    # 计算本周和本月汇总
    this_week = _calculate_period_summary(db, week_start, today)
    this_month = _calculate_period_summary(db, month_start, today)
    
    # 关键指标
    key_metrics = _calculate_key_metrics(db, today_summary, yesterday_summary)
    
    # 预警信息
    alerts = _generate_alerts(db, today)
    
    # 图表数据
    charts_data = _generate_charts_data(db, today)
    
    return DashboardSummaryResponse(
        today=DailySalesSummaryResponse.from_orm(today_summary),
        yesterday=DailySalesSummaryResponse.from_orm(yesterday_summary),
        this_week=this_week,
        this_month=this_month,
        key_metrics=key_metrics,
        alerts=alerts,
        charts_data=charts_data
    )


def _calculate_sales_trends(summaries: List[DailySalesSummary]) -> dict:
    """计算销售趋势"""
    if len(summaries) < 2:
        return {"revenue_trend": 0, "order_trend": 0, "customer_trend": 0}
    
    # 简单的趋势计算：最后一天vs前一天
    last_day = summaries[-1]
    prev_day = summaries[-2]
    
    revenue_trend = ((last_day.total_revenue - prev_day.total_revenue) / prev_day.total_revenue * 100) if prev_day.total_revenue > 0 else 0
    order_trend = ((last_day.total_orders - prev_day.total_orders) / prev_day.total_orders * 100) if prev_day.total_orders > 0 else 0
    customer_trend = ((last_day.total_customers - prev_day.total_customers) / prev_day.total_customers * 100) if prev_day.total_customers > 0 else 0
    
    return {
        "revenue_trend": float(revenue_trend),
        "order_trend": float(order_trend),
        "customer_trend": float(customer_trend)
    }


def _aggregate_top_products(behaviors: List[DailyUserBehavior]) -> List[dict]:
    """汇总热门商品"""
    product_counts = {}
    
    for behavior in behaviors:
        if behavior.top_viewed_products:
            for product in behavior.top_viewed_products:
                product_id = product.get('product_id')
                if product_id:
                    if product_id not in product_counts:
                        product_counts[product_id] = {
                            'product_id': product_id,
                            'product_name': product.get('product_name', ''),
                            'total_views': 0
                        }
                    product_counts[product_id]['total_views'] += product.get('view_count', 0)
    
    # 按总浏览量排序
    sorted_products = sorted(product_counts.values(), key=lambda x: x['total_views'], reverse=True)
    return sorted_products[:10]


def _aggregate_top_keywords(behaviors: List[DailyUserBehavior]) -> List[dict]:
    """汇总热门搜索词"""
    keyword_counts = {}
    
    for behavior in behaviors:
        if behavior.top_search_keywords:
            for keyword in behavior.top_search_keywords:
                keyword_text = keyword.get('keyword')
                if keyword_text:
                    if keyword_text not in keyword_counts:
                        keyword_counts[keyword_text] = {
                            'keyword': keyword_text,
                            'total_count': 0
                        }
                    keyword_counts[keyword_text]['total_count'] += keyword.get('count', 0)
    
    # 按总搜索次数排序
    sorted_keywords = sorted(keyword_counts.values(), key=lambda x: x['total_count'], reverse=True)
    return sorted_keywords[:10]


def _calculate_category_performance(performances: List[DailyProductPerformance]) -> dict:
    """计算分类表现"""
    category_stats = {}
    
    for perf in performances:
        category = perf.category_name or 'Unknown'
        if category not in category_stats:
            category_stats[category] = {
                'revenue': 0,
                'quantity_sold': 0,
                'product_count': 0
            }
        
        category_stats[category]['revenue'] += float(perf.revenue)
        category_stats[category]['quantity_sold'] += perf.quantity_sold
        category_stats[category]['product_count'] += 1
    
    return category_stats


def _calculate_channel_performance(ads: List[DailyAdPerformance]) -> dict:
    """计算渠道表现"""
    channel_stats = {}
    
    for ad in ads:
        channel = ad.channel
        if channel not in channel_stats:
            channel_stats[channel] = {
                'cost': 0,
                'conversions': 0,
                'revenue': 0,
                'roi': 0
            }
        
        channel_stats[channel]['cost'] += float(ad.cost)
        channel_stats[channel]['conversions'] += ad.conversions
        channel_stats[channel]['revenue'] += float(ad.conversion_value)
    
    # 计算ROI
    for channel, stats in channel_stats.items():
        if stats['cost'] > 0:
            stats['roi'] = (stats['revenue'] - stats['cost']) / stats['cost']
    
    return channel_stats


def _calculate_period_summary(db: Session, start_date: date, end_date: date) -> dict:
    """计算时段汇总"""
    summaries = db.query(DailySalesSummary).filter(
        and_(
            DailySalesSummary.report_date >= start_date,
            DailySalesSummary.report_date <= end_date
        )
    ).all()
    
    if not summaries:
        return {
            "total_orders": 0,
            "total_revenue": 0,
            "total_customers": 0,
            "avg_conversion_rate": 0
        }
    
    return {
        "total_orders": sum(s.total_orders for s in summaries),
        "total_revenue": float(sum(s.total_revenue for s in summaries)),
        "total_customers": sum(s.total_customers for s in summaries),
        "avg_conversion_rate": float(sum(s.conversion_rate for s in summaries) / len(summaries))
    }


def _calculate_key_metrics(db: Session, today: DailySalesSummary, yesterday: DailySalesSummary) -> dict:
    """计算关键指标"""
    revenue_change = 0
    order_change = 0
    
    if yesterday.total_revenue > 0:
        revenue_change = ((today.total_revenue - yesterday.total_revenue) / yesterday.total_revenue) * 100
    
    if yesterday.total_orders > 0:
        order_change = ((today.total_orders - yesterday.total_orders) / yesterday.total_orders) * 100
    
    return {
        "revenue_change_percent": float(revenue_change),
        "order_change_percent": float(order_change),
        "conversion_rate": float(today.conversion_rate),
        "avg_order_value": float(today.avg_order_value)
    }


def _generate_alerts(db: Session, target_date: date) -> List[dict]:
    """生成预警信息"""
    alerts = []
    
    # 库存预警
    low_stock_products = db.query(DailyProductPerformance).filter(
        and_(
            DailyProductPerformance.report_date == target_date,
            DailyProductPerformance.stock_level <= DailyProductPerformance.low_stock_alert,
            DailyProductPerformance.stock_level > 0
        )
    ).count()
    
    if low_stock_products > 0:
        alerts.append({
            "type": "stock_warning",
            "message": f"有 {low_stock_products} 个商品库存不足",
            "severity": "warning"
        })
    
    # 缺货预警
    out_of_stock = db.query(DailyProductPerformance).filter(
        and_(
            DailyProductPerformance.report_date == target_date,
            DailyProductPerformance.is_out_of_stock == 1
        )
    ).count()
    
    if out_of_stock > 0:
        alerts.append({
            "type": "stock_critical",
            "message": f"有 {out_of_stock} 个商品已缺货",
            "severity": "critical"
        })
    
    return alerts


def _generate_charts_data(db: Session, target_date: date) -> dict:
    """生成图表数据"""
    # 获取最近7天的销售数据
    seven_days_ago = target_date - timedelta(days=6)
    
    recent_sales = db.query(DailySalesSummary).filter(
        and_(
            DailySalesSummary.report_date >= seven_days_ago,
            DailySalesSummary.report_date <= target_date
        )
    ).order_by(DailySalesSummary.report_date).all()
    
    return {
        "sales_trend": [
            {
                "date": s.report_date.isoformat(),
                "revenue": float(s.total_revenue),
                "orders": s.total_orders
            }
            for s in recent_sales
        ]
    }