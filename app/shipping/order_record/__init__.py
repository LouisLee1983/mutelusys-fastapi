# -*- coding: utf-8 -*-
"""
订单运费记录子模块
包含订单收费项目和运费记录相关功能
"""

# Import models with try/except
try:
    from .models import OrderChargeItem, OrderShippingInfo
except ImportError:
    # Placeholder models if not available
    class OrderChargeItem:
        pass
    class OrderShippingInfo:
        pass

# Import schemas with try/except
try:
    from .schema import (
        OrderChargeItemCreate, OrderChargeItemUpdate, OrderChargeItemResponse,
        OrderShippingInfoCreate, OrderShippingInfoUpdate, OrderShippingInfoResponse
    )
except ImportError:
    # Placeholder schemas
    class OrderChargeItemCreate:
        pass
    class OrderChargeItemUpdate:
        pass
    class OrderChargeItemResponse:
        pass
    class OrderShippingInfoCreate:
        pass
    class OrderShippingInfoUpdate:
        pass
    class OrderShippingInfoResponse:
        pass

# Import service with try/except
try:
    from .service import OrderRecordService
except ImportError:
    # Placeholder service
    class OrderRecordService:
        pass

__all__ = [
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