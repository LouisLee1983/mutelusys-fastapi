from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security.dependencies import get_current_active_admin
from app.product.inventory.schema import (
    ProductInventory,
    ProductInventoryCreate,
    ProductInventoryUpdate,
    ProductInventoryList,
    ProductInventoryAdjustment,
    ProductInventoryAdjustmentResult,
    ProductInventoryReservation,
    ProductInventoryReservationResult,
    ProductInventoryStatistics,
    InventoryMovement
)
from app.product.inventory.service import ProductInventoryService

router = APIRouter(prefix="/api/v1/admin/inventories")

# 获取库存列表
@router.get("", response_model=ProductInventoryList)
def get_inventories(
    skip: int = Query(0, description="跳过前N个记录"),
    limit: int = Query(100, description="返回记录数量"),
    product_id: Optional[UUID] = Query(None, description="产品ID"),
    category_id: Optional[UUID] = Query(None, description="分类ID"),
    warehouse_id: Optional[UUID] = Query(None, description="仓库ID"),
    sku_code: Optional[str] = Query(None, description="SKU编码"),
    is_low_stock: Optional[bool] = Query(None, description="是否低库存"),
    is_out_of_stock: Optional[bool] = Query(None, description="是否缺货"),
    search: Optional[str] = Query(None, description="搜索关键字"),
    sort_by: str = Query("updated_at", description="排序字段"),
    sort_desc: bool = Query(True, description="是否降序排序"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> ProductInventoryList:
    """
    获取库存列表，支持分页、过滤和搜索
    """
    return ProductInventoryService.get_inventories(
        db=db,
        skip=skip,
        limit=limit,
        product_id=product_id,
        category_id=category_id,
        warehouse_id=warehouse_id,
        sku_code=sku_code,
        is_low_stock=is_low_stock,
        is_out_of_stock=is_out_of_stock,
        search=search,
        sort_by=sort_by,
        sort_desc=sort_desc
    )

# 获取库存详情
@router.get("/{inventory_id}", response_model=ProductInventory)
def get_inventory(
    inventory_id: UUID = Path(..., description="库存ID"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> ProductInventory:
    """
    根据ID获取库存详情
    """
    return ProductInventoryService.get_inventory_by_id(db=db, inventory_id=inventory_id)

# 创建库存
@router.post("", response_model=ProductInventory, status_code=status.HTTP_201_CREATED)
def create_inventory(
    inventory_data: ProductInventoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> ProductInventory:
    """
    创建新的库存记录
    """
    return ProductInventoryService.create_inventory(db=db, inventory_data=inventory_data)

# 更新库存
@router.put("/{inventory_id}", response_model=ProductInventory)
def update_inventory(
    inventory_id: UUID,
    inventory_data: ProductInventoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> ProductInventory:
    """
    更新库存信息
    """
    return ProductInventoryService.update_inventory(
        db=db, 
        inventory_id=inventory_id, 
        inventory_data=inventory_data
    )

# 删除库存
@router.delete("/{inventory_id}", response_model=Dict[str, Any])
def delete_inventory(
    inventory_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> Dict[str, Any]:
    """
    删除库存记录
    """
    return ProductInventoryService.delete_inventory(db=db, inventory_id=inventory_id)

# 调整库存
@router.post("/adjust", response_model=ProductInventoryAdjustmentResult)
def adjust_inventory(
    adjustment_data: ProductInventoryAdjustment,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> ProductInventoryAdjustmentResult:
    """
    调整库存数量，支持增加或减少库存
    """
    return ProductInventoryService.adjust_inventory(db=db, adjustment_data=adjustment_data)

# 库存预留
@router.post("/reserve", response_model=ProductInventoryReservationResult)
def reserve_inventory(
    reservation_data: ProductInventoryReservation,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> ProductInventoryReservationResult:
    """
    预留库存，用于订单锁定库存等场景
    """
    return ProductInventoryService.reserve_inventory(db=db, reservation_data=reservation_data)

# 释放预留库存
@router.post("/release", response_model=Dict[str, Any])
def release_reservation(
    sku_id: UUID = Query(..., description="SKU ID"),
    quantity: int = Query(..., gt=0, description="释放数量"),
    order_id: Optional[UUID] = Query(None, description="订单ID"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> Dict[str, Any]:
    """
    释放预留的库存，用于订单取消等场景
    """
    return ProductInventoryService.release_reservation(
        db=db,
        sku_id=sku_id,
        quantity=quantity,
        order_id=order_id
    )

# 获取库存统计
@router.get("/statistics/overview", response_model=ProductInventoryStatistics)
def get_inventory_statistics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> ProductInventoryStatistics:
    """
    获取库存统计信息，包括总数、低库存、缺货等数据
    """
    return ProductInventoryService.get_inventory_statistics(db=db)

# 库存转移
@router.post("/transfer", response_model=Dict[str, Any])
def transfer_inventory(
    movement_data: InventoryMovement,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> Dict[str, Any]:
    """
    在仓库之间转移库存
    """
    return ProductInventoryService.transfer_inventory(db=db, movement_data=movement_data)

# 获取仓库列表（用于库存管理界面的仓库选择）
# 仓库功能已简化，跨境电商不需要复杂的仓库管理
@router.get("/warehouses", response_model=List[Dict[str, Any]])
def get_warehouses_for_inventory(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> List[Dict[str, Any]]:
    """
    获取可用仓库列表，用于库存管理界面的仓库选择
    仓库功能已简化，返回空列表
    """
    # 仓库功能已删除，跨境电商不需要复杂的仓库管理
    return []

# 公开API - 检查SKU库存状态
@router.get("/public/sku/{sku_id}/status", response_model=Dict[str, Any])
def get_sku_inventory_status(
    sku_id: UUID,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    公开API：获取SKU库存状态，供前台展示使用
    """
    try:
        inventory = ProductInventoryService.get_inventory_by_sku(db=db, sku_id=sku_id)
        available = inventory.quantity - inventory.reserved_quantity
        
        return {
            "sku_id": sku_id,
            "in_stock": inventory.quantity > 0,
            "available_quantity": available if available > 0 else 0,
            "status": "in_stock" if inventory.quantity > 0 else "out_of_stock"
        }
    except HTTPException:
        return {
            "sku_id": sku_id,
            "in_stock": False,
            "available_quantity": 0,
            "status": "not_found"
        }
