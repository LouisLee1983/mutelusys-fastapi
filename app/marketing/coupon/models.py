import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.marketing.promotion.models import Promotion, PromotionType, DiscountType


class CouponStatus(str, enum.Enum):
    ACTIVE = "active"        # 激活
    INACTIVE = "inactive"    # 未激活
    EXPIRED = "expired"      # 已过期
    USED = "used"            # 已使用
    CANCELLED = "cancelled"  # 已取消


class CouponFormat(str, enum.Enum):
    ALPHANUMERIC = "alphanumeric"  # 字母数字混合
    NUMERIC = "numeric"            # 纯数字
    ALPHABETIC = "alphabetic"      # 纯字母
    CUSTOM = "custom"              # 自定义


class Coupon(Base):
    """优惠券，继承自Promotion，包含折扣码、使用限制等"""
    __tablename__ = "coupons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    promotion_id = Column(UUID(as_uuid=True), ForeignKey("promotions.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(50), nullable=False, unique=True, comment="优惠码")
    status = Column(Enum(CouponStatus), default=CouponStatus.ACTIVE, nullable=False, comment="状态")
    
    # 生成设置
    format = Column(Enum(CouponFormat), default=CouponFormat.ALPHANUMERIC, comment="优惠码格式")
    prefix = Column(String(10), nullable=True, comment="前缀")
    suffix = Column(String(10), nullable=True, comment="后缀")
    length = Column(Integer, default=8, comment="长度")
    
    # 使用限制
    max_uses = Column(Integer, nullable=True, comment="最大使用次数，空表示不限制")
    max_uses_per_customer = Column(Integer, default=1, comment="每个客户最大使用次数")
    current_uses = Column(Integer, default=0, comment="当前使用次数")
    is_single_use = Column(Boolean, default=True, comment="是否一次性使用")
    requires_authentication = Column(Boolean, default=True, comment="是否需要用户登录")
    
    # 使用控制
    valid_from = Column(DateTime, nullable=False, comment="有效期开始")
    valid_to = Column(DateTime, nullable=True, comment="有效期结束，空表示永久有效")
    
    # 批量生成设置
    is_batch = Column(Boolean, default=False, comment="是否批量优惠券")
    batch_id = Column(UUID(as_uuid=True), ForeignKey("coupon_batches.id"), nullable=True)
    
    # 分销规则
    is_referral = Column(Boolean, default=False, comment="是否推荐优惠券")
    referrer_reward = Column(Float, nullable=True, comment="推荐人奖励")
    
    # 邮件和分享设置
    is_public = Column(Boolean, default=False, comment="是否公开可用（无需特定分发）")
    is_featured = Column(Boolean, default=False, comment="是否推荐显示")
    auto_apply = Column(Boolean, default=False, comment="是否自动应用")
    
    # 赠品配置
    free_product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True)
    free_product_quantity = Column(Integer, default=1, comment="赠品数量")
    
    # 统计数据
    view_count = Column(Integer, default=0, comment="查看次数")
    conversion_rate = Column(Float, default=0, comment="转化率")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    promotion = relationship("Promotion", backref="coupons")
    batch = relationship("CouponBatch", back_populates="coupons")
    free_product = relationship("Product")
    customer_coupons = relationship("CustomerCoupon", back_populates="coupon", cascade="all, delete-orphan")


class CouponBatch(Base):
    """优惠券批次表"""
    __tablename__ = "coupon_batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="批次名称")
    description = Column(Text, nullable=True, comment="批次描述")
    
    # 批次信息
    code_prefix = Column(String(10), nullable=True, comment="前缀")
    code_format = Column(Enum(CouponFormat), default=CouponFormat.ALPHANUMERIC, comment="优惠码格式")
    code_length = Column(Integer, default=8, comment="优惠码长度")
    quantity = Column(Integer, nullable=False, comment="生成数量")
    generated_count = Column(Integer, default=0, comment="已生成数量")
    used_count = Column(Integer, default=0, comment="已使用数量")
    
    # 批次规则
    max_uses_per_coupon = Column(Integer, default=1, comment="每个优惠券最大使用次数")
    valid_from = Column(DateTime, nullable=False, comment="有效期开始")
    valid_to = Column(DateTime, nullable=True, comment="有效期结束")
    
    # 分发设置
    is_exported = Column(Boolean, default=False, comment="是否已导出")
    export_date = Column(DateTime, nullable=True, comment="导出日期")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    coupons = relationship("Coupon", back_populates="batch")
