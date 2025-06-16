from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from app.marketing.coupon.models import CouponStatus, CouponFormat
from app.marketing.promotion.models import PromotionType, DiscountType


# 基础响应模型
class ResponseBase(BaseModel):
    code: int = 200
    message: str = "Success"
    data: Any = None


# 促销基础模型
class PromotionBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: PromotionType = PromotionType.COUPON  # 默认为优惠券类型
    is_active: bool = True
    
    # 时间设置
    start_date: datetime
    end_date: Optional[datetime] = None
    active_days: Optional[List[int]] = None  # 0-6表示周日到周�?
    active_hours_start: Optional[int] = None  # 0-23
    active_hours_end: Optional[int] = None  # 0-23
    
    # 促销规则
    discount_type: DiscountType
    discount_value: float
    min_order_amount: Optional[float] = None
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    
    # 地区和货币设�?
    applicable_countries: Optional[List[str]] = None
    excluded_countries: Optional[List[str]] = None
    applicable_currencies: Optional[List[str]] = None
    
    # 客户限制
    customer_eligibility: str = "all"  # all, new, existing, specific
    eligible_customer_groups: Optional[List[UUID]] = None
    min_customer_orders: Optional[int] = None
    
    # 产品限制
    applicable_products: Optional[List[UUID]] = None
    excluded_products: Optional[List[UUID]] = None
    applicable_categories: Optional[List[UUID]] = None
    excluded_categories: Optional[List[UUID]] = None
    
    # 组合规则
    combination_strategy: str = "stack"  # stack(叠加), exclusive(独占), priority(优先)
    priority: int = 0
    
    # 显示设置
    image_url: Optional[str] = None
    banner_url: Optional[str] = None
    highlight_color: Optional[str] = None
    is_featured: bool = False
    
    # 文化和主题关�?
    cultural_theme: Optional[str] = None
    intention_type: Optional[str] = None
    
    # 额外设置
    meta_data: Optional[Dict[str, Any]] = None


# 优惠券基础模型
class CouponBase(BaseModel):
    code: Optional[str] = None  # 可以为空，由系统自动生成
    status: CouponStatus = CouponStatus.ACTIVE
    
    # 生成设置
    format: CouponFormat = CouponFormat.ALPHANUMERIC
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    length: int = 8
    
    # 使用限制
    max_uses: Optional[int] = None
    max_uses_per_customer: int = 1
    is_single_use: bool = True
    requires_authentication: bool = True
    
    # 使用控制 (注：从Promotion中继承start_date和end_date)
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    
    # 分销规则
    is_referral: bool = False
    referrer_reward: Optional[float] = None
    
    # 邮件和分享设�?
    is_public: bool = False
    is_featured: bool = False
    auto_apply: bool = False
    
    # 赠品配置
    free_product_id: Optional[UUID] = None
    free_product_quantity: int = 1
    
    # 额外信息
    meta_data: Optional[Dict[str, Any]] = None


# 创建单个优惠�?
class CouponCreate(BaseModel):
    promotion: PromotionBase
    coupon: CouponBase


# 批量创建优惠�?
class CouponBatchCreate(BaseModel):
    promotion: PromotionBase
    batch_name: str
    batch_description: Optional[str] = None
    code_prefix: Optional[str] = None
    code_format: CouponFormat = CouponFormat.ALPHANUMERIC
    code_length: int = 8
    quantity: int = Field(..., gt=0, le=10000)  # 限制数量
    max_uses_per_coupon: int = 1
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    
    @validator('quantity')
    def check_quantity(cls, v):
        if v <= 0:
            raise ValueError("数量必须大于0")
        if v > 10000:
            raise ValueError("单次批量创建数量不能超过10000")
        return v


# 更新优惠�?
class CouponUpdate(BaseModel):
    status: Optional[CouponStatus] = None
    max_uses: Optional[int] = None
    max_uses_per_customer: Optional[int] = None
    is_single_use: Optional[bool] = None
    requires_authentication: Optional[bool] = None
    valid_to: Optional[datetime] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None
    auto_apply: Optional[bool] = None
    meta_data: Optional[Dict[str, Any]] = None


# 优惠券验�?
class CouponValidate(BaseModel):
    code: str
    customer_id: Optional[UUID] = None
    order_amount: float
    products: List[Dict[str, Any]] = []  # 包含产品ID、数量、价格等信息
    currency_code: str = "USD"
    country_code: Optional[str] = None


# 优惠券发�?
class CouponIssue(BaseModel):
    coupon_id: UUID
    customer_ids: List[UUID]
    issue_method: str
    custom_message: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    notification_method: Optional[str] = None
    referrer_id: Optional[UUID] = None
    notes: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


# 查询过滤
class CouponFilter(BaseModel):
    code: Optional[str] = None
    status: Optional[CouponStatus] = None
    batch_id: Optional[UUID] = None
    is_referral: Optional[bool] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None
    valid_from_start: Optional[datetime] = None
    valid_from_end: Optional[datetime] = None
    valid_to_start: Optional[datetime] = None
    valid_to_end: Optional[datetime] = None
    created_at_start: Optional[datetime] = None
    created_at_end: Optional[datetime] = None


# 分页参数
class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
    sort_desc: bool = True


# 优惠券列表请�?
class CouponListRequest(BaseModel):
    filters: Optional[CouponFilter] = None
    pagination: Optional[PaginationParams] = PaginationParams()


# 优惠券响应模�?
class CouponResponse(BaseModel):
    id: UUID
    promotion_id: UUID
    code: str
    status: CouponStatus
    format: CouponFormat
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    length: int
    max_uses: Optional[int] = None
    max_uses_per_customer: int
    current_uses: int = 0
    is_single_use: bool
    requires_authentication: bool
    valid_from: datetime
    valid_to: Optional[datetime] = None
    is_batch: bool = False
    batch_id: Optional[UUID] = None
    is_referral: bool
    referrer_reward: Optional[float] = None
    is_public: bool
    is_featured: bool
    auto_apply: bool
    free_product_id: Optional[UUID] = None
    free_product_quantity: int
    view_count: int = 0
    conversion_rate: float = 0
    meta_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    # 关联的促销信息
    promotion_name: str
    promotion_description: Optional[str] = None
    promotion_type: PromotionType
    discount_type: DiscountType
    discount_value: float
    
    class Config:
        from_attributes = True


# 优惠券详情响�?
class CouponDetailResponse(ResponseBase):
    data: Optional[CouponResponse] = None


# 优惠券列表响�?
class CouponListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }


# 优惠券验证响�?
class CouponValidationResponse(ResponseBase):
    data: Dict[str, Any] = {
        "is_valid": False,
        "discount_amount": 0,
        "message": ""
    }


# 优惠券批次响�?
class CouponBatchResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    code_prefix: Optional[str] = None
    code_format: CouponFormat
    code_length: int
    quantity: int
    generated_count: int
    used_count: int
    max_uses_per_coupon: int
    valid_from: datetime
    valid_to: Optional[datetime] = None
    is_exported: bool
    export_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 客户优惠券响�?
class CustomerCouponResponse(BaseModel):
    id: UUID
    customer_id: UUID
    coupon_id: UUID
    status: str
    issue_method: str
    issued_by: Optional[UUID] = None
    issued_at: datetime
    used_at: Optional[datetime] = None
    order_id: Optional[UUID] = None
    discount_amount: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    notification_sent: bool
    notification_method: Optional[str] = None
    referrer_id: Optional[UUID] = None
    custom_message: Optional[str] = None
    notes: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    # 关联的优惠券信息
    coupon_code: str
    coupon_promotion_name: str
    discount_type: DiscountType
    discount_value: float
    
    class Config:
        from_attributes = True


# 客户优惠券列表响�?
class CustomerCouponListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }
