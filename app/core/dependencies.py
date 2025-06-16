from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.session import get_db
from app.core.config import settings
from app.core.security import verify_token

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")

# 正确的get_current_user实现
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """从JWT令牌获取当前用户（仅限管理员）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证管理员凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user_id is None:
            raise credentials_exception
            
        # 验证是否为管理员的JWT
        if role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无效的用户类型，请使用管理员账号登录"
            )
            
    except JWTError:
        raise credentials_exception
    
    # 从数据库查询用户
    from app.security.user.service import get_user_by_id
    from uuid import UUID
    
    try:
        user = get_user_by_id(db, UUID(user_id))
        
        if not user:
            raise credentials_exception
            
        # 检查用户状态
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号已被禁用，请联系系统管理员"
            )
            
        return user
        
    except Exception:
        raise credentials_exception

# 获取当前管理员用户
async def get_current_admin(
    current_user = Depends(get_current_user)
):
    """验证当前用户是否为管理员"""
    # 由于get_current_user已经验证了role="admin"，这里只需要检查活跃状态
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号已被禁用，请联系系统管理员"
        )
    return current_user

# 为了兼容性，提供get_current_admin_user作为get_current_admin的别名
get_current_admin_user = get_current_admin

# 获取当前C端用户
async def get_current_customer(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """从JWT令牌获取当前C端用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证顾客凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        customer_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        if customer_id is None:
            raise credentials_exception
            
        # 验证是否为C端用户的JWT
        if role != "customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无效的用户类型，请使用C端用户账号登录"
            )
            
    except JWTError:
        raise credentials_exception
    
    # 从数据库查询Customer
    from app.customer.service import CustomerService
    from uuid import UUID
    
    try:
        customer = CustomerService.get_customer_by_id(db, UUID(customer_id))
        
        # 检查客户状态
        if customer.status != "active":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号已被禁用，请联系客服"
            )
            
        return customer
        
    except Exception:
        raise credentials_exception

# 重导出这些依赖函数，以便统一使用
__all__ = [
    "get_db",
    "get_current_user",
    "get_current_admin",
    "get_current_admin_user",
    "get_current_customer",
] 