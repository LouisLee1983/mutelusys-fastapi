from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel

from app.db.session import get_db
from app.order.promotion_integration import OrderPromotionIntegration


router = APIRouter()


class CartItem(BaseModel):
    product_id: UUID
    sku_id: Optional[UUID] = None
    name: str
    price: float
    quantity: int
    subtotal: float


class CartData(BaseModel):
    customer_id: Optional[UUID] = None
    items: List[CartItem]
    total: float


class ApplyPromotionToCartRequest(BaseModel):
    cart_data: CartData
    promotion_code: str


class ValidatePromotionRequest(BaseModel):
    order_id: UUID


@router.post("/cart/apply-promotion")
async def apply_promotion_to_cart(
    request: ApplyPromotionToCartRequest,
    db: Session = Depends(get_db)
):
    """应用促销到购物车（实时计算）"""
    promotion_integration = OrderPromotionIntegration(db)
    
    # 转换购物车数据格式
    cart_dict = {
        "customer_id": request.cart_data.customer_id,
        "items": [
            {
                "product_id": str(item.product_id),
                "sku_id": str(item.sku_id) if item.sku_id else None,
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
                "subtotal": item.subtotal
            }
            for item in request.cart_data.items
        ],
        "total": request.cart_data.total
    }
    
    result = promotion_integration.calculate_real_time_promotion(
        cart_data=cart_dict,
        promotion_code=request.promotion_code
    )
    
    return result


@router.post("/cart/available-promotions")
async def get_available_promotions(
    cart_data: CartData,
    db: Session = Depends(get_db)
):
    """获取购物车可用的自动促销"""
    promotion_integration = OrderPromotionIntegration(db)
    
    # 转换购物车数据格式
    cart_dict = {
        "customer_id": cart_data.customer_id,
        "items": [
            {
                "product_id": str(item.product_id),
                "sku_id": str(item.sku_id) if item.sku_id else None,
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
                "subtotal": item.subtotal
            }
            for item in cart_data.items
        ],
        "total": cart_data.total
    }
    
    available_promotions = promotion_integration.get_available_promotions_for_cart(
        cart_data=cart_dict,
        customer_id=cart_data.customer_id
    )
    
    return {
        "available_promotions": available_promotions,
        "count": len(available_promotions)
    }


@router.post("/validate-promotion")
async def validate_promotion_before_payment(
    request: ValidatePromotionRequest,
    db: Session = Depends(get_db)
):
    """支付前验证促销是否有效"""
    promotion_integration = OrderPromotionIntegration(db)
    
    result = promotion_integration.validate_promotion_before_payment(request.order_id)
    
    if not result["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result


@router.get("/promotion-templates")
async def get_promotion_templates():
    """获取促销模板（用于管理后台快速创建）"""
    from app.marketing.simple_promotion.schema import PROMOTION_TEMPLATES
    return {"templates": PROMOTION_TEMPLATES}


@router.post("/estimate-savings")
async def estimate_potential_savings(
    cart_data: CartData,
    db: Session = Depends(get_db)
):
    """估算购物车潜在节省金额"""
    promotion_integration = OrderPromotionIntegration(db)
    
    # 转换购物车数据格式
    cart_dict = {
        "customer_id": cart_data.customer_id,
        "items": [
            {
                "product_id": str(item.product_id),
                "sku_id": str(item.sku_id) if item.sku_id else None,
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
                "subtotal": item.subtotal
            }
            for item in cart_data.items
        ],
        "total": cart_data.total
    }
    
    # 获取所有可用促销
    available_promotions = promotion_integration.get_available_promotions_for_cart(
        cart_data=cart_dict,
        customer_id=cart_data.customer_id
    )
    
    # 计算最大节省金额
    max_savings = 0
    best_promotion = None
    
    for promotion in available_promotions:
        if promotion["discount_amount"] > max_savings:
            max_savings = promotion["discount_amount"]
            best_promotion = promotion
    
    return {
        "original_total": cart_data.total,
        "max_savings": max_savings,
        "final_total": cart_data.total - max_savings,
        "best_promotion": best_promotion,
        "savings_percentage": (max_savings / cart_data.total * 100) if cart_data.total > 0 else 0
    }