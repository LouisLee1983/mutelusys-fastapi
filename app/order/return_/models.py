import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum, Numeric, JSON, Float, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ReturnStatus(str, enum.Enum):
    PENDING = "pending"              # 待处理
    APPROVED = "approved"            # 已批准
    RECEIVED = "received"            # 已收到退货
    COMPLETED = "completed"          # 已完成
    REJECTED = "rejected"            # 已拒绝
    CANCELLED = "cancelled"          # 已取消
    PARTIALLY_REFUNDED = "partially_refunded"  # 部分退款
    REFUNDED = "refunded"            # 已退款


class ReturnReason(str, enum.Enum):
    DAMAGED = "damaged"              # 商品损坏
    DEFECTIVE = "defective"          # 商品有缺陷
    NOT_AS_DESCRIBED = "not_as_described"  # 与描述不符
    WRONG_ITEM = "wrong_item"        # 错误商品
    UNWANTED = "unwanted"            # 不想要了
    SIZE_ISSUE = "size_issue"        # 尺寸问题
    QUALITY_ISSUE = "quality_issue"  # 质量问题
    LATE_DELIVERY = "late_delivery"  # 送达太晚
    OTHER = "other"                  # 其他原因


class ReturnAction(str, enum.Enum):
    REFUND = "refund"                # 退款
    REPLACE = "replace"              # 更换
    REPAIR = "repair"                # 修理
    STORE_CREDIT = "store_credit"    # 商店积分
    EXCHANGE = "exchange"            # 交换其他商品


# 退货与订单项的多对多关联表
return_item = Table(
    "return_item",
    Base.metadata,
    Column("return_id", UUID(as_uuid=True), ForeignKey("order_returns.id", ondelete="CASCADE"), primary_key=True),
    Column("order_item_id", UUID(as_uuid=True), ForeignKey("order_items.id", ondelete="CASCADE"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1, comment="退货数量"),
    Column("reason", String(50), nullable=True, comment="退货原因"),
    Column("reason_detail", Text, nullable=True, comment="退货原因详情"),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class OrderReturn(Base):
    """退换货申请记录，包含原因、状态、处理结果等"""
    __tablename__ = "order_returns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    return_number = Column(String(50), nullable=False, unique=True, index=True, comment="退货单号")
    status = Column(Enum(ReturnStatus), nullable=False, default=ReturnStatus.PENDING, comment="退货状态")
    
    # 退货信息
    reason = Column(Enum(ReturnReason), nullable=False, comment="退货原因")
    reason_detail = Column(Text, nullable=True, comment="退货原因详情")
    requested_action = Column(Enum(ReturnAction), nullable=False, comment="请求的处理方式")
    approved_action = Column(Enum(ReturnAction), nullable=True, comment="批准的处理方式")
    
    # 退款信息
    refund_amount = Column(Numeric(10, 2), nullable=True, comment="退款金额")
    refund_tax = Column(Numeric(10, 2), nullable=True, comment="退款税费")
    refund_shipping = Column(Numeric(10, 2), nullable=True, comment="退款运费")
    refund_total = Column(Numeric(10, 2), nullable=True, comment="退款总额")
    refund_method = Column(String(50), nullable=True, comment="退款方式")
    refund_transaction_id = Column(String(100), nullable=True, comment="退款交易ID")
    
    # 退货物流信息
    return_shipping_method = Column(String(100), nullable=True, comment="退货物流方式")
    return_tracking_number = Column(String(100), nullable=True, comment="退货物流单号")
    return_label_url = Column(String(255), nullable=True, comment="退货标签URL")
    customer_needs_to_ship = Column(Boolean, default=True, comment="客户是否需要返回商品")
    
    # 图片和附件
    images = Column(JSON, nullable=True, comment="图片URL列表")
    attachments = Column(JSON, nullable=True, comment="附件URL列表")
    
    # 处理信息
    handler_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="处理人ID")
    handler_name = Column(String(100), nullable=True, comment="处理人姓名")
    resolution_comment = Column(Text, nullable=True, comment="处理结果说明")
    customer_comment = Column(Text, nullable=True, comment="客户备注")
    admin_comment = Column(Text, nullable=True, comment="管理员备注")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    approved_at = Column(DateTime, nullable=True, comment="批准时间")
    received_at = Column(DateTime, nullable=True, comment="收到退货时间")
    refunded_at = Column(DateTime, nullable=True, comment="退款时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    
    # 关联关系
    # order = relationship("Order", back_populates="returns")  # 暂时注释，避免循环导入
    items = relationship("OrderItem", secondary=return_item)
