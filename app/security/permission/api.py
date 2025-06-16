from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.security.models import Permission, User
from app.admin.dependencies import get_current_admin_user, get_current_admin
from app.security.user.api import success_response, error_response
from . import schema, service

# 创建路由器
router = APIRouter()


# 获取权限列表 - 仅管理员可用
@router.get(
    "/admin/permissions", 
    summary="获取权限列表", 
    tags=["权限管理"],
    response_model=None  # 使用自定义响应格式
)
async def get_permission_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    sort_field: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向 (asc/desc)"),
    name: Optional[str] = None,
    module: Optional[str] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取权限列表（仅管理员可用）"""
    # 构建过滤条件
    filters = {}
    if name:
        filters["name"] = name
    if module:
        filters["module"] = module
    
    # 获取权限列表
    result = service.get_permissions(
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
    items = [schema.PermissionResponse.from_orm(permission) for permission in result["items"]]
    
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


# 创建权限 - 仅管理员可用
@router.post(
    "/admin/permissions", 
    summary="创建新权限", 
    tags=["权限管理"],
    status_code=status.HTTP_201_CREATED
)
async def create_permission(
    permission_data: schema.PermissionCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """创建新权限（仅管理员可用）"""
    try:
        permission = service.create_permission(db, permission_data)
        return success_response(
            schema.PermissionResponse.from_orm(permission),
            "权限创建成功",
            201
        )
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 获取指定权限 - 仅管理员可用
@router.get(
    "/admin/permissions/{permission_id}", 
    summary="获取指定权限信息", 
    tags=["权限管理"]
)
async def get_permission_by_id(
    permission_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取指定权限的详细信息（仅管理员可用）"""
    permission = service.get_permission_by_id(db, permission_id)
    if not permission:
        return error_response("权限不存在", 404)
    
    return success_response(schema.PermissionResponse.from_orm(permission))


# 更新指定权限 - 仅管理员可用
@router.patch(
    "/admin/permissions/{permission_id}", 
    summary="更新指定权限信息", 
    tags=["权限管理"]
)
async def update_permission_by_id(
    permission_id: UUID,
    permission_data: schema.PermissionUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """更新指定权限的信息（仅管理员可用）"""
    try:
        updated_permission = service.update_permission(db, permission_id, permission_data)
        return success_response(schema.PermissionResponse.from_orm(updated_permission))
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 删除指定权限 - 仅管理员可用
@router.delete(
    "/admin/permissions/{permission_id}", 
    response_model=Dict[str, Any], 
    summary="删除指定权限", 
    tags=["权限管理"]
)
async def delete_permission_by_id(
    permission_id: UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除指定权限（仅管理员可用）"""
    try:
        service.delete_permission(db, permission_id)
        return success_response(message="权限删除成功")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)


# 初始化默认权限 - 仅超级管理员可用
@router.post(
    "/admin/permissions/init-default", 
    response_model=Dict[str, Any], 
    summary="初始化默认权限", 
    tags=["权限管理"]
)
async def init_default_permissions(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """初始化系统默认权限（仅超级管理员可用）"""
    if not current_admin.is_superuser:
        return error_response("只有超级管理员可以执行此操作", 403)
    
    service.create_default_permissions(db)
    return success_response(message="默认权限初始化成功")
