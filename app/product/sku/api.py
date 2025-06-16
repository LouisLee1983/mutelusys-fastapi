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
    ProductSkuBulkStatusUpdate
)
from app.product.models import ProductStatus
from app.product.sku.service import ProductSkuService
from app.security.models import User


router = APIRouter(prefix="/skus", tags=["产品SKU管理"])


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
