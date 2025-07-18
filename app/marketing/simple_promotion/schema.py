from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

from .models import SimplePromotionType, DiscountType


class SimplePromotionBase(BaseModel):
    code: str = Field(..., description="促销代码")
    name: str = Field(..., description="促销名称")
    description: Optional[str] = Field(None, description="促销描述")
    type: SimplePromotionType = Field(..., description="促销类型")
    is_active: bool = Field(True, description="是否激活")
    start_date: datetime = Field(..., description="开始时间")
    end_date: Optional[datetime] = Field(None, description="结束时间")
    discount_type: DiscountType = Field(..., description="折扣类型")
    discount_value: float = Field(..., description="折扣值")
    usage_limit: Optional[int] = Field(None, description="使用次数限制")
    per_customer_limit: int = Field(1, description="每客户使用次数限制")
    rules: Optional[Dict[str, Any]] = Field(None, description="促销规则")


class SimplePromotionCreate(SimplePromotionBase):
    pass


class SimplePromotionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = None
    usage_limit: Optional[int] = None
    per_customer_limit: Optional[int] = None
    rules: Optional[Dict[str, Any]] = None


class SimplePromotionResponse(SimplePromotionBase):
    id: UUID
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 促销规则的具体Schema定义
class DiscountRules(BaseModel):
    """折扣/满减规则"""
    min_amount: Optional[float] = Field(None, description="最低消费金额")
    max_discount: Optional[float] = Field(None, description="最大折扣金额")
    applicable_products: Optional[List[UUID]] = Field(None, description="适用商品ID列表")
    excluded_products: Optional[List[UUID]] = Field(None, description="排除商品ID列表")


class BundleRules(BaseModel):
    """打包优惠规则"""
    product_ids: List[UUID] = Field(..., description="打包商品ID列表")
    bundle_price: Optional[float] = Field(None, description="套装价格")
    min_quantity: Optional[int] = Field(None, description="最少购买数量")


class CouponRules(BaseModel):
    """优惠券规则"""
    min_amount: Optional[float] = Field(None, description="最低消费金额")
    max_discount: Optional[float] = Field(None, description="最大折扣金额")
    first_purchase_only: bool = Field(False, description="仅限首次购买")


# 促销应用请求
class ApplyPromotionRequest(BaseModel):
    promotion_code: str = Field(..., description="促销代码")
    customer_id: Optional[UUID] = Field(None, description="客户ID")
    cart_items: List[Dict[str, Any]] = Field(..., description="购物车商品")


# 促销应用结果
class PromotionResult(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    discount_amount: float = Field(0, description="折扣金额")
    original_total: float = Field(..., description="原始总金额")
    final_total: float = Field(..., description="最终总金额")
    applied_promotion: Optional[SimplePromotionResponse] = Field(None, description="应用的促销")


# 常用促销模板
class PromotionTemplate(BaseModel):
    name: str
    type: SimplePromotionType
    discount_type: DiscountType
    discount_value: float
    rules: Dict[str, Any]
    description: str


# 预定义模板
PROMOTION_TEMPLATES = [
    PromotionTemplate(
        name="新客首单8折",
        type=SimplePromotionType.DISCOUNT,
        discount_type=DiscountType.PERCENTAGE,
        discount_value=20,
        rules={"first_purchase_only": True},
        description="新客户首次购买享受8折优惠"
    ),
    PromotionTemplate(
        name="满500减50",
        type=SimplePromotionType.DISCOUNT,
        discount_type=DiscountType.FIXED_AMOUNT,
        discount_value=50,
        rules={"min_amount": 500},
        description="单笔订单满500元减50元"
    ),
    PromotionTemplate(
        name="护身符套装优惠",
        type=SimplePromotionType.BUNDLE,
        discount_type=DiscountType.FIXED_AMOUNT,
        discount_value=100,
        rules={"product_ids": [], "bundle_price": 999},
        description="购买指定护身符套装享受特价"
    )
]