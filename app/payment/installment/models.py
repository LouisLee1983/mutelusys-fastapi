import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class InstallmentPlanStatus(str, enum.Enum):
    ACTIVE = "active"          # 激活
    INACTIVE = "inactive"      # 不可用
    PROMOTIONAL = "promotional"  # 促销活动


class InstallmentPlan(Base):
    """分期付款计划，包含期数、手续费等"""
    __tablename__ = "installment_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="计划名称")
    code = Column(String(50), nullable=False, unique=True, comment="计划代码")
    description = Column(Text, nullable=True, comment="计划描述")
    status = Column(Enum(InstallmentPlanStatus), default=InstallmentPlanStatus.INACTIVE, nullable=False, comment="状态")
    
    # 分期设置
    number_of_installments = Column(Integer, nullable=False, comment="分期数量")
    installment_interval_days = Column(Integer, default=30, comment="分期间隔天数")
    min_down_payment_percentage = Column(Float, default=0, comment="最小首付百分比")
    
    # 费用设置
    interest_rate = Column(Float, default=0, comment="年利率")
    fee_fixed = Column(Float, default=0, comment="固定手续费")
    fee_percentage = Column(Float, default=0, comment="百分比手续费")
    
    # 限制设置
    min_order_amount = Column(Float, nullable=True, comment="最小订单金额")
    max_order_amount = Column(Float, nullable=True, comment="最大订单金额")
    allowed_currencies = Column(ARRAY(String), nullable=True, comment="允许的货币代码列表")
    allowed_countries = Column(ARRAY(String), nullable=True, comment="允许的国家代码列表")
    
    # 支付网关关联
    payment_gateway_id = Column(UUID(as_uuid=True), ForeignKey("payment_gateways.id"), nullable=True)
    gateway_plan_id = Column(String(100), nullable=True, comment="网关端计划ID")
    
    # 客户限制
    allowed_customer_groups = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="允许的客户组ID列表")
    min_customer_orders = Column(Integer, nullable=True, comment="客户最小历史订单数")
    requires_credit_check = Column(Boolean, default=False, comment="是否需要信用检查")
    
    # 产品限制
    allowed_product_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="允许的产品分类ID列表")
    excluded_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除的产品ID列表")
    
    # 促销设置
    is_promotional = Column(Boolean, default=False, comment="是否促销计划")
    promotion_start_date = Column(DateTime, nullable=True, comment="促销开始日期")
    promotion_end_date = Column(DateTime, nullable=True, comment="促销结束日期")
    
    # 显示设置
    icon_url = Column(String(255), nullable=True, comment="图标URL")
    logo_url = Column(String(255), nullable=True, comment="Logo URL")
    promotion_banner_url = Column(String(255), nullable=True, comment="促销横幅URL")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
    # 用户界面设置
    ui_template = Column(String(50), nullable=True, comment="UI模板")
    payment_schedule_template = Column(Text, nullable=True, comment="还款计划模板")
    terms_and_conditions = Column(Text, nullable=True, comment="条款和条件")
    
    # 额外设置
    meta_data = Column(JSON, nullable=True, comment="额外元数据")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    payment_gateway = relationship("PaymentGateway")
