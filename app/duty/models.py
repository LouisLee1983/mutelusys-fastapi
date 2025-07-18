import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class DutyZone(Base):
    """关税区域表"""
    __tablename__ = 'duty_zones'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment='关税区域名称')
    tax_free_threshold = Column(Float, default=0.0, comment='免税阈值金额')
    default_tax_rate = Column(Float, default=0.0, comment='默认税率 0.08表示8%')
    currency = Column(String(3), default='USD', comment='计算货币')
    status = Column(String(20), default='active', comment='状态 active/inactive')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    translations = relationship("DutyZoneTranslation", back_populates="zone", cascade="all, delete-orphan")
    countries = relationship("DutyZoneCountry", back_populates="zone", cascade="all, delete-orphan")
    rules = relationship("DutyRule", back_populates="zone", cascade="all, delete-orphan")


class DutyZoneTranslation(Base):
    """关税区域翻译表"""
    __tablename__ = 'duty_zone_translations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = Column(UUID(as_uuid=True), ForeignKey('duty_zones.id', ondelete='CASCADE'), nullable=False)
    language = Column(String(10), nullable=False, comment='语言代码')
    name = Column(String(100), nullable=False, comment='翻译名称')
    description = Column(Text, comment='描述')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    zone = relationship("DutyZone", back_populates="translations")


class DutyZoneCountry(Base):
    """关税区域国家关联表"""
    __tablename__ = 'duty_zone_countries'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = Column(UUID(as_uuid=True), ForeignKey('duty_zones.id', ondelete='CASCADE'), nullable=False)
    country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 关系
    zone = relationship("DutyZone", back_populates="countries")
    # country关系需要在localization模块中定义


class ProductDutyCategory(Base):
    """商品关税分类表"""
    __tablename__ = 'product_duty_categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment='分类名称')
    tax_rate = Column(Float, comment='该分类的税率，可覆盖地区默认税率')
    status = Column(String(20), default='active', comment='状态 active/inactive')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    translations = relationship("ProductDutyCategoryTranslation", back_populates="category", cascade="all, delete-orphan")
    rules = relationship("DutyRule", back_populates="category", cascade="all, delete-orphan")


class ProductDutyCategoryTranslation(Base):
    """商品关税分类翻译表"""
    __tablename__ = 'product_duty_category_translations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey('product_duty_categories.id', ondelete='CASCADE'), nullable=False)
    language = Column(String(10), nullable=False, comment='语言代码')
    name = Column(String(100), nullable=False, comment='翻译名称')
    description = Column(Text, comment='描述')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    category = relationship("ProductDutyCategory", back_populates="translations")


class DutyRule(Base):
    """关税规则表"""
    __tablename__ = 'duty_rules'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = Column(UUID(as_uuid=True), ForeignKey('duty_zones.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('product_duty_categories.id', ondelete='SET NULL'), nullable=True, comment='商品分类ID，null表示通用规则')
    tax_free_amount = Column(Float, default=0.0, comment='免税金额')
    tax_rate = Column(Float, nullable=False, comment='税率，覆盖默认税率')
    min_tax_amount = Column(Float, default=0.0, comment='最低征税额')
    max_tax_amount = Column(Float, comment='最高征税额，可选')
    priority = Column(Integer, default=1, comment='优先级，数字越小优先级越高')
    valid_from = Column(DateTime, default=datetime.utcnow, comment='生效时间')
    valid_to = Column(DateTime, comment='失效时间，可选')
    status = Column(String(20), default='active', comment='状态 active/inactive')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    zone = relationship("DutyZone", back_populates="rules")
    category = relationship("ProductDutyCategory", back_populates="rules")


class OrderDutyCharge(Base):
    """订单关税记录表"""
    __tablename__ = 'order_duty_charges'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, comment='订单ID')
    country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'), nullable=False, comment='收货国家ID')
    duty_zone_id = Column(UUID(as_uuid=True), ForeignKey('duty_zones.id'), nullable=False, comment='关税区域ID')
    taxable_amount = Column(Float, nullable=False, comment='应税金额 商品金额+运费')
    tax_rate = Column(Float, nullable=False, comment='适用税率')
    duty_amount = Column(Float, nullable=False, comment='关税金额')
    currency = Column(String(3), nullable=False, comment='货币')
    calculation_details = Column(Text, comment='JSON格式的计算明细')
    status = Column(String(20), default='pending', comment='状态 pending/paid/refunded')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系将在order模块中定义
    # order = relationship("Order", back_populates="duty_charge")
    # country = relationship("Country")
    # duty_zone = relationship("DutyZone")