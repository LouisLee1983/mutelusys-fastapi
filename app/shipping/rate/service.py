# -*- coding: utf-8 -*-
"""
运费规则服务层
包含运费规则的CRUD操作
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, selectinload

from app.shipping.rate.models import ShippingRate
from app.shipping.rate.schema import ShippingRateCreate, ShippingRateUpdate


class ShippingRateService:
    """运费规则服务类"""

    @staticmethod
    def get_shipping_rates(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        method_id: Optional[UUID] = None,
        zone_id: Optional[UUID] = None,
        is_active: Optional[bool] = None
    ):
        """获取运费规则列表（静态方法）"""
        service = ShippingRateService(db)
        return service.get_all(
            skip=skip, limit=limit, method_id=method_id, 
            zone_id=zone_id, is_active=is_active
        )

    @staticmethod
    def get_shipping_rate_by_id(db: Session, rate_id: UUID):
        """根据ID获取运费规则（静态方法）"""
        service = ShippingRateService(db)
        return service.get_by_id(rate_id)

    @staticmethod
    def get_rate_by_method_zone_quantity(
        db: Session, 
        method_id: UUID, 
        zone_id: UUID, 
        quantity: int
    ):
        """根据快递方式、地区和件数获取运费规则（静态方法）"""
        service = ShippingRateService(db)
        return service.get_by_method_zone_quantity(method_id, zone_id, quantity)

    @staticmethod
    def create_shipping_rate(db: Session, rate_data: ShippingRateCreate):
        """创建运费规则（静态方法）"""
        service = ShippingRateService(db)
        return service.create(rate_data)

    @staticmethod
    def update_shipping_rate(db: Session, rate_id: UUID, rate_data: ShippingRateUpdate):
        """更新运费规则（静态方法）"""
        service = ShippingRateService(db)
        return service.update(rate_id, rate_data)

    @staticmethod
    def delete_shipping_rate(db: Session, rate_id: UUID) -> bool:
        """删除运费规则（静态方法）"""
        service = ShippingRateService(db)
        return service.delete(rate_id)

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        method_id: Optional[UUID] = None,
        zone_id: Optional[UUID] = None,
        is_active: Optional[bool] = None
    ) -> List[ShippingRate]:
        """获取运费规则列表"""
        query = self.db.query(ShippingRate).options(
            selectinload(ShippingRate.method),
            selectinload(ShippingRate.zone)
        )
        
        if is_active is not None:
            query = query.filter(ShippingRate.is_active == is_active)
        
        if method_id:
            query = query.filter(ShippingRate.shipping_method_id == method_id)
            
        if zone_id:
            query = query.filter(ShippingRate.shipping_zone_id == zone_id)
        
        return query.order_by(
            ShippingRate.sort_order, 
            ShippingRate.min_quantity,
            ShippingRate.created_at
        ).offset(skip).limit(limit).all()

    def get_by_id(self, rate_id: UUID) -> Optional[ShippingRate]:
        """根据ID获取运费规则"""
        return self.db.query(ShippingRate).options(
            selectinload(ShippingRate.method),
            selectinload(ShippingRate.zone)
        ).filter(ShippingRate.id == rate_id).first()

    def get_by_method_zone_quantity(
        self, 
        method_id: UUID, 
        zone_id: UUID, 
        quantity: int
    ) -> Optional[ShippingRate]:
        """根据快递方式、地区和件数获取运费规则"""
        return self.db.query(ShippingRate).filter(
            ShippingRate.shipping_method_id == method_id,
            ShippingRate.shipping_zone_id == zone_id,
            ShippingRate.is_active == True,
            ShippingRate.min_quantity <= quantity,
            # max_quantity为null表示无上限，或者quantity <= max_quantity
            (ShippingRate.max_quantity.is_(None)) | (ShippingRate.max_quantity >= quantity)
        ).order_by(ShippingRate.sort_order, ShippingRate.min_quantity).first()

    def create(self, rate_data: ShippingRateCreate) -> ShippingRate:
        """创建运费规则"""
        rate = ShippingRate(
            shipping_method_id=rate_data.shipping_method_id,
            shipping_zone_id=rate_data.shipping_zone_id,
            min_quantity=rate_data.min_quantity,
            max_quantity=rate_data.max_quantity,
            base_cost=rate_data.base_cost,
            per_item_cost=rate_data.per_item_cost,
            is_active=rate_data.is_active,
            sort_order=rate_data.sort_order
        )
        
        self.db.add(rate)
        self.db.commit()
        self.db.refresh(rate)
        return rate

    def update(self, rate_id: UUID, rate_data: ShippingRateUpdate) -> Optional[ShippingRate]:
        """更新运费规则"""
        rate = self.get_by_id(rate_id)
        if not rate:
            return None

        # 更新字段
        update_data = rate_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(rate, field, value)

        rate.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(rate)
        return rate

    def delete(self, rate_id: UUID) -> bool:
        """删除运费规则"""
        rate = self.get_by_id(rate_id)
        if not rate:
            return False

        self.db.delete(rate)
        self.db.commit()
        return True 