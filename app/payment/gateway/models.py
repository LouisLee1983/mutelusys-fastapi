import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class GatewayStatus(str, enum.Enum):
    ACTIVE = "active"        # 激活
    INACTIVE = "inactive"    # 不可用
    TESTING = "testing"      # 测试模式
    MAINTENANCE = "maintenance"  # 维护


class PaymentGateway(Base):
    """支付网关配置，如ShopeePay、GrabPay、PayPal等"""
    __tablename__ = "payment_gateways"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False, unique=True, comment="网关代码")
    name = Column(String(100), nullable=False, comment="网关名称")
    description = Column(Text, nullable=True, comment="网关描述")
    status = Column(Enum(GatewayStatus), default=GatewayStatus.INACTIVE, nullable=False, comment="状态")
    
    # 网关配置
    api_url = Column(String(255), nullable=True, comment="API URL")
    sandbox_api_url = Column(String(255), nullable=True, comment="沙盒API URL")
    api_key = Column(String(255), nullable=True, comment="API Key")
    api_secret = Column(String(255), nullable=True, comment="API Secret")
    merchant_id = Column(String(100), nullable=True, comment="商户ID")
    webhook_url = Column(String(255), nullable=True, comment="Webhook URL")
    callback_url = Column(String(255), nullable=True, comment="回调URL")
    
    # 环境设置
    is_sandbox = Column(Boolean, default=True, comment="是否沙盒环境")
    
    # 安全设置
    encryption_key = Column(String(255), nullable=True, comment="加密密钥")
    encryption_method = Column(String(50), nullable=True, comment="加密方法")
    signature_key = Column(String(255), nullable=True, comment="签名密钥")
    
    # 支持功能
    supports_refund = Column(Boolean, default=False, comment="是否支持退款")
    supports_partial_refund = Column(Boolean, default=False, comment="是否支持部分退款")
    supports_installment = Column(Boolean, default=False, comment="是否支持分期付款")
    supports_recurring = Column(Boolean, default=False, comment="是否支持周期性付款")
    supports_multi_currency = Column(Boolean, default=False, comment="是否支持多币种")
    
    # 支持的货币和国家
    supported_currencies = Column(JSON, nullable=True, comment="支持的货币")
    supported_countries = Column(JSON, nullable=True, comment="支持的国家/地区")
    
    # 结算信息
    settlement_currency = Column(String(3), nullable=True, comment="结算货币")
    settlement_period_days = Column(Integer, nullable=True, comment="结算周期(天)")
    
    # 显示设置
    logo_url = Column(String(255), nullable=True, comment="Logo URL")
    icon_url = Column(String(255), nullable=True, comment="图标URL")
    
    # 扩展设置
    config = Column(JSON, nullable=True, comment="额外配置信息")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    payment_methods = relationship("PaymentMethod", back_populates="gateway")
