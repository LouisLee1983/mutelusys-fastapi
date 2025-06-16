import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, JSON, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class CurrencyRate(Base):
    """货币汇率，用于多币种转换"""
    __tablename__ = "currency_rates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_currency = Column(String(3), nullable=False, comment="源货币代码")
    to_currency = Column(String(3), nullable=False, comment="目标货币代码")
    rate = Column(Float, nullable=False, comment="汇率")
    inverse_rate = Column(Float, nullable=False, comment="反向汇率")
    
    # 数据来源信息
    source = Column(String(100), nullable=True, comment="数据来源")
    source_timestamp = Column(DateTime, nullable=True, comment="源数据时间戳")
    
    # 有效期设置
    is_active = Column(Boolean, default=True, comment="是否激活")
    effective_date = Column(DateTime, nullable=False, default=datetime.utcnow, comment="生效日期")
    expiry_date = Column(DateTime, nullable=True, comment="过期日期")
    
    # 管理设置
    is_manual = Column(Boolean, default=False, comment="是否手动设置")
    is_default = Column(Boolean, default=False, comment="是否默认汇率")
    manual_adjustment = Column(Float, default=0, comment="手动调整百分比")
    
    # 汇率信息
    bid_rate = Column(Float, nullable=True, comment="买入汇率")
    ask_rate = Column(Float, nullable=True, comment="卖出汇率")
    mid_rate = Column(Float, nullable=True, comment="中间汇率")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 索引和约束
    __table_args__ = (
        # 确保同一天同一货币对只有一个激活的汇率记录
        UniqueConstraint('from_currency', 'to_currency', 'effective_date', 'is_active', 
                        name='uix_currency_rate_active'),
        # 索引优化查询
        Index('idx_currency_rate_from_to', 'from_currency', 'to_currency'),
        Index('idx_currency_rate_effective_date', 'effective_date'),
    )


class Currency(Base):
    """货币设置，包含代码、符号、格式等"""
    __tablename__ = "currencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(3), nullable=False, unique=True, comment="货币代码（ISO 4217）")
    name = Column(String(100), nullable=False, comment="货币名称")
    symbol = Column(String(10), nullable=True, comment="货币符号")
    
    # 格式设置
    decimal_places = Column(Integer, default=2, comment="小数位数")
    decimal_separator = Column(String(1), default=".", comment="小数分隔符")
    thousand_separator = Column(String(1), default=",", comment="千位分隔符")
    symbol_position = Column(String(10), default="before", comment="符号位置：before, after")
    
    # 显示设置
    format_pattern = Column(String(50), nullable=True, comment="格式模式，如 %s%v")
    
    # 系统设置
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_base_currency = Column(Boolean, default=False, comment="是否基础货币")
    is_default = Column(Boolean, default=False, comment="是否默认货币")
    
    # 地区设置
    countries = Column(JSON, nullable=True, comment="使用此货币的国家")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
