# -*- coding: utf-8 -*-
"""
快递方式API路由
包含快递方式和翻译的管理接口
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.common.response import ResponseModel, success_response, error_response
from app.shipping.method.models import ShippingMethod, ShippingMethodTranslation
from app.shipping.method.schema import (
    ShippingMethodCreate, ShippingMethodUpdate, ShippingMethodResponse,
    ShippingMethodTranslationCreate, ShippingMethodTranslationUpdate,
    ShippingMethodTranslationResponse
)
from app.shipping.method.service import ShippingMethodService

router = APIRouter(prefix="/methods")


# ==================== 快递方式管理接口 ====================

@router.get("/shipping-methods", response_model=ResponseModel)
async def get_shipping_methods(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    transport_type: Optional[str] = Query(None, description="运输类型筛选"),
    is_active: Optional[bool] = Query(None, description="是否启用筛选")
):
    """获取快递方式列表"""
    try:
        methods = ShippingMethodService.get_shipping_methods(
            db=db, skip=skip, limit=limit, search=search,
            transport_type=transport_type, is_active=is_active
        )
        
        # 统计总数
        total_query = db.query(ShippingMethod)
        if is_active is not None:
            total_query = total_query.filter(ShippingMethod.is_active == is_active)
        if transport_type:
            total_query = total_query.filter(ShippingMethod.transport_type == transport_type)
        if search:
            total_query = total_query.filter(
                ShippingMethod.name.ilike(f"%{search}%") |
                ShippingMethod.company_name.ilike(f"%{search}%") |
                ShippingMethod.code.ilike(f"%{search}%")
            )
        total = total_query.count()
        
        return success_response(
            data={
                "list": [ShippingMethodResponse.from_orm(method) for method in methods],
                "total": total,
                "page": skip // limit + 1,
                "page_size": limit
            },
            message="获取快递方式列表成功"
        )
    except Exception as e:
        return error_response(message=f"获取快递方式列表失败: {str(e)}")


@router.get("/shipping-methods/{method_id}", response_model=ResponseModel)
async def get_shipping_method(method_id: UUID, db: Session = Depends(get_db)):
    """获取快递方式详情"""
    try:
        method = ShippingMethodService.get_shipping_method_by_id(db, method_id)
        if not method:
            raise HTTPException(status_code=404, detail="快递方式不存在")
        
        return success_response(
            data=ShippingMethodResponse.from_orm(method),
            message="获取快递方式详情成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"获取快递方式详情失败: {str(e)}")


@router.post("/shipping-methods", response_model=ResponseModel)
async def create_shipping_method(
    method_data: ShippingMethodCreate,
    db: Session = Depends(get_db)
):
    """创建快递方式"""
    try:
        # 检查代码是否已存在
        existing = db.query(ShippingMethod).filter(
            ShippingMethod.code == method_data.code
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="快递方式代码已存在")
        
        method = ShippingMethodService.create_shipping_method(db, method_data)
        return success_response(
            data=ShippingMethodResponse.from_orm(method),
            message="创建快递方式成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"创建快递方式失败: {str(e)}")


@router.put("/shipping-methods/{method_id}", response_model=ResponseModel)
async def update_shipping_method(
    method_id: UUID,
    method_data: ShippingMethodUpdate,
    db: Session = Depends(get_db)
):
    """更新快递方式"""
    try:
        # 检查代码是否被其他记录使用
        if method_data.code:
            existing = db.query(ShippingMethod).filter(
                ShippingMethod.code == method_data.code,
                ShippingMethod.id != method_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="快递方式代码已存在")
        
        method = ShippingMethodService.update_shipping_method(db, method_id, method_data)
        if not method:
            raise HTTPException(status_code=404, detail="快递方式不存在")
        
        return success_response(
            data=ShippingMethodResponse.from_orm(method),
            message="更新快递方式成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"更新快递方式失败: {str(e)}")


@router.delete("/shipping-methods/{method_id}", response_model=ResponseModel)
async def delete_shipping_method(method_id: UUID, db: Session = Depends(get_db)):
    """删除快递方式"""
    try:
        success = ShippingMethodService.delete_shipping_method(db, method_id)
        if not success:
            raise HTTPException(status_code=404, detail="快递方式不存在")
        
        return success_response(message="删除快递方式成功")
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"删除快递方式失败: {str(e)}")


# ==================== 快递方式翻译管理接口 ====================

@router.get("/methods/{method_id}/translations", response_model=ResponseModel)
async def get_method_translations(method_id: UUID, db: Session = Depends(get_db)):
    """获取快递方式翻译列表"""
    try:
        # 检查快递方式是否存在
        method = ShippingMethodService.get_shipping_method_by_id(db, method_id)
        if not method:
            raise HTTPException(status_code=404, detail="快递方式不存在")
        
        translations = ShippingMethodService.get_translations(db, method_id)
        return success_response(
            data=[ShippingMethodTranslationResponse.from_orm(trans) for trans in translations],
            message="获取翻译列表成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"获取翻译列表失败: {str(e)}")


@router.post("/methods/{method_id}/translations", response_model=ResponseModel)
async def create_method_translation(
    method_id: UUID,
    translation_data: ShippingMethodTranslationCreate,
    db: Session = Depends(get_db)
):
    """创建快递方式翻译"""
    try:
        # 检查快递方式是否存在
        method = ShippingMethodService.get_shipping_method_by_id(db, method_id)
        if not method:
            raise HTTPException(status_code=404, detail="快递方式不存在")
        
        # 检查语言代码是否已存在
        existing = db.query(ShippingMethodTranslation).filter(
            ShippingMethodTranslation.shipping_method_id == method_id,
            ShippingMethodTranslation.language_code == translation_data.language_code
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="该语言的翻译已存在")
        
        translation = ShippingMethodService.create_translation(db, method_id, translation_data)
        return success_response(
            data=ShippingMethodTranslationResponse.from_orm(translation),
            message="创建翻译成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"创建翻译失败: {str(e)}")


@router.put("/methods/{method_id}/translations/{language_code}", response_model=ResponseModel)
async def update_method_translation(
    method_id: UUID,
    language_code: str,
    translation_data: ShippingMethodTranslationUpdate,
    db: Session = Depends(get_db)
):
    """更新快递方式翻译"""
    try:
        translation = ShippingMethodService.update_translation(
            db, method_id, language_code, translation_data
        )
        if not translation:
            raise HTTPException(status_code=404, detail="翻译不存在")
        
        return success_response(
            data=ShippingMethodTranslationResponse.from_orm(translation),
            message="更新翻译成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"更新翻译失败: {str(e)}")


@router.delete("/methods/{method_id}/translations/{language_code}", response_model=ResponseModel)
async def delete_method_translation(
    method_id: UUID,
    language_code: str,
    db: Session = Depends(get_db)
):
    """删除快递方式翻译"""
    try:
        success = ShippingMethodService.delete_translation(db, method_id, language_code)
        if not success:
            raise HTTPException(status_code=404, detail="翻译不存在")
        
        return success_response(message="删除翻译成功")
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"删除翻译失败: {str(e)}") 