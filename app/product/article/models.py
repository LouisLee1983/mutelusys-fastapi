"""
产品文章管理模型
用于管理可共享的产品介绍文章，支持多语种翻译和多产品关联
"""

import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ArticleStatus(str, enum.Enum):
    """文章状态枚举"""
    DRAFT = "draft"        # 草稿
    PUBLISHED = "published"  # 已发布
    ARCHIVED = "archived"  # 已归档


class ArticleType(str, enum.Enum):
    """文章类型枚举"""
    PRODUCT_INTRO = "product_intro"      # 产品介绍
    MATERIAL_GUIDE = "material_guide"    # 材质指南
    USAGE_GUIDE = "usage_guide"          # 使用指南
    CULTURAL_STORY = "cultural_story"    # 文化故事
    CARE_INSTRUCTION = "care_instruction" # 保养说明


# 产品与文章的多对多关联表
product_article_association = Table(
    'product_article_associations',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('article_id', UUID(as_uuid=True), ForeignKey('product_articles.id', ondelete="CASCADE"), primary_key=True),
    Column('is_default', Boolean, default=False, comment="是否为该产品的默认文章"),
    Column('sort_order', Integer, default=0, comment="在该产品下的显示顺序"),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False)
)


class ProductArticle(Base):
    """产品文章表 - 可被多个产品共享的介绍文章"""
    __tablename__ = "product_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="文章标题")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="文章别名，用于URL")
    article_type = Column(Enum(ArticleType), nullable=False, default=ArticleType.PRODUCT_INTRO, comment="文章类型")
    status = Column(Enum(ArticleStatus), nullable=False, default=ArticleStatus.DRAFT, comment="文章状态")
    
    # 内容字段
    summary = Column(Text, nullable=True, comment="文章摘要")
    content = Column(Text, nullable=True, comment="文章正文内容")
    featured_image_url = Column(String(512), nullable=True, comment="文章特色图片URL")
    
    # 分类和标签
    category = Column(String(100), nullable=True, comment="文章分类")
    tags = Column(String(500), nullable=True, comment="文章标签，逗号分隔")
    
    # SEO字段
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    
    # 管理字段
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="作者ID")
    is_featured = Column(Boolean, default=False, comment="是否推荐文章")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    view_count = Column(Integer, default=0, comment="浏览次数")
    
    # 自动分配规则
    auto_assign_materials = Column(String(500), nullable=True, comment="自动分配给包含这些材质的产品，逗号分隔材质名称")
    auto_assign_categories = Column(String(500), nullable=True, comment="自动分配给这些分类的产品，逗号分隔分类名称")
    auto_assign_tags = Column(String(500), nullable=True, comment="自动分配给包含这些标签的产品，逗号分隔标签名称")
    
    # 时间字段
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("ProductArticleTranslation", back_populates="article", cascade="all, delete-orphan")
    # products = relationship("Product", secondary=product_article_association, back_populates="articles")  # 暂时注释，避免循环依赖


class ProductArticleTranslation(Base):
    """产品文章多语言翻译表"""
    __tablename__ = "product_article_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("product_articles.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN, th-TH")
    
    # 翻译内容
    title = Column(String(255), nullable=False, comment="文章标题翻译")
    summary = Column(Text, nullable=True, comment="文章摘要翻译")
    content = Column(Text, nullable=True, comment="文章正文内容翻译")
    
    # SEO翻译
    seo_title = Column(String(255), nullable=True, comment="SEO标题翻译")
    seo_description = Column(String(500), nullable=True, comment="SEO描述翻译")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词翻译")
    
    # 分类标签翻译
    category = Column(String(100), nullable=True, comment="文章分类翻译")
    tags = Column(String(500), nullable=True, comment="文章标签翻译，逗号分隔")
    
    # 管理字段
    is_auto_translated = Column(Boolean, default=False, comment="是否为自动翻译")
    translator_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="翻译者ID")
    
    # 时间字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    article = relationship("ProductArticle", back_populates="translations")

    # 唯一约束：一个文章在同一语言下只能有一个翻译
    __table_args__ = (
        {'comment': '产品文章翻译表'},
    )


class ProductArticleTemplate(Base):
    """产品文章模板表 - 用于快速创建标准化的产品文章"""
    __tablename__ = "product_article_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, comment="模板名称")
    description = Column(Text, nullable=True, comment="模板描述")
    article_type = Column(Enum(ArticleType), nullable=False, comment="适用的文章类型")
    
    # 模板内容
    title_template = Column(String(255), nullable=True, comment="标题模板，支持变量如{product_name}")
    summary_template = Column(Text, nullable=True, comment="摘要模板")
    content_template = Column(Text, nullable=True, comment="正文模板")
    
    # 自动填充规则
    auto_fill_rules = Column(Text, nullable=True, comment="自动填充规则的JSON配置")
    
    # 管理字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)