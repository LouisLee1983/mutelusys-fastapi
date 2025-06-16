import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class IntentionBundleStatus(str, enum.Enum):
    DRAFT = "draft"           # 草稿
    ACTIVE = "active"         # 活跃
    INACTIVE = "inactive"     # 非活跃
    SEASONAL = "seasonal"     # 季节性
    FEATURED = "featured"     # 特色


class IntentionBundle(Base):
    """意图套装，按照特定意图（如平衡、保护）组合的产品套装促销"""
    __tablename__ = "intention_bundles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="套装名称")
    description = Column(Text, nullable=True, comment="套装描述")
    status = Column(Enum(IntentionBundleStatus), default=IntentionBundleStatus.DRAFT, nullable=False, comment="状态")
    
    # 意图相关
    primary_intention = Column(String(50), nullable=False, comment="主要意图：平衡、保护、爱情、财富等")
    secondary_intentions = Column(ARRAY(String), nullable=True, comment="次要意图")
    intention_description = Column(Text, nullable=True, comment="意图详细描述")
    
    # 产品组合
    products = Column(ARRAY(UUID(as_uuid=True)), nullable=False, comment="产品ID列表")
    main_product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True, comment="主要产品ID")
    min_products = Column(Integer, default=1, comment="最少选择数量")
    max_products = Column(Integer, nullable=True, comment="最多选择数量")
    
    # 价格设置
    original_price = Column(Float, nullable=True, comment="原价总和")
    bundle_price = Column(Float, nullable=True, comment="套装价格")
    discount_percentage = Column(Float, nullable=True, comment="折扣百分比")
    discount_amount = Column(Float, nullable=True, comment="折扣金额")
    discount_type = Column(String(20), default="percentage", comment="折扣类型：percentage, fixed_amount")
    
    # 展示设置
    is_featured = Column(Boolean, default=False, comment="是否特色展示")
    display_order = Column(Integer, default=0, comment="显示顺序")
    thumbnail_url = Column(String(255), nullable=True, comment="缩略图URL")
    banner_url = Column(String(255), nullable=True, comment="横幅URL")
    
    # 内容设置
    usage_guide = Column(Text, nullable=True, comment="使用指南")
    benefits = Column(ARRAY(String), nullable=True, comment="收益列表")
    spiritual_meaning = Column(Text, nullable=True, comment="精神意义")
    
    # 促销设置
    promotion_id = Column(UUID(as_uuid=True), ForeignKey("promotions.id"), nullable=True, comment="关联促销ID")
    
    # 时间设置
    start_date = Column(DateTime, nullable=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    is_limited_time = Column(Boolean, default=False, comment="是否限时")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    purchase_count = Column(Integer, default=0, comment="购买次数")
    recommendation_count = Column(Integer, default=0, comment="推荐次数")
    
    # 额外信息
    customization_options = Column(JSON, nullable=True, comment="定制选项")
    gift_wrapping_options = Column(JSON, nullable=True, comment="礼品包装选项")
    tags = Column(ARRAY(String), nullable=True, comment="标签列表")
    cultural_context = Column(Text, nullable=True, comment="文化背景")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    main_product = relationship("Product", foreign_keys=[main_product_id])
    promotion = relationship("Promotion")
    creator = relationship("User")
    bundle_items = relationship("BundleItem", back_populates="bundle", cascade="all, delete-orphan")


class BundleItem(Base):
    """套装内的具体商品项目"""
    __tablename__ = "bundle_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bundle_id = Column(UUID(as_uuid=True), ForeignKey("intention_bundles.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    
    # 商品设置
    quantity = Column(Integer, default=1, comment="数量")
    is_required = Column(Boolean, default=True, comment="是否必选")
    is_highlighted = Column(Boolean, default=False, comment="是否高亮")
    display_order = Column(Integer, default=0, comment="显示顺序")
    
    # 价格设置
    original_price = Column(Float, nullable=True, comment="原价")
    discounted_price = Column(Float, nullable=True, comment="折扣价")
    
    # 描述
    custom_name = Column(String(100), nullable=True, comment="自定义名称")
    custom_description = Column(Text, nullable=True, comment="自定义描述")
    custom_image_url = Column(String(255), nullable=True, comment="自定义图片URL")
    
    # 角色描述
    role_in_bundle = Column(String(100), nullable=True, comment="在套装中的角色")
    intention_contribution = Column(Text, nullable=True, comment="对意图的贡献")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    bundle = relationship("IntentionBundle", back_populates="bundle_items")
    product = relationship("Product")


class BundleRecommendation(Base):
    """套装推荐记录"""
    __tablename__ = "bundle_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bundle_id = Column(UUID(as_uuid=True), ForeignKey("intention_bundles.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="客户ID，可为空")
    session_id = Column(String(100), nullable=True, comment="会话ID，用于匿名用户")
    
    # 推荐信息
    recommendation_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="推荐时间")
    recommendation_source = Column(String(50), nullable=True, comment="推荐来源：product_page, cart, homepage等")
    recommendation_context = Column(JSON, nullable=True, comment="推荐上下文")
    
    # 互动信息
    was_clicked = Column(Boolean, default=False, comment="是否被点击")
    was_added_to_cart = Column(Boolean, default=False, comment="是否加入购物车")
    was_purchased = Column(Boolean, default=False, comment="是否购买")
    
    # 时间记录
    clicked_at = Column(DateTime, nullable=True, comment="点击时间")
    added_to_cart_at = Column(DateTime, nullable=True, comment="加入购物车时间")
    purchased_at = Column(DateTime, nullable=True, comment="购买时间")
    
    # 关联订单
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True, comment="订单ID")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    bundle = relationship("IntentionBundle")
    customer = relationship("Customer")
    order = relationship("Order")
