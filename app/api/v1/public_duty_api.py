from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.duty.service import DutyCalculationService
from app.duty.schema import (
    DutyCalculationRequest, DutyCalculationResult,
    SupportedCountriesResponse, SupportedCountry
)

router = APIRouter(prefix="/duty")


@router.post("/calculate", response_model=DutyCalculationResult, summary="计算关税 (公开API)")
def calculate_duty_public(
    request: DutyCalculationRequest,
    db: Session = Depends(get_db)
):
    """
    公开的关税计算API - 供前端购物车和结账页面使用
    
    计算基于以下逻辑：
    1. 根据国家代码查找关税区域
    2. 计算应税金额 = 商品总价 + 运费
    3. 检查是否超过免税阈值
    4. 应用适用的税率规则
    5. 返回最终关税金额
    """
    try:
        service = DutyCalculationService(db)
        return service.calculate_duty(request)
    except Exception as e:
        # 记录错误但不暴露内部细节
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to calculate duty: {str(e)}"
        )


@router.get("/supported-countries", response_model=SupportedCountriesResponse, summary="获取支持关税计算的国家")
def get_supported_countries_public(
    db: Session = Depends(get_db)
):
    """
    获取支持关税计算的国家列表 (公开API)
    
    返回包含以下信息的国家列表：
    - 国家基本信息 (代码、名称)
    - 关税区域信息
    - 免税阈值
    - 默认税率
    """
    try:
        service = DutyCalculationService(db)
        countries_data = service.get_supported_countries()
        
        countries = [
            SupportedCountry(**country_data)
            for country_data in countries_data
        ]
        
        return SupportedCountriesResponse(
            countries=countries,
            total=len(countries)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Failed to fetch supported countries"
        )


@router.get("/quick-quote/{country_code}", response_model=dict, summary="快速关税报价")
def get_quick_duty_quote(
    country_code: str,
    amount: float,
    currency: str = "USD",
    db: Session = Depends(get_db)
):
    """
    快速关税报价 - 基于单一金额快速估算关税
    
    Args:
        country_code: 国家代码
        amount: 商品总金额
        currency: 货币代码
    
    Returns:
        快速报价结果，包含预估关税金额和相关提示
    """
    try:
        service = DutyCalculationService(db)
        
        # 创建简化的计算请求
        request = DutyCalculationRequest(
            country_code=country_code,
            items=[{
                "product_id": "quick-quote",
                "quantity": 1,
                "price": amount
            }],
            shipping_cost=0.0,
            currency=currency
        )
        
        result = service.calculate_duty(request)
        
        # 返回简化的响应
        return {
            "country_code": country_code,
            "amount": amount,
            "currency": currency,
            "duty_amount": result.duty_amount,
            "tax_rate": result.tax_rate,
            "is_tax_free": result.is_tax_free,
            "duty_zone": result.duty_zone_name,
            "tips": {
                "tax_free_threshold": result.calculation_details.get("tax_free_threshold", 0),
                "is_estimate": True,
                "disclaimer": "实际关税可能因海关政策变化而有差异"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to get duty quote: {str(e)}"
        )


@router.get("/policy/{country_code}", response_model=dict, summary="获取国家关税政策信息")
def get_country_duty_policy(
    country_code: str,
    db: Session = Depends(get_db)
):
    """
    获取特定国家的关税政策信息
    
    Args:
        country_code: 国家代码
    
    Returns:
        关税政策信息，包含免税阈值、税率等
    """
    try:
        service = DutyCalculationService(db)
        
        # 查找关税区域
        duty_zone = service._find_duty_zone_by_country(country_code)
        
        if not duty_zone:
            return {
                "country_code": country_code,
                "has_duty": False,
                "message": "该国家暂不收取关税或不在我们的关税计算范围内",
                "policy": {
                    "tax_free_threshold": 0,
                    "default_tax_rate": 0,
                    "currency": "USD"
                }
            }
        
        return {
            "country_code": country_code,
            "has_duty": True,
            "duty_zone": duty_zone.name,
            "policy": {
                "tax_free_threshold": duty_zone.tax_free_threshold,
                "default_tax_rate": duty_zone.default_tax_rate,
                "currency": duty_zone.currency,
                "description": f"低于 {duty_zone.currency} {duty_zone.tax_free_threshold} 免税"
            },
            "tips": [
                "关税由买家承担，将在结账时收取",
                "小包裹通常享有免税优惠",
                "实际关税可能因海关政策调整而变化",
                "我们会在订单中详细记录关税计算过程"
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to get duty policy: {str(e)}"
        )


@router.get("/estimate-savings/{country_code}", response_model=dict, summary="估算免税节省金额")
def estimate_tax_free_savings(
    country_code: str,
    current_amount: float,
    currency: str = "USD",
    db: Session = Depends(get_db)
):
    """
    估算达到免税阈值可以节省的关税金额
    
    Args:
        country_code: 国家代码
        current_amount: 当前购物车金额
        currency: 货币代码
    
    Returns:
        免税节省估算信息
    """
    try:
        service = DutyCalculationService(db)
        duty_zone = service._find_duty_zone_by_country(country_code)
        
        if not duty_zone:
            return {
                "country_code": country_code,
                "has_savings": False,
                "message": "该国家不收取关税"
            }
        
        # 如果已经免税
        if current_amount <= duty_zone.tax_free_threshold:
            remaining_free = duty_zone.tax_free_threshold - current_amount
            return {
                "country_code": country_code,
                "current_amount": current_amount,
                "is_tax_free": True,
                "remaining_free_amount": remaining_free,
                "currency": duty_zone.currency,
                "message": f"当前订单免税！还可以再购买 {duty_zone.currency} {remaining_free:.2f} 仍享受免税"
            }
        
        # 计算当前需要的关税
        current_duty = (current_amount - duty_zone.tax_free_threshold) * duty_zone.default_tax_rate
        
        # 计算免税阈值的关税节省
        threshold_duty = duty_zone.tax_free_threshold * duty_zone.default_tax_rate
        
        return {
            "country_code": country_code,
            "current_amount": current_amount,
            "is_tax_free": False,
            "tax_free_threshold": duty_zone.tax_free_threshold,
            "current_duty": round(current_duty, 2),
            "potential_savings": round(threshold_duty, 2),
            "currency": duty_zone.currency,
            "recommendation": f"如果订单金额控制在 {duty_zone.currency} {duty_zone.tax_free_threshold} 以下，可节省关税约 {duty_zone.currency} {threshold_duty:.2f}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to estimate savings: {str(e)}"
        )