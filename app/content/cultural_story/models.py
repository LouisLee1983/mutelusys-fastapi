import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 文化区域枚举
class CulturalRegion(str, enum.Enum):
    ASIA_SOUTHEAST = "asia_southeast"  # 东南亚
    ASIA_EAST = "asia_east"            # 东亚
    ASIA_SOUTH = "asia_south"          # 南亚
    ASIA_CENTRAL = "asia_central"      # 中亚
    AFRICA = "africa"                  # 非洲
    EUROPE = "europe"                  # 欧洲
    AMERICAS = "americas"              # 美洲
    OCEANIA = "oceania"                # 大洋洲
    GLOBAL = "global"                  # 全球性


# 文化故事与产品符号的多对多关联表
cultural_story_symbol = Table(
    "cultural_story_symbol",
    Base.metadata,
    Column("story_id", UUID(as_uuid=True), ForeignKey("cultural_stories.id", ondelete="CASCADE"), primary_key=True),
    Column("symbol_id", UUID(as_uuid=True), ForeignKey("product_symbols.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


# 文化故事与产品的多对多关联表
cultural_story_product = Table(
    "cultural_story_product",
    Base.metadata,
    Column("story_id", UUID(as_uuid=True), ForeignKey("cultural_stories.id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class CulturalStory(Base):
    """文化故事内容表，关联产品背后的文化意义和精神象征"""
    __tablename__ = "cultural_stories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="故事标题")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="故事别名，用于URL")
    content = Column(Text, nullable=False, comment="故事内容")
    excerpt = Column(Text, nullable=True, comment="故事摘要")
    cultural_region = Column(Enum(CulturalRegion), nullable=False, comment="文化区域")
    historical_period = Column(String(100), nullable=True, comment="历史时期")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, comment="状态")
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    view_count = Column(Integer, default=0, comment="浏览次数")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    additional_media = Column(JSON, nullable=True, comment="额外媒体，如视频、音频链接")
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("CulturalStoryTranslation", back_populates="story", cascade="all, delete-orphan")
    symbols = relationship("ProductSymbol", secondary=cultural_story_symbol, back_populates="stories")
    products = relationship("Product", secondary=cultural_story_product, back_populates="stories")


class CulturalStoryTranslation(Base):
    """文化故事多语言翻译表"""
    __tablename__ = "cultural_story_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    story_id = Column(UUID(as_uuid=True), ForeignKey("cultural_stories.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="故事标题")
    content = Column(Text, nullable=False, comment="故事内容")
    excerpt = Column(Text, nullable=True, comment="故事摘要")
    historical_period = Column(String(100), nullable=True, comment="历史时期")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    story = relationship("CulturalStory", back_populates="translations")

    # 联合索引确保每个故事对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
