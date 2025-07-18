import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_, and_, text
import random
import string

from app.order.models import Order, OrderStatus, PaymentStatus, ShippingStatus, OrderItem, OrderItemStatus
from app.order.schema import OrderCreate, OrderStatusUpdate, OrderPaymentStatusUpdate, OrderShippingStatusUpdate, OrderFilter, OrderListParams
from app.order.duty_integration import OrderDutyIntegrationService
from app.order.promotion_integration import OrderPromotionIntegration
from app.points.service import PointsService
from app.customer.models import Customer, PointsTransactionType
from app.product.sku.service import ProductSkuService


class OrderService:
    @staticmethod
    def generate_order_number() -> str:
        """生成订单编号，格式为：年月日+6位随机数字"""
        date_prefix = datetime.now().strftime("%Y%m%d")
        random_suffix = ''.join(random.choices(string.digits, k=6))
        return f"{date_prefix}{random_suffix}"

    @staticmethod
    def create_order(db: Session, order_data: OrderCreate) -> Order:
        """创建订单"""
        order_number = OrderService.generate_order_number()
        
        # 1. 检查库存
        sku_service = ProductSkuService()
        for item in order_data.items:
            if item.sku_id:  # 如果有SKU ID，检查库存
                if not sku_service.check_stock(db, item.sku_id, item.quantity):
                    raise ValueError(f"商品 {item.name} 库存不足")
        
        # 2. 应用促销计算
        promotion_integration = OrderPromotionIntegration(db)
        try:
            updated_order_data = promotion_integration.apply_promotion_to_order(order_data)
        except ValueError as e:
            # 促销应用失败，继续处理但不应用促销
            print(f"促销应用失败: {str(e)}")
            updated_order_data = order_data
            updated_order_data.coupon_code = None
            updated_order_data.discount_amount = 0
        
        # 3. 集成关税计算
        duty_integration = OrderDutyIntegrationService(db)
        duty_integration_result = duty_integration.calculate_and_apply_duty(updated_order_data)
        
        # 使用更新后的订单数据（包含关税和促销）
        final_order_data = duty_integration_result["order_data"]
        duty_result = duty_integration_result["duty_result"]
        duty_applied = duty_integration_result["duty_applied"]
        
        # 创建订单
        order = Order(
            order_number=order_number,
            customer_id=final_order_data.customer_id,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            shipping_status=ShippingStatus.PENDING,
            currency_code=final_order_data.currency_code,
            subtotal=final_order_data.subtotal,
            shipping_amount=final_order_data.shipping_amount,
            tax_amount=final_order_data.tax_amount,
            discount_amount=final_order_data.discount_amount,
            total_amount=final_order_data.total_amount,
            # 收货地址
            shipping_name=order_data.shipping_address.name,
            shipping_phone=order_data.shipping_address.phone,
            shipping_email=order_data.shipping_address.email,
            shipping_address1=order_data.shipping_address.address1,
            shipping_address2=order_data.shipping_address.address2,
            shipping_city=order_data.shipping_address.city,
            shipping_state=order_data.shipping_address.state,
            shipping_country=order_data.shipping_address.country,
            shipping_postcode=order_data.shipping_address.postcode,
            # 账单地址（如果提供）
            billing_name=order_data.billing_address.name if order_data.billing_address else None,
            billing_phone=order_data.billing_address.phone if order_data.billing_address else None,
            billing_email=order_data.billing_address.email if order_data.billing_address else None,
            billing_address1=order_data.billing_address.address1 if order_data.billing_address else None,
            billing_address2=order_data.billing_address.address2 if order_data.billing_address else None,
            billing_city=order_data.billing_address.city if order_data.billing_address else None,
            billing_state=order_data.billing_address.state if order_data.billing_address else None,
            billing_country=order_data.billing_address.country if order_data.billing_address else None,
            billing_postcode=order_data.billing_address.postcode if order_data.billing_address else None,
            # 其他信息
            coupon_code=final_order_data.coupon_code,
            is_gift=order_data.is_gift,
            gift_message=order_data.gift_message,
            customer_note=order_data.customer_note,
            ip_address=order_data.ip_address,
            user_agent=order_data.user_agent,
            source=order_data.source,
        )
        
        db.add(order)
        db.flush()  # 获取订单ID
        
        # 创建订单项
        for item_data in final_order_data.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data.product_id,
                sku_id=item_data.sku_id,
                status=OrderItemStatus.PENDING,
                name=item_data.name,
                sku_code=item_data.sku_code,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                subtotal=item_data.subtotal,
                discount_amount=item_data.discount_amount,
                tax_amount=item_data.tax_amount,
                final_price=item_data.final_price,
                discount_type=item_data.discount_type,
                coupon_code=item_data.coupon_code,
                attributes=item_data.attributes,
                image_url=item_data.image_url
            )
            db.add(order_item)
        
        db.commit()
        db.refresh(order)
        
        # 4. 扣减库存
        for item in final_order_data.items:
            if item.sku_id:  # 如果有SKU ID，扣减库存
                sku_service.adjust_stock(
                    db=db,
                    sku_id=item.sku_id,
                    quantity_change=-item.quantity,  # 负数表示减少
                    change_type="order",
                    order_id=order.id,
                    remark=f"订单 {order.order_number}"
                )
        
        # 5. 如果应用了关税，创建关税记录
        if duty_applied and duty_result:
            duty_integration.create_duty_charge_record(order, duty_result, final_order_data)
        
        return order
    
    @staticmethod
    def create_points_order(db: Session, order_data: OrderCreate) -> Order:
        """创建积分兑换订单（仅限积分兑换类别的商品）"""
        from app.product.models import Product, ProductCategory
        from app.customer.models import Customer
        
        # 验证客户存在
        customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
        if not customer:
            raise ValueError("客户不存在")
        
        # 计算所需总积分
        total_points_needed = 0
        
        # 验证所有商品都属于积分兑换类别
        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise ValueError(f"商品ID {item.product_id} 不存在")
            
            # 检查商品类别是否为"积分兑换"
            if not product.category or product.category.name != "积分兑换":
                raise ValueError(f"商品 {product.name} 不属于积分兑换类别")
            
            # 使用商品价格作为积分价格（1 USD = 100积分）
            points_per_item = int(float(product.price) * 100)
            total_points_needed += points_per_item * item.quantity
        
        # 检查客户积分余额
        if customer.current_points < total_points_needed:
            raise ValueError(f"积分不足。需要 {total_points_needed} 积分，当前余额 {customer.current_points} 积分")
        
        # 创建订单（总金额为0，支付方式为POINTS）
        order_number = OrderService.generate_order_number()
        
        order = Order(
            order_number=order_number,
            customer_id=order_data.customer_id,
            status=OrderStatus.PAID,  # 积分订单直接设为已支付
            payment_status=PaymentStatus.PAID,
            payment_method='POINTS',
            shipping_status=ShippingStatus.PENDING,
            currency_code=order_data.currency_code,
            subtotal=0,  # 积分订单金额为0
            shipping_amount=0,  # 积分商品免运费
            tax_amount=0,
            discount_amount=0,
            total_amount=0,
            points_used=total_points_needed,  # 记录使用的积分
            # 收货地址
            shipping_name=order_data.shipping_address.name,
            shipping_phone=order_data.shipping_address.phone,
            shipping_email=order_data.shipping_address.email,
            shipping_address1=order_data.shipping_address.address1,
            shipping_address2=order_data.shipping_address.address2,
            shipping_city=order_data.shipping_address.city,
            shipping_state=order_data.shipping_address.state,
            shipping_postcode=order_data.shipping_address.postcode,
            shipping_country=order_data.shipping_address.country,
            # 其他信息
            customer_note=order_data.customer_note,
            is_gift=order_data.is_gift,
            gift_message=order_data.gift_message,
            paid_at=datetime.utcnow()  # 积分支付立即完成
        )
        
        db.add(order)
        db.flush()  # 获取订单ID
        
        # 创建订单项
        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            
            order_item = OrderItem(
                id=uuid.uuid4(),
                order_id=order.id,
                product_id=item.product_id,
                sku_id=item.sku_variant_id,
                name=product.name,
                sku_code=product.sku if hasattr(product, 'sku') else None,
                quantity=item.quantity,
                unit_price=0,  # 积分商品单价为0
                subtotal=0,
                discount_amount=0,
                tax_amount=0,
                final_price=0,
                status=OrderItemStatus.PENDING
            )
            db.add(order_item)
        
        # 扣除积分
        try:
            PointsService.redeem_points_for_order(
                db=db,
                customer_id=customer.id,
                points_to_use=total_points_needed,
                order_id=order.id
            )
            
            # 添加订单备注
            from app.order.models import OrderNote
            note = OrderNote(
                id=uuid.uuid4(),
                order_id=order.id,
                note=f"积分兑换订单，使用 {total_points_needed} 积分",
                author_type="system",
                is_visible_to_customer=True
            )
            db.add(note)
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"积分扣除失败: {str(e)}")
        
        db.commit()
        db.refresh(order)
        
        return order

    @staticmethod
    def get_order_by_id(db: Session, order_id: uuid.UUID) -> Optional[Order]:
        """通过ID获取订单详情"""
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_order_by_number(db: Session, order_number: str) -> Optional[Order]:
        """通过订单号获取订单详情"""
        return db.query(Order).filter(Order.order_number == order_number).first()

    @staticmethod
    def get_orders(db: Session, params: OrderListParams) -> Tuple[List[Order], int]:
        """获取订单列表，支持分页、排序和过滤"""
        from sqlalchemy.orm import joinedload
        
        query = db.query(Order)
        
        # 应用过滤条件
        if params.filters:
            filters = params.filters
            if filters.order_number:
                query = query.filter(Order.order_number.ilike(f"%{filters.order_number}%"))
            if filters.customer_id:
                query = query.filter(Order.customer_id == filters.customer_id)
            if filters.status:
                query = query.filter(Order.status == filters.status)
            if filters.payment_status:
                query = query.filter(Order.payment_status == filters.payment_status)
            if filters.shipping_status:
                query = query.filter(Order.shipping_status == filters.shipping_status)
            if filters.date_from:
                query = query.filter(Order.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(Order.created_at <= filters.date_to)
            if filters.min_amount:
                query = query.filter(Order.total_amount >= filters.min_amount)
            if filters.max_amount:
                query = query.filter(Order.total_amount <= filters.max_amount)
            if filters.is_gift is not None:
                query = query.filter(Order.is_gift == filters.is_gift)
        
        # 获取总数
        total = query.count()
        
        # 应用排序
        if params.sort_desc:
            query = query.order_by(desc(getattr(Order, params.sort_by)))
        else:
            query = query.order_by(asc(getattr(Order, params.sort_by)))
        
        # 应用分页和预加载关联数据
        offset = (params.page - 1) * params.page_size
        query = query.options(joinedload(Order.items)).offset(offset).limit(params.page_size)
        
        return query.all(), total

    @staticmethod
    def update_order_status(db: Session, order_id: uuid.UUID, status_data: OrderStatusUpdate) -> Optional[Order]:
        """更新订单状态"""
        order = OrderService.get_order_by_id(db, order_id)
        if not order:
            return None
        
        old_status = order.status
        order.status = status_data.status
        
        # 添加状态历史记录
        from app.order.models import OrderStatusHistory
        status_history = OrderStatusHistory(
            id=uuid.uuid4(),
            order_id=order.id,
            previous_status=old_status,
            new_status=status_data.status,
            comment=status_data.admin_note,
        )
        db.add(status_history)
        
        # 更新时间戳
        if status_data.status == OrderStatus.PAID:
            order.paid_at = datetime.utcnow()
            # 记录促销使用
            if order.coupon_code:
                promotion_integration = OrderPromotionIntegration(db)
                try:
                    promotion_integration.record_promotion_usage_on_payment(order.id)
                except Exception as e:
                    print(f"记录促销使用失败: {str(e)}")
        elif status_data.status == OrderStatus.SHIPPED:
            order.shipped_at = datetime.utcnow()
        elif status_data.status == OrderStatus.DELIVERED:
            order.delivered_at = datetime.utcnow()
        elif status_data.status == OrderStatus.COMPLETED:
            order.completed_at = datetime.utcnow()
            
            # 订单完成时发放积分
            if order.customer_id and order.payment_method != 'POINTS':  # 积分订单不再发放积分
                try:
                    # 获取客户信息
                    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
                    if customer:
                        # 计算应得积分
                        points_to_earn = PointsService.calculate_order_points(
                            order_amount_usd=float(order.total_amount),  # 假设金额已经是USD
                            customer=customer
                        )
                        
                        # 发放积分
                        if points_to_earn > 0:
                            PointsService.add_points(
                                db=db,
                                customer_id=order.customer_id,
                                amount=points_to_earn,
                                transaction_type=PointsTransactionType.EARN_ORDER,
                                description=f"订单 {order.order_number} 完成奖励",
                                reference_type="order",
                                reference_id=order.id
                            )
                            
                            # 添加订单备注
                            from app.order.models import OrderNote
                            note = OrderNote(
                                id=uuid.uuid4(),
                                order_id=order.id,
                                note=f"订单完成，已发放 {points_to_earn} 积分给客户",
                                author_type="system",
                                is_visible_to_customer=True
                            )
                            db.add(note)
                except Exception as e:
                    # 积分发放失败不应该影响订单状态更新
                    print(f"积分发放失败: {str(e)}")
                    
        elif status_data.status == OrderStatus.CANCELLED:
            order.cancelled_at = datetime.utcnow()
            
            # 3. 取消订单时恢复库存（只有待支付和已支付未发货的订单才恢复库存）
            if old_status in [OrderStatus.PENDING, OrderStatus.PAID]:
                sku_service = ProductSkuService()
                for item in order.items:
                    if item.sku_id:  # 如果有SKU ID，恢复库存
                        sku_service.adjust_stock(
                            db=db,
                            sku_id=item.sku_id,
                            quantity_change=item.quantity,  # 正数表示增加
                            change_type="cancel",
                            order_id=order.id,
                            remark=f"取消订单 {order.order_number}"
                        )
        
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_payment_status(db: Session, order_id: uuid.UUID, status_data: OrderPaymentStatusUpdate) -> Optional[Order]:
        """更新支付状态"""
        order = OrderService.get_order_by_id(db, order_id)
        if not order:
            return None
        
        old_status = order.payment_status
        order.payment_status = status_data.payment_status
        
        # 如果提供了已支付金额，则更新
        if status_data.paid_amount is not None:
            order.paid_amount = status_data.paid_amount
            # 如果全额支付，则更新支付时间
            if status_data.paid_amount >= order.total_amount:
                order.paid_at = datetime.utcnow()
        
        # 如果状态变更为已支付，但未设置支付时间，则自动设置
        if status_data.payment_status == PaymentStatus.PAID and not order.paid_at:
            order.paid_at = datetime.utcnow()
        
        # 添加状态历史和备注
        if status_data.admin_note:
            from app.order.models import OrderNote
            note = OrderNote(
                id=uuid.uuid4(),
                order_id=order.id,
                note=f"支付状态从 {old_status} 更新为 {status_data.payment_status}。备注: {status_data.admin_note}",
                author_type="admin",
                is_visible_to_customer=False
            )
            db.add(note)
        
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_shipping_status(db: Session, order_id: uuid.UUID, status_data: OrderShippingStatusUpdate) -> Optional[Order]:
        """更新物流状态"""
        order = OrderService.get_order_by_id(db, order_id)
        if not order:
            return None
        
        old_status = order.shipping_status
        order.shipping_status = status_data.shipping_status
        
        # 更新时间戳
        if status_data.shipping_status == ShippingStatus.SHIPPED and not order.shipped_at:
            order.shipped_at = datetime.utcnow()
        elif status_data.shipping_status == ShippingStatus.DELIVERED and not order.delivered_at:
            order.delivered_at = datetime.utcnow()
        
        # 添加状态历史和备注
        if status_data.admin_note:
            from app.order.models import OrderNote
            note = OrderNote(
                id=uuid.uuid4(),
                order_id=order.id,
                note=f"物流状态从 {old_status} 更新为 {status_data.shipping_status}。备注: {status_data.admin_note}",
                author_type="admin",
                is_visible_to_customer=False
            )
            db.add(note)
        
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_customer_orders(db: Session, customer_id: uuid.UUID, page: int = 1, page_size: int = 20) -> Tuple[List[Order], int]:
        """获取指定客户的订单列表"""
        from sqlalchemy.orm import joinedload
        
        query = db.query(Order).filter(Order.customer_id == customer_id)
        total = query.count()
        
        offset = (page - 1) * page_size
        orders = query.options(joinedload(Order.items)).order_by(desc(Order.created_at)).offset(offset).limit(page_size).all()
        
        return orders, total

    @staticmethod
    def count_orders_by_status(db: Session) -> Dict[str, int]:
        """统计各状态的订单数量"""
        result = {}
        for status in OrderStatus:
            count = db.query(Order).filter(Order.status == status).count()
            result[status.value] = count
        return result

    @staticmethod
    def search_orders(db: Session, keyword: str, page: int = 1, page_size: int = 20) -> Tuple[List[Order], int]:
        """搜索订单（订单号、客户名称、客户电话等）"""
        from sqlalchemy.orm import joinedload
        
        query = db.query(Order).filter(
            or_(
                Order.order_number.ilike(f"%{keyword}%"),
                Order.shipping_name.ilike(f"%{keyword}%"),
                Order.shipping_phone.ilike(f"%{keyword}%"),
                Order.shipping_email.ilike(f"%{keyword}%")
            )
        )
        
        total = query.count()
        
        offset = (page - 1) * page_size
        orders = query.options(joinedload(Order.items)).order_by(desc(Order.created_at)).offset(offset).limit(page_size).all()
        
        return orders, total

    # 关税相关方法
    @staticmethod
    def get_order_duty_info(db: Session, order_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """获取订单关税信息"""
        duty_integration = OrderDutyIntegrationService(db)
        return duty_integration.get_order_duty_info(order_id)
    
    @staticmethod
    def update_order_duty_status(db: Session, order_id: uuid.UUID, status: str) -> Optional[Dict[str, Any]]:
        """更新订单关税状态"""
        duty_integration = OrderDutyIntegrationService(db)
        duty_charge = duty_integration.update_duty_status(order_id, status)
        
        # 如果关税状态为已支付，同时更新订单支付状态
        if status == 'paid':
            order = OrderService.get_order_by_id(db, order_id)
            if order and order.payment_status == PaymentStatus.PENDING:
                # 这里可以根据业务逻辑决定是否自动更新订单支付状态
                pass
        
        return duty_integration.get_order_duty_info(order_id)
    
    @staticmethod
    def recalculate_order_duty(db: Session, order_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """重新计算订单关税（当订单修改时）"""
        order = OrderService.get_order_by_id(db, order_id)
        if not order:
            return None
        
        duty_integration = OrderDutyIntegrationService(db)
        return duty_integration.recalculate_duty_for_order(order)
    
    @staticmethod
    def get_orders_with_duty(db: Session, page: int = 1, page_size: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        """获取包含关税信息的订单列表"""
        from app.duty.models import OrderDutyCharge
        from sqlalchemy.orm import joinedload
        
        # 获取有关税记录的订单
        query = (
            db.query(Order)
            .join(OrderDutyCharge, Order.id == OrderDutyCharge.order_id)
            .options(joinedload(Order.items))
        )
        
        total = query.count()
        offset = (page - 1) * page_size
        orders = query.order_by(desc(Order.created_at)).offset(offset).limit(page_size).all()
        
        # 构建包含关税信息的结果
        results = []
        for order in orders:
            duty_integration = OrderDutyIntegrationService(db)
            duty_info = duty_integration.get_order_duty_info(order.id)
            
            results.append({
                "order": order,
                "duty_info": duty_info
            })
        
        return results, total
