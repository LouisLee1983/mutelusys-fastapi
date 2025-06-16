import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


class BlogCategory(Base):
    """博客分类表"""
    __tablename__ = "blog_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="分类别名，用于URL")
    description = Column(Text, nullable=True, comment="分类描述")
    parent_id = Column(UUID(as_uuid=True), ForeignKey("blog_categories.id"), nullable=True, comment="父分类ID")
    image_url = Column(String(255), nullable=True, comment="分类图片URL")
    icon = Column(String(100), nullable=True, comment="分类图标")
    is_active = Column(Boolean, default=True, comment="是否激活")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    parent = relationship("BlogCategory", remote_side=[id], backref="children")
    blogs = relationship("Blog", back_populates="category")
    translations = relationship("BlogCategoryTranslation", back_populates="category", cascade="all, delete-orphan")


class BlogCategoryTranslation(Base):
    """博客分类多语言翻译表"""
    __tablename__ = "blog_category_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("blog_categories.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    name = Column(String(100), nullable=False, comment="分类名称")
    description = Column(Text, nullable=True, comment="分类描述")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    category = relationship("BlogCategory", back_populates="translations")

    # 联合索引确保每个分类对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
