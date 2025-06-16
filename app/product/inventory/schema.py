from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from app.product.models import ProductStatus


class ProductInventoryBase(BaseModel):
    """产品库存基础模型"""
    product_id: UUID = Field(..., description="产品ID")
    sku_id: Optional[UUID] = Field(None, description="SKU ID")
    warehouse_id: Optional[UUID] = Field(None, description="仓库ID")
    quantity: int = Field(default=0, ge=0, description="可用库存数量")
    reserved_quantity: int = Field(default=0, ge=0, description="已预留数量（已下单未发货）")
    alert_threshold: Optional[int] = Field(None, description="库存预警阈值")
    ideal_quantity: Optional[int] = Field(None, description="理想库存量")
    reorder_point: Optional[int] = Field(None, description="重新订货点")
    reorder_quantity: Optional[int] = Field(None, description="重新订货数量")
    is_in_stock: bool = Field(default=True, description="是否有库存")
    is_managed: bool = Field(default=True, description="是否进行库存管理")
    location: Optional[str] = Field(None, description="库存位置编码")
    notes: Optional[str] = Field(None, description="备注信息")


class ProductInventoryCreate(ProductInventoryBase):
    """库存创建模型"""
    pass


class ProductInventoryUpdate(BaseModel):
    """库存更新模型"""
    warehouse_id: Optional[UUID] = None
    quantity: Optional[int] = Field(None, ge=0)
    reserved_quantity: Optional[int] = Field(None, ge=0)
    alert_threshold: Optional[int] = Field(None, ge=0)
    ideal_quantity: Optional[int] = Field(None, ge=0)
    reorder_point: Optional[int] = Field(None, ge=0)
    reorder_quantity: Optional[int] = Field(None, ge=0)
    is_in_stock: Optional[bool] = None
    is_managed: Optional[bool] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class ProductInventory(ProductInventoryBase):
    """库存响应模型"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    status: str = Field(None, description="库存状态，如正常、低库存、缺货等")

    class Config:
        from_attributes = True


class ProductInventoryAdjustment(BaseModel):
    """库存调整模型"""
    sku_id: UUID = Field(..., description="SKU ID")
    quantity: int = Field(..., description="调整数量，正数为增加，负数为减少")
    reason: str = Field("手动调整", description="调整原因")
    notes: Optional[str] = Field(None, description="备注")
    reference_id: Optional[UUID] = Field(None, description="关联ID，如订单ID")
    reference_type: Optional[str] = Field(None, description="关联类型，如order, return等")


class ProductInventoryAdjustmentResult(BaseModel):
    """库存调整结果"""
    success: bool
    message: str
    sku_id: UUID
    sku_code: str
    product_id: UUID
    previous_quantity: int
    current_quantity: int
    adjustment: int
    is_low_stock: bool
    is_out_of_stock: bool


class ProductInventoryList(BaseModel):
    """库存列表响应"""
    items: List[Dict[str, Any]]
    total: int
    page: int
    size: int
    pages: int


class ProductInventoryStatistics(BaseModel):
    """库存统计信息"""
    total_products: int
    total_skus: int
    total_quantity: int
    low_stock_count: int  # 低库存商品数
    out_of_stock_count: int  # 缺货商品数
    inventory_value: float  # 库存价值
    categories: List[Dict[str, Any]]  # 按分类统计


class ProductInventoryReservation(BaseModel):
    """库存预留模型"""
    sku_id: UUID = Field(..., description="SKU ID")
    quantity: int = Field(..., gt=0, description="预留数量")
    order_id: Optional[UUID] = Field(None, description="订单ID")
    expiry_time: Optional[datetime] = Field(None, description="预留过期时间")
    notes: Optional[str] = Field(None, description="备注")


class ProductInventoryReservationResult(BaseModel):
    """库存预留结果"""
    success: bool
    message: str
    reservation_id: Optional[UUID] = None
    sku_id: UUID
    quantity: int
    available_after_reservation: int


class ProductInventoryWarehouse(BaseModel):
    """仓库信息模型"""
    id: UUID
    name: str
    address: str
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryMovement(BaseModel):
    """库存转移模型"""
    sku_id: UUID = Field(..., description="SKU ID")
    quantity: int = Field(..., gt=0, description="转移数量")
    source_warehouse_id: UUID = Field(..., description="源仓库ID")
    destination_warehouse_id: UUID = Field(..., description="目标仓库ID")
    reason: str = Field("库存转移", description="转移原因")
    notes: Optional[str] = Field(None, description="备注")
