# -*- coding: utf-8 -*-
"""
商品翻译管理的Pydantic模型
包含商品多语言翻译的创建、更新、查询等数据模型
"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class ProductTranslationBase(BaseModel):
    """商品翻译基础模型"""
    language_code: str = Field(..., max_length=10, description="语言代码，如en-US, zh-CN")
    name: str = Field(..., max_length=255, description="商品名称")
    short_description: Optional[str] = Field(None, description="商品简短描述")
    description: Optional[str] = Field(None, description="商品详细描述")
    specifications: Optional[str] = Field(None, description="商品规格")
    benefits: Optional[str] = Field(None, description="商品好处/特点")
    instructions: Optional[str] = Field(None, description="使用说明")
    seo_title: Optional[str] = Field(None, max_length=255, description="SEO标题")
    seo_description: Optional[str] = Field(None, max_length=500, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, max_length=255, description="SEO关键词")

    @validator('language_code')
    def validate_language_code(cls, v):
        # 验证语言代码格式
        if not v or len(v) < 2:
            raise ValueError('语言代码格式不正确')
        return v.lower()

    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('商品名称不能为空')
        return v.strip()


class ProductTranslationCreate(ProductTranslationBase):
    """创建商品翻译模型"""
    pass


class ProductTranslationUpdate(BaseModel):
    """更新商品翻译模型"""
    language_code: Optional[str] = Field(None, max_length=10, description="语言代码")
    name: Optional[str] = Field(None, max_length=255, description="商品名称")
    short_description: Optional[str] = Field(None, description="商品简短描述")
    description: Optional[str] = Field(None, description="商品详细描述")
    specifications: Optional[str] = Field(None, description="商品规格")
    benefits: Optional[str] = Field(None, description="商品好处/特点")
    instructions: Optional[str] = Field(None, description="使用说明")
    seo_title: Optional[str] = Field(None, max_length=255, description="SEO标题")
    seo_description: Optional[str] = Field(None, max_length=500, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, max_length=255, description="SEO关键词")

    @validator('name')
    def validate_name(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('商品名称不能为空')
        return v.strip() if v else v


class ProductTranslationResponse(ProductTranslationBase):
    """商品翻译响应模型"""
    id: UUID
    product_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductTranslationListResponse(BaseModel):
    """商品翻译列表响应模型"""
    items: List[ProductTranslationResponse]
    total: int
    page: int
    size: int
    pages: int


class ProductTranslationBatchCreate(BaseModel):
    """批量创建商品翻译模型"""
    translations: List[ProductTranslationCreate] = Field(..., description="翻译列表")


class ProductTranslationBatchUpdate(BaseModel):
    """批量更新商品翻译模型"""
    translations: List[dict] = Field(..., description="翻译更新列表，包含id和更新字段")


class LanguageTranslationInfo(BaseModel):
    """语言翻译信息模型"""
    language_code: str
    name: str
    short_description: Optional[str] = None
    description: Optional[str] = None
    has_seo: bool = False
    is_complete: bool = False


class ProductTranslationSummary(BaseModel):
    """商品翻译汇总模型"""
    product_id: UUID
    default_language: str
    languages: List[LanguageTranslationInfo]
    total_languages: int
    completion_rate: float


class TranslationContentUpdate(BaseModel):
    """翻译内容更新模型"""
    name: Optional[str] = Field(None, description="商品名称")
    short_description: Optional[str] = Field(None, description="商品简短描述")
    description: Optional[str] = Field(None, description="商品详细描述")
    specifications: Optional[str] = Field(None, description="商品规格")
    benefits: Optional[str] = Field(None, description="商品好处/特点")
    instructions: Optional[str] = Field(None, description="使用说明")


class TranslationSEOUpdate(BaseModel):
    """翻译SEO更新模型"""
    seo_title: Optional[str] = Field(None, max_length=255, description="SEO标题")
    seo_description: Optional[str] = Field(None, max_length=500, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, max_length=255, description="SEO关键词") 