# -*- coding: utf-8 -*-
"""
运费地区子模块
包含地区运费配置和翻译相关的数据模型
"""

# Import models with try/except
try:
    from .models import ShippingZone, ShippingZoneTranslation
except ImportError:
    # Placeholder models if not available
    class ShippingZone:
        pass
    class ShippingZoneTranslation:
        pass

# Import schemas with try/except
try:
    from .schema import (
        ShippingZoneCreate, ShippingZoneUpdate, ShippingZoneResponse,
        ShippingZoneTranslationCreate, ShippingZoneTranslationUpdate,
        ShippingZoneTranslationResponse
    )
except ImportError:
    # Placeholder schemas
    class ShippingZoneCreate:
        pass
    class ShippingZoneUpdate:
        pass
    class ShippingZoneResponse:
        pass
    class ShippingZoneTranslationCreate:
        pass
    class ShippingZoneTranslationUpdate:
        pass
    class ShippingZoneTranslationResponse:
        pass

# Import service with try/except
try:
    from .service import ShippingZoneService
except ImportError:
    # Placeholder service
    class ShippingZoneService:
        pass

# Import API router with try/except
try:
    from .api import router as zone_router
except ImportError:
    # Placeholder router
    try:
        from fastapi import APIRouter
        zone_router = APIRouter()
    except ImportError:
        # If FastAPI is not available, create a mock router
        class MockRouter:
            def __init__(self):
                pass
        zone_router = MockRouter()

__all__ = [
    "ShippingZone",
    "ShippingZoneTranslation", 
    "ShippingZoneCreate",
    "ShippingZoneUpdate",
    "ShippingZoneResponse",
    "ShippingZoneTranslationCreate",
    "ShippingZoneTranslationUpdate",
    "ShippingZoneTranslationResponse",
    "ShippingZoneService",
    "zone_router",
] 