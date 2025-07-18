# -*- coding: utf-8 -*-
"""
运费地区Schema定义
包含地区运费配置和翻译的Pydantic模型
"""
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator
from datetime import datetime


# ==================== 运费地区翻译 ====================

class ShippingZoneTranslationBase(BaseModel):
    """运费地区翻译基础Schema"""
    language_code: str = Field(..., max_length=10, description="语言代码")
    name: str = Field(..., max_length=100, description="地区名称翻译")
    description: Optional[str] = Field(None, description="地区描述翻译")


class ShippingZoneTranslationCreate(ShippingZoneTranslationBase):
    """创建运费地区翻译Schema"""
    pass


class ShippingZoneTranslationUpdate(BaseModel):
    """更新运费地区翻译Schema"""
    name: Optional[str] = Field(None, max_length=100, description="地区名称翻译")
    description: Optional[str] = Field(None, description="地区描述翻译")


class ShippingZoneTranslationResponse(ShippingZoneTranslationBase):
    """运费地区翻译响应Schema"""
    id: UUID
    shipping_zone_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 运费地区 ====================

class ShippingZoneBase(BaseModel):
    """运费地区基础Schema"""
    code: str = Field(..., max_length=20, description="地区代码")
    name: str = Field(..., max_length=100, description="地区名称")
    description: Optional[str] = Field(None, description="地区描述")
    countries: str = Field(..., description="包含的国家代码列表，逗号分隔")
    is_active: bool = Field(True, description="是否启用")
    sort_order: int = Field(0, description="排序")

    @validator('countries')
    def validate_countries(cls, v):
        """验证国家代码格式"""
        if not v or not v.strip():
            raise ValueError("国家代码列表不能为空")
        
        # 检查国家代码格式（2-3位字母）
        country_codes = [code.strip().upper() for code in v.split(',')]
        for code in country_codes:
            if not code.isalpha() or len(code) < 2 or len(code) > 3:
                raise ValueError(f"无效的国家代码: {code}")
        
        return ','.join(country_codes)


class ShippingZoneCreate(ShippingZoneBase):
    """创建运费地区Schema"""
    translations: Optional[List[ShippingZoneTranslationCreate]] = Field(None, description="翻译列表")


class ShippingZoneUpdate(BaseModel):
    """更新运费地区Schema"""
    code: Optional[str] = Field(None, max_length=20, description="地区代码")
    name: Optional[str] = Field(None, max_length=100, description="地区名称")
    description: Optional[str] = Field(None, description="地区描述")
    countries: Optional[str] = Field(None, description="包含的国家代码列表，逗号分隔")
    is_active: Optional[bool] = Field(None, description="是否启用")
    sort_order: Optional[int] = Field(None, description="排序")

    @validator('countries')
    def validate_countries(cls, v):
        """验证国家代码格式"""
        if v is None:
            return v
            
        if not v.strip():
            raise ValueError("国家代码列表不能为空")
        
        # 检查国家代码格式（2-3位字母）
        country_codes = [code.strip().upper() for code in v.split(',')]
        for code in country_codes:
            if not code.isalpha() or len(code) < 2 or len(code) > 3:
                raise ValueError(f"无效的国家代码: {code}")
        
        return ','.join(country_codes)


class ShippingZoneResponse(ShippingZoneBase):
    """运费地区响应Schema"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    translations: List[ShippingZoneTranslationResponse] = Field(default_factory=list, description="翻译列表")

    class Config:
        from_attributes = True


class ShippingZoneListResponse(BaseModel):
    """运费地区列表响应Schema"""
    code: int = Field(200, description="响应代码")
    message: str = Field("获取成功", description="响应消息")
    data: List[ShippingZoneResponse] = Field(..., description="运费地区列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量") 