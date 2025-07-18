# -*- coding: utf-8 -*-
"""
运费规则Schema定义
包含运费规则的Pydantic模型
"""
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ShippingRateBase(BaseModel):
    """运费规则基础Schema"""
    shipping_method_id: UUID = Field(..., description="快递方式ID")
    shipping_zone_id: UUID = Field(..., description="运费地区ID")
    min_quantity: int = Field(1, ge=1, description="最小件数")
    max_quantity: Optional[int] = Field(None, ge=1, description="最大件数，null表示无上限")
    base_cost: Decimal = Field(0, ge=0, description="基础运费")
    per_item_cost: Decimal = Field(0, ge=0, description="每件额外费用")
    is_active: bool = Field(True, description="是否启用")
    sort_order: int = Field(0, description="排序")

    @validator('max_quantity')
    def validate_max_quantity(cls, v, values):
        """验证最大件数"""
        if v is not None and 'min_quantity' in values and v < values['min_quantity']:
            raise ValueError("最大件数不能小于最小件数")
        return v


class ShippingRateCreate(ShippingRateBase):
    """创建运费规则Schema"""
    pass


class ShippingRateUpdate(BaseModel):
    """更新运费规则Schema"""
    shipping_method_id: Optional[UUID] = Field(None, description="快递方式ID")
    shipping_zone_id: Optional[UUID] = Field(None, description="运费地区ID")
    min_quantity: Optional[int] = Field(None, ge=1, description="最小件数")
    max_quantity: Optional[int] = Field(None, ge=1, description="最大件数，null表示无上限")
    base_cost: Optional[Decimal] = Field(None, ge=0, description="基础运费")
    per_item_cost: Optional[Decimal] = Field(None, ge=0, description="每件额外费用")
    is_active: Optional[bool] = Field(None, description="是否启用")
    sort_order: Optional[int] = Field(None, description="排序")

    @validator('max_quantity')
    def validate_max_quantity(cls, v, values):
        """验证最大件数"""
        if v is not None and 'min_quantity' in values and values['min_quantity'] is not None and v < values['min_quantity']:
            raise ValueError("最大件数不能小于最小件数")
        return v


class ShippingRateResponse(ShippingRateBase):
    """运费规则响应Schema"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ShippingRateListResponse(BaseModel):
    """运费规则列表响应Schema"""
    code: int = Field(200, description="响应代码")
    message: str = Field("获取成功", description="响应消息")
    data: List[ShippingRateResponse] = Field(..., description="运费规则列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量") 