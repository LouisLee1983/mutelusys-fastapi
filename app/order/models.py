import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text, Float, Enum, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"                  # 待处理
    PROCESSING = "PROCESSING"            # 处理中
    AWAITING_PAYMENT = "AWAITING_PAYMENT"  # 等待付款
    PAID = "PAID"                        # 已付款
    PARTIALLY_PAID = "PARTIALLY_PAID"    # 部分付款
    SHIPPED = "SHIPPED"                  # 已发货
    PARTIALLY_SHIPPED = "PARTIALLY_SHIPPED"  # 部分发货
    DELIVERED = "DELIVERED"              # 已送达
    COMPLETED = "COMPLETED"              # 已完成
    CANCELLED = "CANCELLED"              # 已取消
    REFUNDED = "REFUNDED"                # 已退款
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"  # 部分退款
    ON_HOLD = "ON_HOLD"                  # 暂停处理


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"                  # 待付款
    PROCESSING = "PROCESSING"            # 处理中
    PAID = "PAID"                        # 已付款
    PARTIALLY_PAID = "PARTIALLY_PAID"    # 部分付款
    FAILED = "FAILED"                    # 支付失败
    REFUNDED = "REFUNDED"                # 已退款
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"  # 部分退款
    CANCELLED = "CANCELLED"              # 已取消


class ShippingStatus(str, enum.Enum):
    PENDING = "PENDING"                  # 待发货
    PROCESSING = "PROCESSING"            # 处理中
    PARTIALLY_SHIPPED = "PARTIALLY_SHIPPED"  # 部分发货
    SHIPPED = "SHIPPED"                  # 已发货
    DELIVERED = "DELIVERED"              # 已送达
    FAILED = "FAILED"                    # 配送失败
    RETURNED = "RETURNED"                # 已退回


class OrderItemStatus(str, enum.Enum):
    """订单项状态"""
    PENDING = "PENDING"              # 待处理
    CONFIRMED = "CONFIRMED"          # 已确认
    PROCESSING = "PROCESSING"        # 处理中
    READY_TO_SHIP = "READY_TO_SHIP"  # 准备发货
    PARTIALLY_SHIPPED = "PARTIALLY_SHIPPED"  # 部分发货
    SHIPPED = "SHIPPED"              # 已发货
    DELIVERED = "DELIVERED"          # 已送达
    CANCELLED = "CANCELLED"          # 已取消
    RETURNED = "RETURNED"            # 已退货
    PARTIALLY_RETURNED = "PARTIALLY_RETURNED"  # 部分退货


class PaymentType(str, enum.Enum):
    """支付类型"""
    CREDIT_CARD = "CREDIT_CARD"      # 信用卡
    DEBIT_CARD = "DEBIT_CARD"        # 借记卡
    PAYPAL = "PAYPAL"                # PayPal
    BANK_TRANSFER = "BANK_TRANSFER"  # 银行转账
    COD = "COD"                      # 货到付款
    WALLET = "WALLET"                # 电子钱包
    CRYPTO = "CRYPTO"                # 加密货币
    GRABPAY = "GRABPAY"              # GrabPay
    SHOPEEPAY = "SHOPEEPAY"          # ShopeePay
    GOPAY = "GOPAY"                  # GoPay
    DANA = "DANA"                    # Dana
    OVO = "OVO"                      # OVO
    LINEPAY = "LINEPAY"              # LINE Pay
    MOMO = "MOMO"                    # MoMo
    OTHER = "OTHER"                  # 其他


class PaymentResult(str, enum.Enum):
    """支付结果"""
    SUCCESS = "SUCCESS"              # 成功
    PENDING = "PENDING"              # 处理中
    FAILED = "FAILED"                # 失败
    CANCELLED = "CANCELLED"          # 已取消
    REFUNDED = "REFUNDED"            # 已退款
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"  # 部分退款


class Order(Base):
    """订单主表，包含订单编号、客户、状态、支付状态、物流状态、金额、币种、支付方式、创建时间等"""
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(50), nullable=False, unique=True, index=True, comment="订单编号")
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="客户ID")
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    shipping_status = Column(Enum(ShippingStatus), nullable=False, default=ShippingStatus.PENDING)
    currency_code = Column(String(3), nullable=False, comment="货币代码，如USD, SGD, MYR")
    
    # 价格相关
    subtotal = Column(Numeric(10, 2), nullable=False, default=0, comment="商品小计")
    shipping_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="运费")
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="税费")
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="折扣金额")
    total_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="订单总金额")
    paid_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="已支付金额")
    
    # 收货信息
    shipping_name = Column(String(100), nullable=True, comment="收货人姓名")
    shipping_phone = Column(String(30), nullable=True, comment="收货人电话")
    shipping_email = Column(String(100), nullable=True, comment="收货人邮箱")
    shipping_address1 = Column(String(255), nullable=True, comment="收货地址1")
    shipping_address2 = Column(String(255), nullable=True, comment="收货地址2")
    shipping_city = Column(String(100), nullable=True, comment="城市")
    shipping_state = Column(String(100), nullable=True, comment="州/省")
    shipping_country = Column(String(100), nullable=True, comment="国家")
    shipping_postcode = Column(String(20), nullable=True, comment="邮编")
    
    # 账单信息（如与收货地址不同）
    billing_name = Column(String(100), nullable=True, comment="账单人姓名")
    billing_phone = Column(String(30), nullable=True, comment="账单人电话")
    billing_email = Column(String(100), nullable=True, comment="账单人邮箱")
    billing_address1 = Column(String(255), nullable=True, comment="账单地址1")
    billing_address2 = Column(String(255), nullable=True, comment="账单地址2")
    billing_city = Column(String(100), nullable=True, comment="城市")
    billing_state = Column(String(100), nullable=True, comment="州/省")
    billing_country = Column(String(100), nullable=True, comment="国家")
    billing_postcode = Column(String(20), nullable=True, comment="邮编")
    
    # 其他信息
    coupon_code = Column(String(50), nullable=True, comment="优惠券代码")
    is_gift = Column(Boolean, default=False, comment="是否为礼品订单")
    gift_message = Column(Text, nullable=True, comment="礼品留言")
    customer_note = Column(Text, nullable=True, comment="客户备注")
    admin_note = Column(Text, nullable=True, comment="管理员备注")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="User Agent")
    source = Column(String(50), nullable=True, comment="订单来源")
    estimate_delivery_date = Column(DateTime, nullable=True, comment="预计送达日期")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")
    shipped_at = Column(DateTime, nullable=True, comment="发货时间")
    delivered_at = Column(DateTime, nullable=True, comment="送达时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    cancelled_at = Column(DateTime, nullable=True, comment="取消时间")
    
    # 关联关系
    # customer = relationship("Customer", back_populates="orders")  # 暂时注释，避免循环导入
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    # payments = relationship("OrderPayment", back_populates="order", cascade="all, delete-orphan")
    shipments = relationship("OrderShipment", back_populates="order", cascade="all, delete-orphan")
    # status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")
    # notes = relationship("OrderNote", back_populates="order", cascade="all, delete-orphan")
    # returns = relationship("OrderReturn", back_populates="order", cascade="all, delete-orphan")
    # gift_info = relationship("GiftOrder", back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderItem(Base):
    """订单项，记录每个商品的数量、价格、SKU、折扣等"""
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=True)  # 暂时移除外键约束
    sku_id = Column(UUID(as_uuid=True), nullable=True)  # 暂时移除外键约束
    # 礼品包装功能已简化，跨境电商不需要复杂的包装管理
    # gift_wrapping_id = Column(UUID(as_uuid=True), ForeignKey("gift_wrappings.id"), nullable=True)
    
    # 订单项状态
    status = Column(Enum(OrderItemStatus), nullable=False, default=OrderItemStatus.PENDING)
    
    # 商品信息（快照）
    name = Column(String(255), nullable=False, comment="商品名称")
    sku_code = Column(String(50), nullable=True, comment="SKU编码")
    quantity = Column(Integer, nullable=False, default=1, comment="数量")
    unit_price = Column(Numeric(10, 2), nullable=False, comment="单价")
    subtotal = Column(Numeric(10, 2), nullable=False, comment="小计（数量 * 单价）")
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="折扣金额")
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="税费")
    final_price = Column(Numeric(10, 2), nullable=False, comment="最终价格（小计 - 折扣 + 税费）")
    weight = Column(Float, nullable=True, comment="重量(克)")
    width = Column(Float, nullable=True, comment="宽度(厘米)")
    height = Column(Float, nullable=True, comment="高度(厘米)")
    length = Column(Float, nullable=True, comment="长度(厘米)")
    
    # 折扣信息
    discount_type = Column(String(50), nullable=True, comment="折扣类型：percentage, fixed_amount")
    discount_percentage = Column(Float, nullable=True, comment="折扣百分比")
    coupon_code = Column(String(50), nullable=True, comment="优惠券代码")
    
    # 属性信息（快照）
    attributes = Column(JSON, nullable=True, comment="商品属性快照，如颜色、尺寸等")
    image_url = Column(String(255), nullable=True, comment="商品图片URL")
    
    # 数量跟踪（支持部分操作）
    confirmed_quantity = Column(Integer, default=0, comment="已确认数量")
    shipped_quantity = Column(Integer, default=0, comment="已发货数量")
    delivered_quantity = Column(Integer, default=0, comment="已送达数量")
    returned_quantity = Column(Integer, default=0, comment="已退货数量")
    cancelled_quantity = Column(Integer, default=0, comment="已取消数量")
    
    # 状态标识（为了查询优化保留）
    is_shipped = Column(Boolean, default=False, comment="是否已发货")
    is_returned = Column(Boolean, default=False, comment="是否已退货")
    is_cancelled = Column(Boolean, default=False, comment="是否已取消")
    
    # 业务支持字段
    can_cancel = Column(Boolean, default=True, comment="是否可以取消")
    can_return = Column(Boolean, default=True, comment="是否可以退货")
    can_exchange = Column(Boolean, default=True, comment="是否可以换货")
    
    # 自定义选项、备注等
    options = Column(JSON, nullable=True, comment="自定义选项")
    note = Column(Text, nullable=True, comment="备注")
    cancel_reason = Column(String(255), nullable=True, comment="取消原因")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    confirmed_at = Column(DateTime, nullable=True, comment="确认时间")
    shipped_at = Column(DateTime, nullable=True, comment="发货时间")
    delivered_at = Column(DateTime, nullable=True, comment="送达时间")
    cancelled_at = Column(DateTime, nullable=True, comment="取消时间")
    
    # 关联关系
    order = relationship("Order", back_populates="items")
    # product = relationship("Product")  # 暂时注释
    # sku = relationship("ProductSku")  # 暂时注释
    # 礼品包装功能已简化
    # gift_wrapping = relationship("GiftWrapping", back_populates="order_items")
    # registry_purchase = relationship("GiftRegistryPurchase", back_populates="order_item", uselist=False)  # 暂时注释


class OrderPayment(Base):
    """订单支付记录，包含支付方式、金额、状态、交易信息等"""
    __tablename__ = "order_payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("payment_methods.id"), nullable=True)
    
    # 支付信息
    payment_type = Column(Enum(PaymentType), nullable=False, comment="支付类型")
    amount = Column(Numeric(10, 2), nullable=False, comment="支付金额")
    currency_code = Column(String(3), nullable=False, comment="货币代码")
    result = Column(Enum(PaymentResult), nullable=False, comment="支付结果")
    transaction_id = Column(String(100), nullable=True, comment="交易ID")
    transaction_reference = Column(String(100), nullable=True, comment="交易参考号")
    
    # 支付方式详情
    payment_method_name = Column(String(100), nullable=True, comment="支付方式名称")
    payment_details = Column(JSON, nullable=True, comment="支付详情，如卡号后四位等")
    
    # 授权信息
    authorization_code = Column(String(100), nullable=True, comment="授权码")
    authorization_transaction_id = Column(String(100), nullable=True, comment="授权交易ID")
    
    # 退款信息
    is_refunded = Column(Integer, default=0, comment="是否已退款：0-否，1-是，2-部分退款")
    refunded_amount = Column(Numeric(10, 2), default=0, comment="已退款金额")
    refund_transaction_id = Column(String(100), nullable=True, comment="退款交易ID")
    
    # 其他信息
    notes = Column(Text, nullable=True, comment="备注")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    error_code = Column(String(50), nullable=True, comment="错误代码")
    error_message = Column(Text, nullable=True, comment="错误信息")
    response_data = Column(JSON, nullable=True, comment="支付网关响应数据")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    refunded_at = Column(DateTime, nullable=True, comment="退款时间")
    
    # 关联关系
    # order = relationship("Order", back_populates="payments")  # 暂时注释


class OrderStatusHistory(Base):
    """订单状态变更历史记录"""
    __tablename__ = "order_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    previous_status = Column(Enum(OrderStatus), nullable=True, comment="之前的订单状态")
    new_status = Column(Enum(OrderStatus), nullable=False, comment="新的订单状态")
    previous_payment_status = Column(Enum(PaymentStatus), nullable=True, comment="之前的支付状态")
    new_payment_status = Column(Enum(PaymentStatus), nullable=True, comment="新的支付状态")
    previous_shipping_status = Column(Enum(ShippingStatus), nullable=True, comment="之前的物流状态")
    new_shipping_status = Column(Enum(ShippingStatus), nullable=True, comment="新的物流状态")
    comment = Column(Text, nullable=True, comment="变更说明")
    operator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="操作人ID")
    operator_name = Column(String(100), nullable=True, comment="操作人姓名")
    is_customer_notified = Column(Integer, default=0, comment="是否已通知客户：0-否，1-是，2-失败")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")

    # 关联关系
    # order = relationship("Order", back_populates="status_history")  # 暂时注释


class OrderNote(Base):
    """订单备注信息，供内部使用"""
    __tablename__ = "order_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text, nullable=False, comment="备注内容")
    is_customer_notified = Column(Boolean, default=False, comment="是否已通知客户")
    is_visible_to_customer = Column(Boolean, default=False, comment="是否对客户可见")
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="作者ID")
    author_name = Column(String(100), nullable=True, comment="作者姓名")
    author_type = Column(String(20), nullable=True, comment="作者类型：admin, customer, system")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关联关系
    # order = relationship("Order", back_populates="notes")  # 暂时注释
