from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel

from app.db.session import get_db
from app.marketing.unified_promotion.service import UnifiedPromotionService
from app.marketing.simple_promotion.schema import ApplyPromotionRequest, PromotionResult


router = APIRouter()


class UnifiedPromotionValidateRequest(BaseModel):
    promotion_code: str
    customer_id: Optional[UUID] = None


@router.post("/validate-code")
async def validate_promotion_code(
    request: UnifiedPromotionValidateRequest,
    db: Session = Depends(get_db)
):
    """统一验证促销代码（支持简化促销和传统优惠券）"""
    unified_service = UnifiedPromotionService(db)
    
    result = unified_service.validate_promotion_code(
        code=request.promotion_code,
        customer_id=request.customer_id
    )
    
    return result


@router.post("/apply-unified", response_model=PromotionResult)
async def apply_unified_promotion(
    request: ApplyPromotionRequest,
    db: Session = Depends(get_db)
):
    """统一应用促销（支持简化促销和传统优惠券）"""
    unified_service = UnifiedPromotionService(db)
    
    result = unified_service.apply_promotion_code(request)
    
    return result


class CartData(BaseModel):
    customer_id: Optional[UUID] = None
    items: List[Dict[str, Any]]
    total: float


@router.post("/all-available")
async def get_all_available_promotions(
    cart_data: CartData,
    db: Session = Depends(get_db)
):
    """获取所有可用的促销活动（包括简化促销和传统优惠券）"""
    unified_service = UnifiedPromotionService(db)
    
    cart_dict = {
        "customer_id": cart_data.customer_id,
        "items": cart_data.items,
        "total": cart_data.total
    }
    
    available_promotions = unified_service.get_all_available_promotions(
        cart_data=cart_dict,
        customer_id=cart_data.customer_id
    )
    
    return {
        "available_promotions": available_promotions,
        "count": len(available_promotions),
        "sources": list(set(p.get('source', 'unknown') for p in available_promotions))
    }