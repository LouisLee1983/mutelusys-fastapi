from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException, status
from app.security.models import Permission
from . import schema

def get_permission_by_id(db: Session, permission_id: UUID) -> Optional[Permission]:
    """通过ID获取权限"""
    return db.query(Permission).filter(Permission.id == permission_id).first()

def get_permission_by_code(db: Session, code: str) -> Optional[Permission]:
    """通过代码获取权限"""
    return db.query(Permission).filter(Permission.code == code).first()

def get_permission_by_name(db: Session, name: str) -> Optional[Permission]:
    """通过名称获取权限"""
    return db.query(Permission).filter(Permission.name == name).first()

def create_permission(db: Session, permission_data: schema.PermissionCreate) -> Permission:
    """创建新权限"""
    # 检查权限代码是否已存在
    if get_permission_by_code(db, permission_data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限代码已存在"
        )
    
    # 检查权限名称是否已存在
    if get_permission_by_name(db, permission_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限名称已存在"
        )
    
    # 创建权限对象
    db_permission = Permission(
        name=permission_data.name,
        code=permission_data.code,
        description=permission_data.description,
        module=permission_data.module
    )
    
    # 保存到数据库
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    
    return db_permission

def update_permission(db: Session, permission_id: UUID, permission_data: schema.PermissionUpdate) -> Permission:
    """更新权限信息"""
    # 获取权限
    db_permission = get_permission_by_id(db, permission_id)
    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    # 检查权限代码唯一性
    if permission_data.code and permission_data.code != db_permission.code:
        if get_permission_by_code(db, permission_data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="权限代码已存在"
            )
    
    # 检查权限名称唯一性
    if permission_data.name and permission_data.name != db_permission.name:
        if get_permission_by_name(db, permission_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="权限名称已存在"
            )
    
    # 更新权限信息
    update_data = permission_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_permission, key, value)
    
    # 保存更新
    db.commit()
    db.refresh(db_permission)
    
    return db_permission

def delete_permission(db: Session, permission_id: UUID) -> bool:
    """删除权限"""
    # 获取权限
    db_permission = get_permission_by_id(db, permission_id)
    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    # 删除权限
    db.delete(db_permission)
    db.commit()
    
    return True

def get_permissions(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    sort_field: str = "created_at",
    sort_order: str = "desc",
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """获取权限列表"""
    # 构建查询
    query = db.query(Permission)
    
    # 应用过滤条件
    if filters:
        if filters.get("name"):
            query = query.filter(Permission.name.ilike(f"%{filters['name']}%"))
        if filters.get("module"):
            query = query.filter(Permission.module == filters["module"])
    
    # 获取总数
    total = query.count()
    
    # 应用排序
    order_field = getattr(Permission, sort_field, Permission.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(asc(order_field))
    else:
        query = query.order_by(desc(order_field))
    
    # 应用分页
    permissions = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": permissions
    }

def create_default_permissions(db: Session) -> bool:
    """创建默认权限"""
    # 定义默认权限
    default_permissions = [
        # 仪表盘权限
        {"name": "查看仪表盘", "code": "dashboard:view", "module": "dashboard", "description": "查看系统仪表盘"},
        
        # 产品管理权限
        {"name": "查看产品", "code": "product:view", "module": "product", "description": "查看产品信息"},
        {"name": "创建产品", "code": "product:create", "module": "product", "description": "创建新产品"},
        {"name": "编辑产品", "code": "product:edit", "module": "product", "description": "编辑产品信息"},
        {"name": "删除产品", "code": "product:delete", "module": "product", "description": "删除产品"},
        {"name": "管理产品分类", "code": "product:category", "module": "product", "description": "管理产品分类"},
        {"name": "管理产品库存", "code": "product:inventory", "module": "product", "description": "管理产品库存"},
        
        # 订单管理权限
        {"name": "查看订单", "code": "order:view", "module": "order", "description": "查看订单信息"},
        {"name": "创建订单", "code": "order:create", "module": "order", "description": "创建新订单"},
        {"name": "编辑订单", "code": "order:edit", "module": "order", "description": "编辑订单信息"},
        {"name": "删除订单", "code": "order:delete", "module": "order", "description": "删除订单"},
        {"name": "处理订单", "code": "order:process", "module": "order", "description": "处理订单状态"},
        {"name": "订单退货", "code": "order:return", "module": "order", "description": "处理订单退货"},
        
        # 客户管理权限
        {"name": "查看客户", "code": "customer:view", "module": "customer", "description": "查看客户信息"},
        {"name": "创建客户", "code": "customer:create", "module": "customer", "description": "创建新客户"},
        {"name": "编辑客户", "code": "customer:edit", "module": "customer", "description": "编辑客户信息"},
        {"name": "删除客户", "code": "customer:delete", "module": "customer", "description": "删除客户"},
        
        # 营销管理权限
        {"name": "查看营销活动", "code": "marketing:view", "module": "marketing", "description": "查看营销活动"},
        {"name": "创建营销活动", "code": "marketing:create", "module": "marketing", "description": "创建营销活动"},
        {"name": "编辑营销活动", "code": "marketing:edit", "module": "marketing", "description": "编辑营销活动"},
        {"name": "删除营销活动", "code": "marketing:delete", "module": "marketing", "description": "删除营销活动"},
        {"name": "管理优惠券", "code": "marketing:coupon", "module": "marketing", "description": "管理优惠券"},
        
        # 财务管理权限
        {"name": "查看财务报表", "code": "finance:view", "module": "finance", "description": "查看财务报表"},
        {"name": "管理支付", "code": "finance:payment", "module": "finance", "description": "管理支付相关功能"},
        {"name": "退款处理", "code": "finance:refund", "module": "finance", "description": "处理退款"},
        
        # 仓库管理权限
        {"name": "查看库存", "code": "warehouse:view", "module": "warehouse", "description": "查看库存信息"},
        {"name": "管理库存", "code": "warehouse:manage", "module": "warehouse", "description": "管理库存操作"},
        {"name": "库存盘点", "code": "warehouse:stocktake", "module": "warehouse", "description": "进行库存盘点"},
        
        # 系统管理权限
        {"name": "用户管理", "code": "system:user", "module": "system", "description": "管理系统用户"},
        {"name": "角色管理", "code": "system:role", "module": "system", "description": "管理用户角色"},
        {"name": "权限管理", "code": "system:permission", "module": "system", "description": "管理系统权限"},
        {"name": "系统设置", "code": "system:settings", "module": "system", "description": "管理系统设置"},
        
        # 内容管理权限
        {"name": "查看内容", "code": "content:view", "module": "content", "description": "查看内容信息"},
        {"name": "创建内容", "code": "content:create", "module": "content", "description": "创建新内容"},
        {"name": "编辑内容", "code": "content:edit", "module": "content", "description": "编辑内容"},
        {"name": "删除内容", "code": "content:delete", "module": "content", "description": "删除内容"},
        
        # 数据分析权限
        {"name": "查看报表", "code": "analytics:view", "module": "analytics", "description": "查看数据报表"},
        {"name": "导出数据", "code": "analytics:export", "module": "analytics", "description": "导出数据"},
    ]
    
    # 创建权限（如果不存在）
    created_count = 0
    for perm_data in default_permissions:
        existing_permission = get_permission_by_code(db, perm_data["code"])
        if not existing_permission:
            permission = Permission(**perm_data)
            db.add(permission)
            created_count += 1
    
    db.commit()
    
    return True
