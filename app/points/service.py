"""
积分服务层
处理积分的增减、查询、过期等业务逻辑
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.customer.models import Customer, CustomerPoints, PointsTransactionType, MembershipLevel, CustomerRole
from app.customer.schema import PointsTransactionCreate, PointsTransactionResponse, CustomerPointsBalance
from app.core.exceptions import BusinessException


class PointsService:
    """积分服务类"""
    
    # 积分配置
    POINTS_PER_USD = 10  # 1美元 = 10积分
    POINTS_EXPIRY_DAYS = 365  # 积分有效期365天
    
    # 会员等级积分倍率
    LEVEL_MULTIPLIERS = {
        MembershipLevel.REGULAR: 1.0,
        MembershipLevel.SILVER: 1.2,
        MembershipLevel.GOLD: 1.5,
        MembershipLevel.PLATINUM: 2.0,
        MembershipLevel.DIAMOND: 3.0
    }
    
    # 角色额外倍率
    ROLE_EXTRA_MULTIPLIERS = {
        CustomerRole.REGULAR: 0.0,
        CustomerRole.KOL: 0.5,  # KOL额外50%
        CustomerRole.VIP: 0.3   # VIP额外30%
    }
    
    @staticmethod
    def calculate_points_multiplier(customer: Customer) -> float:
        """计算客户的积分倍率"""
        # 基础倍率（根据会员等级）
        base_multiplier = PointsService.LEVEL_MULTIPLIERS.get(
            customer.membership_level, 1.0
        )
        
        # 角色额外倍率
        extra_multiplier = PointsService.ROLE_EXTRA_MULTIPLIERS.get(
            customer.role, 0.0
        )
        
        # 总倍率 = 基础倍率 * (1 + 额外倍率)
        return base_multiplier * (1 + extra_multiplier)
    
    @staticmethod
    def calculate_order_points(order_amount_usd: float, customer: Customer) -> int:
        """计算订单应获得的积分"""
        # 基础积分
        base_points = int(order_amount_usd * PointsService.POINTS_PER_USD)
        
        # 获取倍率
        multiplier = PointsService.calculate_points_multiplier(customer)
        
        # 计算最终积分
        return int(base_points * multiplier)
    
    @staticmethod
    def add_points(
        db: Session,
        customer_id: UUID,
        amount: int,
        transaction_type: PointsTransactionType,
        description: str,
        reference_type: Optional[str] = None,
        reference_id: Optional[UUID] = None
    ) -> CustomerPoints:
        """添加积分（增加或扣除）"""
        # 获取客户
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise BusinessException("客户不存在")
        
        # 如果是扣除积分，检查余额
        if amount < 0 and customer.current_points < abs(amount):
            raise BusinessException("积分余额不足")
        
        # 计算过期时间（只有获得积分才设置过期时间）
        expiry_date = None
        if amount > 0:
            expiry_date = datetime.utcnow() + timedelta(days=PointsService.POINTS_EXPIRY_DAYS)
        
        # 创建积分记录
        points_record = CustomerPoints(
            customer_id=customer_id,
            amount=amount,
            description=description,
            transaction_type=transaction_type,
            reference_type=reference_type,
            reference_id=reference_id,
            expiry_date=expiry_date,
            is_expired=False
        )
        
        # 更新客户积分余额
        customer.current_points += amount
        if amount > 0:
            customer.total_points_earned += amount
        
        db.add(points_record)
        db.commit()
        db.refresh(points_record)
        
        return points_record
    
    @staticmethod
    def get_customer_points_balance(db: Session, customer_id: UUID) -> CustomerPointsBalance:
        """获取客户积分余额信息"""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise BusinessException("客户不存在")
        
        # 计算即将过期的积分（30天内）
        expiry_threshold = datetime.utcnow() + timedelta(days=30)
        expiring_points = db.query(func.sum(CustomerPoints.amount)).filter(
            and_(
                CustomerPoints.customer_id == customer_id,
                CustomerPoints.amount > 0,
                CustomerPoints.is_expired == False,
                CustomerPoints.expiry_date != None,
                CustomerPoints.expiry_date <= expiry_threshold
            )
        ).scalar() or 0
        
        # 获取最近的过期时间
        nearest_expiry = db.query(func.min(CustomerPoints.expiry_date)).filter(
            and_(
                CustomerPoints.customer_id == customer_id,
                CustomerPoints.amount > 0,
                CustomerPoints.is_expired == False,
                CustomerPoints.expiry_date != None,
                CustomerPoints.expiry_date > datetime.utcnow()
            )
        ).scalar()
        
        return CustomerPointsBalance(
            customer_id=customer_id,
            current_points=customer.current_points,
            total_points_earned=customer.total_points_earned,
            expiring_points=int(expiring_points),
            expiry_date=nearest_expiry
        )
    
    @staticmethod
    def get_points_history(
        db: Session,
        customer_id: UUID,
        page: int = 1,
        size: int = 20,
        transaction_type: Optional[PointsTransactionType] = None
    ) -> Dict[str, Any]:
        """获取客户积分历史记录"""
        query = db.query(CustomerPoints).filter(
            CustomerPoints.customer_id == customer_id
        )
        
        # 按交易类型筛选
        if transaction_type:
            query = query.filter(CustomerPoints.transaction_type == transaction_type)
        
        # 按时间倒序
        query = query.order_by(CustomerPoints.created_at.desc())
        
        # 分页
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        
        # 获取余额信息
        balance = PointsService.get_customer_points_balance(db, customer_id)
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size,
            "balance": balance
        }
    
    @staticmethod
    def expire_points(db: Session) -> int:
        """处理过期积分（定时任务调用）"""
        now = datetime.utcnow()
        
        # 查找所有过期但未处理的积分记录
        expired_records = db.query(CustomerPoints).filter(
            and_(
                CustomerPoints.is_expired == False,
                CustomerPoints.expiry_date != None,
                CustomerPoints.expiry_date <= now,
                CustomerPoints.amount > 0
            )
        ).all()
        
        expired_count = 0
        
        for record in expired_records:
            # 获取客户
            customer = db.query(Customer).filter(
                Customer.id == record.customer_id
            ).first()
            
            if customer:
                # 扣除过期积分
                customer.current_points = max(0, customer.current_points - record.amount)
                
                # 标记为已过期
                record.is_expired = True
                
                # 创建过期记录
                expire_record = CustomerPoints(
                    customer_id=record.customer_id,
                    amount=-record.amount,
                    description=f"积分过期 (原因: {record.description})",
                    transaction_type=PointsTransactionType.EXPIRE,
                    reference_type="points",
                    reference_id=record.id,
                    is_expired=False
                )
                db.add(expire_record)
                expired_count += 1
        
        if expired_count > 0:
            db.commit()
        
        return expired_count
    
    @staticmethod
    def grant_registration_points(db: Session, customer_id: UUID) -> Optional[CustomerPoints]:
        """发放注册奖励积分"""
        # 检查是否已经发放过注册积分
        existing = db.query(CustomerPoints).filter(
            and_(
                CustomerPoints.customer_id == customer_id,
                CustomerPoints.transaction_type == PointsTransactionType.EARN_REGISTER
            )
        ).first()
        
        if existing:
            return None  # 已经发放过
        
        # 发放100积分
        return PointsService.add_points(
            db=db,
            customer_id=customer_id,
            amount=100,
            transaction_type=PointsTransactionType.EARN_REGISTER,
            description="新用户注册奖励"
        )
    
    @staticmethod
    def grant_referral_points(db: Session, referrer_id: UUID, referred_email: str) -> Optional[CustomerPoints]:
        """发放推荐奖励积分"""
        # 发放200积分给推荐人
        return PointsService.add_points(
            db=db,
            customer_id=referrer_id,
            amount=200,
            transaction_type=PointsTransactionType.EARN_REFERRAL,
            description=f"成功推荐新用户 {referred_email}"
        )
    
    @staticmethod
    def grant_birthday_points(db: Session, customer_id: UUID) -> Optional[CustomerPoints]:
        """发放生日奖励积分"""
        # 检查今年是否已经发放过生日积分
        current_year = datetime.utcnow().year
        existing = db.query(CustomerPoints).filter(
            and_(
                CustomerPoints.customer_id == customer_id,
                CustomerPoints.transaction_type == PointsTransactionType.EARN_BIRTHDAY,
                func.extract('year', CustomerPoints.created_at) == current_year
            )
        ).first()
        
        if existing:
            return None  # 今年已经发放过
        
        # 发放300积分
        return PointsService.add_points(
            db=db,
            customer_id=customer_id,
            amount=300,
            transaction_type=PointsTransactionType.EARN_BIRTHDAY,
            description=f"{current_year}年生日礼物"
        )
    
    @staticmethod
    def redeem_points_for_order(
        db: Session,
        customer_id: UUID,
        points_to_use: int,
        order_id: UUID
    ) -> CustomerPoints:
        """使用积分兑换商品（创建积分订单时调用）"""
        return PointsService.add_points(
            db=db,
            customer_id=customer_id,
            amount=-points_to_use,
            transaction_type=PointsTransactionType.REDEEM_PRODUCT,
            description="积分兑换商品",
            reference_type="order",
            reference_id=order_id
        )
    
    @staticmethod
    def refund_order_points(
        db: Session,
        customer_id: UUID,
        order_id: UUID,
        points_earned: int
    ) -> Optional[CustomerPoints]:
        """退款时回收积分"""
        if points_earned <= 0:
            return None
        
        # 扣除之前获得的积分
        return PointsService.add_points(
            db=db,
            customer_id=customer_id,
            amount=-points_earned,
            transaction_type=PointsTransactionType.DEDUCT_REFUND,
            description="订单退款，扣除获得的积分",
            reference_type="order",
            reference_id=order_id
        )