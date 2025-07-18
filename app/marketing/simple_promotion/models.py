import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class SimplePromotionType(str, enum.Enum):
    DISCOUNT = "discount"        # 折扣/满减
    BUNDLE = "bundle"           # 打包优惠
    COUPON = "coupon"           # 优惠券


class DiscountType(str, enum.Enum):
    PERCENTAGE = "percentage"    # 百分比折扣
    FIXED_AMOUNT = "fixed_amount"  # 固定金额


class SimplePromotion(Base):
    """简化的促销模型，支持基本的折扣、满减、打包优惠功能"""
    __tablename__ = "simple_promotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, comment="促销代码")
    name = Column(String(100), nullable=False, comment="促销名称")
    description = Column(Text, nullable=True, comment="促销描述")
    type = Column(Enum(SimplePromotionType), nullable=False, comment="促销类型")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间控制
    start_date = Column(DateTime, nullable=False, comment="开始时间")
    end_date = Column(DateTime, nullable=True, comment="结束时间")
    
    # 折扣设置
    discount_type = Column(Enum(DiscountType), nullable=False, comment="折扣类型")
    discount_value = Column(Float, nullable=False, comment="折扣值")
    
    # 使用限制
    usage_limit = Column(Integer, nullable=True, comment="总使用次数限制")
    usage_count = Column(Integer, default=0, comment="已使用次数")
    per_customer_limit = Column(Integer, default=1, comment="每客户使用次数限制")
    
    # 促销规则 (JSON格式，灵活配置)
    rules = Column(JSON, nullable=True, comment="促销规则配置")
    
    # 创建时间
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CustomerPromotionUsage(Base):
    """客户促销使用记录"""
    __tablename__ = "customer_promotion_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), nullable=False, comment="客户ID")
    promotion_id = Column(UUID(as_uuid=True), nullable=False, comment="促销ID")
    order_id = Column(UUID(as_uuid=True), nullable=True, comment="订单ID")
    usage_count = Column(Integer, default=1, comment="使用次数")
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)