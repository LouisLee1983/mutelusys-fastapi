from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any, Dict
from uuid import UUID
from pydantic import BaseModel, Field, validator, EmailStr

from app.order.shipment.models import ShipmentStatus, TrackingStatus, PackageType


# 基础响应模型
class ResponseBase(BaseModel):
    code: int = 200
    message: str = "Success"
    data: Any = None


# 承运商模型
class CarrierBase(BaseModel):
    name: str
    code: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    tracking_url_template: Optional[str] = None


class CarrierCreate(CarrierBase):
    supported_countries: Optional[List[str]] = None
    service_types: Optional[List[str]] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    api_config: Optional[Dict[str, Any]] = None
    is_active: bool = True
    priority: int = 0


class CarrierResponse(CarrierBase):
    id: UUID
    is_active: bool
    priority: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 发货商品明细模型
class ShipmentItemCreate(BaseModel):
    order_item_id: UUID
    product_id: UUID
    sku_id: Optional[UUID] = None
    product_name: str
    sku_code: Optional[str] = None
    quantity_shipped: int
    unit_price: Decimal
    attributes: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    weight_per_unit: Optional[float] = None


class ShipmentItemResponse(BaseModel):
    id: UUID
    order_item_id: UUID
    product_id: UUID
    sku_id: Optional[UUID] = None
    product_name: str
    sku_code: Optional[str] = None
    quantity_shipped: int
    unit_price: Decimal
    attributes: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    weight_per_unit: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# 简化的物流跟踪记录模型（专注于货运位置信息）
class TrackingRecordCreate(BaseModel):
    tracking_status: TrackingStatus
    location: str = Field(..., description="当前货运位置，如：北京分拣中心、上海派送中心等")
    description: str = Field(..., description="状态描述，如：已发货、运输中、派送中等")
    timestamp: datetime
    operator_name: Optional[str] = None  # 操作员或快递员姓名
    is_auto_generated: bool = True


class TrackingRecordResponse(BaseModel):
    id: UUID
    tracking_status: TrackingStatus
    location: str
    description: str
    operator_name: Optional[str] = None
    timestamp: datetime
    is_auto_generated: bool
    created_at: datetime

    class Config:
        from_attributes = True


# 简化的物流追踪更新模型（用于API）
class TrackingUpdateCreate(BaseModel):
    tracking_status: TrackingStatus
    location: str = Field(..., description="当前货运位置")
    description: str = Field(..., description="状态描述")
    timestamp: Optional[datetime] = None  # 如果为空则使用当前时间
    operator_name: Optional[str] = None  # 操作员或快递员姓名


class TrackingUpdateResponse(BaseModel):
    id: UUID
    tracking_status: TrackingStatus
    location: str
    description: str
    operator_name: Optional[str] = None
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# 简化的发货记录创建模型（专注于快递公司和基本信息）
class ShipmentCreate(BaseModel):
    order_id: UUID
    
    # 快递公司信息（核心字段）
    carrier_name: str = Field(..., description="快递公司名称")
    tracking_number: Optional[str] = None
    shipping_method: str = Field(..., description="快递方式，如：标准快递、特快专递等")
    
    # 收货地址（基本信息）
    recipient_name: str
    recipient_phone: str
    recipient_email: Optional[str] = None
    shipping_address1: str
    shipping_city: str
    shipping_country: str
    shipping_postcode: str
    
    # 包裹基本信息
    weight: float = Field(..., gt=0, description="重量(kg)")
    shipping_cost: Decimal = Field(default=Decimal("0"), ge=0, description="运费")
    
    # 预计时间
    estimated_delivery_date: Optional[datetime] = None
    
    # 备注
    notes: Optional[str] = None
    
    # 发货商品（简化）
    items: List[ShipmentItemCreate]
    
    @validator('items')
    def check_items_not_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError('发货记录必须包含至少一个商品')
        return v


# 发货记录更新模型
class ShipmentUpdate(BaseModel):
    carrier_id: Optional[UUID] = None
    carrier_name: Optional[str] = None
    carrier_code: Optional[str] = None
    tracking_number: Optional[str] = None
    shipping_method: Optional[str] = None
    service_type: Optional[str] = None
    
    # 包裹信息
    weight: Optional[float] = Field(None, gt=0)
    length: Optional[float] = Field(None, gt=0)
    width: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    package_type: Optional[PackageType] = None
    
    # 费用信息
    shipping_cost: Optional[Decimal] = Field(None, ge=0)
    insurance_value: Optional[Decimal] = Field(None, ge=0)
    cod_amount: Optional[Decimal] = Field(None, ge=0)
    
    # 服务选项
    signature_required: Optional[bool] = None
    fragile: Optional[bool] = None
    urgent: Optional[bool] = None
    
    # 时间
    estimated_pickup_date: Optional[datetime] = None
    estimated_delivery_date: Optional[datetime] = None
    actual_pickup_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    
    # 备注
    notes: Optional[str] = None
    delivery_instructions: Optional[str] = None


# 发货状态更新模型
class ShipmentStatusUpdate(BaseModel):
    status: ShipmentStatus
    notes: Optional[str] = None


# 简化的发货记录响应模型（专注于快递公司和基本追踪信息）
class ShipmentResponse(BaseModel):
    id: UUID
    shipment_code: str
    order_id: UUID
    status: ShipmentStatus
    
    # 快递公司信息
    carrier_name: str
    tracking_number: Optional[str] = None
    shipping_method: str
    
    # 收货地址
    recipient_name: str
    recipient_phone: str
    recipient_email: Optional[str] = None
    shipping_address1: str
    shipping_city: str
    shipping_country: str
    shipping_postcode: str
    
    # 包裹基本信息
    weight: float
    shipping_cost: Decimal
    
    # 时间信息
    estimated_delivery_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    # 备注
    notes: Optional[str] = None
    
    # 关联数据
    items: List[ShipmentItemResponse] = []
    tracking_records: List[TrackingRecordResponse] = []

    class Config:
        from_attributes = True


# 发货记录查询过滤
class ShipmentFilter(BaseModel):
    order_id: Optional[UUID] = None
    shipment_code: Optional[str] = None
    status: Optional[ShipmentStatus] = None
    carrier_id: Optional[UUID] = None
    tracking_number: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    recipient_name: Optional[str] = None
    recipient_phone: Optional[str] = None


# 发货记录列表查询参数
class ShipmentListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
    sort_desc: bool = True
    filters: Optional[ShipmentFilter] = None


# 发货记录列表响应
class ShipmentListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }


# 简化的物流记录简要信息模型（专注于快递公司和基本追踪信息）
class ShipmentBriefResponse(BaseModel):
    id: UUID
    shipment_code: str
    order_id: UUID
    status: ShipmentStatus
    
    # 快递公司信息
    carrier_name: str
    tracking_number: Optional[str] = None
    shipping_method: str
    
    # 收货人信息
    recipient_name: str
    recipient_phone: str
    shipping_city: str
    shipping_country: str
    
    # 时间信息
    created_at: datetime
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    # 最新追踪状态
    latest_tracking_status: Optional[str] = None
    latest_tracking_location: Optional[str] = None
    latest_tracking_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# 发货记录详情响应
class ShipmentDetailResponse(ResponseBase):
    data: Optional[ShipmentResponse] = None


# 承运商列表响应
class CarrierListResponse(ResponseBase):
    data: List[CarrierResponse] = []


# 物流跟踪响应
class TrackingResponse(ResponseBase):
    data: List[TrackingRecordResponse] = []
