from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any, Dict
from uuid import UUID
from pydantic import BaseModel, Field, validator, EmailStr

from app.order.models import OrderStatus, PaymentStatus, ShippingStatus


# 基础响应模型
class ResponseBase(BaseModel):
    code: int = 200
    message: str = "Success"
    data: Any = None


# 订单项模型
class OrderItemCreate(BaseModel):
    product_id: UUID
    sku_id: Optional[UUID] = None
    quantity: int
    unit_price: Decimal
    
    # 兼容前端字段名
    product_name: Optional[str] = None  # 前端使用的字段名
    sku_name: Optional[str] = None      # 前端使用的字段名
    
    # 内部使用的字段名（优先级高于前端字段）
    name: Optional[str] = None          # 商品名称
    sku_code: Optional[str] = None      # SKU代码
    
    # 可选的计算字段（如果前端不提供，会自动计算）
    subtotal: Optional[Decimal] = None
    discount_amount: Decimal = 0
    tax_amount: Decimal = 0
    final_price: Optional[Decimal] = None
    
    attributes: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    
    @validator('name', pre=True, always=True)
    def set_name(cls, v, values):
        """如果name为空，使用product_name"""
        return v or values.get('product_name') or 'Unknown Product'
    
    @validator('sku_code', pre=True, always=True)
    def set_sku_code(cls, v, values):
        """如果sku_code为空，使用sku_name"""
        return v or values.get('sku_name')
    
    @validator('subtotal', pre=True, always=True)
    def calculate_subtotal(cls, v, values):
        """如果subtotal为空，自动计算：数量 × 单价"""
        if v is not None:
            return v
        quantity = values.get('quantity', 1)
        unit_price = values.get('unit_price', 0)
        return Decimal(str(quantity)) * unit_price
    
    @validator('final_price', pre=True, always=True)
    def calculate_final_price(cls, v, values):
        """如果final_price为空，自动计算：小计 - 折扣 + 税费"""
        if v is not None:
            return v
        
        quantity = values.get('quantity', 1)
        unit_price = values.get('unit_price', 0)
        subtotal = Decimal(str(quantity)) * unit_price
        
        discount_amount = values.get('discount_amount', 0)
        tax_amount = values.get('tax_amount', 0)
        
        return subtotal - discount_amount + tax_amount


class OrderItemResponse(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    sku_id: Optional[UUID] = None
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    product_name: str = Field(alias="name")  # 映射数据库的name字段到product_name
    sku_name: Optional[str] = Field(default=None, alias="sku_code")  # 映射数据库的sku_code字段到sku_name
    attributes: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True  # 允许使用字段名和别名


# 订单地址模型
class AddressInfo(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    address1: str
    address2: Optional[str] = None
    city: str
    state: Optional[str] = None
    country: str
    postcode: str
    
    @validator('email', pre=True)
    def validate_email(cls, v):
        """将空字符串转换为None，以便正确处理可选的邮箱字段"""
        if v == '' or v is None:
            return None
        return v


# 订单创建模型
class OrderCreate(BaseModel):
    customer_id: Optional[UUID] = None
    currency_code: str = Field(..., min_length=3, max_length=3)
    
    # 订单金额字段 - 变为可选，可以自动计算
    subtotal: Optional[Decimal] = None
    shipping_amount: Decimal = 0
    tax_amount: Decimal = 0
    discount_amount: Decimal = 0
    total_amount: Optional[Decimal] = None
    
    items: List[OrderItemCreate]
    shipping_address: AddressInfo
    billing_address: Optional[AddressInfo] = None
    coupon_code: Optional[str] = None
    is_gift: bool = False
    gift_message: Optional[str] = None
    customer_note: Optional[str] = None
    source: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    @validator('items')
    def check_items_not_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError('订单必须包含至少一个商品')
        return v
    
    @validator('subtotal', pre=True, always=True)
    def calculate_subtotal(cls, v, values):
        """如果subtotal为空，自动计算所有商品小计之和"""
        if v is not None:
            return v
        
        items = values.get('items', [])
        if not items:
            return Decimal('0')
        
        total = Decimal('0')
        for item in items:
            try:
                # 计算每个商品的小计
                if isinstance(item, dict):
                    quantity = item.get('quantity', 1)
                    unit_price = item.get('unit_price', 0)
                else:
                    # Pydantic对象
                    quantity = getattr(item, 'quantity', 1)
                    unit_price = getattr(item, 'unit_price', 0)
                
                total += Decimal(str(quantity)) * Decimal(str(unit_price))
            except Exception as e:
                print(f"计算商品小计时出错: {e}, item: {item}")
                continue
        
        return total
    
    @validator('total_amount', pre=True, always=True)
    def calculate_total_amount(cls, v, values):
        """如果total_amount为空，自动计算：小计 + 运费 + 税费 - 折扣"""
        if v is not None:
            return v
        
        # 使用已计算的小计，如果没有则重新计算
        subtotal = values.get('subtotal')
        if subtotal is None:
            items = values.get('items', [])
            subtotal = Decimal('0')
            if items:
                for item in items:
                    try:
                        if isinstance(item, dict):
                            quantity = item.get('quantity', 1)
                            unit_price = item.get('unit_price', 0)
                        else:
                            quantity = getattr(item, 'quantity', 1)
                            unit_price = getattr(item, 'unit_price', 0)
                        
                        subtotal += Decimal(str(quantity)) * Decimal(str(unit_price))
                    except Exception as e:
                        print(f"计算总额时商品小计出错: {e}, item: {item}")
                        continue
        
        shipping_amount = Decimal(str(values.get('shipping_amount', 0)))
        tax_amount = Decimal(str(values.get('tax_amount', 0)))
        discount_amount = Decimal(str(values.get('discount_amount', 0)))
        
        return subtotal + shipping_amount + tax_amount - discount_amount


# 订单状态更新模型
class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    admin_note: Optional[str] = None


class OrderPaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus
    paid_amount: Optional[Decimal] = None
    admin_note: Optional[str] = None


class OrderShippingStatusUpdate(BaseModel):
    shipping_status: ShippingStatus
    admin_note: Optional[str] = None


# 订单查询过滤模型
class OrderFilter(BaseModel):
    order_number: Optional[str] = None
    customer_id: Optional[UUID] = None
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    shipping_status: Optional[ShippingStatus] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    is_gift: Optional[bool] = None


# 订单分页查询参数
class OrderListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
    sort_desc: bool = True
    filters: Optional[OrderFilter] = None


# 订单响应模型
class OrderResponse(BaseModel):
    id: UUID
    order_number: str
    customer_id: Optional[UUID] = None
    status: OrderStatus
    payment_status: PaymentStatus
    shipping_status: ShippingStatus
    currency_code: str
    
    subtotal: Decimal
    shipping_amount: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    
    shipping_name: Optional[str] = None
    shipping_phone: Optional[str] = None
    shipping_email: Optional[EmailStr] = None
    shipping_address1: Optional[str] = None
    shipping_address2: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_country: Optional[str] = None
    shipping_postcode: Optional[str] = None
    
    coupon_code: Optional[str] = None
    is_gift: bool
    gift_message: Optional[str] = None
    customer_note: Optional[str] = None
    source: Optional[str] = None
    
    estimate_delivery_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


# 订单列表分页响应
class OrderListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }


# 订单详情响应
class OrderDetailResponse(ResponseBase):
    data: Optional[OrderResponse] = None
