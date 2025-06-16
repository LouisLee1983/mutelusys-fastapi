# -*- coding: utf-8 -*-
"""
商品价格管理的Pydantic模型
包含商品多币种价格的创建、更新、查询等数据模型
"""
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, validator


class ProductPriceBase(BaseModel):
    """商品价格基础模型"""
    currency_code: str = Field(..., max_length=3, description="货币代码，如USD, SGD, MYR")
    regular_price: float = Field(..., gt=0, description="原始价格")
    sale_price: Optional[float] = Field(None, ge=0, description="销售价格")
    discount_percentage: Optional[float] = Field(None, ge=0, le=100, description="折扣百分比")
    special_price: Optional[float] = Field(None, ge=0, description="特价")
    special_price_start_date: Optional[date] = Field(None, description="特价开始日期")
    special_price_end_date: Optional[date] = Field(None, description="特价结束日期")
    min_quantity: int = Field(default=1, ge=1, description="最小购买数量")
    is_default: bool = Field(default=False, description="是否为默认币种价格")

    @validator('sale_price')
    def validate_sale_price(cls, v, values):
        if v is not None and 'regular_price' in values and v > values['regular_price']:
            raise ValueError('销售价格不能高于原始价格')
        return v

    @validator('special_price')
    def validate_special_price(cls, v, values):
        if v is not None and 'regular_price' in values and v > values['regular_price']:
            raise ValueError('特价不能高于原始价格')
        return v

    @validator('special_price_end_date')
    def validate_special_price_dates(cls, v, values):
        if v is not None and 'special_price_start_date' in values and values['special_price_start_date'] is not None:
            if v <= values['special_price_start_date']:
                raise ValueError('特价结束日期必须晚于开始日期')
        return v


class ProductPriceCreate(ProductPriceBase):
    """创建商品价格模型"""
    pass


class ProductPriceUpdate(BaseModel):
    """更新商品价格模型"""
    currency_code: Optional[str] = Field(None, max_length=3, description="货币代码")
    regular_price: Optional[float] = Field(None, gt=0, description="原始价格")
    sale_price: Optional[float] = Field(None, ge=0, description="销售价格")
    discount_percentage: Optional[float] = Field(None, ge=0, le=100, description="折扣百分比")
    special_price: Optional[float] = Field(None, ge=0, description="特价")
    special_price_start_date: Optional[date] = Field(None, description="特价开始日期")
    special_price_end_date: Optional[date] = Field(None, description="特价结束日期")
    min_quantity: Optional[int] = Field(None, ge=1, description="最小购买数量")
    is_default: Optional[bool] = Field(None, description="是否为默认币种价格")


class ProductPriceResponse(ProductPriceBase):
    """商品价格响应模型"""
    id: UUID
    product_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductPriceListResponse(BaseModel):
    """商品价格列表响应模型"""
    items: List[ProductPriceResponse]
    total: int
    page: int
    size: int
    pages: int


class ProductPriceBatchCreate(BaseModel):
    """批量创建商品价格模型"""
    prices: List[ProductPriceCreate] = Field(..., description="价格列表")


class ProductPriceBatchUpdate(BaseModel):
    """批量更新商品价格模型"""
    prices: List[dict] = Field(..., description="价格更新列表，包含id和更新字段")


class CurrencyPriceInfo(BaseModel):
    """币种价格信息模型"""
    currency_code: str
    regular_price: float
    sale_price: Optional[float] = None
    special_price: Optional[float] = None
    is_special_active: bool = False
    discount_percentage: Optional[float] = None
    min_quantity: int = 1
    is_default: bool = False


class ProductPriceSummary(BaseModel):
    """商品价格汇总模型"""
    product_id: UUID
    default_currency: str
    default_price: float
    currencies: List[CurrencyPriceInfo]
    total_currencies: int
