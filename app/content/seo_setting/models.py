import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


# SEO实体类型枚举
class SEOEntityType(str, enum.Enum):
    HOMEPAGE = "homepage"          # 首页
    PRODUCT = "product"            # 商品页
    CATEGORY = "category"          # 分类页
    BLOG = "blog"                  # 博客文章页
    BLOG_CATEGORY = "blog_category"  # 博客分类页
    PAGE = "page"                  # 自定义页面
    OTHER = "other"                # 其他页面


class SEOSetting(Base):
    """SEO设置表，包含Meta标题、描述、关键词等"""
    __tablename__ = "seo_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(Enum(SEOEntityType), nullable=False, comment="实体类型")
    entity_id = Column(UUID(as_uuid=True), nullable=True, comment="实体ID，如商品ID、分类ID等")
    page_path = Column(String(255), nullable=True, comment="页面路径，用于自定义页面")
    title = Column(String(255), nullable=False, comment="Meta标题")
    description = Column(String(500), nullable=True, comment="Meta描述")
    keywords = Column(String(255), nullable=True, comment="Meta关键词")
    canonical_url = Column(String(255), nullable=True, comment="规范URL")
    robots = Column(String(50), nullable=True, default="index,follow", comment="robots指令")
    og_title = Column(String(255), nullable=True, comment="Open Graph标题")
    og_description = Column(String(500), nullable=True, comment="Open Graph描述")
    og_image = Column(String(255), nullable=True, comment="Open Graph图片")
    twitter_card = Column(String(20), nullable=True, default="summary", comment="Twitter卡片类型")
    twitter_title = Column(String(255), nullable=True, comment="Twitter标题")
    twitter_description = Column(String(500), nullable=True, comment="Twitter描述")
    twitter_image = Column(String(255), nullable=True, comment="Twitter图片")
    schema_markup = Column(Text, nullable=True, comment="Schema.org结构化标记")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("SEOSettingTranslation", back_populates="seo_setting", cascade="all, delete-orphan")


class SEOSettingTranslation(Base):
    """SEO设置多语言翻译表"""
    __tablename__ = "seo_setting_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seo_setting_id = Column(UUID(as_uuid=True), ForeignKey("seo_settings.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="Meta标题")
    description = Column(String(500), nullable=True, comment="Meta描述")
    keywords = Column(String(255), nullable=True, comment="Meta关键词")
    og_title = Column(String(255), nullable=True, comment="Open Graph标题")
    og_description = Column(String(500), nullable=True, comment="Open Graph描述")
    twitter_title = Column(String(255), nullable=True, comment="Twitter标题")
    twitter_description = Column(String(500), nullable=True, comment="Twitter描述")
    schema_markup = Column(Text, nullable=True, comment="Schema.org结构化标记")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    seo_setting = relationship("SEOSetting", back_populates="translations")

    # 联合索引确保每个SEO设置对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
