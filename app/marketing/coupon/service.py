import uuid
import random
import string
import math
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_, and_, func

from app.marketing.coupon.models import Coupon, CouponBatch, CouponStatus, CouponFormat
from app.marketing.customer_coupon.models import CustomerCoupon, CustomerCouponStatus, IssueMethod
from app.marketing.promotion.models import Promotion, PromotionType, DiscountType
from app.marketing.coupon.schema import (
    CouponCreate, CouponUpdate, CouponValidate, 
    CouponBatchCreate, CouponIssue, CouponFilter,
    PaginationParams
)


class CouponService:
    @staticmethod
    def generate_coupon_code(prefix: Optional[str] = None, suffix: Optional[str] = None, 
                            length: int = 8, format: CouponFormat = CouponFormat.ALPHANUMERIC) -> str:
        """生成优惠券码"""
        if length < 4:
            length = 4  # 确保最小长度
        
        # 根据格式生成字符
        if format == CouponFormat.NUMERIC:
            chars = string.digits
        elif format == CouponFormat.ALPHABETIC:
            chars = string.ascii_uppercase
        else:  # ALPHANUMERIC 或其他
            chars = string.ascii_uppercase + string.digits
        
        # 移除容易混淆的字符
        if format != CouponFormat.NUMERIC:
            for c in "O0I1":
                chars = chars.replace(c, "")
        
        # 生成随机字符串
        code = ''.join(random.choice(chars) for _ in range(length))
        
        # 添加前后缀
        if prefix:
            code = f"{prefix}{code}"
        if suffix:
            code = f"{code}{suffix}"
            
        return code

    @staticmethod
    def create_promotion(db: Session, promotion_data: Dict[str, Any]) -> Promotion:
        """创建促销记录"""
        promotion = Promotion(
            id=uuid.uuid4(),
            name=promotion_data.get("name"),
            description=promotion_data.get("description"),
            type=promotion_data.get("type", PromotionType.COUPON),
            is_active=promotion_data.get("is_active", True),
            
            # 时间设置
            start_date=promotion_data.get("start_date"),
            end_date=promotion_data.get("end_date"),
            active_days=promotion_data.get("active_days"),
            active_hours_start=promotion_data.get("active_hours_start"),
            active_hours_end=promotion_data.get("active_hours_end"),
            
            # 促销规则
            discount_type=promotion_data.get("discount_type"),
            discount_value=promotion_data.get("discount_value"),
            min_order_amount=promotion_data.get("min_order_amount"),
            max_discount_amount=promotion_data.get("max_discount_amount"),
            usage_limit=promotion_data.get("usage_limit"),
            
            # 地区和货币设置
            applicable_countries=promotion_data.get("applicable_countries"),
            excluded_countries=promotion_data.get("excluded_countries"),
            applicable_currencies=promotion_data.get("applicable_currencies"),
            
            # 客户限制
            customer_eligibility=promotion_data.get("customer_eligibility", "all"),
            eligible_customer_groups=promotion_data.get("eligible_customer_groups"),
            min_customer_orders=promotion_data.get("min_customer_orders"),
            
            # 产品限制
            applicable_products=promotion_data.get("applicable_products"),
            excluded_products=promotion_data.get("excluded_products"),
            applicable_categories=promotion_data.get("applicable_categories"),
            excluded_categories=promotion_data.get("excluded_categories"),
            
            # 组合规则
            combination_strategy=promotion_data.get("combination_strategy", "stack"),
            priority=promotion_data.get("priority", 0),
            
            # 显示设置
            image_url=promotion_data.get("image_url"),
            banner_url=promotion_data.get("banner_url"),
            highlight_color=promotion_data.get("highlight_color"),
            is_featured=promotion_data.get("is_featured", False),
            
            # 文化和主题关联
            cultural_theme=promotion_data.get("cultural_theme"),
            intention_type=promotion_data.get("intention_type"),
            
            # 额外设置
            meta_data=promotion_data.get("meta_data")
        )
        
        db.add(promotion)
        db.flush()
        return promotion

    @staticmethod
    def create_coupon(db: Session, coupon_data: CouponCreate) -> Coupon:
        """创建单个优惠券"""
        # 1. 创建促销
        promotion_dict = coupon_data.promotion.dict()
        promotion = CouponService.create_promotion(db, promotion_dict)
        
        # 2. 生成或验证优惠券码
        coupon_dict = coupon_data.coupon.dict()
        if not coupon_dict.get("code"):
            # 生成唯一的优惠券码
            while True:
                code = CouponService.generate_coupon_code(
                    prefix=coupon_dict.get("prefix"),
                    suffix=coupon_dict.get("suffix"),
                    length=coupon_dict.get("length", 8),
                    format=coupon_dict.get("format", CouponFormat.ALPHANUMERIC)
                )
                # 检查优惠券码是否已存在
                existing = db.query(Coupon).filter(Coupon.code == code).first()
                if not existing:
                    break
        else:
            # 检查提供的优惠券码是否已存在
            code = coupon_dict.get("code")
            existing = db.query(Coupon).filter(Coupon.code == code).first()
            if existing:
                raise ValueError(f"优惠券码 {code} 已存在")
        
        # 3. 设置有效期（如果未指定，则用促销的有效期）
        if not coupon_dict.get("valid_from"):
            coupon_dict["valid_from"] = promotion.start_date
        if not coupon_dict.get("valid_to") and promotion.end_date:
            coupon_dict["valid_to"] = promotion.end_date
        
        # 4. 创建优惠券
        coupon = Coupon(
            id=uuid.uuid4(),
            promotion_id=promotion.id,
            code=code,
            status=coupon_dict.get("status", CouponStatus.ACTIVE),
            
            # 生成设置
            format=coupon_dict.get("format", CouponFormat.ALPHANUMERIC),
            prefix=coupon_dict.get("prefix"),
            suffix=coupon_dict.get("suffix"),
            length=coupon_dict.get("length", 8),
            
            # 使用限制
            max_uses=coupon_dict.get("max_uses"),
            max_uses_per_customer=coupon_dict.get("max_uses_per_customer", 1),
            current_uses=0,
            is_single_use=coupon_dict.get("is_single_use", True),
            requires_authentication=coupon_dict.get("requires_authentication", True),
            
            # 使用控制
            valid_from=coupon_dict.get("valid_from"),
            valid_to=coupon_dict.get("valid_to"),
            
            # 分销规则
            is_referral=coupon_dict.get("is_referral", False),
            referrer_reward=coupon_dict.get("referrer_reward"),
            
            # 邮件和分享设置
            is_public=coupon_dict.get("is_public", False),
            is_featured=coupon_dict.get("is_featured", False),
            auto_apply=coupon_dict.get("auto_apply", False),
            
            # 赠品配置
            free_product_id=coupon_dict.get("free_product_id"),
            free_product_quantity=coupon_dict.get("free_product_quantity", 1),
            
            # 统计数据
            view_count=0,
            conversion_rate=0.0,
            
            # 元数据
            meta_data=coupon_dict.get("meta_data")
        )
        
        db.add(coupon)
        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def create_coupon_batch(db: Session, batch_data: CouponBatchCreate) -> Tuple[CouponBatch, int]:
        """批量创建优惠券"""
        # 1. 创建促销
        promotion_dict = batch_data.promotion.dict()
        promotion = CouponService.create_promotion(db, promotion_dict)
        
        # 2. 创建批次
        batch = CouponBatch(
            id=uuid.uuid4(),
            name=batch_data.batch_name,
            description=batch_data.batch_description,
            code_prefix=batch_data.code_prefix,
            code_format=batch_data.code_format,
            code_length=batch_data.code_length,
            quantity=batch_data.quantity,
            generated_count=0,
            used_count=0,
            max_uses_per_coupon=batch_data.max_uses_per_coupon,
            valid_from=batch_data.valid_from or promotion.start_date,
            valid_to=batch_data.valid_to or promotion.end_date
        )
        
        db.add(batch)
        db.flush()
        
        # 3. 生成优惠券
        coupons_created = 0
        for _ in range(batch_data.quantity):
            # 生成唯一优惠券码
            while True:
                code = CouponService.generate_coupon_code(
                    prefix=batch_data.code_prefix,
                    length=batch_data.code_length,
                    format=batch_data.code_format
                )
                # 检查优惠券码是否已存在
                existing = db.query(Coupon).filter(Coupon.code == code).first()
                if not existing:
                    break
            
            # 创建优惠券
            coupon = Coupon(
                id=uuid.uuid4(),
                promotion_id=promotion.id,
                code=code,
                status=CouponStatus.ACTIVE,
                
                # 批次信息
                is_batch=True,
                batch_id=batch.id,
                
                # 生成设置
                format=batch_data.code_format,
                prefix=batch_data.code_prefix,
                length=batch_data.code_length,
                
                # 使用限制
                max_uses=batch_data.max_uses_per_coupon,
                max_uses_per_customer=1,  # 每个客户默认只能使用一次
                current_uses=0,
                is_single_use=True,
                requires_authentication=True,
                
                # 使用控制
                valid_from=batch.valid_from,
                valid_to=batch.valid_to,
                
                # 默认设置
                is_referral=False,
                is_public=False,
                is_featured=False,
                auto_apply=False
            )
            
            db.add(coupon)
            coupons_created += 1
        
        # 更新批次生成数量
        batch.generated_count = coupons_created
        
        db.commit()
        db.refresh(batch)
        return batch, coupons_created

    @staticmethod
    def update_coupon(db: Session, coupon_id: uuid.UUID, update_data: CouponUpdate) -> Optional[Coupon]:
        """更新优惠券"""
        coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
        if not coupon:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(coupon, key, value)
        
        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def get_coupon_by_id(db: Session, coupon_id: uuid.UUID) -> Optional[Coupon]:
        """通过ID获取优惠券"""
        return db.query(Coupon).filter(Coupon.id == coupon_id).first()

    @staticmethod
    def get_coupon_by_code(db: Session, code: str) -> Optional[Coupon]:
        """通过优惠券码获取优惠券"""
        return db.query(Coupon).filter(Coupon.code == code).first()

    @staticmethod
    def get_coupons(db: Session, filters: Optional[CouponFilter] = None, 
                   pagination: Optional[PaginationParams] = None) -> Tuple[List[Coupon], int]:
        """获取优惠券列表，支持过滤和分页"""
        query = db.query(Coupon)
        
        # 应用过滤条件
        if filters:
            if filters.code:
                query = query.filter(Coupon.code.ilike(f"%{filters.code}%"))
            if filters.status:
                query = query.filter(Coupon.status == filters.status)
            if filters.batch_id:
                query = query.filter(Coupon.batch_id == filters.batch_id)
            if filters.is_referral is not None:
                query = query.filter(Coupon.is_referral == filters.is_referral)
            if filters.is_public is not None:
                query = query.filter(Coupon.is_public == filters.is_public)
            if filters.is_featured is not None:
                query = query.filter(Coupon.is_featured == filters.is_featured)
            
            # 日期范围过滤
            if filters.valid_from_start:
                query = query.filter(Coupon.valid_from >= filters.valid_from_start)
            if filters.valid_from_end:
                query = query.filter(Coupon.valid_from <= filters.valid_from_end)
            if filters.valid_to_start:
                query = query.filter(Coupon.valid_to >= filters.valid_to_start)
            if filters.valid_to_end:
                query = query.filter(Coupon.valid_to <= filters.valid_to_end)
            if filters.created_at_start:
                query = query.filter(Coupon.created_at >= filters.created_at_start)
            if filters.created_at_end:
                query = query.filter(Coupon.created_at <= filters.created_at_end)
        
        # 计算总数
        total = query.count()
        
        # 应用分页和排序
        if pagination:
            if pagination.sort_desc:
                query = query.order_by(desc(getattr(Coupon, pagination.sort_by)))
            else:
                query = query.order_by(asc(getattr(Coupon, pagination.sort_by)))
            
            query = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size)
        
        return query.all(), total

    @staticmethod
    def validate_coupon(db: Session, validate_data: CouponValidate) -> Dict[str, Any]:
        """验证优惠券是否有效，并计算折扣金额"""
        coupon = db.query(Coupon).filter(Coupon.code == validate_data.code).first()
        if not coupon:
            return {
                "is_valid": False,
                "message": "优惠券不存在",
                "discount_amount": 0
            }
        
        # 获取促销信息
        promotion = db.query(Promotion).filter(Promotion.id == coupon.promotion_id).first()
        if not promotion:
            return {
                "is_valid": False,
                "message": "促销信息不存在",
                "discount_amount": 0
            }
        
        # 检查优惠券状态
        if coupon.status != CouponStatus.ACTIVE:
            return {
                "is_valid": False,
                "message": f"优惠券状态无效: {coupon.status}",
                "discount_amount": 0
            }
        
        # 检查有效期
        now = datetime.utcnow()
        if coupon.valid_from and coupon.valid_from > now:
            return {
                "is_valid": False,
                "message": f"优惠券尚未生效，生效时间: {coupon.valid_from}",
                "discount_amount": 0
            }
        
        if coupon.valid_to and coupon.valid_to < now:
            return {
                "is_valid": False,
                "message": f"优惠券已过期，过期时间: {coupon.valid_to}",
                "discount_amount": 0
            }
        
        # 检查使用次数
        if coupon.max_uses and coupon.current_uses >= coupon.max_uses:
            return {
                "is_valid": False,
                "message": "优惠券已达到最大使用次数",
                "discount_amount": 0
            }
        
        # 检查客户使用情况
        if validate_data.customer_id and coupon.requires_authentication:
            # 检查该客户之前的使用次数
            customer_uses = db.query(func.count(CustomerCoupon.id)).filter(
                CustomerCoupon.coupon_id == coupon.id,
                CustomerCoupon.customer_id == validate_data.customer_id,
                CustomerCoupon.status == CustomerCouponStatus.USED
            ).scalar()
            
            if customer_uses >= coupon.max_uses_per_customer:
                return {
                    "is_valid": False,
                    "message": "您已达到此优惠券的最大使用次数",
                    "discount_amount": 0
                }
        
        # 检查促销限制
        
        # 检查最低订单金额
        if promotion.min_order_amount and validate_data.order_amount < promotion.min_order_amount:
            return {
                "is_valid": False,
                "message": f"订单金额不满足最低要求: {promotion.min_order_amount}",
                "discount_amount": 0
            }
        
        # 检查货币限制
        if promotion.applicable_currencies and validate_data.currency_code not in promotion.applicable_currencies:
            return {
                "is_valid": False,
                "message": f"货币不适用: {validate_data.currency_code}",
                "discount_amount": 0
            }
        
        # 检查国家限制
        if validate_data.country_code:
            if promotion.excluded_countries and validate_data.country_code in promotion.excluded_countries:
                return {
                    "is_valid": False,
                    "message": f"不适用于该国家/地区: {validate_data.country_code}",
                    "discount_amount": 0
                }
            
            if promotion.applicable_countries and validate_data.country_code not in promotion.applicable_countries:
                return {
                    "is_valid": False,
                    "message": f"不适用于该国家/地区: {validate_data.country_code}",
                    "discount_amount": 0
                }
        
        # 计算折扣金额
        discount_amount = 0
        
        if promotion.discount_type == DiscountType.PERCENTAGE:
            # 百分比折扣
            discount_amount = validate_data.order_amount * (promotion.discount_value / 100)
        elif promotion.discount_type == DiscountType.FIXED_AMOUNT:
            # 固定金额折扣
            discount_amount = promotion.discount_value
        
        # 应用最大折扣限制
        if promotion.max_discount_amount and discount_amount > promotion.max_discount_amount:
            discount_amount = promotion.max_discount_amount
        
        # 确保折扣不超过订单金额
        if discount_amount > validate_data.order_amount:
            discount_amount = validate_data.order_amount
        
        return {
            "is_valid": True,
            "message": "优惠券有效",
            "discount_amount": round(discount_amount, 2),
            "coupon_id": str(coupon.id),
            "promotion_id": str(promotion.id),
            "discount_type": promotion.discount_type,
            "discount_value": promotion.discount_value
        }

    @staticmethod
    def issue_coupon_to_customers(db: Session, issue_data: CouponIssue, issued_by: Optional[uuid.UUID] = None) -> List[CustomerCoupon]:
        """将优惠券发放给客户"""
        coupon = db.query(Coupon).filter(Coupon.id == issue_data.coupon_id).first()
        if not coupon:
            raise ValueError(f"优惠券ID {issue_data.coupon_id} 不存在")
        
        # 验证优惠券状态
        if coupon.status != CouponStatus.ACTIVE:
            raise ValueError(f"只能发放激活状态的优惠券，当前状态: {coupon.status}")
        
        customer_coupons = []
        
        for customer_id in issue_data.customer_ids:
            # 检查该客户是否已有此优惠券
            existing = db.query(CustomerCoupon).filter(
                CustomerCoupon.coupon_id == coupon.id,
                CustomerCoupon.customer_id == customer_id,
                CustomerCoupon.status.in_([CustomerCouponStatus.AVAILABLE, CustomerCouponStatus.USED])
            ).first()
            
            if existing:
                # 如果客户已经有此优惠券且未使用，则跳过
                if existing.status == CustomerCouponStatus.AVAILABLE:
                    continue
            
            # 创建客户优惠券关联
            customer_coupon = CustomerCoupon(
                id=uuid.uuid4(),
                customer_id=customer_id,
                coupon_id=coupon.id,
                status=CustomerCouponStatus.AVAILABLE,
                issue_method=issue_data.issue_method,
                issued_by=issued_by,
                issued_at=datetime.utcnow(),
                valid_from=issue_data.valid_from or coupon.valid_from,
                valid_to=issue_data.valid_to or coupon.valid_to,
                notification_sent=False,
                notification_method=issue_data.notification_method,
                referrer_id=issue_data.referrer_id,
                custom_message=issue_data.custom_message,
                notes=issue_data.notes,
                meta_data=issue_data.meta_data
            )
            
            db.add(customer_coupon)
            customer_coupons.append(customer_coupon)
        
        db.commit()
        
        # 刷新对象以获取生成的ID
        for cc in customer_coupons:
            db.refresh(cc)
        
        return customer_coupons

    @staticmethod
    def get_customer_coupons(db: Session, customer_id: uuid.UUID, include_used: bool = False) -> List[CustomerCoupon]:
        """获取客户的所有优惠券"""
        query = db.query(CustomerCoupon).filter(CustomerCoupon.customer_id == customer_id)
        
        if not include_used:
            query = query.filter(CustomerCoupon.status == CustomerCouponStatus.AVAILABLE)
        
        return query.all()

    @staticmethod
    def use_coupon(db: Session, coupon_code: str, customer_id: uuid.UUID, order_id: uuid.UUID, 
                  discount_amount: float) -> Optional[CustomerCoupon]:
        """使用优惠券"""
        # 获取优惠券
        coupon = db.query(Coupon).filter(Coupon.code == coupon_code).first()
        if not coupon:
            raise ValueError(f"优惠券码 {coupon_code} 不存在")
        
        # 获取客户的优惠券
        customer_coupon = db.query(CustomerCoupon).filter(
            CustomerCoupon.coupon_id == coupon.id,
            CustomerCoupon.customer_id == customer_id,
            CustomerCoupon.status == CustomerCouponStatus.AVAILABLE
        ).first()
        
        # 如果客户没有此优惠券但优惠券是公开的，则创建一个新的客户优惠券关联
        if not customer_coupon and coupon.is_public:
            customer_coupon = CustomerCoupon(
                id=uuid.uuid4(),
                customer_id=customer_id,
                coupon_id=coupon.id,
                status=CustomerCouponStatus.AVAILABLE,
                issue_method=IssueMethod.AUTOMATIC,
                issued_at=datetime.utcnow(),
                valid_from=coupon.valid_from,
                valid_to=coupon.valid_to,
                notification_sent=False
            )
            db.add(customer_coupon)
            db.flush()
        
        if not customer_coupon:
            raise ValueError("客户未拥有此优惠券")
        
        # 更新客户优惠券状态
        customer_coupon.status = CustomerCouponStatus.USED
        customer_coupon.used_at = datetime.utcnow()
        customer_coupon.order_id = order_id
        customer_coupon.discount_amount = discount_amount
        
        # 更新优惠券使用次数
        coupon.current_uses += 1
        
        # 如果达到最大使用次数，更新状态
        if coupon.max_uses and coupon.current_uses >= coupon.max_uses:
            coupon.status = CouponStatus.USED
        
        # 更新批次使用数量
        if coupon.is_batch and coupon.batch_id:
            batch = db.query(CouponBatch).filter(CouponBatch.id == coupon.batch_id).first()
            if batch:
                batch.used_count += 1
        
        db.commit()
        db.refresh(customer_coupon)
        return customer_coupon

    @staticmethod
    def cancel_coupon(db: Session, coupon_id: uuid.UUID) -> Optional[Coupon]:
        """取消优惠券"""
        coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
        if not coupon:
            return None
        
        # 只有未使用的优惠券可以取消
        if coupon.status not in [CouponStatus.ACTIVE, CouponStatus.INACTIVE]:
            raise ValueError(f"只有激活或未激活状态的优惠券可以取消，当前状态: {coupon.status}")
        
        coupon.status = CouponStatus.CANCELLED
        
        # 同时取消所有未使用的客户优惠券
        db.query(CustomerCoupon).filter(
            CustomerCoupon.coupon_id == coupon_id,
            CustomerCoupon.status == CustomerCouponStatus.AVAILABLE
        ).update({"status": CustomerCouponStatus.CANCELLED})
        
        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def get_batch_by_id(db: Session, batch_id: uuid.UUID) -> Optional[CouponBatch]:
        """通过ID获取优惠券批次"""
        return db.query(CouponBatch).filter(CouponBatch.id == batch_id).first()

    @staticmethod
    def get_coupon_batches(db: Session, page: int = 1, page_size: int = 20) -> Tuple[List[CouponBatch], int]:
        """获取优惠券批次列表，支持分页"""
        query = db.query(CouponBatch)
        total = query.count()
        
        batches = query.order_by(desc(CouponBatch.created_at)) \
                     .offset((page - 1) * page_size) \
                     .limit(page_size) \
                     .all()
        
        return batches, total
