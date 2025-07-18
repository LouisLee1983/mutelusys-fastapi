from typing import List, Dict, Any, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from uuid import UUID

from app.marketing.simple_promotion.service import PromotionService
from app.marketing.simple_promotion.schema import ApplyPromotionRequest
from app.order.schema import OrderCreate, OrderItemCreate


class OrderPromotionIntegration:
    """订单促销集成服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.promotion_service = PromotionService(db)
    
    def apply_promotion_to_order(self, order_data: OrderCreate, promotion_code: str = None) -> OrderCreate:
        """
        在订单创建前应用促销
        
        Args:
            order_data: 订单数据
            promotion_code: 促销代码，如果为空则使用order_data中的coupon_code
            
        Returns:
            更新后的订单数据
        """
        # 使用传入的促销代码或订单中的优惠券代码
        code = promotion_code or order_data.coupon_code
        
        if not code:
            return order_data
        
        # 构建购物车数据
        cart_items = []
        for item in order_data.items:
            cart_items.append({
                "product_id": str(item.product_id),
                "sku_id": str(item.sku_id) if item.sku_id else None,
                "name": item.name,
                "price": float(item.unit_price),
                "quantity": item.quantity,
                "subtotal": float(item.subtotal)
            })
        
        # 应用促销
        promotion_request = ApplyPromotionRequest(
            promotion_code=code,
            customer_id=order_data.customer_id,
            cart_items=cart_items
        )
        
        promotion_result = self.promotion_service.apply_promotion(promotion_request)
        
        if promotion_result.success:
            # 更新订单折扣信息
            order_data.coupon_code = code
            order_data.discount_amount = Decimal(str(promotion_result.discount_amount))
            
            # 重新计算订单总金额
            order_data.total_amount = order_data.subtotal + order_data.shipping_amount + order_data.tax_amount - order_data.discount_amount
            
            # 分配折扣到订单项
            updated_items = self._distribute_discount_to_items(
                order_data.items, 
                promotion_result.discount_amount,
                promotion_result.applied_promotion
            )
            order_data.items = updated_items
            
            return order_data
        else:
            # 促销应用失败，抛出异常
            raise ValueError(promotion_result.message)
    
    def _distribute_discount_to_items(
        self, 
        items: List[OrderItemCreate], 
        total_discount: float,
        applied_promotion = None
    ) -> List[OrderItemCreate]:
        """
        将折扣分配到订单项
        
        Args:
            items: 订单项列表
            total_discount: 总折扣金额
            applied_promotion: 应用的促销信息
            
        Returns:
            更新后的订单项列表
        """
        if total_discount <= 0:
            return items
        
        # 计算每个商品应分配的折扣比例
        total_subtotal = sum(float(item.subtotal) for item in items)
        
        if total_subtotal <= 0:
            return items
        
        updated_items = []
        remaining_discount = total_discount
        
        for i, item in enumerate(items):
            if i == len(items) - 1:
                # 最后一个商品承担剩余的折扣（避免小数精度问题）
                item_discount = remaining_discount
            else:
                # 按比例分配折扣
                discount_ratio = float(item.subtotal) / total_subtotal
                item_discount = total_discount * discount_ratio
                remaining_discount -= item_discount
            
            # 更新订单项
            item.discount_amount = Decimal(str(item_discount))
            item.final_price = item.subtotal - item.discount_amount + item.tax_amount
            
            # 设置折扣相关信息
            if applied_promotion:
                item.discount_type = applied_promotion.discount_type.value if hasattr(applied_promotion, 'discount_type') else None
                item.coupon_code = applied_promotion.code if hasattr(applied_promotion, 'code') else None
            
            updated_items.append(item)
        
        return updated_items
    
    def validate_promotion_before_payment(self, order_id: UUID) -> Dict[str, Any]:
        """
        在支付前验证促销是否仍然有效
        
        Args:
            order_id: 订单ID
            
        Returns:
            验证结果
        """
        from app.order.models import Order
        
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order or not order.coupon_code:
            return {"valid": True, "message": "无促销代码"}
        
        # 重新验证促销代码
        promotion = self.promotion_service.get_promotion_by_code(order.coupon_code)
        
        if not promotion:
            return {"valid": False, "message": "促销代码已失效"}
        
        if not self.promotion_service.is_promotion_valid(promotion):
            return {"valid": False, "message": "促销已过期"}
        
        # 检查客户使用限制
        if order.customer_id:
            customer_usage = self.promotion_service.check_customer_usage(promotion.id, order.customer_id)
            if customer_usage >= promotion.per_customer_limit:
                return {"valid": False, "message": "已达到使用次数限制"}
        
        return {"valid": True, "message": "促销代码有效"}
    
    def record_promotion_usage_on_payment(self, order_id: UUID):
        """
        在订单支付成功后记录促销使用
        
        Args:
            order_id: 订单ID
        """
        from app.order.models import Order
        
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order or not order.coupon_code:
            return
        
        promotion = self.promotion_service.get_promotion_by_code(order.coupon_code)
        if promotion:
            self.promotion_service.record_promotion_usage(
                promotion_id=promotion.id,
                customer_id=order.customer_id,
                order_id=order_id
            )
    
    def calculate_real_time_promotion(self, cart_data: Dict[str, Any], promotion_code: str = None) -> Dict[str, Any]:
        """
        实时计算购物车的促销优惠（用于前端显示）
        
        Args:
            cart_data: 购物车数据
            promotion_code: 促销代码
            
        Returns:
            计算结果
        """
        if not promotion_code:
            return {
                "success": False,
                "message": "请输入促销代码",
                "discount_amount": 0,
                "original_total": cart_data.get("total", 0),
                "final_total": cart_data.get("total", 0)
            }
        
        # 构建促销请求
        promotion_request = ApplyPromotionRequest(
            promotion_code=promotion_code,
            customer_id=cart_data.get("customer_id"),
            cart_items=cart_data.get("items", [])
        )
        
        result = self.promotion_service.apply_promotion(promotion_request)
        
        return {
            "success": result.success,
            "message": result.message,
            "discount_amount": result.discount_amount,
            "original_total": result.original_total,
            "final_total": result.final_total,
            "promotion_name": result.applied_promotion.name if result.applied_promotion else None
        }
    
    def get_available_promotions_for_cart(self, cart_data: Dict[str, Any], customer_id: UUID = None) -> List[Dict[str, Any]]:
        """
        获取购物车可用的促销活动（自动促销）
        
        Args:
            cart_data: 购物车数据
            customer_id: 客户ID
            
        Returns:
            可用促销列表
        """
        from app.marketing.simple_promotion.models import SimplePromotion, SimplePromotionType
        
        # 获取所有激活的自动促销（无需优惠码的促销）
        auto_promotions = self.db.query(SimplePromotion).filter(
            SimplePromotion.is_active == True,
            SimplePromotion.type.in_([SimplePromotionType.DISCOUNT, SimplePromotionType.BUNDLE])
        ).all()
        
        available_promotions = []
        
        for promotion in auto_promotions:
            # 简单检查是否符合条件（这里可以扩展更复杂的逻辑）
            if self.promotion_service.is_promotion_valid(promotion):
                # 测试性地应用促销看是否有效
                test_request = ApplyPromotionRequest(
                    promotion_code=promotion.code,
                    customer_id=customer_id,
                    cart_items=cart_data.get("items", [])
                )
                
                test_result = self.promotion_service.apply_promotion(test_request)
                
                if test_result.success and test_result.discount_amount > 0:
                    available_promotions.append({
                        "id": str(promotion.id),
                        "code": promotion.code,
                        "name": promotion.name,
                        "description": promotion.description,
                        "discount_amount": test_result.discount_amount,
                        "discount_type": promotion.discount_type.value,
                        "discount_value": promotion.discount_value
                    })
        
        return available_promotions