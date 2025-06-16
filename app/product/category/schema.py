from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator

from app.product.models import CategoryLevel


class ProductCategoryTranslationBase(BaseModel):
    """商品分类翻译基础模型"""
    language_code: str = Field(..., description="语言代码，如en-US, zh-CN")
    name: str = Field(..., min_length=1, max_length=100, description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    seo_title: Optional[str] = Field(None, max_length=255, description="SEO标题")
    seo_description: Optional[str] = Field(None, max_length=500, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, max_length=255, description="SEO关键词")


class ProductCategoryTranslationCreate(ProductCategoryTranslationBase):
    pass


class ProductCategoryTranslationUpdate(ProductCategoryTranslationBase):
    language_code: Optional[str] = None
    name: Optional[str] = None


class ProductCategoryTranslation(ProductCategoryTranslationBase):
    """商品分类翻译响应模型"""
    id: UUID
    category_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCategoryBase(BaseModel):
    """商品分类基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="分类名称(默认语言)")
    slug: str = Field(..., min_length=1, max_length=100, description="分类别名，用于URL")
    description: Optional[str] = Field(None, description="分类描述(默认语言)")
    parent_id: Optional[UUID] = Field(None, description="父分类ID")
    level: CategoryLevel = Field(default=CategoryLevel.LEVEL_1, description="分类层级")
    image_url: Optional[str] = Field(None, max_length=255, description="分类图片URL")
    icon_url: Optional[str] = Field(None, max_length=255, description="分类图标URL")
    is_active: bool = Field(default=True, description="是否激活")
    is_featured: bool = Field(default=False, description="是否推荐分类")
    sort_order: int = Field(default=0, description="排序顺序")
    seo_title: Optional[str] = Field(None, max_length=255, description="SEO标题")
    seo_description: Optional[str] = Field(None, max_length=500, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, max_length=255, description="SEO关键词")


class ProductCategoryCreate(ProductCategoryBase):
    """商品分类创建模型"""
    translations: Optional[List[ProductCategoryTranslationCreate]] = Field(default_factory=list)


class ProductCategoryUpdate(BaseModel):
    """商品分类更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    level: Optional[CategoryLevel] = None
    image_url: Optional[str] = None
    icon_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    translations: Optional[List[ProductCategoryTranslationUpdate]] = None


class ProductCategory(ProductCategoryBase):
    """商品分类响应模型"""
    id: UUID
    parent_id: Optional[UUID] = None
    children: Optional[List["ProductCategory"]] = None
    translations: List[ProductCategoryTranslation] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 用于嵌套子类别的循环引用
ProductCategory.update_forward_refs()


class ProductCategoryListItem(BaseModel):
    """商品分类列表项"""
    id: UUID
    name: str
    slug: str
    level: CategoryLevel
    parent_id: Optional[UUID] = None
    image_url: Optional[str] = None
    icon_url: Optional[str] = None
    is_active: bool
    is_featured: bool
    sort_order: int
    products_count: Optional[int] = 0
    children_count: Optional[int] = 0

    class Config:
        from_attributes = True


class ProductCategoryTree(ProductCategoryListItem):
    """带子类别的商品分类树结构"""
    children: Optional[List["ProductCategoryTree"]] = None

    class Config:
        from_attributes = True


# 更新前向引用，解决递归引用问题
ProductCategoryTree.update_forward_refs()


class ProductCategoryList(BaseModel):
    """商品分类列表响应"""
    items: List[ProductCategoryListItem]
    total: int
    page: int
    size: int
    pages: int


class ProductCategoryTreeList(BaseModel):
    """商品分类树响应"""
    items: List[ProductCategoryTree]
    total: int
