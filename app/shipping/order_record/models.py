# -*- coding: utf-8 -*-
"""
订单运费记录数据模型
包含订单收费项目和运费记录表
"""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, DECIMAL, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class OrderChargeItem(Base):
    """订单收费项目表"""
    __tablename__ = "order_charge_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="收费项目ID")
    order_id = Column(String(50), nullable=False, index=True, comment="订单号")
    item_type = Column(String(20), nullable=False, comment="收费项目类型（shipping/tax/discount等）")
    item_code = Column(String(50), comment="项目代码")
    item_name = Column(String(100), nullable=False, comment="项目名称")
    item_description = Column(Text, comment="项目描述")
    
    # 金额信息
    amount = Column(DECIMAL(10, 2), nullable=False, comment="收费金额")
    currency_code = Column(String(3), nullable=False, default="USD", comment="货币代码")
    
    # 关联信息（用于快递费）
    shipping_method_id = Column(UUID(as_uuid=True), ForeignKey("shipping_methods.id"), comment="快递方式ID")
    shipping_zone_id = Column(UUID(as_uuid=True), ForeignKey("shipping_zones.id"), comment="运费地区ID")
    free_shipping_rule_id = Column(UUID(as_uuid=True), ForeignKey("free_shipping_rules.id"), comment="免运费规则ID")
    
    # 扩展信息
    item_metadata = Column(JSON, comment="扩展元数据")
    
    # 状态和时间
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关联关系
    shipping_method = relationship("ShippingMethod", back_populates="order_charge_items")
    shipping_zone = relationship("ShippingZone", back_populates="order_charge_items")
    free_shipping_rule = relationship("FreeShippingRule", back_populates="order_charge_items")

    def __repr__(self):
        return f"<OrderChargeItem(order_id='{self.order_id}', type='{self.item_type}', amount={self.amount})>"


class OrderShippingInfo(Base):
    """订单运费记录表"""
    __tablename__ = "order_shipping_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="运费记录ID")
    order_id = Column(String(50), nullable=False, unique=True, index=True, comment="订单号")
    
    # 收货地址信息
    country_code = Column(String(2), nullable=False, comment="收货国家代码")
    state_province = Column(String(50), comment="州/省")
    city = Column(String(50), comment="城市")
    postal_code = Column(String(20), comment="邮政编码")
    full_address = Column(Text, comment="完整地址")
    
    # 商品信息
    total_quantity = Column(Integer, nullable=False, comment="商品总件数")
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment="商品总金额")
    currency_code = Column(String(3), nullable=False, default="USD", comment="货币代码")
    
    # 快递信息
    shipping_method_id = Column(UUID(as_uuid=True), ForeignKey("shipping_methods.id"), nullable=False, comment="选择的快递方式ID")
    shipping_method_code = Column(String(20), nullable=False, comment="快递方式代码")
    shipping_method_name = Column(String(100), nullable=False, comment="快递方式名称")
    shipping_company = Column(String(100), comment="快递公司名称")
    transport_type = Column(String(20), comment="运输类型")
    
    # 运费地区信息
    shipping_zone_id = Column(UUID(as_uuid=True), ForeignKey("shipping_zones.id"), nullable=False, comment="运费地区ID")
    shipping_zone_name = Column(String(100), nullable=False, comment="运费地区名称")
    
    # 运费计算结果
    base_shipping_cost = Column(DECIMAL(10, 2), nullable=False, comment="基础运费")
    discount_amount = Column(DECIMAL(10, 2), nullable=False, default=0, comment="折扣金额")
    final_shipping_cost = Column(DECIMAL(10, 2), nullable=False, comment="最终运费")
    
    # 免运费信息
    is_free_shipping = Column(Boolean, nullable=False, default=False, comment="是否免运费")
    free_shipping_rule_id = Column(UUID(as_uuid=True), ForeignKey("free_shipping_rules.id"), comment="应用的免运费规则ID")
    free_shipping_rule_name = Column(String(100), comment="免运费规则名称")
    free_shipping_reason = Column(String(200), comment="免运费原因")
    savings_amount = Column(DECIMAL(10, 2), comment="节省的运费金额")
    
    # 配送时间预估
    estimated_delivery_days = Column(Integer, comment="预估配送天数")
    min_delivery_days = Column(Integer, comment="最小配送天数")
    max_delivery_days = Column(Integer, comment="最大配送天数")
    delivery_time_text = Column(String(100), comment="配送时间文本描述")
    
    # 跟踪信息
    tracking_number = Column(String(100), comment="快递单号")
    tracking_url = Column(String(500), comment="跟踪链接")
    shipping_status = Column(String(20), default="pending", comment="发货状态")
    shipped_at = Column(DateTime, comment="发货时间")
    delivered_at = Column(DateTime, comment="签收时间")
    
    # 计算详情（JSON存储）
    calculation_details = Column(JSON, comment="运费计算详情")
    calculation_metadata = Column(JSON, comment="计算过程元数据")
    
    # 时间戳
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关联关系
    shipping_method = relationship("ShippingMethod", back_populates="order_shipping_infos")
    shipping_zone = relationship("ShippingZone", back_populates="order_shipping_infos")
    free_shipping_rule = relationship("FreeShippingRule", back_populates="order_shipping_infos")

    def __repr__(self):
        return f"<OrderShippingInfo(order_id='{self.order_id}', method='{self.shipping_method_code}', cost={self.final_shipping_cost})>" 