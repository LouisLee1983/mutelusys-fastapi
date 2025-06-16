from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.security.models import User, Role, UserRole, LoginLog
from app.core.security import create_access_token
from . import schema

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否正确"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """通过用户名获取用户"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """通过邮箱获取用户"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """通过ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """认证用户"""
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user_data: schema.UserCreate, is_superuser: bool = False) -> User:
    """创建新用户"""
    # 检查用户名是否已存在
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建用户对象
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        phone_number=user_data.phone_number,
        is_active=user_data.is_active,
        is_superuser=is_superuser
    )
    
    # 保存到数据库
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def update_user(db: Session, user_id: UUID, user_data: schema.UserUpdate) -> User:
    """更新用户信息"""
    # 获取用户
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查用户名唯一性
    if user_data.username and user_data.username != db_user.username:
        if get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
    
    # 检查邮箱唯一性
    if user_data.email and user_data.email != db_user.email:
        if get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
    
    # 更新用户信息
    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # 保存更新
    db.commit()
    db.refresh(db_user)
    
    return db_user


def change_password(db: Session, user_id: UUID, password_data: schema.PasswordChange) -> bool:
    """修改用户密码"""
    # 获取用户
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证当前密码
    if not verify_password(password_data.current_password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码不正确"
        )
    
    # 更新密码
    db_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return True


def delete_user(db: Session, user_id: UUID) -> bool:
    """删除用户"""
    # 获取用户
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 删除用户
    db.delete(db_user)
    db.commit()
    
    return True


def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    sort_field: str = "created_at",
    sort_order: str = "desc",
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """获取用户列表"""
    # 构建查询
    query = db.query(User)
    
    # 应用过滤条件
    if filters:
        if filters.get("username"):
            query = query.filter(User.username.ilike(f"%{filters['username']}%"))
        if filters.get("email"):
            query = query.filter(User.email.ilike(f"%{filters['email']}%"))
        if filters.get("is_active") is not None:
            query = query.filter(User.is_active == filters["is_active"])
    
    # 获取总数
    total = query.count()
    
    # 应用排序
    order_field = getattr(User, sort_field, User.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(asc(order_field))
    else:
        query = query.order_by(desc(order_field))
    
    # 应用分页
    users = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": users
    }


def assign_role_to_user(db: Session, user_id: UUID, role_id: UUID) -> UserRole:
    """为用户分配角色"""
    # 检查用户是否存在
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查角色是否存在
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查是否已分配该角色
    existing_assignment = (
        db.query(UserRole)
        .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
        .first()
    )
    if existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户已拥有此角色"
        )
    
    # 创建新的角色分配
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    
    return user_role


def remove_role_from_user(db: Session, user_id: UUID, role_id: UUID) -> bool:
    """从用户移除角色"""
    # 检查角色分配是否存在
    user_role = (
        db.query(UserRole)
        .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
        .first()
    )
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该用户未分配此角色"
        )
    
    # 删除角色分配
    db.delete(user_role)
    db.commit()
    
    return True


def log_user_login(db: Session, user: User, ip_address: str, user_agent: str = None, success: bool = True, message: str = None) -> LoginLog:
    """记录用户登录日志"""
    # 创建登录日志
    login_log = LoginLog(
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
        device_type=get_device_type(user_agent) if user_agent else None,
        login_status=success,
        status_message=message
    )
    
    # 更新用户最后登录时间
    if success:
        user.last_login = datetime.utcnow()
        db.add(user)
    
    # 保存日志
    db.add(login_log)
    db.commit()
    db.refresh(login_log)
    
    return login_log


def get_device_type(user_agent: str) -> str:
    """从User-Agent中获取设备类型"""
    user_agent = user_agent.lower()
    if "mobile" in user_agent or "android" in user_agent or "iphone" in user_agent:
        return "mobile"
    elif "tablet" in user_agent or "ipad" in user_agent:
        return "tablet"
    else:
        return "desktop"
