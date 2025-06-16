from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from uuid import UUID
from datetime import timedelta

from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token

# C端用户专用的OAuth2 scheme
customer_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/public/customers/login")

async def get_current_customer(
    token: str = Depends(customer_oauth2_scheme),
    db: Session = Depends(get_db)
):
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
    
    try:
        customer = CustomerService.get_customer_by_id(db, UUID(customer_id))
        
        if not customer:
            raise credentials_exception
            
        # 检查客户状态
        if customer.status != "active":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号已被禁用，请联系客服"
            )
            
        return customer
        
    except Exception:
        raise credentials_exception

def create_customer_token(customer_id: str, email: str) -> str:
    """创建C端用户的JWT token（100年有效期，实际上永不过期）"""
    access_token = create_access_token(
        data={
            "sub": str(customer_id),
            "role": "customer", 
            "email": email
        },
        expires_delta=timedelta(days=36500)  # 100年有效期，实际上永不过期
    )
    return access_token

def get_customer_token_response(access_token: str, customer) -> dict:
    """获取C端用户登录/注册的统一响应格式"""
    from app.customer.schema import CustomerResponse
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 36500 * 24 * 60 * 60,  # 100年，单位秒
        "customer": CustomerResponse.from_orm(customer)
    } 