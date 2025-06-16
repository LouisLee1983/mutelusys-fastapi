import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 材质类型枚举
class MaterialType(str, enum.Enum):
    GEM = "gem"                    # 宝石
    CRYSTAL = "crystal"            # 水晶
    WOOD = "wood"                  # 木材
    METAL = "metal"                # 金属
    FABRIC = "fabric"              # 布料
    CERAMIC = "ceramic"            # 陶瓷
    LEATHER = "leather"            # 皮革
    STONE = "stone"                # 石材
    PLANT = "plant"                # 植物材料
    OTHER = "other"                # 其他材质


# 材质指南与产品材质的多对多关联表
material_guide_product_material = Table(
    "material_guide_product_material",
    Base.metadata,
    Column("guide_id", UUID(as_uuid=True), ForeignKey("material_guides.id", ondelete="CASCADE"), primary_key=True),
    Column("material_id", UUID(as_uuid=True), ForeignKey("product_materials.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class MaterialGuide(Base):
    """材质指南表，介绍各类宝石、木材等材质的特性和价值"""
    __tablename__ = "material_guides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="材质指南标题")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="别名，用于URL")
    content = Column(Text, nullable=False, comment="材质详细介绍")
    excerpt = Column(Text, nullable=True, comment="摘要")
    material_type = Column(Enum(MaterialType), nullable=False, comment="材质类型")
    origin = Column(String(100), nullable=True, comment="原产地")
    physical_properties = Column(Text, nullable=True, comment="物理特性")
    spiritual_properties = Column(Text, nullable=True, comment="精神特性")
    care_instructions = Column(Text, nullable=True, comment="保养说明")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    additional_images = Column(ARRAY(String), nullable=True, comment="额外图片URL数组")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, comment="状态")
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    view_count = Column(Integer, default=0, comment="浏览次数")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    video_url = Column(String(255), nullable=True, comment="相关视频URL")
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("MaterialGuideTranslation", back_populates="guide", cascade="all, delete-orphan")
    materials = relationship("ProductMaterial", secondary=material_guide_product_material, back_populates="guides")


class MaterialGuideTranslation(Base):
    """材质指南多语言翻译表"""
    __tablename__ = "material_guide_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guide_id = Column(UUID(as_uuid=True), ForeignKey("material_guides.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="材质指南标题")
    content = Column(Text, nullable=False, comment="材质详细介绍")
    excerpt = Column(Text, nullable=True, comment="摘要")
    origin = Column(String(100), nullable=True, comment="原产地")
    physical_properties = Column(Text, nullable=True, comment="物理特性")
    spiritual_properties = Column(Text, nullable=True, comment="精神特性")
    care_instructions = Column(Text, nullable=True, comment="保养说明")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    guide = relationship("MaterialGuide", back_populates="translations")

    # 联合索引确保每个材质指南对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
