import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class CampaignType(str, enum.Enum):
    EMAIL = "email"           # 邮件营销
    SMS = "sms"               # 短信营销
    PUSH = "push"             # 推送通知
    SOCIAL = "social"         # 社交媒体
    DISPLAY = "display"       # 展示广告
    SEARCH = "search"         # 搜索广告
    AFFILIATE = "affiliate"   # 联盟营销
    REFERRAL = "referral"     # 推荐营销
    CONTENT = "content"       # 内容营销
    INFLUENCER = "influencer"  # 网红营销
    EVENT = "event"           # 活动营销
    SEASONAL = "seasonal"     # 季节性营销
    LOYALTY = "loyalty"       # 忠诚度营销
    RETARGETING = "retargeting"  # 再营销


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"          # 草稿
    SCHEDULED = "scheduled"  # 已计划
    ACTIVE = "active"        # 激活
    PAUSED = "paused"        # 暂停
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class Campaign(Base):
    """营销活动，包含渠道、预算、效果等"""
    __tablename__ = "marketing_campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="活动名称")
    description = Column(Text, nullable=True, comment="活动描述")
    type = Column(Enum(CampaignType), nullable=False, comment="活动类型")
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False, comment="活动状态")
    
    # 时间设置
    start_date = Column(DateTime, nullable=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    execution_time = Column(DateTime, nullable=True, comment="执行时间（对于定时活动）")
    
    # 受众设置
    target_audience = Column(String(50), default="all", comment="目标受众：all, segment, specific")
    customer_segments = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="客户细分ID列表")
    target_customers = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="目标客户ID列表")
    exclusion_list = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除客户ID列表")
    audience_size = Column(Integer, nullable=True, comment="受众大小")
    
    # 预算与费用
    budget = Column(Float, nullable=True, comment="活动预算")
    actual_cost = Column(Float, default=0, comment="实际费用")
    cost_per_acquisition = Column(Float, nullable=True, comment="客户获取成本")
    currency_code = Column(String(3), default="USD", comment="货币代码")
    
    # 内容设置
    content_template_id = Column(UUID(as_uuid=True), nullable=True, comment="内容模板ID")
    subject_line = Column(String(200), nullable=True, comment="主题行(适用于邮件)")
    sender_name = Column(String(100), nullable=True, comment="发件人名称")
    sender_email = Column(String(100), nullable=True, comment="发件人邮箱")
    reply_to = Column(String(100), nullable=True, comment="回复邮箱")
    
    # 促销相关
    promotion_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="相关促销ID列表")
    
    # 渠道设置
    primary_channel = Column(String(50), nullable=False, comment="主要渠道")
    secondary_channels = Column(ARRAY(String), nullable=True, comment="次要渠道列表")
    utm_source = Column(String(100), nullable=True, comment="UTM来源")
    utm_medium = Column(String(100), nullable=True, comment="UTM媒介")
    utm_campaign = Column(String(100), nullable=True, comment="UTM活动")
    
    # 执行状态
    sent_count = Column(Integer, default=0, comment="发送数量")
    delivered_count = Column(Integer, default=0, comment="送达数量")
    open_count = Column(Integer, default=0, comment="打开数量")
    click_count = Column(Integer, default=0, comment="点击数量")
    conversion_count = Column(Integer, default=0, comment="转化数量")
    bounce_count = Column(Integer, default=0, comment="退回数量")
    unsubscribe_count = Column(Integer, default=0, comment="退订数量")
    execution_status = Column(String(50), nullable=True, comment="执行状态详情")
    
    # 效果评估
    revenue_generated = Column(Float, default=0, comment="产生收入")
    roi = Column(Float, nullable=True, comment="投资回报率")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    open_rate = Column(Float, nullable=True, comment="打开率")
    click_rate = Column(Float, nullable=True, comment="点击率")
    
    # A/B测试
    is_ab_test = Column(Boolean, default=False, comment="是否A/B测试")
    test_variants = Column(JSON, nullable=True, comment="测试变体配置")
    winning_variant = Column(String(50), nullable=True, comment="胜出变体")
    
    # 关联和标签
    parent_campaign_id = Column(UUID(as_uuid=True), ForeignKey("marketing_campaigns.id"), nullable=True)
    tags = Column(ARRAY(String), nullable=True, comment="标签列表")
    
    # 文化和意图
    cultural_theme = Column(String(100), nullable=True, comment="文化主题")
    intention_focus = Column(String(100), nullable=True, comment="意图焦点")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    parent_campaign = relationship("Campaign", remote_side=[id], backref="sub_campaigns")
    creator = relationship("User")
    campaign_events = relationship("CampaignEvent", back_populates="campaign", cascade="all, delete-orphan")


class CampaignEvent(Base):
    """活动事件日志"""
    __tablename__ = "campaign_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("marketing_campaigns.id", ondelete="CASCADE"), nullable=False)
    
    # 事件信息
    event_type = Column(String(50), nullable=False, comment="事件类型")
    event_date = Column(DateTime, default=datetime.utcnow, nullable=False, comment="事件日期")
    details = Column(JSON, nullable=True, comment="事件详情")
    
    # 客户相关
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    
    # 关联关系
    campaign = relationship("Campaign", back_populates="campaign_events")
    customer = relationship("Customer")
