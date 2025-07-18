# -*- coding: utf-8 -*-
"""
运费地区API路由
包含地区运费配置和翻译的管理接口
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.common.response import ResponseModel, success_response, error_response
from app.shipping.zone.models import ShippingZone, ShippingZoneTranslation
from app.shipping.zone.schema import (
    ShippingZoneCreate, ShippingZoneUpdate, ShippingZoneResponse,
    ShippingZoneTranslationCreate, ShippingZoneTranslationUpdate,
    ShippingZoneTranslationResponse
)
from app.shipping.zone.service import ShippingZoneService

router = APIRouter(prefix="/zones")


# ==================== 运费地区管理接口 ====================

@router.get("/zones", response_model=ResponseModel)
async def get_shipping_zones(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[bool] = Query(None, description="是否启用筛选")
):
    """获取运费地区列表"""
    try:
        zones = ShippingZoneService.get_shipping_zones(
            db=db, skip=skip, limit=limit, search=search, is_active=is_active
        )
        
        # 统计总数
        total_query = db.query(ShippingZone)
        if is_active is not None:
            total_query = total_query.filter(ShippingZone.is_active == is_active)
        if search:
            total_query = total_query.filter(
                ShippingZone.name.ilike(f"%{search}%") |
                ShippingZone.code.ilike(f"%{search}%") |
                ShippingZone.countries.ilike(f"%{search}%")
            )
        total = total_query.count()
        
        return success_response(
            data={
                "list": [ShippingZoneResponse.from_orm(zone) for zone in zones],
                "total": total,
                "page": skip // limit + 1,
                "page_size": limit
            },
            message="获取运费地区列表成功"
        )
    except Exception as e:
        return error_response(message=f"获取运费地区列表失败: {str(e)}")


@router.get("/zones/{zone_id}", response_model=ResponseModel)
async def get_shipping_zone(zone_id: UUID, db: Session = Depends(get_db)):
    """获取运费地区详情"""
    try:
        zone = ShippingZoneService.get_shipping_zone_by_id(db, zone_id)
        if not zone:
            raise HTTPException(status_code=404, detail="运费地区不存在")
        
        return success_response(
            data=ShippingZoneResponse.from_orm(zone),
            message="获取运费地区详情成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"获取运费地区详情失败: {str(e)}")


@router.post("/zones", response_model=ResponseModel)
async def create_shipping_zone(
    zone_data: ShippingZoneCreate,
    db: Session = Depends(get_db)
):
    """创建运费地区"""
    try:
        # 检查代码是否已存在
        existing = db.query(ShippingZone).filter(
            ShippingZone.code == zone_data.code
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="运费地区代码已存在")
        
        zone = ShippingZoneService.create_shipping_zone(db, zone_data)
        return success_response(
            data=ShippingZoneResponse.from_orm(zone),
            message="创建运费地区成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"创建运费地区失败: {str(e)}")


@router.put("/zones/{zone_id}", response_model=ResponseModel)
async def update_shipping_zone(
    zone_id: UUID,
    zone_data: ShippingZoneUpdate,
    db: Session = Depends(get_db)
):
    """更新运费地区"""
    try:
        # 检查代码是否被其他记录使用
        if zone_data.code:
            existing = db.query(ShippingZone).filter(
                ShippingZone.code == zone_data.code,
                ShippingZone.id != zone_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="运费地区代码已存在")
        
        zone = ShippingZoneService.update_shipping_zone(db, zone_id, zone_data)
        if not zone:
            raise HTTPException(status_code=404, detail="运费地区不存在")
        
        return success_response(
            data=ShippingZoneResponse.from_orm(zone),
            message="更新运费地区成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"更新运费地区失败: {str(e)}")


@router.delete("/zones/{zone_id}", response_model=ResponseModel)
async def delete_shipping_zone(zone_id: UUID, db: Session = Depends(get_db)):
    """删除运费地区"""
    try:
        success = ShippingZoneService.delete_shipping_zone(db, zone_id)
        if not success:
            raise HTTPException(status_code=404, detail="运费地区不存在")
        
        return success_response(message="删除运费地区成功")
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"删除运费地区失败: {str(e)}")


# ==================== 运费地区翻译管理接口 ====================

@router.get("/zones/{zone_id}/translations", response_model=ResponseModel)
async def get_zone_translations(zone_id: UUID, db: Session = Depends(get_db)):
    """获取运费地区翻译列表"""
    try:
        # 检查运费地区是否存在
        zone = ShippingZoneService.get_shipping_zone_by_id(db, zone_id)
        if not zone:
            raise HTTPException(status_code=404, detail="运费地区不存在")
        
        translations = ShippingZoneService.get_translations(db, zone_id)
        return success_response(
            data=[ShippingZoneTranslationResponse.from_orm(trans) for trans in translations],
            message="获取翻译列表成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"获取翻译列表失败: {str(e)}")


@router.post("/zones/{zone_id}/translations", response_model=ResponseModel)
async def create_zone_translation(
    zone_id: UUID,
    translation_data: ShippingZoneTranslationCreate,
    db: Session = Depends(get_db)
):
    """创建运费地区翻译"""
    try:
        # 检查运费地区是否存在
        zone = ShippingZoneService.get_shipping_zone_by_id(db, zone_id)
        if not zone:
            raise HTTPException(status_code=404, detail="运费地区不存在")
        
        # 检查语言代码是否已存在
        existing = db.query(ShippingZoneTranslation).filter(
            ShippingZoneTranslation.shipping_zone_id == zone_id,
            ShippingZoneTranslation.language_code == translation_data.language_code
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="该语言的翻译已存在")
        
        translation = ShippingZoneService.create_translation(db, zone_id, translation_data)
        return success_response(
            data=ShippingZoneTranslationResponse.from_orm(translation),
            message="创建翻译成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"创建翻译失败: {str(e)}")


@router.put("/zones/{zone_id}/translations/{language_code}", response_model=ResponseModel)
async def update_zone_translation(
    zone_id: UUID,
    language_code: str,
    translation_data: ShippingZoneTranslationUpdate,
    db: Session = Depends(get_db)
):
    """更新运费地区翻译"""
    try:
        translation = ShippingZoneService.update_translation(
            db, zone_id, language_code, translation_data
        )
        if not translation:
            raise HTTPException(status_code=404, detail="翻译不存在")
        
        return success_response(
            data=ShippingZoneTranslationResponse.from_orm(translation),
            message="更新翻译成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"更新翻译失败: {str(e)}")


@router.delete("/zones/{zone_id}/translations/{language_code}", response_model=ResponseModel)
async def delete_zone_translation(
    zone_id: UUID,
    language_code: str,
    db: Session = Depends(get_db)
):
    """删除运费地区翻译"""
    try:
        success = ShippingZoneService.delete_translation(db, zone_id, language_code)
        if not success:
            raise HTTPException(status_code=404, detail="翻译不存在")
        
        return success_response(message="删除翻译成功")
    except HTTPException:
        raise
    except Exception as e:
        return error_response(message=f"删除翻译失败: {str(e)}")


# ==================== 公开接口 ====================

@router.get("/zones/by-country/{country_code}", response_model=ResponseModel)
async def get_zone_by_country(country_code: str, db: Session = Depends(get_db)):
    """根据国家代码获取运费地区"""
    try:
        zone = ShippingZoneService.get_zone_by_country(db, country_code)
        if not zone:
            return success_response(data=None, message="未找到对应的运费地区")
        
        return success_response(
            data=ShippingZoneResponse.from_orm(zone),
            message="获取运费地区成功"
        )
    except Exception as e:
        return error_response(message=f"获取运费地区失败: {str(e)}") 