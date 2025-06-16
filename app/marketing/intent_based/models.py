import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class IntentBasedCampaign(Base):
    """基于意图的营销，针对不同精神需求的用户群"""
    __tablename__ = "intent_based_campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="活动名称")
    description = Column(Text, nullable=True, comment="活动描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 意图相关设置
    primary_intent = Column(String(50), nullable=False, comment="主要意图：保护、财富、爱情、平衡等")
    secondary_intents = Column(ARRAY(String), nullable=True, comment="次要意图列表")
    intent_description = Column(Text, nullable=True, comment="意图描述和背景")
    
    # 目标用户
    target_segments = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="目标客户细分ID")
    target_preferences = Column(JSON, nullable=True, comment="目标偏好设置")
    
    # 内容设置
    content_story = Column(Text, nullable=True, comment="意图故事内容")
    content_images = Column(ARRAY(String), nullable=True, comment="相关图片URL")
    video_url = Column(String(255), nullable=True, comment="视频URL")
    
    # 产品关联
    product_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="关联产品ID")
    bundle_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="关联套装ID")
    featured_product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True, comment="特色产品ID")
    
    # 优惠设置
    promotion_id = Column(UUID(as_uuid=True), ForeignKey("promotions.id"), nullable=True, comment="相关促销ID")
    coupon_id = Column(UUID(as_uuid=True), ForeignKey("coupons.id"), nullable=True, comment="相关优惠券ID")
    
    # 营销渠道
    email_template_id = Column(String(100), nullable=True, comment="邮件模板ID")
    landing_page_url = Column(String(255), nullable=True, comment="落地页URL")
    social_media_assets = Column(JSON, nullable=True, comment="社交媒体资源")
    
    # 推送设置
    push_title = Column(String(100), nullable=True, comment="推送标题")
    push_body = Column(Text, nullable=True, comment="推送内容")
    push_image_url = Column(String(255), nullable=True, comment="推送图片URL")
    
    # 行动召唤
    cta_text = Column(String(100), nullable=True, comment="行动召唤文本")
    cta_url = Column(String(255), nullable=True, comment="行动召唤URL")
    
    # 时间设置
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    click_count = Column(Integer, default=0, comment="点击次数")
    conversion_count = Column(Integer, default=0, comment="转化次数")
    revenue = Column(Float, default=0, comment="产生收入")
    
    # 额外信息
    tags = Column(ARRAY(String), nullable=True, comment="标签列表")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    featured_product = relationship("Product", foreign_keys=[featured_product_id])
    promotion = relationship("Promotion")
    coupon = relationship("Coupon")
    creator = relationship("User")
    engagement_records = relationship("IntentEngagementRecord", back_populates="campaign", cascade="all, delete-orphan")


class IntentEngagementRecord(Base):
    """意图参与记录，跟踪用户与意图营销的互动"""
    __tablename__ = "intent_engagement_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("intent_based_campaigns.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="客户ID，可为空")
    session_id = Column(String(100), nullable=True, comment="会话ID，用于匿名用户")
    
    # 互动信息
    engagement_type = Column(String(50), nullable=False, comment="互动类型：view, click, add_to_cart, purchase")
    engagement_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="互动时间")
    
    # 内容详情
    content_id = Column(String(100), nullable=True, comment="内容ID")
    content_type = Column(String(50), nullable=True, comment="内容类型")
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True, comment="相关产品ID")
    
    # 设备信息
    device_type = Column(String(50), nullable=True, comment="设备类型")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    
    # 订单信息
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True, comment="相关订单ID")
    order_value = Column(Float, nullable=True, comment="订单金额")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    campaign = relationship("IntentBasedCampaign", back_populates="engagement_records")
    customer = relationship("Customer")
    product = relationship("Product")
    order = relationship("Order")
