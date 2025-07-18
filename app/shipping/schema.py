# -*- coding: utf-8 -*-
"""
快递运费Schema统一导入
从子模块导入所有Schema模型
"""

# 从子模块导入schemas
from .method.schema import (
    ShippingMethodCreate, ShippingMethodUpdate, ShippingMethodResponse,
    ShippingMethodTranslationCreate, ShippingMethodTranslationUpdate,
    ShippingMethodTranslationResponse, ShippingMethodListResponse
)

from .zone.schema import (
    ShippingZoneCreate, ShippingZoneUpdate, ShippingZoneResponse,
    ShippingZoneTranslationCreate, ShippingZoneTranslationUpdate,
    ShippingZoneTranslationResponse, ShippingZoneListResponse
)

from .rate.schema import (
    ShippingRateCreate, ShippingRateUpdate, ShippingRateResponse,
    ShippingRateListResponse
)

# 导出所有schemas
__all__ = [
    # 快递方式相关
    "ShippingMethodCreate",
    "ShippingMethodUpdate", 
    "ShippingMethodResponse",
    "ShippingMethodTranslationCreate",
    "ShippingMethodTranslationUpdate",
    "ShippingMethodTranslationResponse",
    "ShippingMethodListResponse",
    
    # 地区相关
    "ShippingZoneCreate",
    "ShippingZoneUpdate",
    "ShippingZoneResponse", 
    "ShippingZoneTranslationCreate",
    "ShippingZoneTranslationUpdate",
    "ShippingZoneTranslationResponse",
    "ShippingZoneListResponse",
    
    # 运费规则相关
    "ShippingRateCreate",
    "ShippingRateUpdate",
    "ShippingRateResponse",
    "ShippingRateListResponse",
] 