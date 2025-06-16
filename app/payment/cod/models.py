import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class CashOnDelivery(Base):
    """货到付款设置，包含可用区域、限额等"""
    __tablename__ = "cash_on_delivery_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="设置名称")
    description = Column(Text, nullable=True, comment="设置描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 区域设置
    allowed_countries = Column(ARRAY(String), nullable=True, comment="允许的国家代码列表")
    allowed_regions = Column(JSON, nullable=True, comment="允许的区域详情，如{country: [regions]}格式")
    excluded_postcodes = Column(ARRAY(String), nullable=True, comment="排除的邮编列表")
    
    # 金额限制
    min_order_amount = Column(Float, nullable=True, comment="最小订单金额")
    max_order_amount = Column(Float, nullable=True, comment="最大订单金额")
    
    # 费用设置
    fee_type = Column(String(20), default="fixed", comment="费用类型：fixed, percentage, mixed")
    fee_amount = Column(Float, default=0, comment="固定费用金额")
    fee_percentage = Column(Float, default=0, comment="百分比费用")
    min_fee = Column(Float, nullable=True, comment="最小费用")
    max_fee = Column(Float, nullable=True, comment="最大费用")
    
    # 产品限制
    excluded_product_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除的产品分类ID列表")
    excluded_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除的产品ID列表")
    max_product_weight = Column(Float, nullable=True, comment="最大产品重量(克)")
    max_product_dimensions = Column(JSON, nullable=True, comment="最大产品尺寸，如{length, width, height}格式")
    
    # 客户限制
    allowed_customer_groups = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="允许的客户组ID列表")
    min_customer_orders = Column(Integer, nullable=True, comment="客户最小历史订单数")
    
    # 安全设置
    requires_verification_call = Column(Boolean, default=False, comment="是否需要电话验证")
    requires_id_verification = Column(Boolean, default=False, comment="是否需要身份验证")
    blacklisted_customers = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="黑名单客户ID列表")
    
    # 配送设置
    allowed_shipping_methods = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="允许的配送方式ID列表")
    delivery_timeframe = Column(String(100), nullable=True, comment="配送时间范围")
    
    # 业务规则
    collection_timeframe = Column(String(100), nullable=True, comment="收款时间范围")
    return_policy = Column(Text, nullable=True, comment="退货政策")
    
    # 通知设置
    notification_emails = Column(ARRAY(String), nullable=True, comment="通知邮箱列表")
    email_template = Column(Text, nullable=True, comment="邮件模板")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
