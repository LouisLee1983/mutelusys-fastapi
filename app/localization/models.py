import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class Language(Base):
    """语言设置表，包含代码、名称、状态等"""
    __tablename__ = "languages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), unique=True, nullable=False, index=True, comment="语言代码，如en-US, zh-CN")
    name = Column(String(50), nullable=False, comment="语言名称")
    native_name = Column(String(50), nullable=True, comment="本土语言名称")
    flag_image = Column(String(255), nullable=True, comment="国旗图片URL")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_default = Column(Boolean, default=False, comment="是否默认语言")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("TranslationValue", back_populates="language", cascade="all, delete-orphan")
    locale_preferences = relationship("LocalePreference", back_populates="language")


class Currency(Base):
    """货币设置表，包含代码、符号、格式等"""
    __tablename__ = "currencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(3), unique=True, nullable=False, index=True, comment="货币代码，如USD, CNY")
    name = Column(String(50), nullable=False, comment="货币名称")
    symbol = Column(String(10), nullable=False, comment="货币符号")
    decimal_places = Column(Integer, default=2, comment="小数位数")
    decimal_separator = Column(String(1), default=".", comment="小数分隔符")
    thousand_separator = Column(String(1), default=",", comment="千位分隔符")
    symbol_position = Column(String(10), default="before", comment="符号位置：before/after")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_default = Column(Boolean, default=False, comment="是否默认货币")
    exchange_rate = Column(Float, default=1.0, comment="与基准货币的汇率")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    locale_preferences = relationship("LocalePreference", back_populates="currency")


class CountryRegion(Base):
    """国家和地区信息表，包含税率、时区等"""
    __tablename__ = "country_regions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(3), unique=True, nullable=False, index=True, comment="国家/地区代码，如US, CN")
    name = Column(String(100), nullable=False, comment="国家/地区名称")
    native_name = Column(String(100), nullable=True, comment="本土名称")
    flag_image = Column(String(255), nullable=True, comment="国旗图片URL")
    phone_code = Column(String(10), nullable=True, comment="电话区号")
    tax_rate = Column(Float, nullable=True, comment="标准税率")
    timezone = Column(String(50), nullable=True, comment="主要时区")
    continent = Column(String(20), nullable=True, comment="所属大洲")
    is_active = Column(Boolean, default=True, comment="是否激活")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    locale_preferences = relationship("LocalePreference", back_populates="country_region")
    cultural_localizations = relationship("CulturalLocalization", back_populates="country_region")


class TranslationKey(Base):
    """翻译键表，用于系统文本翻译"""
    __tablename__ = "translation_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(255), unique=True, nullable=False, index=True, comment="翻译键")
    description = Column(String(255), nullable=True, comment="说明")
    module = Column(String(50), nullable=True, comment="所属模块")
    is_system = Column(Boolean, default=False, comment="是否系统内置")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    values = relationship("TranslationValue", back_populates="translation_key", cascade="all, delete-orphan")


class TranslationValue(Base):
    """翻译值表，用于存储各语言的翻译内容"""
    __tablename__ = "translation_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    translation_key_id = Column(UUID(as_uuid=True), ForeignKey("translation_keys.id", ondelete="CASCADE"), nullable=False)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id", ondelete="CASCADE"), nullable=False)
    value = Column(Text, nullable=False, comment="翻译内容")
    is_approved = Column(Boolean, default=True, comment="是否已审核")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translation_key = relationship("TranslationKey", back_populates="values")
    language = relationship("Language", back_populates="translations")

    # 联合唯一索引
    __table_args__ = (
        {},
    )


class LocalePreference(Base):
    """区域偏好设置表，如日期格式、数字格式等"""
    __tablename__ = "locale_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, comment="用户ID，可为空表示系统默认")
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=False)
    country_region_id = Column(UUID(as_uuid=True), ForeignKey("country_regions.id"), nullable=False)
    date_format = Column(String(20), default="YYYY-MM-DD", comment="日期格式")
    time_format = Column(String(20), default="HH:mm:ss", comment="时间格式")
    number_format = Column(String(20), default="#,##0.00", comment="数字格式")
    first_day_of_week = Column(Integer, default=1, comment="每周第一天，1=周一")
    measurement_unit = Column(String(10), default="metric", comment="度量单位：metric/imperial")
    timezone = Column(String(50), nullable=True, comment="时区")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    language = relationship("Language", back_populates="locale_preferences")
    currency = relationship("Currency", back_populates="locale_preferences")
    country_region = relationship("CountryRegion", back_populates="locale_preferences")


class CulturalLocalization(Base):
    """文化本地化表，不同区域特有的文化符号和意义翻译"""
    __tablename__ = "cultural_localizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_region_id = Column(UUID(as_uuid=True), ForeignKey("country_regions.id"), nullable=False)
    symbol_id = Column(UUID(as_uuid=True), ForeignKey("product_symbols.id", ondelete="CASCADE"), nullable=True, comment="符号ID，可空")
    element_name = Column(String(100), nullable=False, comment="文化元素名称")
    local_meaning = Column(Text, nullable=False, comment="本地文化含义")
    usage_context = Column(Text, nullable=True, comment="使用场景")
    local_taboos = Column(Text, nullable=True, comment="文化禁忌")
    recommendations = Column(Text, nullable=True, comment="建议使用方式")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    country_region = relationship("CountryRegion", back_populates="cultural_localizations")
    translations = relationship("CulturalLocalizationTranslation", back_populates="cultural_localization", cascade="all, delete-orphan")


class CulturalLocalizationTranslation(Base):
    """文化本地化多语言翻译表"""
    __tablename__ = "cultural_localization_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cultural_localization_id = Column(UUID(as_uuid=True), ForeignKey("cultural_localizations.id", ondelete="CASCADE"), nullable=False)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id", ondelete="CASCADE"), nullable=False)
    element_name = Column(String(100), nullable=False, comment="文化元素名称")
    local_meaning = Column(Text, nullable=False, comment="本地文化含义")
    usage_context = Column(Text, nullable=True, comment="使用场景")
    local_taboos = Column(Text, nullable=True, comment="文化禁忌")
    recommendations = Column(Text, nullable=True, comment="建议使用方式")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    cultural_localization = relationship("CulturalLocalization", back_populates="translations")

    # 联合唯一索引
    __table_args__ = (
        {},
    )
