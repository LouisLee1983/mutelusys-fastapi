from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.security.models import Role, User
from app.admin.dependencies import get_current_admin_user, get_current_admin
from app.security.user.api import success_response, error_response
from . import schema, service

# 创建路由器
router = APIRouter()


# 获取角色列表 - 仅管理员可用
@router.get(
    "/admin/roles", 
    summary="获取角色列表"
)
async def get_role_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    sort_field: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向 (asc/desc)"),
    name: Optional[str] = None,
    is_default: Optional[bool] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取角色列表（仅管理员可用）"""
    # 构建过滤条件
    filters = {}
    if name:
        filters["name"] = name
    if is_default is not None:
        filters["is_default"] = is_default
    
    # 获取角色列表
    result = service.get_roles(
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
    items = [schema.RoleResponse.from_orm(role) for role in result["items"]]
    
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


# 创建角色 - 仅管理员可用
@router.post(
    "/admin/roles", 
    summary="创建新角色",
    status_code=status.HTTP_201_CREATED
)
async def create_role(
    role_data: schema.RoleCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """创建新角色（仅管理员可用）"""
    try:
        role = service.create_role(db, role_data)
        return success_response(
            schema.RoleResponse.from_orm(role),
            "角色创建成功",
            201
        )
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 获取指定角色 - 仅管理员可用
@router.get(
    "/admin/roles/{role_id}", 
    summary="获取指定角色信息"
)
async def get_role_by_id(
    role_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取指定角色的详细信息（仅管理员可用）"""
    role = service.get_role_by_id(db, role_id)
    if not role:
        return error_response("角色不存在", 404)
    
    return success_response(schema.RoleResponse.from_orm(role))


# 更新指定角色 - 仅管理员可用
@router.patch(
    "/admin/roles/{role_id}", 
    summary="更新指定角色信息"
)
async def update_role_by_id(
    role_id: UUID,
    role_data: schema.RoleUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """更新指定角色的信息（仅管理员可用）"""
    try:
        updated_role = service.update_role(db, role_id, role_data)
        return success_response(schema.RoleResponse.from_orm(updated_role))
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 删除指定角色 - 仅管理员可用
@router.delete(
    "/admin/roles/{role_id}", 
    response_model=Dict[str, Any], 
    summary="删除指定角色"
)
async def delete_role_by_id(
    role_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除指定角色（仅管理员可用）"""
    try:
        service.delete_role(db, role_id)
        return success_response(message="角色删除成功")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 获取角色权限 - 仅管理员可用
@router.get(
    "/admin/roles/{role_id}/permissions", 
    summary="获取角色权限"
)
async def get_role_permissions_api(
    role_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取指定角色的所有权限（仅管理员可用）"""
    try:
        permissions = service.get_role_permissions(db, role_id)
        return success_response([schema.PermissionSimple.from_orm(p) for p in permissions])
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 设置角色权限 - 仅管理员可用
@router.post(
    "/admin/roles/{role_id}/permissions", 
    summary="设置角色权限"
)
async def assign_permissions_to_role_api(
    role_id: UUID,
    permission_data: schema.RolePermissionAssign,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """为指定角色分配权限（仅管理员可用）"""
    try:
        role = service.assign_permissions_to_role(db, role_id, permission_data.permission_ids)
        return success_response(
            schema.RoleResponse.from_orm(role),
            "权限分配成功"
        )
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 初始化默认角色 - 仅超级管理员可用
@router.post(
    "/admin/roles/init-default", 
    response_model=Dict[str, Any], 
    summary="初始化默认角色"
)
async def init_default_roles(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """初始化系统默认角色（仅超级管理员可用）"""
    if not current_admin.is_superuser:
        return error_response("只有超级管理员可以执行此操作", 403)
    
    service.create_default_roles(db)
    return success_response(message="默认角色初始化成功")
