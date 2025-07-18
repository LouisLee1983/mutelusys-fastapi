# -*- coding: utf-8 -*-
"""
运费地区数据模型
包含地区运费配置和翻译表
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class ShippingZone(Base):
    """运费地区配置表"""
    __tablename__ = "shipping_zones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="地区ID")
    code = Column(String(20), unique=True, nullable=False, comment="地区代码")
    name = Column(String(100), nullable=False, comment="地区名称")
    description = Column(Text, comment="地区描述")
    countries = Column(Text, nullable=False, comment="包含的国家代码列表，逗号分隔")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

    # 关联关系
    translations = relationship("ShippingZoneTranslation", back_populates="zone", cascade="all, delete-orphan")
    shipping_rates = relationship("ShippingRate", back_populates="zone", cascade="all, delete-orphan")
    order_charge_items = relationship("OrderChargeItem", back_populates="shipping_zone")
    order_shipping_infos = relationship("OrderShippingInfo", back_populates="shipping_zone")

    def __repr__(self):
        return f"<ShippingZone(code='{self.code}', name='{self.name}')>"


class ShippingZoneTranslation(Base):
    """运费地区翻译表"""
    __tablename__ = "shipping_zone_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="翻译ID")
    shipping_zone_id = Column(UUID(as_uuid=True), ForeignKey("shipping_zones.id", ondelete="CASCADE"), nullable=False, comment="地区ID")
    language_code = Column(String(10), nullable=False, comment="语言代码")
    name = Column(String(100), nullable=False, comment="地区名称翻译")
    description = Column(Text, comment="地区描述翻译")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

    # 关联关系
    zone = relationship("ShippingZone", back_populates="translations")

    # 复合唯一索引
    __table_args__ = (
        {'comment': '运费地区翻译表'},
    )

    def __repr__(self):
        return f"<ShippingZoneTranslation(zone_id='{self.shipping_zone_id}', language='{self.language_code}')>" 