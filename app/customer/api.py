from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, Body, status, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.admin.dependencies import get_current_admin_user
from app.customer.dependencies import get_current_customer, create_customer_token, get_customer_token_response
from app.customer.schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerDetailedResponse,
    CustomerList,
    CustomerPublicCreate,
    CustomerSimpleRegister,
    EmailVerificationCodeRequest,
    EmailVerificationCodeVerify,
    CustomerCodeLogin,
    CustomerLogin,
    CustomerLoginResponse,
    CustomerPasswordChange,
    CustomerPasswordSet,
    CustomerPasswordReset,
    CustomerPasswordResetRequest,
    CustomerEmailVerification
)
from app.customer.service import CustomerService
from app.customer.verification_service import EmailVerificationService
from app.customer.models import RegistrationSource

# 管理端API路由
admin_router = APIRouter(prefix="/admin/customers", tags=["customers-admin"])

# C端用户API路由
user_router = APIRouter(prefix="/customer/profile", tags=["customer-profile"])

# 公开API路由
public_router = APIRouter(prefix="/public/customers", tags=["customers-public"])


# ----- 管理端API -----

@admin_router.get("", response_model=CustomerList)
def get_customers(
    skip: int = Query(0, description="跳过前N个记录"),
    limit: int = Query(100, description="返回记录数量"),
    status: Optional[str] = Query(None, description="客户状态筛选"),
    membership_level: Optional[str] = Query(None, description="会员等级筛选"),
    group_id: Optional[UUID] = Query(None, description="客户分组筛选"),
    search: Optional[str] = Query(None, description="搜索关键字"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_desc: bool = Query(True, description="是否降序排序"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
) -> CustomerList:
    """
    获取客户列表，支持分页、过滤和搜索（管理员接口）
    """
    return CustomerService.get_customers(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        membership_level=membership_level,
        group_id=group_id,
        search=search,
        sort_by=sort_by,
        sort_desc=sort_desc
    )


@admin_router.get("/stats", response_model=Dict[str, Any])
def get_customers_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    获取客户统计信息（管理员接口）
    """
    return CustomerService.get_customers_global_stats(db=db)


@admin_router.get("/{customer_id}", response_model=CustomerDetailedResponse)
def get_customer_detail(
    customer_id: UUID = Path(..., description="客户ID"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
) -> CustomerDetailedResponse:
    """
    获取客户详细信息，包括地址、积分等相关数据（管理员接口）
    """
    customer_data = CustomerService.get_customer_detailed(db=db, customer_id=customer_id)
    # 构建响应对象
    customer = customer_data["customer"]
    response = CustomerDetailedResponse(
        id=customer.id,
        email=customer.email,
        first_name=customer.first_name,
        last_name=customer.last_name,
        phone_number=customer.phone_number,
        birth_date=customer.birth_date,
        gender=customer.gender,
        status=customer.status,
        membership_level=customer.membership_level,
        current_points=customer.current_points,
        total_points_earned=customer.total_points_earned,
        registration_source=customer.registration_source,
        last_login_at=customer.last_login_at,
        is_verified=customer.is_verified,
        referral_code=customer.referral_code,
        language_preference=customer.language_preference,
        currency_preference=customer.currency_preference,
        created_at=customer.created_at,
        updated_at=customer.updated_at,
        groups=customer_data["groups"],
        addresses=[{
            "id": addr.id,
            "address_type": addr.address_type,
            "is_default": addr.is_default,
            "full_name": f"{addr.first_name} {addr.last_name}",
            "phone_number": addr.phone_number,
            "address_line1": addr.address_line1,
            "address_line2": addr.address_line2,
            "city": addr.city,
            "state_province": addr.state_province,
            "postal_code": addr.postal_code,
            "country_code": addr.country_code
        } for addr in customer_data["addresses"]],
        points_history=[{
            "id": point.id,
            "amount": point.amount,
            "description": point.description,
            "transaction_type": point.transaction_type,
            "created_at": point.created_at
        } for point in customer_data["points_history"]],
        orders_count=customer_data["orders_count"],
        total_spent=customer_data["total_spent"]
    )
    return response


@admin_router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
) -> CustomerResponse:
    """
    创建新客户（管理员接口）
    """
    return CustomerService.create_customer(db=db, customer_data=customer_data)


@admin_router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: UUID,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
) -> CustomerResponse:
    """
    更新客户信息（管理员接口）
    """
    return CustomerService.update_customer(db=db, customer_id=customer_id, customer_data=customer_data)


@admin_router.delete("/{customer_id}", response_model=Dict[str, Any])
def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    删除客户（管理员接口，软删除）
    """
    return CustomerService.delete_customer(db=db, customer_id=customer_id)


# ----- C端用户API -----

@user_router.get("", response_model=CustomerResponse)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> CustomerResponse:
    """
    获取当前登录用户的个人资料
    """
    # 创建响应对象，包含has_password字段
    response = CustomerResponse.model_validate(current_customer)
    # 检查用户是否有密码
    response.has_password = current_customer.password_hash is not None
    return response


@user_router.put("", response_model=CustomerResponse)
def update_current_user_profile(
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> CustomerResponse:
    """
    更新当前登录用户的个人资料
    """
    updated_customer = CustomerService.update_customer(db=db, customer_id=current_customer.id, customer_data=customer_data)
    # 创建响应对象，包含has_password字段
    response = CustomerResponse.model_validate(updated_customer)
    # 检查用户是否有密码
    response.has_password = updated_customer.password_hash is not None
    return response


@user_router.post("/change-password", response_model=Dict[str, Any])
def change_current_user_password(
    password_data: CustomerPasswordChange,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    修改当前登录用户的密码
    """
    return CustomerService.change_password(
        db=db,
        customer_id=current_customer.id,
        password_data=password_data
    )


@user_router.post("/set-password", response_model=Dict[str, Any])
def set_current_user_password(
    password_data: CustomerPasswordSet,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    为当前登录用户设置初始密码（用于通过验证码注册的用户）
    """
    return CustomerService.set_password(
        db=db,
        customer_id=current_customer.id,
        password_data=password_data
    )


@user_router.get("/stats", response_model=Dict[str, Any])
def get_current_user_stats(
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    获取当前登录用户的统计信息
    """
    return CustomerService.get_customer_stats(db=db, customer_id=current_customer.id)


# ----- 公开API -----

@public_router.post("/send-verification-code", response_model=Dict[str, Any])
def send_verification_code(
    request_data: EmailVerificationCodeRequest,
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    发送邮箱验证码
    """
    
    # 获取客户端信息
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")
    
    return EmailVerificationService.send_verification_code(
        db=db,
        email=request_data.email,
        purpose=request_data.purpose,
        ip_address=ip_address,
        user_agent=user_agent
    )


@public_router.post("/verify-code", response_model=Dict[str, Any])
def verify_verification_code(
    verify_data: EmailVerificationCodeVerify,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    验证邮箱验证码（不会标记为已使用，用于前端验证）
    """
    return EmailVerificationService.verify_code(
        db=db,
        email=verify_data.email,
        verification_code=verify_data.verification_code,
        purpose=verify_data.purpose,
        auto_mark_used=False
    )


@public_router.post("/register-with-code", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def register_customer_with_code(
    customer_data: CustomerSimpleRegister,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    C端用户使用验证码完成注册（账户已在发送验证码时创建）
    """
    # 验证验证码
    EmailVerificationService.verify_code(
        db=db,
        email=customer_data.email,
        verification_code=customer_data.verification_code,
        purpose="register",
        auto_mark_used=True
    )
    
    # 获取已创建的客户
    customer = CustomerService.get_customer_by_email(db=db, email=customer_data.email)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在，请重新发送验证码"
        )
    
    # 如果提供了推荐码，更新客户信息
    if customer_data.referral_code:
        referrer = db.query(Customer).filter(Customer.referral_code == customer_data.referral_code).first()
        if referrer:
            customer.referred_by = referrer.id
            db.commit()
    
    # 生成JWT（永不过期）
    access_token = create_customer_token(customer.id, customer.email)
    
    return {
        "code": 200,
        "message": "注册验证成功",
        "data": get_customer_token_response(access_token, customer)
    }


@public_router.post("/login-with-code", response_model=Dict[str, Any])
def login_customer_with_code(
    login_data: CustomerCodeLogin,
    response: Response,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    C端用户使用验证码登录
    """
    # 验证验证码
    EmailVerificationService.verify_code(
        db=db,
        email=login_data.email,
        verification_code=login_data.verification_code,
        purpose="login",
        auto_mark_used=True
    )
    
    # 获取客户
    customer = CustomerService.get_customer_by_email(db=db, email=login_data.email)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查用户状态
    if customer.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号已被禁用，请联系客服"
        )
    
    # 更新最后登录时间
    customer.last_login_at = datetime.utcnow()
    db.commit()
    
    # 生成JWT（永不过期）
    access_token = create_customer_token(customer.id, customer.email)
    
    # 设置cookie（可选，现在使用永久有效期）
    if login_data.keep_logged_in:
        cookie_max_age = 60 * 60 * 24 * 365 * 100  # 100年，单位为秒
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=cookie_max_age,
            samesite="lax"
        )
    
    return {
        "code": 200,
        "message": "登录成功",
        "data": get_customer_token_response(access_token, customer)
    }


@public_router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register_customer(
    customer_data: CustomerPublicCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    C端用户注册
    """
    # 使用CustomerCreate模型创建客户，忽略confirm_password字段
    create_data = CustomerCreate(
        email=customer_data.email,
        password=customer_data.password,
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        phone_number=customer_data.phone_number,
        birth_date=customer_data.birth_date,
        gender=customer_data.gender,
        registration_source=customer_data.registration_source,
        referral_code=customer_data.referral_code,
        language_preference=customer_data.language_preference,
        currency_preference=customer_data.currency_preference
    )
    
    customer = CustomerService.create_customer(db=db, customer_data=create_data)
    
    # 生成JWT（永不过期）
    access_token = create_customer_token(customer.id, customer.email)
    
    return {
        "code": 201,
        "message": "注册成功",
        "data": get_customer_token_response(access_token, customer)
    }


@public_router.post("/login", response_model=Dict[str, Any])
def login_customer(
    response: Response,
    login_data: CustomerLogin,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    C端用户登录
    """
    # 检查用户是否存在
    customer = CustomerService.get_customer_by_email(db=db, email=login_data.email)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    
    # 检查用户状态
    if customer.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号已被禁用，请联系客服"
        )
    
    # 验证密码
    from app.customer.service import pwd_context
    if not pwd_context.verify(login_data.password, customer.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    
    # 更新最后登录时间
    customer.last_login_at = datetime.utcnow()
    db.commit()
    
    # 生成JWT（永不过期）
    access_token = create_customer_token(customer.id, customer.email)
    
    # 设置cookie（可选，现在使用永久有效期）
    if login_data.keep_logged_in:
        cookie_max_age = 60 * 60 * 24 * 365 * 100  # 100年，单位为秒
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=cookie_max_age,
            samesite="lax"
        )
    
    return {
        "code": 200,
        "message": "登录成功",
        "data": get_customer_token_response(access_token, customer)
    }


@public_router.post("/password-reset-request", response_model=Dict[str, Any])
def request_password_reset(
    reset_request: CustomerPasswordResetRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    请求密码重置，生成重置令牌并发送邮件
    """
    return CustomerService.request_password_reset(db=db, reset_request=reset_request)


@public_router.post("/password-reset", response_model=Dict[str, Any])
def reset_password(
    reset_data: CustomerPasswordReset,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    使用重置令牌重置密码
    """
    return CustomerService.reset_password(db=db, reset_data=reset_data)


@public_router.post("/verify-email", response_model=Dict[str, Any])
def verify_email(
    verification_data: CustomerEmailVerification,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    验证用户邮箱
    """
    return CustomerService.verify_customer_email(
        db=db,
        email=verification_data.email,
        verification_token=verification_data.verification_token
    )
