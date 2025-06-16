from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.product.attribute.schema import (
    ProductAttribute,
    ProductAttributeCreate,
    ProductAttributeUpdate,
    ProductAttributeList,
    ProductAttributeValue,
    ProductAttributeValueCreate,
    ProductAttributeValueUpdate,
    ProductAttributeValueList
)
from app.product.attribute.service import ProductAttributeService, ProductAttributeValueService
from app.security.models import User

router = APIRouter(prefix="/attributes", tags=["商品属性管理"])

# 统一响应格式
def success_response(data: Any = None, message: str = "操作成功", code: int = 200):
    return {"code": code, "message": message, "data": data}

def error_response(message: str = "操作失败", code: int = 400, data: Any = None):
    return {"code": code, "message": message, "data": data}


# ==================== 商品属性 API ====================

@router.get("", response_model=Dict[str, Any])
def get_attributes(
    skip: int = Query(0, ge=0, description="分页起始位置"),
    limit: int = Query(100, ge=1, le=1000, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    type_filter: Optional[str] = Query(None, description="属性类型过滤"),
    is_configurable: Optional[bool] = Query(None, description="是否可配置过滤"),
    is_visible: Optional[bool] = Query(None, description="是否前端可见过滤"),
    db: Session = Depends(get_db)
):
    """
    获取商品属性列表，支持分页、搜索和过滤
    """
    result = ProductAttributeService.get_attributes(
        db, skip, limit, search, type_filter, is_configurable, is_visible
    )
    return success_response(data=result)


@router.get("/configurable")
def get_configurable_attributes(
    db: Session = Depends(get_db)
):
    """
    获取可配置的属性列表（用于SKU配置）
    """
    result = ProductAttributeService.get_configurable_attributes(db)
    return success_response(data=result)


@router.get("/{attribute_id}")
def get_attribute(
    attribute_id: UUID = Path(..., description="属性ID"),
    db: Session = Depends(get_db)
):
    """
    根据ID获取商品属性详情
    """
    result = ProductAttributeService.get_attribute_by_id(db, attribute_id)
    return success_response(data=result)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_attribute(
    *,
    attribute: ProductAttributeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的商品属性
    """
    result = ProductAttributeService.create_attribute(db, attribute)
    return success_response(data=result, message="创建属性成功", code=201)


@router.put("/{attribute_id}")
def update_attribute(
    *,
    attribute_id: UUID = Path(..., description="属性ID"),
    attribute: ProductAttributeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新商品属性信息
    """
    result = ProductAttributeService.update_attribute(db, attribute_id, attribute)
    return success_response(data=result, message="更新属性成功")


@router.delete("/{attribute_id}")
def delete_attribute(
    attribute_id: UUID = Path(..., description="属性ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除商品属性
    """
    ProductAttributeService.delete_attribute(db, attribute_id)
    return success_response(message="删除属性成功")


# ==================== 商品属性值 API ====================

@router.get("/{attribute_id}/values", response_model=Dict[str, Any])
def get_attribute_values(
    attribute_id: UUID = Path(..., description="属性ID"),
    skip: int = Query(0, ge=0, description="分页起始位置"),
    limit: int = Query(100, ge=1, le=1000, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """
    获取指定属性的属性值列表
    """
    result = ProductAttributeValueService.get_attribute_values(
        db, attribute_id, skip, limit, search
    )
    return success_response(data=result)


@router.get("/values/{value_id}", response_model=Dict[str, Any])
def get_attribute_value(
    value_id: UUID = Path(..., description="属性值ID"),
    db: Session = Depends(get_db)
):
    """
    根据ID获取属性值详情
    """
    result = ProductAttributeValueService.get_attribute_value_by_id(db, value_id)
    return success_response(data=result)


@router.post("/{attribute_id}/values", status_code=status.HTTP_201_CREATED)
def create_attribute_value(
    *,
    attribute_id: UUID = Path(..., description="属性ID"),
    value: ProductAttributeValueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为指定属性创建新的属性值
    """
    result = ProductAttributeValueService.create_attribute_value(db, attribute_id, value)
    return success_response(data=result, message="创建属性值成功", code=201)


@router.post("/{attribute_id}/values/batch", status_code=status.HTTP_201_CREATED)
def batch_create_attribute_values(
    *,
    attribute_id: UUID = Path(..., description="属性ID"),
    values: List[ProductAttributeValueCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    批量创建属性值
    """
    result = ProductAttributeValueService.batch_create_attribute_values(db, attribute_id, values)
    return success_response(data=result, message=f"成功创建 {len(result)} 个属性值", code=201)


@router.put("/values/{value_id}")
def update_attribute_value(
    *,
    value_id: UUID = Path(..., description="属性值ID"),
    value: ProductAttributeValueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新属性值信息
    """
    result = ProductAttributeValueService.update_attribute_value(db, value_id, value)
    return success_response(data=result, message="更新属性值成功")


@router.delete("/values/{value_id}")
def delete_attribute_value(
    value_id: UUID = Path(..., description="属性值ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除属性值
    """
    ProductAttributeValueService.delete_attribute_value(db, value_id)
    return success_response(message="删除属性值成功")
