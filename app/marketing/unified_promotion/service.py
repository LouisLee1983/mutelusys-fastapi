"""
统一促销服务
整合简化促销系统和传统优惠券系统
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.marketing.simple_promotion.service import PromotionService
from app.marketing.simple_promotion.schema import ApplyPromotionRequest, PromotionResult
from app.marketing.coupon.service import CouponService
from app.marketing.coupon.schema import CouponValidate


class UnifiedPromotionService:
    """统一促销服务，整合简化促销和传统优惠券"""
    
    def __init__(self, db: Session):
        self.db = db
        self.promotion_service = PromotionService(db)
        
    def apply_promotion_code(self, request: ApplyPromotionRequest) -> PromotionResult:
        """
        统一应用促销代码
        
        先尝试简化促销系统，如果找不到，再尝试传统优惠券系统
        """
        # 1. 先尝试简化促销系统
        try:
            result = self.promotion_service.apply_promotion(request)
            if result.success:
                return result
        except Exception:
            pass
        
        # 2. 如果简化促销系统找不到，尝试传统优惠券系统
        try:
            return self._apply_traditional_coupon(request)
        except Exception:
            pass
            
        # 3. 都找不到，返回失败
        return PromotionResult(
            success=False,
            message="促销代码不存在或已过期",
            discount_amount=0,
            original_total=self._calculate_cart_total(request.cart_items),
            final_total=self._calculate_cart_total(request.cart_items)
        )
    
    def _apply_traditional_coupon(self, request: ApplyPromotionRequest) -> PromotionResult:
        """应用传统优惠券"""
        cart_total = self._calculate_cart_total(request.cart_items)
        
        # 构建优惠券验证请求
        coupon_validate = CouponValidate(
            code=request.promotion_code,
            customer_id=request.customer_id,
            order_amount=cart_total
        )
        
        # 验证优惠券
        validation_result = CouponService.validate_coupon(self.db, coupon_validate)
        
        if validation_result["is_valid"]:
            discount_amount = validation_result.get("discount_amount", 0)
            
            return PromotionResult(
                success=True,
                message="优惠券应用成功",
                discount_amount=discount_amount,
                original_total=cart_total,
                final_total=max(0, cart_total - discount_amount),
                applied_promotion=None  # 可以添加优惠券信息
            )
        else:
            return PromotionResult(
                success=False,
                message=validation_result.get("message", "优惠券无效"),
                discount_amount=0,
                original_total=cart_total,
                final_total=cart_total
            )
    
    def _calculate_cart_total(self, cart_items: List[Dict[str, Any]]) -> float:
        """计算购物车总金额"""
        total = 0
        for item in cart_items:
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 1))
            total += price * quantity
        return total
    
    def get_all_available_promotions(self, cart_data: Dict[str, Any], customer_id: UUID = None) -> List[Dict[str, Any]]:
        """获取所有可用的促销活动（包括简化促销和传统优惠券）"""
        available_promotions = []
        
        # 1. 获取简化促销系统的可用促销
        try:
            simple_promotions = self.promotion_service.get_available_promotions_for_cart(
                cart_data, customer_id
            )
            for promo in simple_promotions:
                promo['source'] = 'simple_promotion'
                available_promotions.append(promo)
        except Exception:
            pass
        
        # 2. 获取传统优惠券系统的公开优惠券
        try:
            from app.marketing.coupon.schema import PaginationParams, CouponFilter
            from app.marketing.coupon.models import CouponStatus
            
            filters = CouponFilter(
                is_public=True,
                status=CouponStatus.ACTIVE
            )
            pagination = PaginationParams(page=1, page_size=10, sort_by="created_at")
            
            coupons, _ = CouponService.get_coupons(self.db, filters, pagination)
            
            for coupon in coupons:
                # 简化优惠券信息显示
                available_promotions.append({
                    'id': str(coupon.id),
                    'code': coupon.code,
                    'name': coupon.title or coupon.code,
                    'description': coupon.description or '',
                    'discount_amount': 0,  # 需要动态计算
                    'discount_type': coupon.discount_type.value if coupon.discount_type else 'unknown',
                    'discount_value': coupon.discount_value or 0,
                    'source': 'traditional_coupon'
                })
        except Exception:
            pass
            
        return available_promotions
    
    def validate_promotion_code(self, code: str, customer_id: UUID = None) -> Dict[str, Any]:
        """验证促销代码（统一接口）"""
        # 先检查简化促销系统
        simple_promotion = self.promotion_service.get_promotion_by_code(code)
        if simple_promotion and self.promotion_service.is_promotion_valid(simple_promotion):
            return {
                "valid": True,
                "message": "促销代码有效",
                "source": "simple_promotion",
                "promotion": {
                    "name": simple_promotion.name,
                    "description": simple_promotion.description,
                    "discount_type": simple_promotion.discount_type.value,
                    "discount_value": simple_promotion.discount_value
                }
            }
        
        # 再检查传统优惠券系统
        try:
            coupon = CouponService.get_coupon_by_code(self.db, code)
            if coupon and coupon.status.value == 'active':
                return {
                    "valid": True,
                    "message": "优惠券有效",
                    "source": "traditional_coupon",
                    "promotion": {
                        "name": coupon.title or coupon.code,
                        "description": coupon.description or '',
                        "discount_type": coupon.discount_type.value if coupon.discount_type else 'unknown',
                        "discount_value": coupon.discount_value or 0
                    }
                }
        except Exception:
            pass
            
        return {
            "valid": False,
            "message": "促销代码不存在或已过期",
            "source": None,
            "promotion": None
        }