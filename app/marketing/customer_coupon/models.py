import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class CustomerCouponStatus(str, enum.Enum):
    AVAILABLE = "available"     # 可用
    USED = "used"               # 已使用
    EXPIRED = "expired"         # 已过期
    CANCELLED = "cancelled"     # 已取消


class IssueMethod(str, enum.Enum):
    MANUAL = "manual"           # 手动分配
    EMAIL = "email"             # 邮件发送
    SMS = "sms"                 # 短信发送
    AUTOMATIC = "automatic"     # 自动分配
    SIGNUP = "signup"           # 注册奖励
    REFERRAL = "referral"       # 推荐奖励
    PURCHASE = "purchase"       # 购买奖励
    LOYALTY = "loyalty"         # 忠诚度奖励
    GIVEAWAY = "giveaway"       # 促销活动


class CustomerCoupon(Base):
    """客户-优惠券关联表，记录发放和使用情况"""
    __tablename__ = "customer_coupons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    coupon_id = Column(UUID(as_uuid=True), ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False)
    
    # 状态信息
    status = Column(Enum(CustomerCouponStatus), default=CustomerCouponStatus.AVAILABLE, nullable=False, comment="状态")
    
    # 发放信息
    issue_method = Column(Enum(IssueMethod), nullable=False, comment="发放方式")
    issued_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="发放人")
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="发放时间")
    
    # 使用信息
    used_at = Column(DateTime, nullable=True, comment="使用时间")
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True, comment="使用订单")
    discount_amount = Column(Float, nullable=True, comment="折扣金额")
    
    # 过期设置
    valid_from = Column(DateTime, nullable=True, comment="有效期开始")
    valid_to = Column(DateTime, nullable=True, comment="有效期结束")
    
    # 通知设置
    notification_sent = Column(Boolean, default=False, comment="是否已发送通知")
    notification_method = Column(String(50), nullable=True, comment="通知方式")
    
    # 推荐信息
    referrer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="推荐人")
    
    # 自定义消息
    custom_message = Column(Text, nullable=True, comment="自定义消息")
    
    # 额外信息
    notes = Column(Text, nullable=True, comment="备注")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    customer = relationship("Customer", foreign_keys=[customer_id], back_populates="coupons")
    coupon = relationship("Coupon", back_populates="customer_coupons")
    order = relationship("Order")
    referrer = relationship("Customer", foreign_keys=[referrer_id])
    issuer = relationship("User")
