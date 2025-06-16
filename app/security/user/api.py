from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import create_access_token, verify_token
from app.admin.dependencies import get_current_admin_user, get_current_admin
from app.security.models import User, UserRole
from . import schema, service
from datetime import timedelta
from app.core.config import settings

# 创建路由器
router = APIRouter()

# 自定义API响应格式
def success_response(data: Any = None, message: str = "操作成功", code: int = 200):
    return {"code": code, "message": message, "data": data}


def error_response(message: str = "操作失败", code: int = 400, data: Any = None):
    return {"code": code, "message": message, "data": data}



# 公开路由 - 用户登录
@router.post("/admin/login", summary="管理员登录", tags=["管理员身份认证"])
async def admin_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """管理员登录接口，返回JWT令牌"""
    # 验证用户
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # 记录失败的登录
        if user_db := service.get_user_by_username(db, form_data.username):
            service.log_user_login(
                db, 
                user_db, 
                request.client.host, 
                request.headers.get("User-Agent"), 
                success=False, 
                message="密码错误"
            )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否为管理员
    if not user.is_superuser:
        # 记录非管理员登录失败
        service.log_user_login(
            db, 
            user, 
            request.client.host, 
            request.headers.get("User-Agent"), 
            success=False, 
            message="非管理员用户"
        )
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限",
        )
    
    # 生成访问令牌
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id), 
            "username": user.username,
            "role": "admin",  # 标识为管理员
            "email": user.email
        }, 
        expires_delta=access_token_expires
    )
    
    # 记录成功登录
    service.log_user_login(
        db, 
        user, 
        request.client.host, 
        request.headers.get("User-Agent")
    )
    
    # 返回统一格式的响应
    return success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer"
        },
        message="登录成功"
    )


# 用户注册 - 仅管理员可用
@router.post(
    "/admin/users", 
    summary="创建新用户", 
    tags=["用户管理"],
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: schema.UserCreate,
    is_superuser: bool = False,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """创建新用户（仅管理员可用）"""
    try:
        user = service.create_user(db, user_data, is_superuser)
        return success_response(
            schema.UserResponse.from_orm(user),
            "用户创建成功",
            201
        )
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 获取当前用户信息
@router.get(
    "/admin/users/me", 
    summary="获取当前用户信息", 
    tags=["用户管理"]
)
async def read_users_me(
    current_user: User = Depends(get_current_admin_user),
):
    """获取当前登录用户的信息"""
    return success_response(schema.UserResponse.from_orm(current_user))


# 更新当前用户信息
@router.patch(
    "/admin/users/me", 
    summary="更新当前用户信息", 
    tags=["用户管理"]
)
async def update_user_me(
    user_data: schema.UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """更新当前登录用户的信息"""
    try:
        updated_user = service.update_user(db, current_user.id, user_data)
        return success_response(schema.UserResponse.from_orm(updated_user))
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 修改当前用户密码
@router.post(
    "/admin/users/me/change-password", 
    response_model=Dict[str, Any], 
    summary="修改当前用户密码", 
    tags=["用户管理"]
)
async def change_user_password(
    password_data: schema.PasswordChange,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """修改当前登录用户的密码"""
    try:
        service.change_password(db, current_user.id, password_data)
        return success_response(message="密码修改成功")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 获取用户列表 - 仅管理员可用
@router.get(
    "/admin/users", 
    summary="获取用户列表", 
    tags=["用户管理"]
)
async def get_user_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    sort_field: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向 (asc/desc)"),
    username: Optional[str] = None,
    email: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取用户列表（仅管理员可用）"""
    # 构建过滤条件
    filters = {}
    if username:
        filters["username"] = username
    if email:
        filters["email"] = email
    if is_active is not None:
        filters["is_active"] = is_active
    
    # 获取用户列表
    result = service.get_users(
        db, 
        skip=skip, 
        limit=limit, 
        sort_field=sort_field,
        sort_order=sort_order,
        filters=filters
    )
    
    # 计算页码
    page = skip // limit + 1 if limit else 1
    # 转换 SQLAlchemy ORM 对象为 Pydantic 对象
    items = [schema.UserResponse.from_orm(user) for user in result["items"]]
    
    # 返回符合规范的结构
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "total": result["total"],
            "page": page,
            "size": limit,
            "items": items
        }
    }


# 获取指定用户 - 仅管理员可用
@router.get(
    "/admin/users/{user_id}", 
    summary="获取指定用户信息", 
    tags=["用户管理"]
)
async def get_user_by_id(
    user_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取指定用户的详细信息（仅管理员可用）"""
    user = service.get_user_by_id(db, user_id)
    if not user:
        return error_response("用户不存在", 404)
    
    return success_response(schema.UserResponse.from_orm(user))


# 更新指定用户 - 仅管理员可用
@router.patch(
    "/admin/users/{user_id}", 
    summary="更新指定用户信息", 
    tags=["用户管理"]
)
async def update_user_by_id(
    user_id: UUID,
    user_data: schema.UserUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """更新指定用户的信息（仅管理员可用）"""
    try:
        updated_user = service.update_user(db, user_id, user_data)
        return success_response(schema.UserResponse.from_orm(updated_user))
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 删除指定用户 - 仅管理员可用
@router.delete(
    "/admin/users/{user_id}", 
    response_model=Dict[str, Any], 
    summary="删除指定用户", 
    tags=["用户管理"]
)
async def delete_user_by_id(
    user_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除指定用户（仅管理员可用）"""
    try:
        # 不能删除自己
        if user_id == current_admin.id:
            return error_response("不能删除当前登录的用户", 400)
        
        service.delete_user(db, user_id)
        return success_response(message="用户删除成功")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 为用户分配角色 - 仅管理员可用
@router.post(
    "/admin/users/{user_id}/roles/{role_id}", 
    response_model=Dict[str, Any], 
    summary="为用户分配角色", 
    tags=["用户角色管理"]
)
async def assign_role_to_user_api(
    user_id: UUID,
    role_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """为用户分配角色（仅管理员可用）"""
    try:
        user_role = service.assign_role_to_user(db, user_id, role_id)
        return success_response(message="角色分配成功")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 从用户移除角色 - 仅管理员可用
@router.delete(
    "/admin/users/{user_id}/roles/{role_id}", 
    response_model=Dict[str, Any], 
    summary="从用户移除角色", 
    tags=["用户角色管理"]
)
async def remove_role_from_user_api(
    user_id: UUID,
    role_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """从用户移除角色（仅管理员可用）"""
    try:
        service.remove_role_from_user(db, user_id, role_id)
        return success_response(message="角色移除成功")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)
