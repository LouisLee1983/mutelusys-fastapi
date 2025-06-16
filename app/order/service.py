import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_, and_, text
import random
import string

from app.order.models import Order, OrderStatus, PaymentStatus, ShippingStatus, OrderItem, OrderItemStatus
from app.order.schema import OrderCreate, OrderStatusUpdate, OrderPaymentStatusUpdate, OrderShippingStatusUpdate, OrderFilter, OrderListParams


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
        
        # 创建订单
        order = Order(
            order_number=order_number,
            customer_id=order_data.customer_id,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            shipping_status=ShippingStatus.PENDING,
            currency_code=order_data.currency_code,
            subtotal=order_data.subtotal,
            shipping_amount=order_data.shipping_amount,
            tax_amount=order_data.tax_amount,
            discount_amount=order_data.discount_amount,
            total_amount=order_data.total_amount,
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
            coupon_code=order_data.coupon_code,
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
        for item_data in order_data.items:
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
                attributes=item_data.attributes,
                image_url=item_data.image_url
            )
            db.add(order_item)
        
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
        elif status_data.status == OrderStatus.SHIPPED:
            order.shipped_at = datetime.utcnow()
        elif status_data.status == OrderStatus.DELIVERED:
            order.delivered_at = datetime.utcnow()
        elif status_data.status == OrderStatus.COMPLETED:
            order.completed_at = datetime.utcnow()
        elif status_data.status == OrderStatus.CANCELLED:
            order.cancelled_at = datetime.utcnow()
        
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
