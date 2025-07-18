# -*- coding: utf-8 -*-
"""
快递运费主模块
包含快递方式、地区配置、运费规则、免运费规则等子模块
"""

# 导入子模块
from .method import (
    ShippingMethod, ShippingMethodTranslation,
    ShippingMethodCreate, ShippingMethodUpdate, ShippingMethodResponse,
    ShippingMethodService, method_router
)

from .zone import (
    ShippingZone, ShippingZoneTranslation,
    ShippingZoneCreate, ShippingZoneUpdate, ShippingZoneResponse,
    ShippingZoneService, zone_router
)

from .rate import (
    ShippingRate,
    ShippingRateCreate, ShippingRateUpdate, ShippingRateResponse,
    ShippingRateService, rate_router
)

from .free_rule import (
    FreeShippingRule, FreeShippingRuleTranslation,
    FreeShippingRuleCreate, FreeShippingRuleUpdate, FreeShippingRuleResponse,
    FreeShippingRuleTranslationCreate, FreeShippingRuleTranslationUpdate,
    FreeShippingRuleTranslationResponse, FreeShippingRuleService,
    ApplyFreeShippingRequest, FreeShippingCheckResult,
    free_rule_router
)

from .calculation import (
    ShippingCalculationRequest, ShippingCalculationResponse,
    ShippingMethodOption, ShippingEstimate, ShippingBreakdown,
    ShippingCalculationService
)

from .order_record import (
    OrderChargeItem, OrderShippingInfo,
    OrderChargeItemCreate, OrderChargeItemUpdate, OrderChargeItemResponse,
    OrderShippingInfoCreate, OrderShippingInfoUpdate, OrderShippingInfoResponse,
    OrderRecordService
)

# 重新导出模型用于数据库迁移
__all__ = [
    # 方式相关
    "ShippingMethod",
    "ShippingMethodTranslation",
    "ShippingMethodCreate", 
    "ShippingMethodUpdate", 
    "ShippingMethodResponse",
    "ShippingMethodService",
    "method_router",
    
    # 地区相关
    "ShippingZone",
    "ShippingZoneTranslation", 
    "ShippingZoneCreate",
    "ShippingZoneUpdate",
    "ShippingZoneResponse",
    "ShippingZoneService",
    "zone_router",
    
    # 运费规则相关
    "ShippingRate",
    "ShippingRateCreate",
    "ShippingRateUpdate", 
    "ShippingRateResponse",
    "ShippingRateService",
    "rate_router",
    
    # 免运费规则相关
    "FreeShippingRule",
    "FreeShippingRuleTranslation",
    "FreeShippingRuleCreate",
    "FreeShippingRuleUpdate",
    "FreeShippingRuleResponse",
    "FreeShippingRuleTranslationCreate",
    "FreeShippingRuleTranslationUpdate",
    "FreeShippingRuleTranslationResponse",
    "FreeShippingRuleService",
    "ApplyFreeShippingRequest",
    "FreeShippingCheckResult",
    "free_rule_router",
    
    # 运费计算相关
    "ShippingCalculationRequest",
    "ShippingCalculationResponse",
    "ShippingMethodOption",
    "ShippingEstimate",
    "ShippingBreakdown",
    "ShippingCalculationService",
    
    # 订单运费记录相关
    "OrderChargeItem",
    "OrderShippingInfo",
    "OrderChargeItemCreate",
    "OrderChargeItemUpdate",
    "OrderChargeItemResponse",
    "OrderShippingInfoCreate",
    "OrderShippingInfoUpdate",
    "OrderShippingInfoResponse",
    "OrderRecordService",
]