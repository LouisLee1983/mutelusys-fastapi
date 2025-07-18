# -*- coding: utf-8 -*-
"""
快递方式服务层
包含快递方式及翻译的CRUD操作
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, selectinload

from app.shipping.method.models import ShippingMethod, ShippingMethodTranslation
from app.shipping.method.schema import (
    ShippingMethodCreate, ShippingMethodUpdate,
    ShippingMethodTranslationCreate, ShippingMethodTranslationUpdate
)


class ShippingMethodService:
    """快递方式服务类"""

    @staticmethod
    def get_shipping_methods(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        transport_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ):
        """获取快递方式列表（静态方法）"""
        service = ShippingMethodService(db)
        return service.get_all(skip=skip, limit=limit, search=search, transport_type=transport_type, is_active=is_active)

    @staticmethod
    def get_shipping_method_by_id(db: Session, method_id: UUID):
        """根据ID获取快递方式（静态方法）"""
        service = ShippingMethodService(db)
        return service.get_by_id(method_id)

    @staticmethod
    def create_shipping_method(db: Session, method_data: ShippingMethodCreate):
        """创建快递方式（静态方法）"""
        service = ShippingMethodService(db)
        return service.create(method_data)

    @staticmethod
    def update_shipping_method(db: Session, method_id: UUID, method_data: ShippingMethodUpdate):
        """更新快递方式（静态方法）"""
        service = ShippingMethodService(db)
        return service.update(method_id, method_data)

    @staticmethod
    def delete_shipping_method(db: Session, method_id: UUID) -> bool:
        """删除快递方式（静态方法）"""
        service = ShippingMethodService(db)
        return service.delete(method_id)

    @staticmethod
    def get_translations(db: Session, method_id: UUID):
        """获取快递方式翻译列表（静态方法）"""
        translations = db.query(ShippingMethodTranslation).filter(
            ShippingMethodTranslation.shipping_method_id == method_id
        ).all()
        return translations

    @staticmethod
    def create_translation(db: Session, method_id: UUID, translation_data: ShippingMethodTranslationCreate):
        """创建快递方式翻译（静态方法）"""
        translation = ShippingMethodTranslation(
            shipping_method_id=method_id,
            language_code=translation_data.language_code,
            name=translation_data.name,
            company_name=translation_data.company_name,
            description=translation_data.description
        )
        db.add(translation)
        db.commit()
        db.refresh(translation)
        return translation

    @staticmethod
    def update_translation(db: Session, method_id: UUID, language_code: str, translation_data: ShippingMethodTranslationUpdate):
        """更新快递方式翻译（静态方法）"""
        translation = db.query(ShippingMethodTranslation).filter(
            ShippingMethodTranslation.shipping_method_id == method_id,
            ShippingMethodTranslation.language_code == language_code
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
    def delete_translation(db: Session, method_id: UUID, language_code: str) -> bool:
        """删除快递方式翻译（静态方法）"""
        translation = db.query(ShippingMethodTranslation).filter(
            ShippingMethodTranslation.shipping_method_id == method_id,
            ShippingMethodTranslation.language_code == language_code
        ).first()
        
        if not translation:
            return False
        
        db.delete(translation)
        db.commit()
        return True

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, search: Optional[str] = None, transport_type: Optional[str] = None, is_active: Optional[bool] = None) -> List[ShippingMethod]:
        """获取快递方式列表"""
        query = self.db.query(ShippingMethod).options(selectinload(ShippingMethod.translations))
        
        if is_active is not None:
            query = query.filter(ShippingMethod.is_active == is_active)
        
        if transport_type:
            query = query.filter(ShippingMethod.transport_type == transport_type)
        
        if search:
            query = query.filter(
                ShippingMethod.name.ilike(f"%{search}%") |
                ShippingMethod.company_name.ilike(f"%{search}%") |
                ShippingMethod.code.ilike(f"%{search}%")
            )
        
        return query.order_by(ShippingMethod.sort_order, ShippingMethod.created_at).offset(skip).limit(limit).all()

    def get_by_id(self, method_id: UUID) -> Optional[ShippingMethod]:
        """根据ID获取快递方式"""
        return self.db.query(ShippingMethod).options(
            selectinload(ShippingMethod.translations)
        ).filter(ShippingMethod.id == method_id).first()

    def create(self, method_data: ShippingMethodCreate) -> ShippingMethod:
        """创建快递方式"""
        # 创建主记录
        method = ShippingMethod(
            code=method_data.code,
            name=method_data.name,
            company_name=method_data.company_name,
            description=method_data.description,
            transport_type=method_data.transport_type,
            min_delivery_days=method_data.min_delivery_days,
            max_delivery_days=method_data.max_delivery_days,
            is_active=method_data.is_active,
            sort_order=method_data.sort_order
        )
        
        self.db.add(method)
        self.db.flush()

        # 创建翻译记录
        if method_data.translations:
            for trans_data in method_data.translations:
                translation = ShippingMethodTranslation(
                    shipping_method_id=method.id,
                    language_code=trans_data.language_code,
                    name=trans_data.name,
                    company_name=trans_data.company_name,
                    description=trans_data.description
                )
                self.db.add(translation)

        self.db.commit()
        self.db.refresh(method)
        return method

    def update(self, method_id: UUID, method_data: ShippingMethodUpdate) -> Optional[ShippingMethod]:
        """更新快递方式"""
        method = self.get_by_id(method_id)
        if not method:
            return None

        # 更新字段
        update_data = method_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(method, field, value)

        method.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(method)
        return method

    def delete(self, method_id: UUID) -> bool:
        """删除快递方式"""
        method = self.get_by_id(method_id)
        if not method:
            return False

        self.db.delete(method)
        self.db.commit()
        return True 