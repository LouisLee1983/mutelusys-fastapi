# -*- coding: utf-8 -*-
"""
运费计算API路由
提供运费计算和预估服务
"""
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db

from .service import ShippingCalculationService
from .schema import (
    ShippingCalculationRequest, ShippingCalculationResponse,
    BatchShippingCalculationRequest, BatchShippingCalculationResponse,
    ShippingQuoteParams
)

router = APIRouter(prefix="/calculation")

# ==================== 公开接口 ====================

@router.post("/calculate", response_model=ShippingCalculationResponse)
async def calculate_shipping(
    request: ShippingCalculationRequest,
    db: Session = Depends(get_db)
):
    """
    计算运费
    
    根据收货地址、商品信息和用户信息计算所有可用快递方式的运费
    """
    service = ShippingCalculationService(db)
    return service.calculate_shipping(request)


@router.post("/calculate/batch", response_model=BatchShippingCalculationResponse)
async def calculate_batch_shipping(
    request: BatchShippingCalculationRequest,
    db: Session = Depends(get_db)
):
    """
    批量计算运费
    
    支持一次性计算多个运费请求，适用于购物车批量估算等场景
    """
    service = ShippingCalculationService(db)
    return service.calculate_batch_shipping(request)


@router.get("/quote")
async def get_shipping_quote(
    country_code: str = Query(..., description="国家代码"),
    quantity: int = Query(1, ge=1, description="商品件数"),
    amount: Optional[Decimal] = Query(None, description="商品金额"),
    method_code: Optional[str] = Query(None, description="指定快递方式代码"),
    db: Session = Depends(get_db)
):
    """
    快速获取运费报价
    
    简化的运费查询接口，用于快速预估运费
    """
    service = ShippingCalculationService(db)
    quote = service.get_quick_quote(country_code, quantity, method_code)
    
    if quote is None:
        raise HTTPException(status_code=404, detail="无法获取运费报价")
    
    return {
        "country_code": country_code,
        "quantity": quantity,
        "method_code": method_code,
        "shipping_cost": quote,
        "currency": "USD"
    }


@router.get("/estimate/{country_code}")
async def estimate_shipping_cost(
    country_code: str,
    quantity: int = Query(1, ge=1, description="商品件数"),
    amount: Decimal = Query(Decimal("0"), ge=0, description="商品金额"),
    language: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """
    运费预估
    
    为指定国家快速预估运费，返回最便宜和最推荐的选项
    """
    request = ShippingCalculationRequest(
        country_code=country_code,
        total_quantity=quantity,
        total_amount=amount,
        currency_code="USD",
        language_code=language
    )
    
    service = ShippingCalculationService(db)
    result = service.calculate_shipping(request)
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return {
        "country_code": country_code,
        "total_estimates": result.total_estimates,
        "recommended": result.recommended_method,
        "cheapest": result.cheapest_method,
        "zone_name": result.zone_name
    }


# ==================== 支持的国家和地区查询 ====================

@router.get("/supported-countries")
async def get_supported_countries(
    db: Session = Depends(get_db)
):
    """
    获取支持配送的国家列表
    
    返回所有配置了运费规则的国家代码
    """
    from ..zone.models import ShippingZone
    
    # 查询所有启用的运费地区
    zones = db.query(ShippingZone).filter(ShippingZone.is_active == True).all()
    
    # 提取所有国家代码
    countries = set()
    for zone in zones:
        if zone.country_codes:
            countries.update(zone.country_codes)
    
    return {
        "supported_countries": sorted(list(countries)),
        "total_countries": len(countries),
        "zones_count": len(zones)
    }


@router.get("/zones/{country_code}")
async def get_shipping_zone_info(
    country_code: str,
    language: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """
    获取指定国家的运费地区信息
    
    返回国家所属的运费地区详情
    """
    service = ShippingCalculationService(db)
    zone = service._find_shipping_zone(country_code)
    
    if not zone:
        raise HTTPException(status_code=404, detail=f"国家 '{country_code}' 不支持配送")
    
    return {
        "zone_id": str(zone.id),
        "zone_name": zone.name,
        "country_code": country_code,
        "covered_countries": zone.country_codes,
        "is_active": zone.is_active
    } 