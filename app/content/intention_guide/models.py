import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 意图使用指南与产品意图的多对多关联表
intention_guide_intent = Table(
    "intention_guide_intent",
    Base.metadata,
    Column("guide_id", UUID(as_uuid=True), ForeignKey("intention_guides.id", ondelete="CASCADE"), primary_key=True),
    Column("intent_id", UUID(as_uuid=True), ForeignKey("product_intents.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


# 意图使用指南与产品的多对多关联表
intention_guide_product = Table(
    "intention_guide_product",
    Base.metadata,
    Column("guide_id", UUID(as_uuid=True), ForeignKey("intention_guides.id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class IntentionGuide(Base):
    """意图使用指南表，解释如何使用产品达到特定意图效果"""
    __tablename__ = "intention_guides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="指南标题")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="别名，用于URL")
    content = Column(Text, nullable=False, comment="详细内容")
    excerpt = Column(Text, nullable=True, comment="摘要")
    usage_steps = Column(Text, nullable=True, comment="使用步骤")
    ritual_description = Column(Text, nullable=True, comment="仪式描述")
    placement_guidance = Column(Text, nullable=True, comment="摆放指导")
    wearing_guidance = Column(Text, nullable=True, comment="佩戴指导")
    activation_method = Column(Text, nullable=True, comment="激活方法")
    maintenance_tips = Column(Text, nullable=True, comment="维护技巧")
    best_practices = Column(Text, nullable=True, comment="最佳实践")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    additional_images = Column(ARRAY(String), nullable=True, comment="额外图片URL数组")
    video_url = Column(String(255), nullable=True, comment="视频指导URL")
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
    translations = relationship("IntentionGuideTranslation", back_populates="guide", cascade="all, delete-orphan")
    # intents = relationship("ProductIntent", secondary=intention_guide_intent, back_populates="intention_guides")  # 暂时注释
    products = relationship("Product", secondary=intention_guide_product, back_populates="intention_guides")


class IntentionGuideTranslation(Base):
    """意图使用指南多语言翻译表"""
    __tablename__ = "intention_guide_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guide_id = Column(UUID(as_uuid=True), ForeignKey("intention_guides.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="指南标题")
    content = Column(Text, nullable=False, comment="详细内容")
    excerpt = Column(Text, nullable=True, comment="摘要")
    usage_steps = Column(Text, nullable=True, comment="使用步骤")
    ritual_description = Column(Text, nullable=True, comment="仪式描述")
    placement_guidance = Column(Text, nullable=True, comment="摆放指导")
    wearing_guidance = Column(Text, nullable=True, comment="佩戴指导")
    activation_method = Column(Text, nullable=True, comment="激活方法")
    maintenance_tips = Column(Text, nullable=True, comment="维护技巧")
    best_practices = Column(Text, nullable=True, comment="最佳实践")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    guide = relationship("IntentionGuide", back_populates="translations")

    # 联合索引确保每个意图指南对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
