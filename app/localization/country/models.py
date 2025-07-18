import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Country(Base):
    """国家表"""
    __tablename__ = 'countries'
    
    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(2), unique=True, nullable=False, comment='ISO 3166-1 alpha-2 国家代码')
    code3 = Column(String(3), unique=True, nullable=False, comment='ISO 3166-1 alpha-3 国家代码')
    name = Column(String(100), nullable=False, comment='英文名称')
    native_name = Column(String(100), comment='本地名称')
    currency = Column(String(3), comment='默认货币代码')
    phone_code = Column(String(10), comment='电话区号')
    status = Column(String(20), default='active', comment='状态 active/inactive')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    translations = relationship("CountryTranslation", back_populates="country", cascade="all, delete-orphan")
    regions = relationship("CountryRegion", back_populates="country", cascade="all, delete-orphan")


class CountryTranslation(Base):
    """国家翻译表"""
    __tablename__ = 'country_translations'
    
    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    country_id = Column(UUID(as_uuid=False), ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    language = Column(String(10), nullable=False, comment='语言代码 如 zh-CN, en-US, th-TH')
    name = Column(String(100), nullable=False, comment='翻译名称')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    country = relationship("Country", back_populates="translations")
    
    # 复合唯一约束
    __table_args__ = (
        {'comment': '国家翻译表'},
    )


class Region(Base):
    """地区表 - 用于关税和运费的地区分组"""
    __tablename__ = 'regions'
    
    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, comment='地区名称')
    code = Column(String(30), unique=True, nullable=False, comment='地区代码')
    description = Column(Text, comment='地区描述')
    status = Column(String(20), default='active', comment='状态 active/inactive')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    translations = relationship("RegionTranslation", back_populates="region", cascade="all, delete-orphan")
    countries = relationship("CountryRegion", back_populates="region", cascade="all, delete-orphan")


class RegionTranslation(Base):
    """地区翻译表"""
    __tablename__ = 'region_translations'
    
    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    region_id = Column(UUID(as_uuid=False), ForeignKey('regions.id', ondelete='CASCADE'), nullable=False)
    language = Column(String(10), nullable=False, comment='语言代码')
    name = Column(String(100), nullable=False, comment='翻译名称')
    description = Column(Text, comment='翻译描述')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    region = relationship("Region", back_populates="translations")


class CountryRegion(Base):
    """国家地区关联表"""
    __tablename__ = 'country_regions'
    
    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    country_id = Column(UUID(as_uuid=False), ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    region_id = Column(UUID(as_uuid=False), ForeignKey('regions.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 关系
    country = relationship("Country", back_populates="regions")
    region = relationship("Region", back_populates="countries")
    
    # 复合唯一约束
    __table_args__ = (
        {'comment': '国家地区关联表'},
    )