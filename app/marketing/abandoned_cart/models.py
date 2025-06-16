import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class CartStatus(str, enum.Enum):
    ACTIVE = "active"               # 活跃
    ABANDONED = "abandoned"         # 已遗弃
    RECOVERED = "recovered"         # 已恢复
    CONVERTED = "converted"         # 已转化为订单
    EXPIRED = "expired"             # 已过期


class ReminderStatus(str, enum.Enum):
    SCHEDULED = "scheduled"         # 已计划
    SENT = "sent"                   # 已发送
    FAILED = "failed"               # 发送失败
    OPENED = "opened"               # 已打开
    CLICKED = "clicked"             # 已点击


class AbandonedCart(Base):
    """放弃购物车记录，用于自动提醒"""
    __tablename__ = "abandoned_carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(255), nullable=True, comment="会话ID（用于非登录用户）")
    
    # 状态信息
    status = Column(Enum(CartStatus), default=CartStatus.ACTIVE, nullable=False, comment="购物车状态")
    abandoned_at = Column(DateTime, nullable=True, comment="遗弃时间")
    recovered_at = Column(DateTime, nullable=True, comment="恢复时间")
    
    # 购物车内容
    items_count = Column(Integer, default=0, comment="商品数量")
    total_value = Column(Float, default=0, comment="总价值")
    currency_code = Column(String(3), default="USD", comment="货币代码")
    cart_items = Column(JSON, nullable=True, comment="购物车商品，格式：[{product_id, sku_id, quantity, price}]")
    
    # 客户信息
    customer_email = Column(String(255), nullable=True, comment="客户邮箱")
    customer_phone = Column(String(50), nullable=True, comment="客户电话")
    
    # 营销关联
    coupon_issued = Column(Boolean, default=False, comment="是否已发放优惠券")
    coupon_id = Column(UUID(as_uuid=True), ForeignKey("coupons.id"), nullable=True, comment="发放的优惠券ID")
    discount_amount = Column(Float, nullable=True, comment="优惠金额")
    
    # 跟踪信息
    utm_source = Column(String(100), nullable=True, comment="UTM来源")
    utm_medium = Column(String(100), nullable=True, comment="UTM媒介")
    utm_campaign = Column(String(100), nullable=True, comment="UTM活动")
    
    # 恢复链接
    recovery_url = Column(String(255), nullable=True, comment="恢复链接")
    recovery_token = Column(String(100), nullable=True, comment="恢复令牌")
    recovery_expires_at = Column(DateTime, nullable=True, comment="恢复链接过期时间")
    
    # 设备信息
    device_type = Column(String(50), nullable=True, comment="设备类型")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    customer = relationship("Customer", back_populates="abandoned_carts")
    coupon = relationship("Coupon")
    reminders = relationship("AbandonedCartReminder", back_populates="cart", cascade="all, delete-orphan")


class AbandonedCartReminder(Base):
    """购物车提醒记录"""
    __tablename__ = "abandoned_cart_reminders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("abandoned_carts.id", ondelete="CASCADE"), nullable=False)
    
    # 提醒信息
    reminder_type = Column(String(20), default="email", comment="提醒类型：email, sms, push等")
    status = Column(Enum(ReminderStatus), default=ReminderStatus.SCHEDULED, nullable=False, comment="提醒状态")
    scheduled_at = Column(DateTime, nullable=False, comment="计划发送时间")
    sent_at = Column(DateTime, nullable=True, comment="实际发送时间")
    
    # 内容信息
    template_id = Column(String(100), nullable=True, comment="模板ID")
    subject = Column(String(255), nullable=True, comment="邮件主题")
    content = Column(Text, nullable=True, comment="邮件内容")
    
    # 统计信息
    opened_at = Column(DateTime, nullable=True, comment="打开时间")
    clicked_at = Column(DateTime, nullable=True, comment="点击时间")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    cart = relationship("AbandonedCart", back_populates="reminders")
