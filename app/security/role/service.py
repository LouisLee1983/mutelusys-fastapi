from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException, status
from app.security.models import Role, Permission, RolePermission
from . import schema

def get_role_by_id(db: Session, role_id: UUID) -> Optional[Role]:
    """通过ID获取角色"""
    return db.query(Role).filter(Role.id == role_id).first()

def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    """通过名称获取角色"""
    return db.query(Role).filter(Role.name == name).first()

def create_role(db: Session, role_data: schema.RoleCreate) -> Role:
    """创建新角色"""
    # 检查角色名称是否已存在
    if get_role_by_name(db, role_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色名称已存在"
        )
    
    # 创建角色对象
    db_role = Role(
        name=role_data.name,
        description=role_data.description,
        is_default=role_data.is_default
    )
    
    # 如果是默认角色，取消其他默认角色
    if role_data.is_default:
        db.query(Role).filter(Role.is_default == True).update({"is_default": False})
    
    # 保存到数据库
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    
    return db_role

def update_role(db: Session, role_id: UUID, role_data: schema.RoleUpdate) -> Role:
    """更新角色信息"""
    # 获取角色
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查名称唯一性
    if role_data.name and role_data.name != db_role.name:
        if get_role_by_name(db, role_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色名称已存在"
            )
    
    # 更新角色信息
    update_data = role_data.dict(exclude_unset=True)
    
    # 处理默认角色逻辑
    if "is_default" in update_data and update_data["is_default"] and not db_role.is_default:
        db.query(Role).filter(Role.is_default == True).update({"is_default": False})
    
    # 更新其他字段
    for key, value in update_data.items():
        setattr(db_role, key, value)
    
    # 保存更新
    db.commit()
    db.refresh(db_role)
    
    return db_role

def delete_role(db: Session, role_id: UUID) -> bool:
    """删除角色"""
    # 获取角色
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查是否为默认角色
    if db_role.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除默认角色"
        )
    
    # 删除角色
    db.delete(db_role)
    db.commit()
    
    return True

def get_roles(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    sort_field: str = "created_at",
    sort_order: str = "desc",
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """获取角色列表"""
    # 构建查询
    query = db.query(Role)
    
    # 应用过滤条件
    if filters:
        if filters.get("name"):
            query = query.filter(Role.name.ilike(f"%{filters['name']}%"))
        if filters.get("is_default") is not None:
            query = query.filter(Role.is_default == filters["is_default"])
    
    # 获取总数
    total = query.count()
    
    # 应用排序
    order_field = getattr(Role, sort_field, Role.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(asc(order_field))
    else:
        query = query.order_by(desc(order_field))
    
    # 应用分页
    roles = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": roles
    }

def get_permissions(db: Session) -> List[Permission]:
    """获取所有权限"""
    return db.query(Permission).all()

def get_permission_by_id(db: Session, permission_id: UUID) -> Optional[Permission]:
    """通过ID获取权限"""
    return db.query(Permission).filter(Permission.id == permission_id).first()

def assign_permissions_to_role(db: Session, role_id: UUID, permission_ids: List[UUID]) -> Role:
    """为角色分配权限"""
    # 检查角色是否存在
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 验证所有权限ID是否有效
    for permission_id in permission_ids:
        if not get_permission_by_id(db, permission_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"权限ID {permission_id} 不存在"
            )
    
    # 清除当前角色的所有权限
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
    
    # 添加新的权限
    for permission_id in permission_ids:
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        db.add(role_permission)
    
    # 提交事务
    db.commit()
    db.refresh(db_role)
    
    return db_role

def get_role_permissions(db: Session, role_id: UUID) -> List[Permission]:
    """获取角色的所有权限"""
    # 检查角色是否存在
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    return db_role.permissions

def create_default_roles(db: Session) -> None:
    """创建系统默认角色"""
    # 超级管理员
    if not get_role_by_name(db, schema.SystemRoles.SUPER_ADMIN):
        super_admin = Role(
            name=schema.SystemRoles.SUPER_ADMIN,
            description="超级管理员，拥有所有权限",
            is_default=True
        )
        db.add(super_admin)
    
    # 普通管理员
    if not get_role_by_name(db, schema.SystemRoles.ADMIN):
        admin = Role(
            name=schema.SystemRoles.ADMIN,
            description="管理员，拥有大部分管理权限",
            is_default=False
        )
        db.add(admin)
    
    # 运营人员
    if not get_role_by_name(db, schema.SystemRoles.OPERATOR):
        operator = Role(
            name=schema.SystemRoles.OPERATOR,
            description="运营人员，负责内容和产品管理",
            is_default=False
        )
        db.add(operator)
    
    # 客服人员
    if not get_role_by_name(db, schema.SystemRoles.CUSTOMER_SERVICE):
        cs = Role(
            name=schema.SystemRoles.CUSTOMER_SERVICE,
            description="客服人员，处理客户问题和订单管理",
            is_default=False
        )
        db.add(cs)
    
    # 仓库管理员
    if not get_role_by_name(db, schema.SystemRoles.WAREHOUSE):
        warehouse = Role(
            name=schema.SystemRoles.WAREHOUSE,
            description="仓库管理员，负责库存和物流管理",
            is_default=False
        )
        db.add(warehouse)
    
    # 财务人员
    if not get_role_by_name(db, schema.SystemRoles.FINANCE):
        finance = Role(
            name=schema.SystemRoles.FINANCE,
            description="财务人员，负责支付和财务管理",
            is_default=False
        )
        db.add(finance)
    
    # 提交事务
    db.commit()
