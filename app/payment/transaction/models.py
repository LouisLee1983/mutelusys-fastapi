import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class TransactionType(str, enum.Enum):
    PAYMENT = "payment"          # 支付
    REFUND = "refund"            # 退款
    AUTHORIZATION = "authorization"  # 授权
    CAPTURE = "capture"          # 捕获
    VOID = "void"                # 撤销


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"          # 处理中
    SUCCESS = "success"          # 成功
    FAILED = "failed"            # 失败
    CANCELLED = "cancelled"      # 已取消
    REFUNDED = "refunded"        # 已退款
    PARTIALLY_REFUNDED = "partially_refunded"  # 部分退款
    AUTHORIZED = "authorized"    # 已授权
    CAPTURED = "captured"        # 已捕获
    VOIDED = "voided"            # 已撤销
    EXPIRED = "expired"          # 已过期


class PaymentTransaction(Base):
    """支付交易记录，关联订单与支付方式"""
    __tablename__ = "payment_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("payment_methods.id"), nullable=False)
    
    # 交易信息
    transaction_type = Column(Enum(TransactionType), nullable=False, comment="交易类型")
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False, comment="交易状态")
    amount = Column(Float, nullable=False, comment="交易金额")
    currency_code = Column(String(3), nullable=False, comment="货币代码")
    fee_amount = Column(Float, default=0, comment="手续费金额")
    transaction_id = Column(String(100), nullable=True, comment="第三方交易ID")
    parent_transaction_id = Column(UUID(as_uuid=True), ForeignKey("payment_transactions.id"), nullable=True, comment="父交易ID")
    
    # 客户信息
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    customer_ip = Column(String(50), nullable=True, comment="客户IP地址")
    customer_user_agent = Column(String(255), nullable=True, comment="客户User-Agent")
    
    # 支付详情
    payment_details = Column(JSON, nullable=True, comment="支付详情，如卡号后四位、支付账户等")
    
    # 交易响应
    response_code = Column(String(50), nullable=True, comment="响应代码")
    response_message = Column(Text, nullable=True, comment="响应消息")
    gateway_response = Column(JSON, nullable=True, comment="网关响应详情")
    
    # 结算信息
    is_settled = Column(Boolean, default=False, comment="是否已结算")
    settlement_date = Column(DateTime, nullable=True, comment="结算日期")
    
    # 其他信息
    description = Column(Text, nullable=True, comment="交易描述")
    note = Column(Text, nullable=True, comment="内部备注")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 退款相关
    refunded_amount = Column(Float, default=0, comment="已退款金额")
    is_refundable = Column(Boolean, default=False, comment="是否可退款")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expired_at = Column(DateTime, nullable=True, comment="过期时间")
    
    # 关联关系
    order = relationship("Order")
    payment_method = relationship("PaymentMethod", back_populates="transactions")
    customer = relationship("Customer")
    parent_transaction = relationship("PaymentTransaction", remote_side=[id])
    child_transactions = relationship("PaymentTransaction", back_populates="parent_transaction")
