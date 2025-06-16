from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
import re

from app.customer.models import AddressType


class AddressBase(BaseModel):
    """地址基础模型"""
    address_type: AddressType = Field(default=AddressType.SHIPPING)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    company_name: Optional[str] = Field(None, max_length=100)
    phone_number: str = Field(..., max_length=20, pattern=r'^\+?[0-9\s\-\(\)]{8,20}$')
    email: Optional[EmailStr] = None
    address_line1: str = Field(..., min_length=3, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country_code: str = Field(..., min_length=2, max_length=2, pattern=r'^[A-Z]{2}$')
    delivery_notes: Optional[str] = None
    is_default: bool = Field(default=False)

    @validator('country_code')
    def country_code_uppercase(cls, v):
        """确保国家代码为大写"""
        return v.upper()


class AddressCreate(AddressBase):
    """地址创建模型 - 管理员使用"""
    customer_id: UUID


class AddressUserCreate(AddressBase):
    """地址创建模型 - C端用户使用（无需customer_id）"""
    customer_id: Optional[UUID] = None  # 会在API中自动设置


class AddressUpdate(BaseModel):
    """地址更新模型"""
    address_type: Optional[AddressType] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    company_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20, pattern=r'^\+?[0-9\s\-\(\)]{8,20}$')
    email: Optional[EmailStr] = None
    address_line1: Optional[str] = Field(None, min_length=3, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country_code: Optional[str] = Field(None, min_length=2, max_length=2, pattern=r'^[A-Z]{2}$')
    delivery_notes: Optional[str] = None
    is_default: Optional[bool] = None

    @validator('country_code')
    def country_code_uppercase(cls, v):
        """确保国家代码为大写"""
        if v:
            return v.upper()
        return v


class AddressResponse(AddressBase):
    """地址响应模型"""
    id: UUID
    customer_id: UUID
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    # 用于计算的字段
    full_name: Optional[str] = None
    full_address: Optional[str] = None
    
    class Config:
        from_attributes = True
        
    @classmethod
    def model_validate(cls, obj, **kwargs):
        """从ORM对象创建响应模型"""
        # 添加计算字段
        if hasattr(obj, 'first_name') and hasattr(obj, 'last_name'):
            obj.full_name = f"{obj.first_name} {obj.last_name}"
            obj.full_address = cls._format_full_address(obj)
        return super().model_validate(obj, **kwargs)
    
    @staticmethod
    def _format_full_address(address) -> str:
        """格式化完整地址"""
        # 使用数据库字段名（不是别名）
        components = [
            getattr(address, 'address_line1', None),
            getattr(address, 'address_line2', None),
            getattr(address, 'city', None),
            getattr(address, 'state_province', None),
            getattr(address, 'postal_code', None),
            getattr(address, 'country_code', None)
        ]
        
        # 过滤掉None值
        components = [c for c in components if c]
        
        return ", ".join(components)


class AddressList(BaseModel):
    """地址列表响应"""
    items: List[AddressResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        from_attributes = True


class SetDefaultAddressRequest(BaseModel):
    """设置默认地址请求"""
    address_id: UUID = Field(..., description="要设置为默认的地址ID")
    address_type: Optional[AddressType] = Field(None, description="要设为默认的地址类型，不指定则为所有类型")
