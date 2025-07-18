# -*- coding: utf-8 -*-
"""
快递方式子模块
管理快递方式及其翻译
"""

# Import models, schemas, services, and API routers
try:
    from .models import ShippingMethod, ShippingMethodTranslation
except ImportError:
    # Placeholder models if not available
    class ShippingMethod:
        pass
    class ShippingMethodTranslation:
        pass

try:
    from .schema import (
        ShippingMethodCreate, ShippingMethodUpdate, ShippingMethodResponse
    )
except ImportError:
    # Placeholder schemas
    class ShippingMethodCreate:
        pass
    class ShippingMethodUpdate:
        pass
    class ShippingMethodResponse:
        pass

try:
    from .service import ShippingMethodService
except ImportError:
    # Placeholder service
    class ShippingMethodService:
        pass

try:
    from .api import router as method_router
except ImportError:
    # Placeholder router
    try:
        from fastapi import APIRouter
        method_router = APIRouter()
    except ImportError:
        # If FastAPI is not available, create a mock router
        class MockRouter:
            def __init__(self):
                pass
        method_router = MockRouter()

__all__ = [
    "ShippingMethod",
    "ShippingMethodTranslation", 
    "ShippingMethodCreate",
    "ShippingMethodUpdate",
    "ShippingMethodResponse",
    "ShippingMethodService",
    "method_router"
] 