from typing import List, Optional, Dict, Any, Union
import uuid
from uuid import UUID
from datetime import datetime, timedelta
import secrets
import string
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, desc, asc, and_
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.customer.models import (
    Customer, 
    CustomerStatus, 
    MembershipLevel, 
    CustomerAddress,
    CustomerGroup,
    CustomerPoints
)
from app.customer.schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerPasswordChange,
    CustomerPasswordReset,
    CustomerPasswordResetRequest
)

# 密码哈希工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CustomerService:
    """客户服务类，提供客户信息的CRUD操作"""
    
    @staticmethod
    def get_customers(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[CustomerStatus] = None,
        membership_level: Optional[MembershipLevel] = None,
        group_id: Optional[UUID] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Dict[str, Any]:
        """
        获取客户列表，支持过滤、搜索和排序
        """
        # 基础查询
        query = db.query(Customer)
        
        # 应用过滤条件
        if status:
            query = query.filter(Customer.status == status)
            
        if membership_level:
            query = query.filter(Customer.membership_level == membership_level)
            
        if group_id:
            query = query.join(Customer.groups).filter(CustomerGroup.id == group_id)
        
        # 搜索功能
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Customer.email.ilike(search_term),
                    Customer.first_name.ilike(search_term),
                    Customer.last_name.ilike(search_term),
                    Customer.phone_number.ilike(search_term)
                )
            )
        
        # 计算总数
        total = query.count()
        
        # 排序
        sort_column = getattr(Customer, sort_by, Customer.created_at)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # 分页
        customers = query.offset(skip).limit(limit).all()
        
        return {
            "items": customers,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }
    
    @staticmethod
    def get_customer_by_id(db: Session, customer_id: UUID) -> Customer:
        """根据ID获取客户详情"""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"客户ID {customer_id} 不存在"
            )
            
        return customer
    
    @staticmethod
    def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
        """根据邮箱获取客户详情"""
        return db.query(Customer).filter(Customer.email == email).first()
    
    @staticmethod
    def get_customer_detailed(db: Session, customer_id: UUID) -> Dict[str, Any]:
        """获取客户详细信息，包含关联数据"""
        # 获取客户基础信息
        customer = CustomerService.get_customer_by_id(db, customer_id)
        
        # 获取客户地址
        addresses = db.query(CustomerAddress).filter(CustomerAddress.customer_id == customer_id).all()
        
        # 获取客户积分历史
        points_history = db.query(CustomerPoints).filter(CustomerPoints.customer_id == customer_id).order_by(desc(CustomerPoints.created_at)).limit(20).all()
        
        # 获取分组信息
        groups = [{"id": group.id, "name": group.name} for group in customer.groups]
        
        # 获取订单统计
        orders_count = db.query(func.count("*")).select_from(Customer).join(Customer.orders).filter(Customer.id == customer_id).scalar() or 0
        
        # 计算总消费金额
        total_spent = db.query(func.sum("orders.total_amount")).select_from(Customer).join(Customer.orders).filter(Customer.id == customer_id).scalar() or 0.0
        
        return {
            "customer": customer,
            "addresses": addresses,
            "points_history": points_history,
            "groups": groups,
            "orders_count": orders_count,
            "total_spent": float(total_spent)
        }
    
    @staticmethod
    def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
        """创建新客户"""
        # 检查邮箱是否已存在
        existing_customer = CustomerService.get_customer_by_email(db, customer_data.email)
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"邮箱 {customer_data.email} 已被注册"
            )
        
        # 生成推荐码
        referral_code = CustomerService._generate_referral_code()
        
        # 生成密码哈希（如果密码为空则设置为None）
        hashed_password = pwd_context.hash(customer_data.password) if customer_data.password else None
        
        # 创建客户记录
        db_customer = Customer(
            email=customer_data.email,
            password_hash=hashed_password,
            first_name=customer_data.first_name,
            last_name=customer_data.last_name,
            phone_number=customer_data.phone_number,
            birth_date=customer_data.birth_date,
            gender=customer_data.gender,
            registration_source=customer_data.registration_source,
            language_preference=customer_data.language_preference,
            currency_preference=customer_data.currency_preference,
            referral_code=referral_code,
            status=CustomerStatus.ACTIVE,
            membership_level=MembershipLevel.REGULAR
        )
        
        # 处理推荐关系
        if customer_data.referral_code:
            referrer = db.query(Customer).filter(Customer.referral_code == customer_data.referral_code).first()
            if referrer:
                db_customer.referred_by = referrer.id
        
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        
        return db_customer
    
    @staticmethod
    def create_customer_public(db: Session, customer_data) -> Customer:
        """创建公开客户（用于订单下单时自动创建）"""
        # 检查邮箱是否已存在
        existing_customer = CustomerService.get_customer_by_email(db, customer_data.email)
        if existing_customer:
            return existing_customer  # 如果客户已存在，直接返回
        
        # 生成推荐码
        referral_code = CustomerService._generate_referral_code()
        
        # 创建客户记录（密码为空，因为是游客下单）
        db_customer = Customer(
            email=customer_data.email,
            password_hash=None,  # 游客下单不设置密码
            first_name=customer_data.first_name,
            last_name=customer_data.last_name,
            phone_number=customer_data.phone_number,
            registration_source=customer_data.registration_source,
            referral_code=referral_code,
            status=CustomerStatus.ACTIVE,
            membership_level=MembershipLevel.REGULAR,
            is_verified=False  # 游客用户默认未验证
        )
        
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        
        return db_customer
    
    @staticmethod
    def update_customer(db: Session, customer_id: UUID, customer_data: CustomerUpdate) -> Customer:
        """更新客户信息"""
        customer = CustomerService.get_customer_by_id(db, customer_id)
        
        # 更新客户字段
        for key, value in customer_data.dict(exclude_unset=True).items():
            setattr(customer, key, value)
        
        db.commit()
        db.refresh(customer)
        
        return customer
    
    @staticmethod
    def delete_customer(db: Session, customer_id: UUID) -> Dict[str, Any]:
        """删除客户（软删除，将状态改为DELETED）"""
        customer = CustomerService.get_customer_by_id(db, customer_id)
        
        # 软删除
        customer.status = CustomerStatus.DELETED
        db.commit()
        
        return {"message": f"客户 {customer.email} 已成功删除"}
    
    @staticmethod
    def change_password(
        db: Session, 
        customer_id: UUID, 
        password_data: CustomerPasswordChange
    ) -> Dict[str, Any]:
        """修改客户密码"""
        customer = CustomerService.get_customer_by_id(db, customer_id)
        
        # 检查用户是否有密码
        if not customer.password_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您还没有设置密码，请先设置密码"
            )
        
        # 验证当前密码
        if not pwd_context.verify(password_data.current_password, customer.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前密码不正确"
            )
        
        # 更新密码
        customer.password_hash = pwd_context.hash(password_data.new_password)
        db.commit()
        
        return {"message": "密码已成功更新"}
    
    @staticmethod
    def set_password(
        db: Session, 
        customer_id: UUID, 
        password_data
    ) -> Dict[str, Any]:
        """设置初始密码（用于没有密码的用户）"""
        customer = CustomerService.get_customer_by_id(db, customer_id)
        
        # 检查用户是否已有密码
        if customer.password_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您已经设置过密码，请使用修改密码功能"
            )
        
        # 设置密码
        customer.password_hash = pwd_context.hash(password_data.new_password)
        db.commit()
        
        return {"message": "密码设置成功"}
    
    @staticmethod
    def request_password_reset(
        db: Session, 
        reset_request: CustomerPasswordResetRequest
    ) -> Dict[str, Any]:
        """请求密码重置，生成重置令牌"""
        customer = CustomerService.get_customer_by_email(db, reset_request.email)
        
        if not customer:
            # 即使用户不存在，也返回成功，避免泄露用户信息
            return {"message": "如果该邮箱存在，重置密码的邮件已发送"}
        
        # 生成密码重置令牌
        reset_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        token_expires = datetime.utcnow() + timedelta(hours=24)
        
        # 更新客户信息
        customer.reset_password_token = reset_token
        customer.reset_password_token_expires_at = token_expires
        db.commit()
        
        # TODO: 发送密码重置邮件（此处仅返回令牌，实际应通过邮件发送）
        
        return {
            "message": "密码重置邮件已发送",
            "token": reset_token  # 仅用于开发和测试，生产环境应移除
        }
    
    @staticmethod
    def reset_password(
        db: Session, 
        reset_data: CustomerPasswordReset
    ) -> Dict[str, Any]:
        """使用重置令牌重置密码"""
        customer = CustomerService.get_customer_by_email(db, reset_data.email)
        
        if not customer or customer.reset_password_token != reset_data.reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的重置令牌"
            )
        
        # 检查令牌是否过期
        if not customer.reset_password_token_expires_at or customer.reset_password_token_expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="重置令牌已过期"
            )
        
        # 更新密码
        customer.password_hash = pwd_context.hash(reset_data.new_password)
        customer.reset_password_token = None
        customer.reset_password_token_expires_at = None
        db.commit()
        
        return {"message": "密码已成功重置"}
    
    @staticmethod
    def verify_customer_email(
        db: Session, 
        email: str,
        verification_token: str
    ) -> Dict[str, Any]:
        """验证客户邮箱"""
        customer = CustomerService.get_customer_by_email(db, email)
        
        if not customer or customer.verification_token != verification_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的验证令牌"
            )
        
        # 检查验证令牌是否过期
        if not customer.verification_token_expires_at or customer.verification_token_expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证令牌已过期"
            )
        
        # 更新验证状态
        customer.is_verified = True
        customer.verification_token = None
        customer.verification_token_expires_at = None
        db.commit()
        
        return {"message": "邮箱验证成功"}
    
    @staticmethod
    def get_customer_stats(db: Session, customer_id: UUID) -> Dict[str, Any]:
        """获取客户统计信息"""
        customer = CustomerService.get_customer_by_id(db, customer_id)
        
        # 这里暂时返回模拟数据，实际项目中会查询相关表
        # 订单数量（需要引入order模块）
        orders_count = 0  # db.query(Order).filter(Order.customer_id == customer_id).count()
        
        # 积分余额
        points_balance = customer.current_points
        
        # 优惠券数量（需要引入coupon模块）
        coupons_count = 0  # db.query(CustomerCoupon).filter(...).count()
        
        # 收藏夹数量（需要引入wishlist模块）
        favorites_count = 0  # db.query(Wishlist).filter(...).count()
        
        return {
            "code": 200,
            "message": "获取统计信息成功",
            "data": {
                "orders_count": orders_count,
                "points_balance": points_balance,
                "coupons_count": coupons_count,
                "favorites_count": favorites_count
            }
        }
    
    @staticmethod
    def get_customers_global_stats(db: Session) -> Dict[str, Any]:
        """获取全局客户统计信息"""
        from datetime import datetime, timedelta
        
        # 总客户数
        total_customers = db.query(func.count(Customer.id)).scalar() or 0
        
        # 活跃客户数
        active_customers = db.query(func.count(Customer.id)).filter(
            Customer.status == CustomerStatus.ACTIVE
        ).scalar() or 0
        
        # 不活跃客户数
        inactive_customers = db.query(func.count(Customer.id)).filter(
            Customer.status == CustomerStatus.INACTIVE
        ).scalar() or 0
        
        # 本月新增客户数
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_this_month = db.query(func.count(Customer.id)).filter(
            Customer.created_at >= current_month_start
        ).scalar() or 0
        
        # VIP客户数（金卡、白金、钻石会员）
        vip_customers = db.query(func.count(Customer.id)).filter(
            Customer.membership_level.in_([
                MembershipLevel.GOLD, 
                MembershipLevel.PLATINUM, 
                MembershipLevel.DIAMOND
            ])
        ).scalar() or 0
        
        return {
            "code": 200,
            "message": "获取客户统计信息成功",
            "data": {
                "total": total_customers,
                "active": active_customers,
                "inactive": inactive_customers,
                "new_this_month": new_this_month,
                "vip": vip_customers
            }
        }

    @staticmethod
    def _generate_referral_code() -> str:
        """生成唯一的推荐码"""
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    @staticmethod
    def _generate_random_password() -> str:
        """生成安全的随机密码"""
        # 8-12位随机密码，包含大小写字母、数字和特殊字符
        length = secrets.randbelow(5) + 8  # 8-12位
        chars = string.ascii_letters + string.digits + "@#$%&*"
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # 确保至少包含一个大写字母、一个小写字母、一个数字
        if not any(c.isupper() for c in password):
            password = password[:-1] + secrets.choice(string.ascii_uppercase)
        if not any(c.islower() for c in password):
            password = password[:-1] + secrets.choice(string.ascii_lowercase)
        if not any(c.isdigit() for c in password):
            password = password[:-1] + secrets.choice(string.digits)
            
        return password
