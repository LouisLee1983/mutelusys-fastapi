# -*- coding: utf-8 -*-
"""
商品核心数据结构定义
包含商品基础信息的Schema定义
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.product.models import ProductStatus


class ProductBase(BaseModel):
    """商品基础信息Schema"""
    sku_code: str = Field(..., description="商品编码，唯一")
    status: ProductStatus = Field(default=ProductStatus.DRAFT, description="商品状态")
    weight: Optional[float] = Field(None, description="商品重量(克)")
    width: Optional[float] = Field(None, description="商品宽度(厘米)")
    height: Optional[float] = Field(None, description="商品高度(厘米)")
    length: Optional[float] = Field(None, description="商品长度(厘米)")
    is_featured: bool = Field(default=False, description="是否推荐商品")
    is_new: bool = Field(default=True, description="是否新品")
    is_bestseller: bool = Field(default=False, description="是否畅销品")
    is_customizable: bool = Field(default=False, description="是否支持定制")
    tax_class: Optional[str] = Field(None, description="税务类别")
    sort_order: int = Field(default=0, description="排序顺序")
    main_image_url: Optional[str] = Field(None, description="商品主图URL，用于列表展示和快速访问")
    seo_title: Optional[str] = Field(None, description="SEO标题")
    seo_description: Optional[str] = Field(None, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, description="SEO关键词")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="元数据")


class ProductCreate(ProductBase):
    """创建商品请求Schema"""
    name: str = Field(..., description="商品名称")
    description: Optional[str] = Field(None, description="商品描述")
    
    @validator('sku_code')
    def validate_sku_code(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('SKU编码至少需要3个字符')
        return v.strip().upper()


class ProductUpdate(BaseModel):
    """更新商品请求Schema"""
    sku_code: Optional[str] = Field(None, description="商品编码")
    name: Optional[str] = Field(None, description="商品名称")
    description: Optional[str] = Field(None, description="商品描述")
    status: Optional[ProductStatus] = Field(None, description="商品状态")
    weight: Optional[float] = Field(None, description="商品重量(克)")
    width: Optional[float] = Field(None, description="商品宽度(厘米)")
    height: Optional[float] = Field(None, description="商品高度(厘米)")
    length: Optional[float] = Field(None, description="商品长度(厘米)")
    is_featured: Optional[bool] = Field(None, description="是否推荐商品")
    is_new: Optional[bool] = Field(None, description="是否新品")
    is_bestseller: Optional[bool] = Field(None, description="是否畅销品")
    is_customizable: Optional[bool] = Field(None, description="是否支持定制")
    tax_class: Optional[str] = Field(None, description="税务类别")
    sort_order: Optional[int] = Field(None, description="排序顺序")
    main_image_url: Optional[str] = Field(None, description="商品主图URL，用于列表展示和快速访问")
    seo_title: Optional[str] = Field(None, description="SEO标题")
    seo_description: Optional[str] = Field(None, description="SEO描述")
    seo_keywords: Optional[str] = Field(None, description="SEO关键词")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="元数据")
    
    @validator('sku_code')
    def validate_sku_code(cls, v):
        if v is not None and (not v or len(v.strip()) < 3):
            raise ValueError('SKU编码至少需要3个字符')
        return v.strip().upper() if v else v


class ProductResponse(ProductBase):
    """商品响应Schema"""
    id: UUID = Field(..., description="商品ID")
    name: Optional[str] = Field(None, description="商品名称（从翻译表获取）")
    description: Optional[str] = Field(None, description="商品描述（从翻译表获取）")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """商品列表响应Schema"""
    items: List[ProductResponse] = Field(..., description="商品列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")


class ProductQueryParams(BaseModel):
    """商品查询参数Schema"""
    skip: int = Field(default=0, ge=0, description="跳过记录数")
    limit: int = Field(default=20, ge=1, le=100, description="返回记录数")
    search: Optional[str] = Field(None, description="搜索关键词")
    status: Optional[ProductStatus] = Field(None, description="商品状态筛选")
    is_featured: Optional[bool] = Field(None, description="是否推荐商品筛选")
    is_new: Optional[bool] = Field(None, description="是否新品筛选")
    is_bestseller: Optional[bool] = Field(None, description="是否畅销品筛选")
    sort_by: str = Field(default="updated_at", description="排序字段")
    sort_desc: bool = Field(default=True, description="是否降序排序") 