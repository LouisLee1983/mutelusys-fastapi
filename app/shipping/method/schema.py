# -*- coding: utf-8 -*-
"""
快递方式Schema定义
包含快递方式和翻译的Pydantic模型
"""
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from app.shipping.method.models import TransportType


# ==================== 快递方式翻译 ====================

class ShippingMethodTranslationBase(BaseModel):
    """快递方式翻译基础Schema"""
    language_code: str = Field(..., max_length=10, description="语言代码")
    name: str = Field(..., max_length=100, description="快递方式名称翻译")
    company_name: Optional[str] = Field(None, max_length=100, description="快递公司名称翻译")
    description: Optional[str] = Field(None, description="描述翻译")


class ShippingMethodTranslationCreate(ShippingMethodTranslationBase):
    """创建快递方式翻译Schema"""
    pass


class ShippingMethodTranslationUpdate(BaseModel):
    """更新快递方式翻译Schema"""
    name: Optional[str] = Field(None, max_length=100, description="快递方式名称翻译")
    company_name: Optional[str] = Field(None, max_length=100, description="快递公司名称翻译")
    description: Optional[str] = Field(None, description="描述翻译")


class ShippingMethodTranslationResponse(ShippingMethodTranslationBase):
    """快递方式翻译响应Schema"""
    id: UUID
    shipping_method_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 快递方式 ====================

class ShippingMethodBase(BaseModel):
    """快递方式基础Schema"""
    code: str = Field(..., max_length=20, description="快递方式代码")
    name: str = Field(..., max_length=100, description="快递方式名称")
    company_name: str = Field(..., max_length=100, description="快递公司名称")
    description: Optional[str] = Field(None, description="描述")
    transport_type: TransportType = Field(..., description="运输类型")
    min_delivery_days: Optional[int] = Field(None, ge=1, description="最小配送天数")
    max_delivery_days: Optional[int] = Field(None, ge=1, description="最大配送天数")
    is_active: bool = Field(True, description="是否启用")
    sort_order: int = Field(0, description="排序")


class ShippingMethodCreate(ShippingMethodBase):
    """创建快递方式Schema"""
    translations: Optional[List[ShippingMethodTranslationCreate]] = Field(None, description="翻译列表")


class ShippingMethodUpdate(BaseModel):
    """更新快递方式Schema"""
    code: Optional[str] = Field(None, max_length=20, description="快递方式代码")
    name: Optional[str] = Field(None, max_length=100, description="快递方式名称")
    company_name: Optional[str] = Field(None, max_length=100, description="快递公司名称")
    description: Optional[str] = Field(None, description="描述")
    transport_type: Optional[TransportType] = Field(None, description="运输类型")
    min_delivery_days: Optional[int] = Field(None, ge=1, description="最小配送天数")
    max_delivery_days: Optional[int] = Field(None, ge=1, description="最大配送天数")
    is_active: Optional[bool] = Field(None, description="是否启用")
    sort_order: Optional[int] = Field(None, description="排序")


class ShippingMethodResponse(ShippingMethodBase):
    """快递方式响应Schema"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    translations: List[ShippingMethodTranslationResponse] = Field(default_factory=list, description="翻译列表")

    class Config:
        from_attributes = True


class ShippingMethodListResponse(BaseModel):
    """快递方式列表响应Schema"""
    code: int = Field(200, description="响应代码")
    message: str = Field("获取成功", description="响应消息")
    data: List[ShippingMethodResponse] = Field(..., description="快递方式列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量") 