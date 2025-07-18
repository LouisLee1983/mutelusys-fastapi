from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# 基础schemas
class DutyZoneTranslationBase(BaseModel):
    language: str = Field(..., description="语言代码")
    name: str = Field(..., description="翻译名称")
    description: Optional[str] = Field(None, description="描述")


class DutyZoneTranslationCreate(DutyZoneTranslationBase):
    pass


class DutyZoneTranslationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="翻译名称")
    description: Optional[str] = Field(None, description="描述")


class DutyZoneTranslation(DutyZoneTranslationBase):
    id: str
    zone_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductDutyCategoryTranslationBase(BaseModel):
    language: str = Field(..., description="语言代码")
    name: str = Field(..., description="翻译名称")
    description: Optional[str] = Field(None, description="描述")


class ProductDutyCategoryTranslationCreate(ProductDutyCategoryTranslationBase):
    pass


class ProductDutyCategoryTranslationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="翻译名称")
    description: Optional[str] = Field(None, description="描述")


class ProductDutyCategoryTranslation(ProductDutyCategoryTranslationBase):
    id: str
    category_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 关税区域schemas
class DutyZoneBase(BaseModel):
    name: str = Field(..., max_length=100, description="关税区域名称")
    tax_free_threshold: float = Field(default=0.0, ge=0, description="免税阈值金额")
    default_tax_rate: float = Field(default=0.0, ge=0, le=1, description="默认税率 0.08表示8%")
    currency: str = Field(default="USD", max_length=3, description="计算货币")
    status: str = Field(default="active", description="状态")


class DutyZoneCreate(DutyZoneBase):
    translations: Optional[List[DutyZoneTranslationCreate]] = Field(default=[], description="翻译列表")
    country_ids: Optional[List[str]] = Field(default=[], description="关联的国家ID列表")


class DutyZoneUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="关税区域名称")
    tax_free_threshold: Optional[float] = Field(None, ge=0, description="免税阈值金额")
    default_tax_rate: Optional[float] = Field(None, ge=0, le=1, description="默认税率")
    currency: Optional[str] = Field(None, max_length=3, description="计算货币")
    status: Optional[str] = Field(None, description="状态")


class DutyZone(DutyZoneBase):
    id: str
    created_at: datetime
    updated_at: datetime
    translations: List[DutyZoneTranslation] = Field(default=[], description="翻译列表")
    
    class Config:
        from_attributes = True


class DutyZoneSimple(BaseModel):
    """简化的关税区域信息"""
    id: str
    name: str
    tax_free_threshold: float
    default_tax_rate: float
    currency: str
    
    class Config:
        from_attributes = True


# 商品关税分类schemas
class ProductDutyCategoryBase(BaseModel):
    name: str = Field(..., max_length=100, description="分类名称")
    tax_rate: Optional[float] = Field(None, ge=0, le=1, description="该分类的税率")
    status: str = Field(default="active", description="状态")


class ProductDutyCategoryCreate(ProductDutyCategoryBase):
    translations: Optional[List[ProductDutyCategoryTranslationCreate]] = Field(default=[], description="翻译列表")


class ProductDutyCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="分类名称")
    tax_rate: Optional[float] = Field(None, ge=0, le=1, description="该分类的税率")
    status: Optional[str] = Field(None, description="状态")


class ProductDutyCategory(ProductDutyCategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime
    translations: List[ProductDutyCategoryTranslation] = Field(default=[], description="翻译列表")
    
    class Config:
        from_attributes = True


class ProductDutyCategorySimple(BaseModel):
    """简化的商品关税分类信息"""
    id: str
    name: str
    tax_rate: Optional[float] = None
    
    class Config:
        from_attributes = True


# 关税规则schemas
class DutyRuleBase(BaseModel):
    zone_id: str = Field(..., description="关税区域ID")
    category_id: Optional[str] = Field(None, description="商品分类ID，null表示通用规则")
    tax_free_amount: float = Field(default=0.0, ge=0, description="免税金额")
    tax_rate: float = Field(..., ge=0, le=1, description="税率")
    min_tax_amount: float = Field(default=0.0, ge=0, description="最低征税额")
    max_tax_amount: Optional[float] = Field(None, ge=0, description="最高征税额")
    priority: int = Field(default=1, ge=1, description="优先级，数字越小优先级越高")
    valid_from: Optional[datetime] = Field(None, description="生效时间")
    valid_to: Optional[datetime] = Field(None, description="失效时间")
    status: str = Field(default="active", description="状态")


class DutyRuleCreate(DutyRuleBase):
    pass


class DutyRuleUpdate(BaseModel):
    zone_id: Optional[str] = Field(None, description="关税区域ID")
    category_id: Optional[str] = Field(None, description="商品分类ID")
    tax_free_amount: Optional[float] = Field(None, ge=0, description="免税金额")
    tax_rate: Optional[float] = Field(None, ge=0, le=1, description="税率")
    min_tax_amount: Optional[float] = Field(None, ge=0, description="最低征税额")
    max_tax_amount: Optional[float] = Field(None, ge=0, description="最高征税额")
    priority: Optional[int] = Field(None, ge=1, description="优先级")
    valid_from: Optional[datetime] = Field(None, description="生效时间")
    valid_to: Optional[datetime] = Field(None, description="失效时间")
    status: Optional[str] = Field(None, description="状态")


class DutyRule(DutyRuleBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DutyRuleWithDetails(DutyRule):
    """包含详细信息的关税规则"""
    zone: Optional[DutyZoneSimple] = None
    category: Optional[ProductDutyCategorySimple] = None


# 订单关税记录schemas
class OrderDutyChargeBase(BaseModel):
    order_id: str = Field(..., description="订单ID")
    country_id: str = Field(..., description="收货国家ID")
    duty_zone_id: str = Field(..., description="关税区域ID")
    taxable_amount: float = Field(..., ge=0, description="应税金额")
    tax_rate: float = Field(..., ge=0, le=1, description="适用税率")
    duty_amount: float = Field(..., ge=0, description="关税金额")
    currency: str = Field(..., max_length=3, description="货币")
    calculation_details: Optional[str] = Field(None, description="JSON格式的计算明细")
    status: str = Field(default="pending", description="状态")


class OrderDutyChargeCreate(OrderDutyChargeBase):
    pass


class OrderDutyChargeUpdate(BaseModel):
    status: Optional[str] = Field(None, description="状态")


class OrderDutyCharge(OrderDutyChargeBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 关税计算相关schemas
class DutyCalculationItem(BaseModel):
    """关税计算的商品项目"""
    product_id: str = Field(..., description="商品ID")
    category_id: Optional[str] = Field(None, description="商品关税分类ID")
    quantity: int = Field(..., gt=0, description="数量")
    price: float = Field(..., gt=0, description="单价")


class DutyCalculationRequest(BaseModel):
    """关税计算请求"""
    country_code: str = Field(..., description="国家代码")
    items: List[DutyCalculationItem] = Field(..., description="商品列表")
    shipping_cost: float = Field(default=0.0, ge=0, description="运费")
    currency: str = Field(default="USD", description="货币")


class DutyCalculationResult(BaseModel):
    """关税计算结果"""
    country_code: str
    duty_zone_id: Optional[str] = None
    duty_zone_name: Optional[str] = None
    taxable_amount: float
    tax_rate: float
    duty_amount: float
    is_tax_free: bool
    currency: str
    calculation_details: Dict[str, Any]


class DutyCalculationBatchRequest(BaseModel):
    """批量关税计算请求"""
    calculations: List[DutyCalculationRequest] = Field(..., description="批量计算请求列表")


class DutyCalculationBatchResult(BaseModel):
    """批量关税计算结果"""
    results: List[DutyCalculationResult]
    total_count: int
    success_count: int
    error_count: int


# 查询和响应schemas
class DutyZoneListResponse(BaseModel):
    zones: List[DutyZone]
    total: int
    page: int
    size: int


class ProductDutyCategoryListResponse(BaseModel):
    categories: List[ProductDutyCategory]
    total: int
    page: int
    size: int


class DutyRuleListResponse(BaseModel):
    rules: List[DutyRuleWithDetails]
    total: int
    page: int
    size: int


class OrderDutyChargeListResponse(BaseModel):
    charges: List[OrderDutyCharge]
    total: int
    page: int
    size: int


# 统计schemas
class DutyStatistics(BaseModel):
    """关税统计信息"""
    total_duty_zones: int
    total_categories: int
    total_rules: int
    total_orders_with_duty: int
    total_duty_amount: float
    average_duty_rate: float


class DutyZoneStatistics(BaseModel):
    """关税区域统计"""
    zone_id: str
    zone_name: str
    order_count: int
    total_duty_amount: float
    average_duty_amount: float
    most_common_rate: float


# 支持的国家schemas
class SupportedCountry(BaseModel):
    """支持关税计算的国家"""
    id: str
    code: str
    name: str
    duty_zone_id: Optional[str] = None
    duty_zone_name: Optional[str] = None
    has_duty: bool
    tax_free_threshold: float
    default_tax_rate: float


class SupportedCountriesResponse(BaseModel):
    """支持的国家列表响应"""
    countries: List[SupportedCountry]
    total: int