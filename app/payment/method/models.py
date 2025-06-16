import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class PaymentMethodStatus(str, enum.Enum):
    ACTIVE = "active"        # 激活
    INACTIVE = "inactive"    # 不可用
    TESTING = "testing"      # 测试模式


class PaymentMethod(Base):
    """支付方式表，包括名称、代码、状态、手续费、图标等"""
    __tablename__ = "payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False, unique=True, comment="支付方式代码")
    name = Column(String(100), nullable=False, comment="支付方式名称")
    description = Column(Text, nullable=True, comment="支付方式描述")
    instructions = Column(Text, nullable=True, comment="支付说明")
    status = Column(Enum(PaymentMethodStatus), default=PaymentMethodStatus.INACTIVE, nullable=False, comment="状态")
    
    # 手续费设置
    fee_type = Column(String(20), nullable=True, comment="手续费类型：fixed, percentage, mixed")
    fee_fixed = Column(Float, default=0, comment="固定手续费")
    fee_percentage = Column(Float, default=0, comment="百分比手续费")
    min_fee = Column(Float, nullable=True, comment="最低手续费")
    max_fee = Column(Float, nullable=True, comment="最高手续费")
    
    # 显示设置
    icon_url = Column(String(255), nullable=True, comment="图标URL")
    logo_url = Column(String(255), nullable=True, comment="Logo URL")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
    # 支付限制
    min_amount = Column(Float, nullable=True, comment="最小支付金额")
    max_amount = Column(Float, nullable=True, comment="最大支付金额")
    allowed_countries = Column(JSON, nullable=True, comment="允许的国家/地区")
    allowed_currencies = Column(JSON, nullable=True, comment="允许的货币")
    
    # 支付网关关联
    gateway_id = Column(UUID(as_uuid=True), ForeignKey("payment_gateways.id"), nullable=True)
    gateway_config = Column(JSON, nullable=True, comment="支付网关配置")
    
    # 系统设置
    is_default = Column(Boolean, default=False, comment="是否默认支付方式")
    is_cod = Column(Boolean, default=False, comment="是否货到付款")
    is_online = Column(Boolean, default=True, comment="是否在线支付")
    is_installment = Column(Boolean, default=False, comment="是否支持分期")
    is_public = Column(Boolean, default=True, comment="是否公开显示")
    
    # 额外设置
    meta_data = Column(JSON, nullable=True, comment="额外元数据")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    gateway = relationship("PaymentGateway", back_populates="payment_methods")
    transactions = relationship("PaymentTransaction", back_populates="payment_method")
