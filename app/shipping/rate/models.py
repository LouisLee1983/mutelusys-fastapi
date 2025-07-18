# -*- coding: utf-8 -*-
"""
运费规则数据模型
包含运费规则配置表
"""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class ShippingRate(Base):
    """运费规则表"""
    __tablename__ = "shipping_rates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="运费规则ID")
    shipping_method_id = Column(UUID(as_uuid=True), ForeignKey("shipping_methods.id", ondelete="CASCADE"), nullable=False, comment="快递方式ID")
    shipping_zone_id = Column(UUID(as_uuid=True), ForeignKey("shipping_zones.id", ondelete="CASCADE"), nullable=False, comment="运费地区ID")
    
    # 件数范围
    min_quantity = Column(Integer, nullable=False, default=1, comment="最小件数")
    max_quantity = Column(Integer, comment="最大件数，null表示无上限")
    
    # 运费设置
    base_cost = Column(DECIMAL(10, 2), nullable=False, default=0, comment="基础运费")
    per_item_cost = Column(DECIMAL(10, 2), default=0, comment="每件额外费用")
    
    # 状态
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

    # 关联关系
    method = relationship("ShippingMethod", back_populates="shipping_rates")
    zone = relationship("ShippingZone", back_populates="shipping_rates")

    def __repr__(self):
        return f"<ShippingRate(method_id='{self.shipping_method_id}', zone_id='{self.shipping_zone_id}', {self.min_quantity}-{self.max_quantity})>"