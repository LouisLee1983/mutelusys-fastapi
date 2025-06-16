from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator

from app.product.models import AttributeType


class ProductAttributeValueBase(BaseModel):
    """商品属性值基础模型"""
    value: str = Field(..., min_length=1, max_length=255, description="属性值")
    label: Optional[str] = Field(None, max_length=255, description="显示标签")
    color_code: Optional[str] = Field(None, max_length=30, description="颜色代码，当类型为颜色时使用")
    image_url: Optional[str] = Field(None, max_length=255, description="图片URL，如颜色样式图")
    sort_order: int = Field(default=0, description="排序顺序")


class ProductAttributeValueCreate(ProductAttributeValueBase):
    """商品属性值创建模型"""
    pass


class ProductAttributeValueUpdate(BaseModel):
    """商品属性值更新模型"""
    value: Optional[str] = Field(None, min_length=1, max_length=255)
    label: Optional[str] = Field(None, max_length=255)
    color_code: Optional[str] = Field(None, max_length=30)
    image_url: Optional[str] = Field(None, max_length=255)
    sort_order: Optional[int] = None


class ProductAttributeValue(ProductAttributeValueBase):
    """商品属性值响应模型"""
    id: UUID
    attribute_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductAttributeBase(BaseModel):
    """商品属性基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="属性名称")
    code: str = Field(..., min_length=1, max_length=50, description="属性代码，如color, size")
    description: Optional[str] = Field(None, description="属性描述")
    type: AttributeType = Field(default=AttributeType.SELECT, description="属性类型")
    display_order: int = Field(default=0, description="显示顺序")
    is_required: bool = Field(default=False, description="是否必填")
    is_configurable: bool = Field(default=True, description="是否用于配置SKU的属性")
    is_searchable: bool = Field(default=False, description="是否可搜索")
    is_comparable: bool = Field(default=False, description="是否可比较")
    is_filterable: bool = Field(default=True, description="是否可筛选")
    is_visible_on_frontend: bool = Field(default=True, description="是否在前端可见")
    configuration: Optional[Dict[str, Any]] = Field(None, description="属性配置信息，如验证规则")

    @validator('code')
    def validate_code(cls, v):
        """验证属性代码格式"""
        if not v.replace('_', '').isalnum():
            raise ValueError('属性代码只能包含字母、数字和下划线')
        return v.lower()


class ProductAttributeCreate(ProductAttributeBase):
    """商品属性创建模型"""
    values: Optional[List[ProductAttributeValueCreate]] = Field(default_factory=list, description="预定义属性值")


class ProductAttributeUpdate(BaseModel):
    """商品属性更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    type: Optional[AttributeType] = None
    display_order: Optional[int] = None
    is_required: Optional[bool] = None
    is_configurable: Optional[bool] = None
    is_searchable: Optional[bool] = None
    is_comparable: Optional[bool] = None
    is_filterable: Optional[bool] = None
    is_visible_on_frontend: Optional[bool] = None
    configuration: Optional[Dict[str, Any]] = None

    @validator('code')
    def validate_code(cls, v):
        """验证属性代码格式"""
        if v is not None and not v.replace('_', '').isalnum():
            raise ValueError('属性代码只能包含字母、数字和下划线')
        return v.lower() if v else v


class ProductAttribute(ProductAttributeBase):
    """商品属性响应模型"""
    id: UUID
    values: List[ProductAttributeValue] = Field(default_factory=list, description="属性值列表")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductAttributeListItem(BaseModel):
    """商品属性列表项"""
    id: UUID
    name: str
    code: str
    type: AttributeType
    display_order: int
    is_required: bool
    is_configurable: bool
    is_searchable: bool
    is_comparable: bool
    is_filterable: bool
    is_visible_on_frontend: bool
    values_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductAttributeList(BaseModel):
    """商品属性列表响应"""
    items: List[ProductAttributeListItem]
    total: int
    page: int
    size: int
    pages: int


class ProductAttributeValueList(BaseModel):
    """商品属性值列表响应"""
    items: List[ProductAttributeValue]
    total: int
    page: int
    size: int
    pages: int
