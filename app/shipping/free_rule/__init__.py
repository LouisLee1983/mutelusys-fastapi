# -*- coding: utf-8 -*-
"""
免运费规则子模块
包含免运费规则和翻译相关的数据模型
"""

# Import models with try/except
try:
    from .models import FreeShippingRule, FreeShippingRuleTranslation
except ImportError:
    # Placeholder models if not available
    class FreeShippingRule:
        pass
    class FreeShippingRuleTranslation:
        pass

# Import schemas with try/except
try:
    from .schema import (
        FreeShippingRuleCreate, FreeShippingRuleUpdate, FreeShippingRuleResponse,
        FreeShippingRuleTranslationCreate, FreeShippingRuleTranslationUpdate,
        FreeShippingRuleTranslationResponse, ApplyFreeShippingRequest, FreeShippingCheckResult
    )
except ImportError:
    # Placeholder schemas
    class FreeShippingRuleCreate:
        pass
    class FreeShippingRuleUpdate:
        pass
    class FreeShippingRuleResponse:
        pass
    class FreeShippingRuleTranslationCreate:
        pass
    class FreeShippingRuleTranslationUpdate:
        pass
    class FreeShippingRuleTranslationResponse:
        pass
    class ApplyFreeShippingRequest:
        pass
    class FreeShippingCheckResult:
        pass

# Import service with try/except
try:
    from .service import FreeShippingRuleService
except ImportError:
    # Placeholder service
    class FreeShippingRuleService:
        pass

# Import API router with try/except
try:
    from .api import router as free_rule_router
except ImportError:
    # Placeholder router
    try:
        from fastapi import APIRouter
        free_rule_router = APIRouter()
    except ImportError:
        # If FastAPI is not available, create a mock router
        class MockRouter:
            def __init__(self):
                pass
        free_rule_router = MockRouter()

__all__ = [
    "FreeShippingRule",
    "FreeShippingRuleTranslation",
    "FreeShippingRuleCreate",
    "FreeShippingRuleUpdate",
    "FreeShippingRuleResponse",
    "FreeShippingRuleTranslationCreate",
    "FreeShippingRuleTranslationUpdate", 
    "FreeShippingRuleTranslationResponse",
    "ApplyFreeShippingRequest",
    "FreeShippingCheckResult",
    "FreeShippingRuleService",
    "free_rule_router",
] 