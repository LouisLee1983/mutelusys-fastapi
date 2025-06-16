import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class CommissionStatus(str, enum.Enum):
    PENDING = "pending"         # 待处理
    APPROVED = "approved"       # 已批准
    REJECTED = "rejected"       # 已拒绝
    PAID = "paid"               # 已支付
    CANCELLED = "cancelled"     # 已取消


class CommissionType(str, enum.Enum):
    FIXED = "fixed"             # 固定金额
    PERCENTAGE = "percentage"   # 百分比
    TIERED = "tiered"           # 阶梯式


class PaymentMethod(str, enum.Enum):
    BANK_TRANSFER = "bank_transfer"  # 银行转账
    PAYPAL = "paypal"               # PayPal
    STRIPE = "stripe"               # Stripe
    CREDIT = "credit"               # 账户余额
    CHECK = "check"                 # 支票
    OTHER = "other"                 # 其他


class AffiliateCommission(Base):
    """分销佣金记录"""
    __tablename__ = "affiliate_commissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affiliate_id = Column(UUID(as_uuid=True), ForeignKey("affiliates.id", ondelete="CASCADE"), nullable=False)
    conversion_id = Column(UUID(as_uuid=True), ForeignKey("affiliate_conversions.id"), nullable=True)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("affiliate_payments.id"), nullable=True)
    
    # 佣金信息
    amount = Column(Float, nullable=False, comment="佣金金额")
    currency_code = Column(String(3), default="USD", comment="货币代码")
    commission_type = Column(Enum(CommissionType), default=CommissionType.PERCENTAGE, nullable=False, comment="佣金类型")
    commission_rate = Column(Float, nullable=True, comment="佣金率")
    
    # 订单信息
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True, comment="关联订单ID")
    order_amount = Column(Float, nullable=True, comment="订单金额")
    order_date = Column(DateTime, nullable=True, comment="订单日期")
    
    # 状态信息
    status = Column(Enum(CommissionStatus), default=CommissionStatus.PENDING, nullable=False, comment="状态")
    approval_date = Column(DateTime, nullable=True, comment="批准日期")
    rejection_date = Column(DateTime, nullable=True, comment="拒绝日期")
    rejection_reason = Column(Text, nullable=True, comment="拒绝原因")
    
    # 支付信息
    payment_date = Column(DateTime, nullable=True, comment="支付日期")
    payment_method = Column(Enum(PaymentMethod), nullable=True, comment="支付方式")
    payment_reference = Column(String(100), nullable=True, comment="支付参考号")
    
    # 佣金期间
    start_date = Column(DateTime, nullable=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    
    # 佣金锁定设置
    is_locked = Column(Boolean, default=False, comment="是否锁定")
    lock_reason = Column(String(255), nullable=True, comment="锁定原因")
    locked_at = Column(DateTime, nullable=True, comment="锁定时间")
    locked_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="锁定用户")
    
    # 审核信息
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="批准用户")
    rejected_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="拒绝用户")
    
    # 备注
    notes = Column(Text, nullable=True, comment="备注")
    admin_notes = Column(Text, nullable=True, comment="管理员备注")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    affiliate = relationship("Affiliate", back_populates="commissions")
    conversion = relationship("AffiliateConversion", back_populates="commission")
    payment = relationship("AffiliatePayment", back_populates="commissions")
    order = relationship("Order")
    locker = relationship("User", foreign_keys=[locked_by])
    approver = relationship("User", foreign_keys=[approved_by])
    rejecter = relationship("User", foreign_keys=[rejected_by])


class AffiliatePayment(Base):
    """分销佣金支付记录"""
    __tablename__ = "affiliate_payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affiliate_id = Column(UUID(as_uuid=True), ForeignKey("affiliates.id", ondelete="CASCADE"), nullable=False)
    
    # 支付信息
    amount = Column(Float, nullable=False, comment="支付金额")
    currency_code = Column(String(3), default="USD", comment="货币代码")
    payment_method = Column(Enum(PaymentMethod), nullable=False, comment="支付方式")
    reference_number = Column(String(100), nullable=True, comment="参考号")
    
    # 状态信息
    status = Column(String(20), default="pending", comment="状态：pending, completed, failed")
    payment_date = Column(DateTime, nullable=True, comment="支付日期")
    
    # 支付详情
    transaction_id = Column(String(100), nullable=True, comment="交易ID")
    payment_details = Column(JSON, nullable=True, comment="支付详情")
    fee_amount = Column(Float, default=0, comment="手续费")
    
    # 佣金期间
    period_start = Column(DateTime, nullable=True, comment="期间开始")
    period_end = Column(DateTime, nullable=True, comment="期间结束")
    
    # 支付摘要
    commissions_count = Column(Integer, default=0, comment="佣金数量")
    notes = Column(Text, nullable=True, comment="备注")
    receipt_url = Column(String(255), nullable=True, comment="收据URL")
    
    # 处理信息
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="处理用户")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    affiliate = relationship("Affiliate")
    commissions = relationship("AffiliateCommission", back_populates="payment")
    processor = relationship("User", foreign_keys=[processed_by])
