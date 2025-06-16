from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from uuid import UUID

from app.db.session import get_db
from app.core.config import settings

# 管理员专用的OAuth2 scheme
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")

async def get_current_admin_user(
    token: str = Depends(admin_oauth2_scheme),
    db: Session = Depends(get_db)
):
    """获取当前认证的管理员用户"""
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
            
        # 检查是否为超级用户（管理员权限）
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足，需要管理员权限"
            )
            
        return user
        
    except Exception:
        raise credentials_exception

# 别名，保持向后兼容
get_current_admin = get_current_admin_user
get_current_user = get_current_admin_user 