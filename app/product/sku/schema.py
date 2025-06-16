from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator

from app.product.models import ProductStatus


class ProductAttributeValueBase(BaseModel):
    """产品属性值基础模型"""
    attribute_id: UUID = Field(..., description="属性ID")
    value: str = Field(..., min_length=1, max_length=255, description="属性值")
    display_name: Optional[str] = Field(None, max_length=255, description="显示名称")
    sort_order: int = Field(default=0, description="排序顺序")


class ProductAttributeValueCreate(ProductAttributeValueBase):
    pass


class ProductAttributeValueUpdate(ProductAttributeValueBase):
    attribute_id: Optional[UUID] = None
    value: Optional[str] = None


class ProductAttributeValue(ProductAttributeValueBase):
    """产品属性值响应模型"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    attribute_name: Optional[str] = None  # 在响应中包含属性名

    class Config:
        from_attributes = True


class ProductSkuBase(BaseModel):
    """SKU基础模型"""
    product_id: UUID = Field(..., description="产品ID")
    sku_code: str = Field(..., min_length=1, max_length=50, description="SKU编码，唯一")
    barcode: Optional[str] = Field(None, max_length=50, description="条形码")
    price_adjustment: Optional[float] = Field(None, description="价格调整，相对于产品基本价格的增减金额")
    price_adjustment_percentage: Optional[float] = Field(None, description="价格调整百分比，相对于产品基本价格的增减百分比")
    weight_adjustment: Optional[float] = Field(None, description="重量调整(克)")
    width_adjustment: Optional[float] = Field(None, description="宽度调整(厘米)")
    height_adjustment: Optional[float] = Field(None, description="高度调整(厘米)")
    length_adjustment: Optional[float] = Field(None, description="长度调整(厘米)")
    is_active: bool = Field(default=True, description="是否激活")
    is_default: bool = Field(default=False, description="是否默认SKU")
    sort_order: int = Field(default=0, description="排序顺序")
    image_url: Optional[str] = Field(None, description="SKU图片URL")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="元数据，存储其他扩展信息")


class ProductSkuCreate(ProductSkuBase):
    """SKU创建模型"""
    attribute_values: List[ProductAttributeValueCreate] = Field(default_factory=list, description="属性值列表")
    quantity: Optional[int] = Field(None, ge=0, description="库存数量")
    low_stock_threshold: Optional[int] = Field(None, ge=0, description="低库存阈值")


class ProductSkuUpdate(BaseModel):
    """SKU更新模型"""
    sku_code: Optional[str] = Field(None, min_length=1, max_length=50)
    barcode: Optional[str] = None
    price_adjustment: Optional[float] = None
    price_adjustment_percentage: Optional[float] = None
    weight_adjustment: Optional[float] = None
    width_adjustment: Optional[float] = None
    height_adjustment: Optional[float] = None
    length_adjustment: Optional[float] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    sort_order: Optional[int] = None
    image_url: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    attribute_values: Optional[List[ProductAttributeValueUpdate]] = None


class ProductSku(ProductSkuBase):
    """SKU响应模型"""
    id: UUID
    attribute_values: List[ProductAttributeValue] = Field(default_factory=list)
    inventory: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductSkuListItem(BaseModel):
    """SKU列表项"""
    id: UUID
    product_id: UUID
    sku_code: str
    status: ProductStatus
    barcode: Optional[str] = None
    price_adjustment: Optional[float] = None
    price_adjustment_percentage: Optional[float] = None
    image_url: Optional[str] = None
    is_default: bool
    sort_order: int
    attribute_summary: Optional[str] = None  # 属性摘要，如"颜色: 红色, 尺寸: XL"
    stock_quantity: Optional[int] = None  # 库存数量
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductSkuList(BaseModel):
    """SKU列表响应"""
    items: List[ProductSkuListItem]
    total: int
    page: int
    size: int
    pages: int


class ProductSkuBulkStatusUpdate(BaseModel):
    """批量更新SKU状态"""
    sku_ids: List[UUID] = Field(..., min_items=1, description="SKU ID列表")
    status: ProductStatus = Field(..., description="新状态")


class ProductSkuInventoryUpdate(BaseModel):
    """更新SKU库存"""
    quantity: int = Field(..., ge=0, description="库存数量")
    low_stock_threshold: Optional[int] = Field(None, ge=0, description="低库存阈值")
