import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 场景内容与产品场景的多对多关联表
scene_content_product_scene = Table(
    "scene_content_product_scene",
    Base.metadata,
    Column("content_id", UUID(as_uuid=True), ForeignKey("scene_based_contents.id", ondelete="CASCADE"), primary_key=True),
    Column("scene_id", UUID(as_uuid=True), ForeignKey("product_scenes.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


# 场景内容与产品的多对多关联表
scene_content_product = Table(
    "scene_content_product",
    Base.metadata,
    Column("content_id", UUID(as_uuid=True), ForeignKey("scene_based_contents.id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class SceneBasedContent(Base):
    """基于场景的内容表，为不同生活场景（如冥想、家居）提供专业知识"""
    __tablename__ = "scene_based_contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="内容标题")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="别名，用于URL")
    content = Column(Text, nullable=False, comment="详细内容")
    excerpt = Column(Text, nullable=True, comment="摘要")
    space_design = Column(Text, nullable=True, comment="空间设计建议")
    color_scheme = Column(Text, nullable=True, comment="色彩方案")
    lighting_tips = Column(Text, nullable=True, comment="灯光建议")
    product_placement = Column(Text, nullable=True, comment="产品摆放")
    styling_tips = Column(Text, nullable=True, comment="搭配技巧")
    maintenance_guidance = Column(Text, nullable=True, comment="维护指导")
    mood_enhancement = Column(Text, nullable=True, comment="氛围提升")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    additional_images = Column(ARRAY(String), nullable=True, comment="额外图片URL数组")
    video_url = Column(String(255), nullable=True, comment="视频URL")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, comment="状态")
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    view_count = Column(Integer, default=0, comment="浏览次数")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("SceneBasedContentTranslation", back_populates="content", cascade="all, delete-orphan")
    scenes = relationship("ProductScene", secondary=scene_content_product_scene, back_populates="scene_contents")
    products = relationship("Product", secondary=scene_content_product, back_populates="scene_contents")


class SceneBasedContentTranslation(Base):
    """基于场景的内容多语言翻译表"""
    __tablename__ = "scene_based_content_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("scene_based_contents.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="内容标题")
    content = Column(Text, nullable=False, comment="详细内容")
    excerpt = Column(Text, nullable=True, comment="摘要")
    space_design = Column(Text, nullable=True, comment="空间设计建议")
    color_scheme = Column(Text, nullable=True, comment="色彩方案")
    lighting_tips = Column(Text, nullable=True, comment="灯光建议")
    product_placement = Column(Text, nullable=True, comment="产品摆放")
    styling_tips = Column(Text, nullable=True, comment="搭配技巧")
    maintenance_guidance = Column(Text, nullable=True, comment="维护指导")
    mood_enhancement = Column(Text, nullable=True, comment="氛围提升")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    content = relationship("SceneBasedContent", back_populates="translations")

    # 联合索引确保每个内容对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
