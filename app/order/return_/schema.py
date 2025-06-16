from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any, Dict
from uuid import UUID
from pydantic import BaseModel, Field, validator, HttpUrl

from app.order.return_.models import ReturnStatus, ReturnReason, ReturnAction


# 基础响应模型
class ResponseBase(BaseModel):
    code: int = 200
    message: str = "Success"
    data: Any = None


# 退货项模型
class ReturnItemCreate(BaseModel):
    order_item_id: UUID
    quantity: int = Field(..., gt=0)
    reason: Optional[str] = None
    reason_detail: Optional[str] = None


class ReturnItemResponse(BaseModel):
    order_item_id: UUID
    quantity: int
    reason: Optional[str] = None
    reason_detail: Optional[str] = None
    
    class Config:
        from_attributes = True


# 创建退货申请模型
class ReturnCreate(BaseModel):
    order_id: UUID
    reason: ReturnReason
    reason_detail: Optional[str] = None
    requested_action: ReturnAction
    items: List[ReturnItemCreate]
    customer_comment: Optional[str] = None
    images: Optional[List[str]] = None
    attachments: Optional[List[str]] = None
    
    @validator('items')
    def check_items_not_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError('退货申请必须包含至少一个商品')
        return v


# 退货状态更新模型
class ReturnStatusUpdate(BaseModel):
    status: ReturnStatus
    admin_comment: Optional[str] = None
    resolution_comment: Optional[str] = None


# 批准退货申请模型
class ReturnApprove(BaseModel):
    approved_action: ReturnAction
    refund_amount: Optional[Decimal] = None
    refund_tax: Optional[Decimal] = None
    refund_shipping: Optional[Decimal] = None
    return_shipping_method: Optional[str] = None
    return_label_url: Optional[str] = None
    customer_needs_to_ship: bool = True
    admin_comment: Optional[str] = None
    resolution_comment: Optional[str] = None


# 拒绝退货申请模型
class ReturnReject(BaseModel):
    admin_comment: Optional[str] = None
    resolution_comment: str


# 确认收到退货模型
class ReturnReceive(BaseModel):
    admin_comment: Optional[str] = None


# 处理退款模型
class ReturnRefund(BaseModel):
    refund_amount: Decimal
    refund_tax: Optional[Decimal] = None
    refund_shipping: Optional[Decimal] = None
    refund_method: str
    refund_transaction_id: Optional[str] = None
    admin_comment: Optional[str] = None


# 退货查询过滤模型
class ReturnFilter(BaseModel):
    order_id: Optional[UUID] = None
    return_number: Optional[str] = None
    status: Optional[ReturnStatus] = None
    reason: Optional[ReturnReason] = None
    requested_action: Optional[ReturnAction] = None
    approved_action: Optional[ReturnAction] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    customer_id: Optional[UUID] = None


# 退货分页查询参数
class ReturnListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
    sort_desc: bool = True
    filters: Optional[ReturnFilter] = None


# 退货详情响应模型
class ReturnResponse(BaseModel):
    id: UUID
    order_id: UUID
    return_number: str
    status: ReturnStatus
    
    reason: ReturnReason
    reason_detail: Optional[str] = None
    requested_action: ReturnAction
    approved_action: Optional[ReturnAction] = None
    
    refund_amount: Optional[Decimal] = None
    refund_tax: Optional[Decimal] = None
    refund_shipping: Optional[Decimal] = None
    refund_total: Optional[Decimal] = None
    refund_method: Optional[str] = None
    refund_transaction_id: Optional[str] = None
    
    return_shipping_method: Optional[str] = None
    return_tracking_number: Optional[str] = None
    return_label_url: Optional[str] = None
    customer_needs_to_ship: bool
    
    images: Optional[List[str]] = None
    attachments: Optional[List[str]] = None
    
    handler_id: Optional[UUID] = None
    handler_name: Optional[str] = None
    resolution_comment: Optional[str] = None
    customer_comment: Optional[str] = None
    admin_comment: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime] = None
    received_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    items: List[ReturnItemResponse] = []
    
    class Config:
        from_attributes = True


# 退货列表分页响应模型
class ReturnListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }


# 退货详情响�?
class ReturnDetailResponse(ResponseBase):
    data: Optional[ReturnResponse] = None


# 更新退货追踪信�?
class UpdateReturnTracking(BaseModel):
    return_tracking_number: str
    admin_comment: Optional[str] = None
