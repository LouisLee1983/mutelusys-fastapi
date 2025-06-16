import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, Enum, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class PromotionType(str, enum.Enum):
    CART_DISCOUNT = "cart_discount"     # 购物车折扣
    PRODUCT_DISCOUNT = "product_discount"  # 产品折扣
    BUY_X_GET_Y = "buy_x_get_y"         # 买X送Y
    BUNDLE = "bundle"                   # 套装优惠
    GIFT = "gift"                       # 赠品
    FREE_SHIPPING = "free_shipping"     # 免运费
    FLASH_SALE = "flash_sale"           # 限时特卖
    COUPON = "coupon"                   # 优惠券
    LOYALTY_POINTS = "loyalty_points"   # 积分奖励
    THEMATIC = "thematic"               # 主题促销
    SEASONAL = "seasonal"               # 季节性促销


class DiscountType(str, enum.Enum):
    PERCENTAGE = "percentage"           # 百分比折扣
    FIXED_AMOUNT = "fixed_amount"       # 固定金额
    FREE_ITEM = "free_item"             # 免费商品
    FIXED_PRICE = "fixed_price"         # 指定价格


class Promotion(Base):
    """促销基类，包含类型、名称、描述、规则、有效期等"""
    __tablename__ = "promotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="促销名称")
    description = Column(Text, nullable=True, comment="促销描述")
    type = Column(Enum(PromotionType), nullable=False, comment="促销类型")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间设置
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    active_days = Column(ARRAY(Integer), nullable=True, comment="生效的星期几：0-6，空表示所有天")
    active_hours_start = Column(Integer, nullable=True, comment="生效开始小时：0-23")
    active_hours_end = Column(Integer, nullable=True, comment="生效结束小时：0-23")
    
    # 促销规则
    discount_type = Column(Enum(DiscountType), nullable=False, comment="折扣类型")
    discount_value = Column(Float, nullable=False, comment="折扣值（百分比或金额）")
    min_order_amount = Column(Float, nullable=True, comment="最低订单金额")
    max_discount_amount = Column(Float, nullable=True, comment="最大折扣金额")
    usage_limit = Column(Integer, nullable=True, comment="使用次数限制")
    usage_count = Column(Integer, default=0, comment="已使用次数")
    
    # 地区和货币设置
    applicable_countries = Column(ARRAY(String), nullable=True, comment="适用国家代码")
    excluded_countries = Column(ARRAY(String), nullable=True, comment="排除国家代码")
    applicable_currencies = Column(ARRAY(String), nullable=True, comment="适用货币代码")
    
    # 客户限制
    customer_eligibility = Column(String(50), default="all", comment="客户资格：all, new, existing, specific")
    eligible_customer_groups = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="符合条件的客户组")
    min_customer_orders = Column(Integer, nullable=True, comment="最低历史订单数")
    
    # 产品限制
    applicable_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="适用产品ID")
    excluded_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除产品ID")
    applicable_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="适用分类ID")
    excluded_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除分类ID")
    
    # 组合规则
    combination_strategy = Column(String(50), default="stack", comment="组合策略：stack(叠加), exclusive(独占), priority(优先)")
    priority = Column(Integer, default=0, comment="优先级，数字越大优先级越高")
    
    # 显示设置
    image_url = Column(String(255), nullable=True, comment="图片URL")
    banner_url = Column(String(255), nullable=True, comment="横幅URL")
    highlight_color = Column(String(7), nullable=True, comment="高亮颜色代码")
    is_featured = Column(Boolean, default=False, comment="是否推荐显示")
    
    # 复杂条件
    conditions = Column(JSON, nullable=True, comment="促销触发条件，复杂JSON结构")
    
    # 文化和主题关联
    cultural_theme = Column(String(100), nullable=True, comment="文化主题")
    intention_type = Column(String(100), nullable=True, comment="意图类型")
    
    # 额外设置
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
