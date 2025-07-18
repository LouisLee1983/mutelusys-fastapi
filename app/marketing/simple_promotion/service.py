from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from uuid import UUID

from .models import SimplePromotion, CustomerPromotionUsage, SimplePromotionType, DiscountType
from .schema import PromotionResult, ApplyPromotionRequest


class PromotionService:
    """简化的促销计算服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_promotion_by_code(self, code: str) -> Optional[SimplePromotion]:
        """根据促销代码获取促销"""
        return self.db.query(SimplePromotion).filter(
            SimplePromotion.code == code,
            SimplePromotion.is_active == True
        ).first()
    
    def is_promotion_valid(self, promotion: SimplePromotion) -> bool:
        """检查促销是否有效"""
        now = datetime.utcnow()
        
        # 检查时间范围
        if promotion.start_date > now:
            return False
        
        if promotion.end_date and promotion.end_date < now:
            return False
        
        # 检查使用次数
        if promotion.usage_limit and promotion.usage_count >= promotion.usage_limit:
            return False
        
        return True
    
    def check_customer_usage(self, promotion_id: UUID, customer_id: UUID) -> int:
        """检查客户使用次数"""
        if not customer_id:
            return 0
            
        usage = self.db.query(CustomerPromotionUsage).filter(
            CustomerPromotionUsage.promotion_id == promotion_id,
            CustomerPromotionUsage.customer_id == customer_id
        ).first()
        
        return usage.usage_count if usage else 0
    
    def calculate_cart_total(self, cart_items: List[Dict[str, Any]]) -> float:
        """计算购物车总金额"""
        total = 0
        for item in cart_items:
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 1))
            total += price * quantity
        return total
    
    def apply_discount_promotion(self, promotion: SimplePromotion, cart_items: List[Dict[str, Any]]) -> float:
        """应用折扣促销"""
        rules = promotion.rules or {}
        cart_total = self.calculate_cart_total(cart_items)
        
        # 检查最低消费
        min_amount = rules.get('min_amount')
        if min_amount and cart_total < min_amount:
            return 0
        
        # 检查商品限制
        applicable_products = rules.get('applicable_products')
        excluded_products = rules.get('excluded_products')
        
        if applicable_products or excluded_products:
            # 只对符合条件的商品计算折扣
            eligible_total = 0
            for item in cart_items:
                product_id = item.get('product_id')
                if applicable_products and str(product_id) not in applicable_products:
                    continue
                if excluded_products and str(product_id) in excluded_products:
                    continue
                
                price = float(item.get('price', 0))
                quantity = int(item.get('quantity', 1))
                eligible_total += price * quantity
            
            cart_total = eligible_total
        
        # 计算折扣
        if promotion.discount_type == DiscountType.PERCENTAGE:
            discount = cart_total * (promotion.discount_value / 100)
        else:  # FIXED_AMOUNT
            discount = promotion.discount_value
        
        # 检查最大折扣限制
        max_discount = rules.get('max_discount')
        if max_discount and discount > max_discount:
            discount = max_discount
        
        return min(discount, cart_total)  # 折扣不能超过总金额
    
    def apply_bundle_promotion(self, promotion: SimplePromotion, cart_items: List[Dict[str, Any]]) -> float:
        """应用打包促销"""
        rules = promotion.rules or {}
        required_products = rules.get('product_ids', [])
        
        if not required_products:
            return 0
        
        # 检查购物车是否包含所有必需商品
        cart_product_ids = [str(item.get('product_id')) for item in cart_items]
        
        if not all(str(pid) in cart_product_ids for pid in required_products):
            return 0
        
        # 计算套装内商品的原价
        bundle_original_price = 0
        for item in cart_items:
            if str(item.get('product_id')) in required_products:
                price = float(item.get('price', 0))
                quantity = int(item.get('quantity', 1))
                bundle_original_price += price * quantity
        
        # 计算折扣
        if promotion.discount_type == DiscountType.PERCENTAGE:
            discount = bundle_original_price * (promotion.discount_value / 100)
        elif promotion.discount_type == DiscountType.FIXED_AMOUNT:
            discount = promotion.discount_value
        else:
            # 套装固定价格
            bundle_price = rules.get('bundle_price', 0)
            discount = bundle_original_price - bundle_price
        
        return max(0, discount)
    
    def apply_promotion(self, request: ApplyPromotionRequest) -> PromotionResult:
        """应用促销"""
        # 获取促销
        promotion = self.get_promotion_by_code(request.promotion_code)
        if not promotion:
            return PromotionResult(
                success=False,
                message="促销代码不存在",
                discount_amount=0,
                original_total=self.calculate_cart_total(request.cart_items),
                final_total=self.calculate_cart_total(request.cart_items)
            )
        
        # 检查促销是否有效
        if not self.is_promotion_valid(promotion):
            return PromotionResult(
                success=False,
                message="促销已过期或无效",
                discount_amount=0,
                original_total=self.calculate_cart_total(request.cart_items),
                final_total=self.calculate_cart_total(request.cart_items)
            )
        
        # 检查客户使用限制
        if request.customer_id:
            customer_usage = self.check_customer_usage(promotion.id, request.customer_id)
            if customer_usage >= promotion.per_customer_limit:
                return PromotionResult(
                    success=False,
                    message="您已达到此促销的使用次数限制",
                    discount_amount=0,
                    original_total=self.calculate_cart_total(request.cart_items),
                    final_total=self.calculate_cart_total(request.cart_items)
                )
        
        # 计算折扣
        original_total = self.calculate_cart_total(request.cart_items)
        discount_amount = 0
        
        if promotion.type == SimplePromotionType.DISCOUNT:
            discount_amount = self.apply_discount_promotion(promotion, request.cart_items)
        elif promotion.type == SimplePromotionType.BUNDLE:
            discount_amount = self.apply_bundle_promotion(promotion, request.cart_items)
        elif promotion.type == SimplePromotionType.COUPON:
            # 优惠券按照折扣逻辑处理
            discount_amount = self.apply_discount_promotion(promotion, request.cart_items)
        
        final_total = max(0, original_total - discount_amount)
        
        if discount_amount > 0:
            return PromotionResult(
                success=True,
                message="促销应用成功",
                discount_amount=discount_amount,
                original_total=original_total,
                final_total=final_total,
                applied_promotion=None  # 这里可以转换为response schema
            )
        else:
            return PromotionResult(
                success=False,
                message="您的购物车不符合此促销条件",
                discount_amount=0,
                original_total=original_total,
                final_total=original_total
            )
    
    def record_promotion_usage(self, promotion_id: UUID, customer_id: UUID, order_id: UUID = None):
        """记录促销使用"""
        # 更新促销使用次数
        promotion = self.db.query(SimplePromotion).filter(SimplePromotion.id == promotion_id).first()
        if promotion:
            promotion.usage_count += 1
        
        # 记录客户使用
        if customer_id:
            existing_usage = self.db.query(CustomerPromotionUsage).filter(
                CustomerPromotionUsage.promotion_id == promotion_id,
                CustomerPromotionUsage.customer_id == customer_id
            ).first()
            
            if existing_usage:
                existing_usage.usage_count += 1
            else:
                new_usage = CustomerPromotionUsage(
                    customer_id=customer_id,
                    promotion_id=promotion_id,
                    order_id=order_id,
                    usage_count=1
                )
                self.db.add(new_usage)
        
        self.db.commit()


class PromotionTemplateService:
    """促销模板服务"""
    
    @staticmethod
    def create_from_template(template_name: str, code: str, start_date: datetime, end_date: datetime = None) -> dict:
        """从模板创建促销"""
        from .schema import PROMOTION_TEMPLATES
        
        template = next((t for t in PROMOTION_TEMPLATES if t.name == template_name), None)
        if not template:
            raise ValueError(f"模板 {template_name} 不存在")
        
        return {
            "code": code,
            "name": template.name,
            "description": template.description,
            "type": template.type,
            "discount_type": template.discount_type,
            "discount_value": template.discount_value,
            "rules": template.rules,
            "start_date": start_date,
            "end_date": end_date,
            "is_active": True
        }