# -*- coding: utf-8 -*-
"""
运费系统主数据模型
导入所有子模块的数据模型，确保SQLAlchemy能够正确识别所有模型关联关系
"""

# 导入所有模型 - 注意导入顺序，确保外键引用的模型先被导入
from .method.models import ShippingMethod, ShippingMethodTranslation, TransportType
from .zone.models import ShippingZone, ShippingZoneTranslation
from .rate.models import ShippingRate
from .free_rule.models import FreeShippingRule, FreeShippingRuleTranslation, FreeShippingRuleType
from .order_record.models import OrderChargeItem, OrderShippingInfo

# 导出所有模型
__all__ = [
    # 快递方式相关
    "ShippingMethod",
    "ShippingMethodTranslation", 
    "TransportType",
    
    # 运费地区相关
    "ShippingZone",
    "ShippingZoneTranslation",
    
    # 运费规则
    "ShippingRate",
    
    # 免运费规则相关
    "FreeShippingRule",
    "FreeShippingRuleTranslation",
    "FreeShippingRuleType",
    
    # 订单运费记录相关
    "OrderChargeItem",
    "OrderShippingInfo"
] 