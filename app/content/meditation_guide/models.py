import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 冥想类型枚举
class MeditationType(str, enum.Enum):
    MINDFULNESS = "mindfulness"          # 正念冥想
    TRANSCENDENTAL = "transcendental"    # 超然冥想
    GUIDED = "guided"                    # 引导式冥想
    CHAKRA = "chakra"                    # 脉轮冥想
    MANTRA = "mantra"                    # 咒语冥想
    VISUALIZATION = "visualization"      # 可视化冥想
    MOVEMENT = "movement"                # 运动冥想
    BREATHING = "breathing"              # 呼吸冥想
    LOVING_KINDNESS = "loving_kindness"  # 慈心冥想
    ZEN = "zen"                          # 禅修
    OTHER = "other"                      # 其他类型


# 体验等级枚举
class ExperienceLevel(str, enum.Enum):
    BEGINNER = "beginner"        # 初学者
    INTERMEDIATE = "intermediate"  # 中级
    ADVANCED = "advanced"        # 高级
    ALL_LEVELS = "all_levels"    # 所有级别


# 冥想指南与意图的多对多关联表
meditation_guide_intent = Table(
    "meditation_guide_intent",
    Base.metadata,
    Column("guide_id", UUID(as_uuid=True), ForeignKey("meditation_guides.id", ondelete="CASCADE"), primary_key=True),
    Column("intent_id", UUID(as_uuid=True), ForeignKey("product_intents.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


# 冥想指南与产品的多对多关联表
meditation_guide_product = Table(
    "meditation_guide_product",
    Base.metadata,
    Column("guide_id", UUID(as_uuid=True), ForeignKey("meditation_guides.id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class MeditationGuide(Base):
    """冥想指南表，提供与产品相关的精神修行内容"""
    __tablename__ = "meditation_guides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="冥想标题")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="别名，用于URL")
    content = Column(Text, nullable=False, comment="详细指导内容")
    excerpt = Column(Text, nullable=True, comment="摘要")
    meditation_type = Column(Enum(MeditationType), nullable=False, comment="冥想类型")
    experience_level = Column(Enum(ExperienceLevel), nullable=False, default=ExperienceLevel.ALL_LEVELS, comment="体验级别")
    duration_minutes = Column(Integer, nullable=True, comment="时长（分钟）")
    benefits = Column(Text, nullable=True, comment="好处")
    instructions = Column(Text, nullable=True, comment="详细步骤说明")
    audio_url = Column(String(255), nullable=True, comment="音频指导URL")
    video_url = Column(String(255), nullable=True, comment="视频指导URL")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    additional_images = Column(ARRAY(String), nullable=True, comment="额外图片URL数组")
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
    translations = relationship("MeditationGuideTranslation", back_populates="guide", cascade="all, delete-orphan")
    # intents = relationship("ProductIntent", secondary=meditation_guide_intent, back_populates="meditation_guides")  # 暂时注释
    products = relationship("Product", secondary=meditation_guide_product, back_populates="meditation_guides")


class MeditationGuideTranslation(Base):
    """冥想指南多语言翻译表"""
    __tablename__ = "meditation_guide_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guide_id = Column(UUID(as_uuid=True), ForeignKey("meditation_guides.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="冥想标题")
    content = Column(Text, nullable=False, comment="详细指导内容")
    excerpt = Column(Text, nullable=True, comment="摘要")
    benefits = Column(Text, nullable=True, comment="好处")
    instructions = Column(Text, nullable=True, comment="详细步骤说明")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    guide = relationship("MeditationGuide", back_populates="translations")

    # 联合索引确保每个冥想指南对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
