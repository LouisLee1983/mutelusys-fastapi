import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.marketing.promotion.models import Promotion, PromotionType, DiscountType


class DiscountRuleType(str, enum.Enum):
    CART_TOTAL = "cart_total"       # 购物车总价
    PRODUCT_QUANTITY = "product_quantity"  # 产品数量
    PRODUCT_COMBINATION = "product_combination"  # 产品组合
    FIRST_PURCHASE = "first_purchase"  # 首次购买
    MEMBERSHIP = "membership"        # 会员等级
    REPEAT_PURCHASE = "repeat_purchase"  # 重复购买
    VOLUME_DISCOUNT = "volume_discount"  # 批量折扣


class Discount(Base):
    """折扣活动，如满减、限时折扣等"""
    __tablename__ = "discounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    promotion_id = Column(UUID(as_uuid=True), ForeignKey("promotions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False, comment="折扣名称")
    description = Column(Text, nullable=True, comment="折扣描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 规则类型
    rule_type = Column(Enum(DiscountRuleType), nullable=False, comment="规则类型")
    
    # 购物车总价规则
    min_cart_total = Column(Float, nullable=True, comment="最低购物车金额")
    max_cart_total = Column(Float, nullable=True, comment="最高购物车金额")
    
    # 产品数量规则
    min_quantity = Column(Integer, nullable=True, comment="最低数量")
    max_quantity = Column(Integer, nullable=True, comment="最高数量")
    
    # 产品组合规则
    required_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="必选产品ID")
    any_required_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="任选产品ID")
    required_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="必选分类ID")
    
    # 折扣属性
    discount_type = Column(String(20), nullable=False, comment="折扣类型：percent, fixed, free_item")
    discount_value = Column(Float, nullable=False, comment="折扣值")
    max_discount_amount = Column(Float, nullable=True, comment="最大折扣金额")
    applies_to = Column(String(20), default="cart", comment="应用于：cart, specific_products, specific_categories")
    target_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="目标产品ID")
    target_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="目标分类ID")
    
    # 重复规则
    repeat_times = Column(Integer, default=1, comment="重复次数，如买三送一中的重复次数为1")
    
    # 阶梯折扣
    tier_rules = Column(JSON, nullable=True, comment="阶梯规则，如[{min: 5, value: 10}, {min: 10, value: 15}]")
    
    # 限制
    usage_limit = Column(Integer, nullable=True, comment="使用次数限制")
    usage_count = Column(Integer, default=0, comment="已使用次数")
    user_limit = Column(Integer, nullable=True, comment="每个用户使用次数限制")
    
    # 有效期
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    is_permanent = Column(Boolean, default=False, comment="是否永久有效")
    
    # 显示设置
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    label = Column(String(50), nullable=True, comment="标签文本")
    label_color = Column(String(7), nullable=True, comment="标签颜色")
    
    # A/B测试
    is_test = Column(Boolean, default=False, comment="是否测试折扣")
    test_group = Column(String(50), nullable=True, comment="测试组")
    
    # 统计数据
    view_count = Column(Integer, default=0, comment="查看次数")
    use_count = Column(Integer, default=0, comment="使用次数")
    revenue_impact = Column(Float, default=0, comment="收入影响")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    promotion = relationship("Promotion", backref="discounts")
