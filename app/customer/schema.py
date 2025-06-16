from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field, validator, model_validator
import re

from app.customer.models import CustomerStatus, MembershipLevel, RegistrationSource


class CustomerBase(BaseModel):
    """客户基础模型"""
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20, pattern=r'^\+?[0-9\s\-\(\)]{8,20}$')
    birth_date: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    language_preference: Optional[str] = Field(None, pattern=r'^[a-z]{2}(-[A-Z]{2})?$')
    currency_preference: Optional[str] = Field(None, pattern=r'^[A-Z]{3}$')


class CustomerCreate(CustomerBase):
    """客户创建模型"""
    password: Optional[str] = Field(None, min_length=8, description="密码，验证码注册时可为空")
    registration_source: RegistrationSource = Field(default=RegistrationSource.WEBSITE)
    referral_code: Optional[str] = Field(None, max_length=20)
   

class CustomerPublicCreate(CustomerBase):
    """C端用户注册模型"""
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    registration_source: RegistrationSource = Field(default=RegistrationSource.WEBSITE)
    referral_code: Optional[str] = Field(None, max_length=20)
    
    @model_validator(mode='after')
    def passwords_match(self):
        """验证两次密码输入一致"""
        if self.password != self.confirm_password:
            raise ValueError('两次输入的密码不匹配')
        return self
    
    @validator('password')
    def password_complexity(cls, v):
        """验证密码复杂度，不需要验证，购物网站没什么好验证的，让客户越简单越好"""
        return v


class CustomerSimpleRegister(BaseModel):
    """C端用户简化注册模型 - 只需要邮箱和验证码"""
    email: EmailStr
    verification_code: str = Field(..., min_length=6, max_length=6, description="6位邮箱验证码")
    referral_code: Optional[str] = Field(None, max_length=20, description="推荐码（可选）")
    
    @validator('verification_code')
    def validate_verification_code(cls, v):
        """验证验证码格式"""
        if not v.isdigit():
            raise ValueError('验证码必须是6位数字')
        return v


class CustomerCreatePublic(BaseModel):
    """公开客户创建模型 - 用于订单下单时自动创建客户"""
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    registration_source: RegistrationSource = Field(default=RegistrationSource.WEBSITE)
    
    class Config:
        from_attributes = True


class EmailVerificationCodeRequest(BaseModel):
    """发送邮箱验证码请求"""
    email: EmailStr
    purpose: str = Field(default="register", description="验证码用途：register(注册), login(登录), reset_password(重置密码)")
    
    @validator('purpose')
    def validate_purpose(cls, v):
        """验证用途"""
        allowed_purposes = ["register", "login", "reset_password"]
        if v not in allowed_purposes:
            raise ValueError(f'验证码用途必须是以下之一: {", ".join(allowed_purposes)}')
        return v


class EmailVerificationCodeVerify(BaseModel):
    """验证邮箱验证码请求"""
    email: EmailStr
    verification_code: str = Field(..., min_length=6, max_length=6, description="6位邮箱验证码")
    purpose: str = Field(default="register", description="验证码用途")
    
    @validator('verification_code')
    def validate_verification_code(cls, v):
        """验证验证码格式"""
        if not v.isdigit():
            raise ValueError('验证码必须是6位数字')
        return v


class CustomerCodeLogin(BaseModel):
    """客户验证码登录请求"""
    email: EmailStr
    verification_code: str = Field(..., min_length=6, max_length=6, description="6位邮箱验证码")
    keep_logged_in: bool = False
    
    @validator('verification_code')
    def validate_verification_code(cls, v):
        """验证验证码格式"""
        if not v.isdigit():
            raise ValueError('验证码必须是6位数字')
        return v


class CustomerUpdate(BaseModel):
    """客户更新模型"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20, pattern=r'^\+?[0-9\s\-\(\)]{8,20}$')
    birth_date: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    status: Optional[CustomerStatus] = None
    membership_level: Optional[MembershipLevel] = None
    language_preference: Optional[str] = Field(None, pattern=r'^[a-z]{2}(-[A-Z]{2})?$')
    currency_preference: Optional[str] = Field(None, pattern=r'^[A-Z]{3}$')
    notes: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    is_verified: Optional[bool] = None


class CustomerPasswordChange(BaseModel):
    """客户密码修改模型"""
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @model_validator(mode='after')
    def passwords_match(self):
        """验证新密码匹配"""
        if self.new_password != self.confirm_password:
            raise ValueError('两次输入的新密码不匹配')
        if self.current_password == self.new_password:
            raise ValueError('新密码不能与当前密码相同')
        return self
    
    @validator('new_password')
    def password_complexity(cls, v):
        """验证密码复杂度"""
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含至少一个数字')
        return v


class CustomerPasswordSet(BaseModel):
    """客户设置初始密码模型（用于没有密码的用户）"""
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @model_validator(mode='after')
    def passwords_match(self):
        """验证新密码匹配"""
        if self.new_password != self.confirm_password:
            raise ValueError('两次输入的新密码不匹配')
        return self
    
    @validator('new_password')
    def password_complexity(cls, v):
        """验证密码复杂度"""
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含至少一个数字')
        return v


class CustomerPasswordReset(BaseModel):
    """客户密码重置模型"""
    email: EmailStr
    reset_token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @model_validator(mode='after')
    def passwords_match(self):
        """验证新密码匹配"""
        if self.new_password != self.confirm_password:
            raise ValueError('两次输入的新密码不匹配')
        return self
    
    @validator('new_password')
    def password_complexity(cls, v):
        """验证密码复杂度"""
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含至少一个数字')
        return v


class CustomerResponse(CustomerBase):
    """客户响应模型"""
    id: UUID
    status: CustomerStatus
    membership_level: MembershipLevel
    current_points: int
    total_points_earned: int
    registration_source: RegistrationSource
    last_login_at: Optional[datetime] = None
    is_verified: bool
    referral_code: Optional[str] = None
    has_password: Optional[bool] = None  # 是否设置了密码
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerDetailedResponse(CustomerResponse):
    """客户详细响应模型，包含关联数据"""
    groups: List[Dict[str, Any]] = []
    addresses: List[Dict[str, Any]] = []
    points_history: Optional[List[Dict[str, Any]]] = None
    orders_count: Optional[int] = None
    total_spent: Optional[float] = None
    
    class Config:
        from_attributes = True


class CustomerList(BaseModel):
    """客户列表响应"""
    items: List[CustomerResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        from_attributes = True


class CustomerLogin(BaseModel):
    """客户登录请求"""
    email: EmailStr
    password: str
    keep_logged_in: bool = False


class CustomerLoginResponse(BaseModel):
    """客户登录响应"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    customer: CustomerResponse


class CustomerEmailVerification(BaseModel):
    """客户邮箱验证请求"""
    email: EmailStr
    verification_token: str


class CustomerPasswordResetRequest(BaseModel):
    """客户密码重置请求"""
    email: EmailStr
