from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.product.sku.schema import (
    ProductSku,
    ProductSkuCreate,
    ProductSkuUpdate,
    ProductSkuList,
    ProductSkuInventoryUpdate,
    ProductSkuBulkStatusUpdate,
    StockAdjustment,
    StockHistory
)
from app.product.models import ProductStatus
from app.product.sku.service import ProductSkuService
from app.security.models import User


router = APIRouter(prefix="/skus")


@router.get("")
def get_all_skus(
    skip: int = Query(0, ge=0, description="分页起始位置"),
    limit: int = Query(20, ge=1, le=500, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词（SKU编码、条形码、产品名称）"),
    product_id: Optional[UUID] = Query(None, description="产品ID过滤"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    low_stock: Optional[bool] = Query(None, description="是否低库存"),
    sort_field: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向 (asc/desc)"),
    include_product: bool = Query(True, description="是否包含产品信息"),
    include_inventory: bool = Query(True, description="是否包含库存信息"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取所有SKU列表，支持分页、过滤、搜索和排序
    """
    return ProductSkuService.get_all_skus(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        product_id=product_id,
        is_active=is_active,
        low_stock=low_stock,
        sort_field=sort_field,
        sort_order=sort_order,
        include_product=include_product,
        include_inventory=include_inventory
    )


@router.get("/product/{product_id}")
def get_product_skus(
    product_id: UUID = Path(..., description="产品ID"),
    skip: int = Query(0, ge=0, description="分页起始位置"),
    limit: int = Query(100, ge=1, le=1000, description="每页数量"),
    status: Optional[ProductStatus] = Query(None, description="SKU状态"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    include_inventory: bool = Query(True, description="是否包含库存信息"),
    db: Session = Depends(get_db)
):
    """
    获取指定产品的SKU列表，支持分页、过滤和搜索
    """
    return ProductSkuService.get_product_skus(
        db, product_id, skip, limit, status, search, include_inventory
    )


@router.get("/stats", response_model=Dict[str, Any])
def get_sku_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取SKU统计数据
    """
    return ProductSkuService.get_sku_stats(db)


@router.get("/code/{sku_code}")
def get_sku_by_code(
    sku_code: str = Path(..., description="SKU编码"),
    db: Session = Depends(get_db)
):
    """
    根据编码获取SKU详情
    """
    return ProductSkuService.get_sku_by_code(db, sku_code)


@router.get("/{sku_id}")
def get_sku(
    sku_id: UUID = Path(..., description="SKU ID"),
    db: Session = Depends(get_db)
):
    """
    根据ID获取SKU详情
    """
    return ProductSkuService.get_sku_by_id(db, sku_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_sku(
    sku: ProductSkuCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的SKU
    """
    return ProductSkuService.create_sku(db, sku)


@router.put("/{sku_id}")
def update_sku(
    sku_id: UUID = Path(..., description="SKU ID"),
    sku: ProductSkuUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新SKU信息
    """
    return ProductSkuService.update_sku(db, sku_id, sku)


@router.delete("/{sku_id}", response_model=Dict[str, Any])
def delete_sku(
    sku_id: UUID = Path(..., description="SKU ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除SKU
    """
    return ProductSkuService.delete_sku(db, sku_id)


@router.put("/{sku_id}/inventory", response_model=Dict[str, Any])
def update_inventory(
    sku_id: UUID = Path(..., description="SKU ID"),
    inventory_data: ProductSkuInventoryUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新SKU库存
    """
    return ProductSkuService.update_inventory(db, sku_id, inventory_data)


@router.post("/{sku_id}/inventory/adjust", response_model=Dict[str, Any])
def adjust_inventory(
    sku_id: UUID = Path(..., description="SKU ID"),
    adjustment: int = Query(..., description="库存调整数量，正数为增加，负数为减少"),
    reason: str = Query("手动调整", description="调整原因"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    调整SKU库存
    """
    return ProductSkuService.adjust_inventory(db, sku_id, adjustment, reason)


@router.post("/bulk/status", response_model=Dict[str, Any])
def bulk_update_status(
    bulk_update: ProductSkuBulkStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    批量更新SKU状态
    """
    return ProductSkuService.bulk_update_status(db, bulk_update)


# ==================== 新增的简化库存管理API ====================

@router.post("/{sku_id}/stock/adjust")
def adjust_stock(
    sku_id: UUID = Path(..., description="SKU ID"),
    adjustment: StockAdjustment = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    手动调整库存（用于盘点、损耗等）
    """
    sku = ProductSkuService.adjust_stock(
        db=db,
        sku_id=sku_id,
        quantity_change=adjustment.quantity_change,
        change_type="adjust",
        remark=adjustment.remark,
        created_by=current_user.username if hasattr(current_user, 'username') else str(current_user.id)
    )
    return {
        "success": True,
        "message": f"库存调整成功",
        "data": {
            "sku_id": str(sku.id),
            "sku_code": sku.sku_code,
            "stock_quantity": sku.stock_quantity,
            "is_low_stock": sku.is_low_stock
        }
    }


@router.get("/{sku_id}/stock/history")
def get_stock_history(
    sku_id: UUID = Path(..., description="SKU ID"),
    skip: int = Query(0, ge=0, description="分页起始位置"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取库存变动历史
    """
    from app.product.models import StockLog
    from sqlalchemy import desc
    
    query = db.query(StockLog).filter(StockLog.sku_id == sku_id)
    total = query.count()
    
    logs = query.order_by(desc(StockLog.created_at)).offset(skip).limit(limit).all()
    
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "total": total,
            "items": [
                {
                    "id": log.id,
                    "change_type": log.change_type,
                    "quantity": log.quantity,
                    "balance": log.balance,
                    "order_id": str(log.order_id) if log.order_id else None,
                    "remark": log.remark,
                    "created_at": log.created_at.isoformat(),
                    "created_by": log.created_by
                }
                for log in logs
            ]
        }
    }
