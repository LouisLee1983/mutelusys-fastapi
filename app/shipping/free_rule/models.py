# -*- coding: utf-8 -*-
"""
免运费规则数据模型
包含免运费规则和翻译表
"""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, DECIMAL, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class FreeShippingRuleType(enum.Enum):
    """免运费规则类型"""
    AMOUNT_BASED = "amount_based"      # 满额免费
    QUANTITY_BASED = "quantity_based"  # 满件免费
    MEMBER_BASED = "member_based"      # 会员免费
    PROMOTION_BASED = "promotion_based" # 促销免费


class FreeShippingRule(Base):
    """免运费规则表"""
    __tablename__ = "free_shipping_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="免运费规则ID")
    code = Column(String(20), unique=True, nullable=False, comment="规则代码")
    name = Column(String(100), nullable=False, comment="规则名称")
    description = Column(Text, comment="规则描述")
    
    # 规则类型和条件
    rule_type = Column(Enum(FreeShippingRuleType), nullable=False, comment="规则类型")
    min_amount = Column(DECIMAL(10, 2), comment="最小金额（满额免费）")
    min_quantity = Column(Integer, comment="最小件数（满件免费）")
    member_levels = Column(Text, comment="适用会员等级，逗号分隔")
    promotion_codes = Column(Text, comment="适用促销代码，逗号分隔")
    
    # 适用范围
    applicable_zones = Column(Text, comment="适用地区代码，逗号分隔，空为全部")
    applicable_methods = Column(Text, comment="适用快递方式代码，逗号分隔，空为全部")
    
    # 时间范围
    start_date = Column(DateTime, comment="开始时间")
    end_date = Column(DateTime, comment="结束时间")
    
    # 状态
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    priority = Column(Integer, default=0, nullable=False, comment="优先级，数值越大优先级越高")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

    # 关联关系
    translations = relationship("FreeShippingRuleTranslation", back_populates="rule", cascade="all, delete-orphan")
    order_charge_items = relationship("OrderChargeItem", back_populates="free_shipping_rule")
    order_shipping_infos = relationship("OrderShippingInfo", back_populates="free_shipping_rule")

    def __repr__(self):
        return f"<FreeShippingRule(code='{self.code}', name='{self.name}', type='{self.rule_type}')>"


class FreeShippingRuleTranslation(Base):
    """免运费规则翻译表"""
    __tablename__ = "free_shipping_rule_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="翻译ID")
    free_shipping_rule_id = Column(UUID(as_uuid=True), ForeignKey("free_shipping_rules.id", ondelete="CASCADE"), nullable=False, comment="免运费规则ID")
    language_code = Column(String(10), nullable=False, comment="语言代码")
    name = Column(String(100), nullable=False, comment="规则名称翻译")
    description = Column(Text, comment="规则描述翻译")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

    # 关联关系
    rule = relationship("FreeShippingRule", back_populates="translations")

    # 复合唯一索引
    __table_args__ = (
        {'comment': '免运费规则翻译表'},
    )

    def __repr__(self):
        return f"<FreeShippingRuleTranslation(rule_id='{self.free_shipping_rule_id}', language='{self.language_code}')>" 