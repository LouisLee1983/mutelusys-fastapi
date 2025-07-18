# -*- coding: utf-8 -*-
"""
运费计算子模块
提供完整的运费计算引擎和相关服务
"""

# Import schemas with try/except
try:
    from .schema import (
        ShippingCalculationRequest, ShippingCalculationResponse,
        ShippingMethodOption, ShippingEstimate, ShippingBreakdown
    )
except ImportError:
    # Placeholder schemas
    class ShippingCalculationRequest:
        pass
    class ShippingCalculationResponse:
        pass
    class ShippingMethodOption:
        pass
    class ShippingEstimate:
        pass
    class ShippingBreakdown:
        pass

# Import service with try/except
try:
    from .service import ShippingCalculationService
except ImportError:
    # Placeholder service
    class ShippingCalculationService:
        pass

__all__ = [
    "ShippingCalculationRequest",
    "ShippingCalculationResponse",
    "ShippingMethodOption",
    "ShippingEstimate",
    "ShippingBreakdown",
    "ShippingCalculationService",
] 