# -*- coding: utf-8 -*-
"""
免运费规则Pydantic模型
包含请求、响应和验证模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

# 枚举类型
class FreeShippingRuleTypeEnum(str, Enum):
    """免运费规则类型"""
    AMOUNT_BASED = "amount_based"      # 满额免费
    QUANTITY_BASED = "quantity_based"  # 满件免费
    MEMBER_BASED = "member_based"      # 会员免费
    PROMOTION_BASED = "promotion_based" # 促销免费


# 免运费规则翻译模型
class FreeShippingRuleTranslationBase(BaseModel):
    """免运费规则翻译基础模型"""
    language_code: str = Field(..., max_length=10, description="语言代码")
    name: str = Field(..., max_length=100, description="规则名称翻译")
    description: Optional[str] = Field(None, description="规则描述翻译")


class FreeShippingRuleTranslationCreate(FreeShippingRuleTranslationBase):
    """创建免运费规则翻译请求模型"""
    pass


class FreeShippingRuleTranslationUpdate(BaseModel):
    """更新免运费规则翻译请求模型"""
    name: Optional[str] = Field(None, max_length=100, description="规则名称翻译")
    description: Optional[str] = Field(None, description="规则描述翻译")


class FreeShippingRuleTranslationResponse(FreeShippingRuleTranslationBase):
    """免运费规则翻译响应模型"""
    id: str = Field(..., description="翻译ID")
    free_shipping_rule_id: str = Field(..., description="免运费规则ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


# 免运费规则模型
class FreeShippingRuleBase(BaseModel):
    """免运费规则基础模型"""
    code: str = Field(..., max_length=20, description="规则代码")
    name: str = Field(..., max_length=100, description="规则名称")
    description: Optional[str] = Field(None, description="规则描述")
    rule_type: FreeShippingRuleTypeEnum = Field(..., description="规则类型")
    
    # 规则条件
    min_amount: Optional[Decimal] = Field(None, ge=0, description="最小金额（满额免费）")
    min_quantity: Optional[int] = Field(None, ge=0, description="最小件数（满件免费）")
    member_levels: Optional[str] = Field(None, description="适用会员等级，逗号分隔")
    promotion_codes: Optional[str] = Field(None, description="适用促销代码，逗号分隔")
    
    # 适用范围
    applicable_zones: Optional[str] = Field(None, description="适用地区代码，逗号分隔，空为全部")
    applicable_methods: Optional[str] = Field(None, description="适用快递方式代码，逗号分隔，空为全部")
    
    # 时间范围
    start_date: Optional[datetime] = Field(None, description="开始时间")
    end_date: Optional[datetime] = Field(None, description="结束时间")
    
    # 状态
    is_active: bool = Field(True, description="是否启用")
    priority: int = Field(0, description="优先级，数值越大优先级越高")
    sort_order: int = Field(0, description="排序")

    @validator('end_date')
    def validate_date_range(cls, v, values):
        """验证结束时间必须大于开始时间"""
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('结束时间必须大于开始时间')
        return v

    @validator('min_amount')
    def validate_amount_based_rule(cls, v, values):
        """验证满额免费规则必须设置最小金额"""
        if values.get('rule_type') == FreeShippingRuleTypeEnum.AMOUNT_BASED and not v:
            raise ValueError('满额免费规则必须设置最小金额')
        return v

    @validator('min_quantity')
    def validate_quantity_based_rule(cls, v, values):
        """验证满件免费规则必须设置最小件数"""
        if values.get('rule_type') == FreeShippingRuleTypeEnum.QUANTITY_BASED and not v:
            raise ValueError('满件免费规则必须设置最小件数')
        return v

    @validator('member_levels')
    def validate_member_based_rule(cls, v, values):
        """验证会员免费规则必须设置会员等级"""
        if values.get('rule_type') == FreeShippingRuleTypeEnum.MEMBER_BASED and not v:
            raise ValueError('会员免费规则必须设置适用会员等级')
        return v

    @validator('promotion_codes')
    def validate_promotion_based_rule(cls, v, values):
        """验证促销免费规则必须设置促销代码"""
        if values.get('rule_type') == FreeShippingRuleTypeEnum.PROMOTION_BASED and not v:
            raise ValueError('促销免费规则必须设置适用促销代码')
        return v


class FreeShippingRuleCreate(FreeShippingRuleBase):
    """创建免运费规则请求模型"""
    translations: Optional[List[FreeShippingRuleTranslationCreate]] = Field(None, description="多语言翻译")


class FreeShippingRuleUpdate(BaseModel):
    """更新免运费规则请求模型"""
    code: Optional[str] = Field(None, max_length=20, description="规则代码")
    name: Optional[str] = Field(None, max_length=100, description="规则名称")
    description: Optional[str] = Field(None, description="规则描述")
    rule_type: Optional[FreeShippingRuleTypeEnum] = Field(None, description="规则类型")
    
    # 规则条件
    min_amount: Optional[Decimal] = Field(None, ge=0, description="最小金额（满额免费）")
    min_quantity: Optional[int] = Field(None, ge=0, description="最小件数（满件免费）")
    member_levels: Optional[str] = Field(None, description="适用会员等级，逗号分隔")
    promotion_codes: Optional[str] = Field(None, description="适用促销代码，逗号分隔")
    
    # 适用范围
    applicable_zones: Optional[str] = Field(None, description="适用地区代码，逗号分隔，空为全部")
    applicable_methods: Optional[str] = Field(None, description="适用快递方式代码，逗号分隔，空为全部")
    
    # 时间范围
    start_date: Optional[datetime] = Field(None, description="开始时间")
    end_date: Optional[datetime] = Field(None, description="结束时间")
    
    # 状态
    is_active: Optional[bool] = Field(None, description="是否启用")
    priority: Optional[int] = Field(None, description="优先级，数值越大优先级越高")
    sort_order: Optional[int] = Field(None, description="排序")


class FreeShippingRuleResponse(FreeShippingRuleBase):
    """免运费规则响应模型"""
    id: str = Field(..., description="免运费规则ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    translations: List[FreeShippingRuleTranslationResponse] = Field([], description="多语言翻译")

    class Config:
        from_attributes = True


# 查询参数模型
class FreeShippingRuleQueryParams(BaseModel):
    """免运费规则查询参数"""
    rule_type: Optional[FreeShippingRuleTypeEnum] = Field(None, description="规则类型筛选")
    is_active: Optional[bool] = Field(None, description="是否启用筛选")
    language_code: Optional[str] = Field("zh-CN", description="语言代码")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页条数")


# 应用免运费规则请求模型
class ApplyFreeShippingRequest(BaseModel):
    """应用免运费规则请求模型"""
    country_code: str = Field(..., description="国家代码")
    total_amount: Decimal = Field(..., ge=0, description="订单总金额")
    total_quantity: int = Field(..., ge=0, description="商品总件数")
    member_level: Optional[str] = Field(None, description="会员等级")
    promotion_codes: Optional[List[str]] = Field(None, description="促销代码列表")
    shipping_method_code: Optional[str] = Field(None, description="快递方式代码")
    language_code: str = Field("zh-CN", description="语言代码")


# 免运费检查结果模型
class FreeShippingCheckResult(BaseModel):
    """免运费检查结果"""
    is_free: bool = Field(..., description="是否免运费")
    applied_rule_id: Optional[str] = Field(None, description="应用的规则ID")
    applied_rule_name: Optional[str] = Field(None, description="应用的规则名称")
    applied_rule_type: Optional[FreeShippingRuleTypeEnum] = Field(None, description="应用的规则类型")
    reason: Optional[str] = Field(None, description="免运费原因描述")
    savings_amount: Optional[Decimal] = Field(None, description="节省的运费金额")
    next_threshold: Optional[Decimal] = Field(None, description="下一个免运费门槛（满额免费）")
    next_quantity: Optional[int] = Field(None, description="下一个免运费件数（满件免费）") 