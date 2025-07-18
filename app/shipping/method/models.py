# -*- coding: utf-8 -*-
"""
快递方式模型
包含快递方式主表和翻译表
"""
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.db.base import Base


class TransportType(str, enum.Enum):
    """运输类型枚举"""
    AIR = "AIR"           # 空运
    STANDARD = "STANDARD" # 普通运输
    EXPRESS = "EXPRESS"   # 快递


class ShippingMethod(Base):
    """快递方式表"""
    __tablename__ = "shipping_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False, comment="快递方式代码")
    name = Column(String(100), nullable=False, comment="快递方式名称(中文默认)")
    company_name = Column(String(100), nullable=False, comment="快递公司名称(中文默认)")
    description = Column(Text, comment="描述(中文默认)")
    transport_type = Column(String(20), nullable=False, comment="运输类型")
    min_delivery_days = Column(Integer, comment="最小配送天数")
    max_delivery_days = Column(Integer, comment="最大配送天数")
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联关系
    translations = relationship("ShippingMethodTranslation", back_populates="method", cascade="all, delete-orphan")
    shipping_rates = relationship("ShippingRate", back_populates="method", cascade="all, delete-orphan")
    order_charge_items = relationship("OrderChargeItem", back_populates="shipping_method")
    order_shipping_infos = relationship("OrderShippingInfo", back_populates="shipping_method")


class ShippingMethodTranslation(Base):
    """快递方式翻译表"""
    __tablename__ = "shipping_method_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipping_method_id = Column(UUID(as_uuid=True), ForeignKey("shipping_methods.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码")
    name = Column(String(100), nullable=False, comment="快递方式名称翻译")
    company_name = Column(String(100), comment="快递公司名称翻译")
    description = Column(Text, comment="描述翻译")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联关系
    method = relationship("ShippingMethod", back_populates="translations")

    # 唯一约束
    __table_args__ = (
        {"comment": "快递方式翻译表"},
    ) 