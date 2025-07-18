"""
产品文章管理相关的Pydantic Schema定义
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.product.article.models import ArticleStatus, ArticleType


# ==================== 基础Schema ====================

class ProductArticleBase(BaseModel):
    """产品文章基础Schema"""
    title: str = Field(..., max_length=255, description="文章标题")
    slug: str = Field(..., max_length=255, description="文章别名")
    article_type: ArticleType = Field(default=ArticleType.PRODUCT_INTRO, description="文章类型")
    summary: Optional[str] = Field(None, description="文章摘要")
    content: Optional[str] = Field(None, description="文章正文内容")
    featured_image_url: Optional[str] = Field(None, max_length=512, description="特色图片URL")
    category: Optional[str] = Field(None, max_length=100, description="文章分类")
    tags: Optional[str] = Field(None, max_length=500, description="文章标签")
    seo_title: Optional[str] = Field(None, max_length=255, description="SEO标题")
    seo_description: Optional[str] = Field(None, max_length=500, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, max_length=255, description="SEO关键词")


# ==================== 请求Schema ====================

class ProductArticleCreateRequest(ProductArticleBase):
    """创建产品文章请求"""
    auto_assign_materials: Optional[str] = Field(None, description="自动分配材质")
    auto_assign_categories: Optional[str] = Field(None, description="自动分配分类")
    auto_assign_tags: Optional[str] = Field(None, description="自动分配标签")
    
    @validator('slug')
    def validate_slug(cls, v):
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Slug只能包含字母、数字、连字符和下划线')
        return v


class ProductArticleUpdateRequest(BaseModel):
    """更新产品文章请求"""
    title: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    article_type: Optional[ArticleType] = None
    status: Optional[ArticleStatus] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    featured_image_url: Optional[str] = Field(None, max_length=512)
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = Field(None, max_length=500)
    seo_title: Optional[str] = Field(None, max_length=255)
    seo_description: Optional[str] = Field(None, max_length=500)
    seo_keywords: Optional[str] = Field(None, max_length=255)
    is_featured: Optional[bool] = None
    auto_assign_materials: Optional[str] = None
    auto_assign_categories: Optional[str] = None
    auto_assign_tags: Optional[str] = None


class ProductArticleTranslationCreateRequest(BaseModel):
    """创建文章翻译请求"""
    language_code: str = Field(..., max_length=10, description="语言代码")
    title: str = Field(..., max_length=255, description="标题翻译")
    summary: Optional[str] = Field(None, description="摘要翻译")
    content: Optional[str] = Field(None, description="内容翻译")
    seo_title: Optional[str] = Field(None, max_length=255)
    seo_description: Optional[str] = Field(None, max_length=500)
    seo_keywords: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = Field(None, max_length=500)


class ProductArticleTranslationUpdateRequest(BaseModel):
    """更新文章翻译请求"""
    title: Optional[str] = Field(None, max_length=255)
    summary: Optional[str] = None
    content: Optional[str] = None
    seo_title: Optional[str] = Field(None, max_length=255)
    seo_description: Optional[str] = Field(None, max_length=500)
    seo_keywords: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = Field(None, max_length=500)


class ProductArticleAssignRequest(BaseModel):
    """将文章分配给产品的请求"""
    product_ids: List[str] = Field(..., description="产品ID列表")
    is_default: bool = Field(default=False, description="是否设为默认文章")
    sort_order: int = Field(default=0, description="显示顺序")


# ==================== 响应Schema ====================

class ProductArticleTranslationResponse(BaseModel):
    """文章翻译响应"""
    id: str
    language_code: str
    title: str
    summary: Optional[str]
    content: Optional[str]
    seo_title: Optional[str]
    seo_description: Optional[str]
    seo_keywords: Optional[str]
    category: Optional[str]
    tags: Optional[str]
    is_auto_translated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductArticleResponse(BaseModel):
    """产品文章响应"""
    id: str
    title: str
    slug: str
    article_type: ArticleType
    status: ArticleStatus
    summary: Optional[str]
    content: Optional[str]
    featured_image_url: Optional[str]
    category: Optional[str]
    tags: Optional[str]
    seo_title: Optional[str]
    seo_description: Optional[str]
    seo_keywords: Optional[str]
    is_featured: bool
    sort_order: int
    view_count: int
    auto_assign_materials: Optional[str]
    auto_assign_categories: Optional[str]
    auto_assign_tags: Optional[str]
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    # 关联数据
    translations: List[ProductArticleTranslationResponse] = []
    product_count: int = Field(default=0, description="关联的产品数量")

    class Config:
        from_attributes = True


class ProductArticleListResponse(BaseModel):
    """文章列表响应"""
    id: str
    title: str
    slug: str
    article_type: ArticleType
    status: ArticleStatus
    category: Optional[str]
    is_featured: bool
    view_count: int
    product_count: int = Field(default=0, description="关联产品数量")
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductWithArticlesResponse(BaseModel):
    """带文章的产品响应"""
    id: str
    name: str
    sku_code: str
    status: str
    articles: List[ProductArticleResponse] = []

    class Config:
        from_attributes = True


# ==================== 分页响应 ====================

class PaginatedArticleResponse(BaseModel):
    """分页文章响应"""
    items: List[ProductArticleListResponse]
    total: int
    page: int
    limit: int
    pages: int


# ==================== 模板相关Schema ====================

class ProductArticleTemplateCreateRequest(BaseModel):
    """创建文章模板请求"""
    name: str = Field(..., max_length=255, description="模板名称")
    description: Optional[str] = Field(None, description="模板描述")
    article_type: ArticleType = Field(..., description="文章类型")
    title_template: Optional[str] = Field(None, max_length=255)
    summary_template: Optional[str] = None
    content_template: Optional[str] = None
    auto_fill_rules: Optional[str] = Field(None, description="自动填充规则JSON")


class ProductArticleTemplateResponse(BaseModel):
    """文章模板响应"""
    id: str
    name: str
    description: Optional[str]
    article_type: ArticleType
    title_template: Optional[str]
    summary_template: Optional[str]
    content_template: Optional[str]
    auto_fill_rules: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== 统计相关Schema ====================

class ArticleStatsResponse(BaseModel):
    """文章统计响应"""
    total_articles: int = Field(description="文章总数")
    published_articles: int = Field(description="已发布文章数")
    draft_articles: int = Field(description="草稿文章数")
    articles_by_type: Dict[str, int] = Field(description="按类型统计")
    most_used_articles: List[Dict[str, Any]] = Field(description="使用最多的文章")
    recent_articles: List[ProductArticleListResponse] = Field(description="最近创建的文章")