import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ContentType(str, enum.Enum):
    BLOG = "blog"             # 博客文章
    STORY = "story"           # 文化故事
    GUIDE = "guide"           # 使用指南
    VIDEO = "video"           # 视频内容
    INFOGRAPHIC = "infographic"  # 信息图表
    SOCIAL_POST = "social_post"  # 社交媒体帖子
    EMAIL = "email"           # 邮件内容


class CulturalContentCampaign(Base):
    """文化内容营销，通过文化故事和符号意义传播产品价值"""
    __tablename__ = "cultural_content_campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="活动名称")
    description = Column(Text, nullable=True, comment="活动描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 文化相关设置
    cultural_theme = Column(String(100), nullable=False, comment="文化主题")
    cultural_region = Column(String(100), nullable=True, comment="文化区域")
    cultural_symbols = Column(ARRAY(String), nullable=True, comment="相关文化符号")
    
    # 内容设置
    main_story = Column(Text, nullable=True, comment="主要故事内容")
    storytelling_angle = Column(String(255), nullable=True, comment="讲故事角度")
    content_keywords = Column(ARRAY(String), nullable=True, comment="内容关键词")
    
    # 目标设置
    target_audience = Column(JSON, nullable=True, comment="目标受众")
    target_channels = Column(ARRAY(String), nullable=True, comment="目标渠道")
    
    # 媒体资源
    media_files = Column(JSON, nullable=True, comment="媒体文件，格式：[{type, url, title, description}]")
    cover_image_url = Column(String(255), nullable=True, comment="封面图片URL")
    featured_video_url = Column(String(255), nullable=True, comment="特色视频URL")
    
    # 产品关联
    related_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="相关产品ID")
    related_symbols = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="相关符号ID")
    related_materials = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="相关材料ID")
    
    # SEO设置
    seo_title = Column(String(100), nullable=True, comment="SEO标题")
    seo_description = Column(String(255), nullable=True, comment="SEO描述")
    seo_keywords = Column(ARRAY(String), nullable=True, comment="SEO关键词")
    
    # 发布设置
    publication_status = Column(String(20), default="draft", comment="发布状态：draft, scheduled, published")
    publish_date = Column(DateTime, nullable=True, comment="发布日期")
    expiry_date = Column(DateTime, nullable=True, comment="过期日期")
    
    # 社交媒体设置
    social_media_caption = Column(Text, nullable=True, comment="社交媒体说明")
    social_media_hashtags = Column(ARRAY(String), nullable=True, comment="社交媒体标签")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    engagement_count = Column(Integer, default=0, comment="互动次数")
    share_count = Column(Integer, default=0, comment="分享次数")
    conversion_count = Column(Integer, default=0, comment="转化次数")
    
    # 额外信息
    tags = Column(ARRAY(String), nullable=True, comment="标签列表")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    creator = relationship("User")
    content_items = relationship("CulturalContentItem", back_populates="campaign", cascade="all, delete-orphan")


class CulturalContentItem(Base):
    """文化内容项目，一个活动可包含多个内容项目"""
    __tablename__ = "cultural_content_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("cultural_content_campaigns.id", ondelete="CASCADE"), nullable=False)
    
    # 内容基本信息
    title = Column(String(255), nullable=False, comment="标题")
    subtitle = Column(String(255), nullable=True, comment="副标题")
    content_type = Column(Enum(ContentType), nullable=False, comment="内容类型")
    content = Column(Text, nullable=True, comment="内容正文")
    
    # 媒体信息
    featured_image_url = Column(String(255), nullable=True, comment="特色图片URL")
    media_gallery = Column(JSON, nullable=True, comment="媒体库")
    
    # 发布信息
    status = Column(String(20), default="draft", comment="状态：draft, review, published")
    publish_date = Column(DateTime, nullable=True, comment="发布日期")
    
    # 内容元数据
    author = Column(String(100), nullable=True, comment="作者")
    reading_time = Column(Integer, nullable=True, comment="阅读时间（分钟）")
    
    # 各渠道URL
    website_url = Column(String(255), nullable=True, comment="网站URL")
    blog_url = Column(String(255), nullable=True, comment="博客URL")
    social_media_urls = Column(JSON, nullable=True, comment="社交媒体URL")
    
    # 统计数据
    views = Column(Integer, default=0, comment="浏览量")
    likes = Column(Integer, default=0, comment="点赞数")
    comments = Column(Integer, default=0, comment="评论数")
    shares = Column(Integer, default=0, comment="分享数")
    
    # 额外设置
    call_to_action = Column(JSON, nullable=True, comment="行动召唤按钮")
    related_product_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="相关产品ID")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    campaign = relationship("CulturalContentCampaign", back_populates="content_items")
    creator = relationship("User")
    engagement_records = relationship("ContentEngagement", back_populates="content_item", cascade="all, delete-orphan")


class ContentEngagement(Base):
    """内容互动记录"""
    __tablename__ = "content_engagements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_item_id = Column(UUID(as_uuid=True), ForeignKey("cultural_content_items.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="客户ID，可为空")
    
    # 互动信息
    engagement_type = Column(String(20), nullable=False, comment="互动类型：view, like, comment, share, click")
    engagement_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="互动时间")
    
    # 内容相关
    comment_text = Column(Text, nullable=True, comment="评论内容")
    rating = Column(Integer, nullable=True, comment="评分（1-5）")
    
    # 设备信息
    device_type = Column(String(50), nullable=True, comment="设备类型")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    
    # 归因信息
    referrer = Column(String(255), nullable=True, comment="来源URL")
    utm_source = Column(String(100), nullable=True, comment="UTM来源")
    utm_medium = Column(String(100), nullable=True, comment="UTM媒介")
    utm_campaign = Column(String(100), nullable=True, comment="UTM活动")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    content_item = relationship("CulturalContentItem", back_populates="engagement_records")
    customer = relationship("Customer")
