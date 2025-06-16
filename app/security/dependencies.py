from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from typing import Optional

from app.db.session import get_db
from app.core.config import settings
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user

def get_current_active_admin(current_user = Depends(get_current_user)):
    # 由于get_current_user已经验证了role="admin"，这里只需要检查活跃状态
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号已被禁用，请联系系统管理员"
        )
    return current_user

def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前认证的C端用户"""
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