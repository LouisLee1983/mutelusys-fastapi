# -*- coding: utf-8 -*-
"""
运费地区服务层
包含地区运费配置及翻译的CRUD操作
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, selectinload

from app.shipping.zone.models import ShippingZone, ShippingZoneTranslation
from app.shipping.zone.schema import (
    ShippingZoneCreate, ShippingZoneUpdate,
    ShippingZoneTranslationCreate, ShippingZoneTranslationUpdate
)


class ShippingZoneService:
    """运费地区服务类"""

    @staticmethod
    def get_shipping_zones(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ):
        """获取运费地区列表（静态方法）"""
        service = ShippingZoneService(db)
        return service.get_all(skip=skip, limit=limit, search=search, is_active=is_active)

    @staticmethod
    def get_shipping_zone_by_id(db: Session, zone_id: UUID):
        """根据ID获取运费地区（静态方法）"""
        service = ShippingZoneService(db)
        return service.get_by_id(zone_id)

    @staticmethod
    def get_zone_by_country(db: Session, country_code: str):
        """根据国家代码获取运费地区（静态方法）"""
        service = ShippingZoneService(db)
        return service.get_by_country(country_code)

    @staticmethod
    def create_shipping_zone(db: Session, zone_data: ShippingZoneCreate):
        """创建运费地区（静态方法）"""
        service = ShippingZoneService(db)
        return service.create(zone_data)

    @staticmethod
    def update_shipping_zone(db: Session, zone_id: UUID, zone_data: ShippingZoneUpdate):
        """更新运费地区（静态方法）"""
        service = ShippingZoneService(db)
        return service.update(zone_id, zone_data)

    @staticmethod
    def delete_shipping_zone(db: Session, zone_id: UUID) -> bool:
        """删除运费地区（静态方法）"""
        service = ShippingZoneService(db)
        return service.delete(zone_id)

    @staticmethod
    def get_translations(db: Session, zone_id: UUID):
        """获取运费地区翻译列表（静态方法）"""
        translations = db.query(ShippingZoneTranslation).filter(
            ShippingZoneTranslation.shipping_zone_id == zone_id
        ).all()
        return translations

    @staticmethod
    def create_translation(db: Session, zone_id: UUID, translation_data: ShippingZoneTranslationCreate):
        """创建运费地区翻译（静态方法）"""
        translation = ShippingZoneTranslation(
            shipping_zone_id=zone_id,
            language_code=translation_data.language_code,
            name=translation_data.name,
            description=translation_data.description
        )
        db.add(translation)
        db.commit()
        db.refresh(translation)
        return translation

    @staticmethod
    def update_translation(db: Session, zone_id: UUID, language_code: str, translation_data: ShippingZoneTranslationUpdate):
        """更新运费地区翻译（静态方法）"""
        translation = db.query(ShippingZoneTranslation).filter(
            ShippingZoneTranslation.shipping_zone_id == zone_id,
            ShippingZoneTranslation.language_code == language_code
        ).first()
        
        if not translation:
            return None
        
        update_data = translation_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(translation, field, value)
        
        translation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(translation)
        return translation

    @staticmethod
    def delete_translation(db: Session, zone_id: UUID, language_code: str) -> bool:
        """删除运费地区翻译（静态方法）"""
        translation = db.query(ShippingZoneTranslation).filter(
            ShippingZoneTranslation.shipping_zone_id == zone_id,
            ShippingZoneTranslation.language_code == language_code
        ).first()
        
        if not translation:
            return False
        
        db.delete(translation)
        db.commit()
        return True

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, search: Optional[str] = None, is_active: Optional[bool] = None) -> List[ShippingZone]:
        """获取运费地区列表"""
        query = self.db.query(ShippingZone).options(selectinload(ShippingZone.translations))
        
        if is_active is not None:
            query = query.filter(ShippingZone.is_active == is_active)
        
        if search:
            query = query.filter(
                ShippingZone.name.ilike(f"%{search}%") |
                ShippingZone.code.ilike(f"%{search}%") |
                ShippingZone.countries.ilike(f"%{search}%")
            )
        
        return query.order_by(ShippingZone.sort_order, ShippingZone.created_at).offset(skip).limit(limit).all()

    def get_by_id(self, zone_id: UUID) -> Optional[ShippingZone]:
        """根据ID获取运费地区"""
        return self.db.query(ShippingZone).options(
            selectinload(ShippingZone.translations)
        ).filter(ShippingZone.id == zone_id).first()

    def get_by_country(self, country_code: str) -> Optional[ShippingZone]:
        """根据国家代码获取运费地区"""
        country_code = country_code.upper()
        return self.db.query(ShippingZone).filter(
            ShippingZone.is_active == True,
            ShippingZone.countries.ilike(f"%{country_code}%")
        ).first()

    def create(self, zone_data: ShippingZoneCreate) -> ShippingZone:
        """创建运费地区"""
        # 创建主记录
        zone = ShippingZone(
            code=zone_data.code,
            name=zone_data.name,
            description=zone_data.description,
            countries=zone_data.countries,
            is_active=zone_data.is_active,
            sort_order=zone_data.sort_order
        )
        
        self.db.add(zone)
        self.db.flush()

        # 创建翻译记录
        if zone_data.translations:
            for trans_data in zone_data.translations:
                translation = ShippingZoneTranslation(
                    shipping_zone_id=zone.id,
                    language_code=trans_data.language_code,
                    name=trans_data.name,
                    description=trans_data.description
                )
                self.db.add(translation)

        self.db.commit()
        self.db.refresh(zone)
        return zone

    def update(self, zone_id: UUID, zone_data: ShippingZoneUpdate) -> Optional[ShippingZone]:
        """更新运费地区"""
        zone = self.get_by_id(zone_id)
        if not zone:
            return None

        # 更新字段
        update_data = zone_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(zone, field, value)

        zone.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete(self, zone_id: UUID) -> bool:
        """删除运费地区"""
        zone = self.get_by_id(zone_id)
        if not zone:
            return False

        self.db.delete(zone)
        self.db.commit()
        return True 