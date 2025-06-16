from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID

# 用户基础模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool = True

# 创建用户时的请求模型
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度必须至少为8个字符')
        if not any(char.isdigit() for char in v):
            raise ValueError('密码必须包含至少一个数字')
        if not any(char.isupper() for char in v):
            raise ValueError('密码必须包含至少一个大写字母')
        return v

# 更新用户信息的请求模型
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None
    
    class Config:
        from_attributes = True

# 修改密码的请求模型
class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度必须至少为8个字符')
        if not any(char.isdigit() for char in v):
            raise ValueError('密码必须包含至少一个数字')
        if not any(char.isupper() for char in v):
            raise ValueError('密码必须包含至少一个大写字母')
        return v

# 用户登录请求模型
class UserLogin(BaseModel):
    username: str
    password: str

# 令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
# 令牌数据模型
class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    username: Optional[str] = None
    roles: Optional[List[str]] = []

# 用户角色响应模型
class RoleSimple(BaseModel):
    id: UUID
    name: str
    
    class Config:
        from_attributes = True

# 返回给API的用户信息模型
class UserResponse(UserBase):
    id: UUID
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    roles: List[RoleSimple] = []
    
    class Config:
        from_attributes = True

# 简化的用户信息模型
class UserSimple(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    
    class Config:
        from_attributes = True

# 用户列表响应模型
class UserListResponse(BaseModel):
    total: int
    items: List[UserResponse]
    
    class Config:
        from_attributes = True
