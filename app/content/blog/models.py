import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 博客文章与标签的多对多关联表
blog_tag = Table(
    "blog_tag",
    Base.metadata,
    Column("blog_id", UUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class Blog(Base):
    """博客文章表，包含标题、内容、作者、标签等"""
    __tablename__ = "blogs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="文章别名，用于URL")
    title = Column(String(255), nullable=False, comment="文章标题")
    content = Column(Text, nullable=True, comment="文章内容")
    excerpt = Column(Text, nullable=True, comment="文章摘要")
    category_id = Column(UUID(as_uuid=True), ForeignKey("blog_categories.id"), nullable=True, comment="分类ID")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, comment="文章状态")
    is_featured = Column(Boolean, default=False, comment="是否推荐文章")
    is_commentable = Column(Boolean, default=True, comment="是否允许评论")
    view_count = Column(Integer, default=0, comment="浏览次数")
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="作者ID")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    category = relationship("BlogCategory", back_populates="blogs")
    translations = relationship("BlogTranslation", back_populates="blog", cascade="all, delete-orphan")
    tags = relationship("BlogTag", secondary=blog_tag, back_populates="blogs")


class BlogTranslation(Base):
    """博客文章多语言翻译表"""
    __tablename__ = "blog_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="文章标题")
    content = Column(Text, nullable=True, comment="文章内容")
    excerpt = Column(Text, nullable=True, comment="文章摘要")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    blog = relationship("Blog", back_populates="translations")

    # 联合索引确保每篇文章对每种语言只有一个翻译
    __table_args__ = (
        {},
    )


class BlogTag(Base):
    """博客标签表"""
    __tablename__ = "blog_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True, comment="标签名称")
    slug = Column(String(50), nullable=False, unique=True, index=True, comment="标签别名，用于URL")
    description = Column(String(255), nullable=True, comment="标签描述")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    blogs = relationship("Blog", secondary=blog_tag, back_populates="tags")
    translations = relationship("BlogTagTranslation", back_populates="tag", cascade="all, delete-orphan")


class BlogTagTranslation(Base):
    """博客标签多语言翻译表"""
    __tablename__ = "blog_tag_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("blog_tags.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    name = Column(String(50), nullable=False, comment="标签名称")
    description = Column(String(255), nullable=True, comment="标签描述")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    tag = relationship("BlogTag", back_populates="translations")

    # 联合索引确保每个标签对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
