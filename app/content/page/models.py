import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


class Page(Base):
    """页面内容表，包含标题、内容、模板、SEO信息等"""
    __tablename__ = "pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="页面别名，用于URL")
    title = Column(String(255), nullable=False, comment="页面标题")
    content = Column(Text, nullable=True, comment="页面内容")
    template = Column(String(100), nullable=True, comment="页面模板")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, comment="页面状态")
    is_homepage = Column(Boolean, default=False, comment="是否首页")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("PageTranslation", back_populates="page", cascade="all, delete-orphan")
