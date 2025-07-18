# -*- coding: utf-8 -*-
"""
运费规则子模块
包含运费规则相关的数据模型
"""

# Import models with try/except
try:
    from .models import ShippingRate
except ImportError:
    # Placeholder model if not available
    class ShippingRate:
        pass

# Import schemas with try/except
try:
    from .schema import (
        ShippingRateCreate, ShippingRateUpdate, ShippingRateResponse
    )
except ImportError:
    # Placeholder schemas
    class ShippingRateCreate:
        pass
    class ShippingRateUpdate:
        pass
    class ShippingRateResponse:
        pass

# Import service with try/except
try:
    from .service import ShippingRateService
except ImportError:
    # Placeholder service
    class ShippingRateService:
        pass

# Import API router with try/except
try:
    from .api import router as rate_router
except ImportError:
    # Placeholder router
    try:
        from fastapi import APIRouter
        rate_router = APIRouter()
    except ImportError:
        # If FastAPI is not available, create a mock router
        class MockRouter:
            def __init__(self):
                pass
        rate_router = MockRouter()

__all__ = [
    "ShippingRate",
    "ShippingRateCreate",
    "ShippingRateUpdate",
    "ShippingRateResponse",
    "ShippingRateService",
    "rate_router",
] 