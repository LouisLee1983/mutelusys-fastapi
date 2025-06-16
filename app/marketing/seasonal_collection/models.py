import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class SeasonType(str, enum.Enum):
    SPRING = "spring"         # 春季
    SUMMER = "summer"         # 夏季
    AUTUMN = "autumn"         # 秋季
    WINTER = "winter"         # 冬季
    NEW_YEAR = "new_year"     # 新年
    FESTIVAL = "festival"     # 节日
    CULTURAL = "cultural"     # 文化节日
    RELIGIOUS = "religious"   # 宗教节日
    CUSTOM = "custom"         # 自定义


class SeasonalCollection(Base):
    """季节性系列，如新年、传统节日等特定时节的产品集合"""
    __tablename__ = "seasonal_collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="集合名称")
    description = Column(Text, nullable=True, comment="集合描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 季节设置
    season_type = Column(Enum(SeasonType), nullable=False, comment="季节类型")
    custom_season_name = Column(String(100), nullable=True, comment="自定义季节名称")
    cultural_context = Column(Text, nullable=True, comment="文化背景")
    
    # 区域和目标受众
    target_regions = Column(ARRAY(String), nullable=True, comment="目标区域")
    target_audience = Column(JSON, nullable=True, comment="目标受众")
    
    # 产品关联
    products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="产品ID列表")
    categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="分类ID列表")
    
    # 设计主题
    theme_color = Column(String(7), nullable=True, comment="主题颜色（HEX）")
    accent_color = Column(String(7), nullable=True, comment="强调色（HEX）")
    design_elements = Column(JSON, nullable=True, comment="设计元素")
    
    # 媒体资源
    banner_url = Column(String(255), nullable=True, comment="横幅URL")
    cover_image_url = Column(String(255), nullable=True, comment="封面图片URL")
    lookbook_images = Column(ARRAY(String), nullable=True, comment="造型集图片URL列表")
    
    # 时间设置
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    is_recurring = Column(Boolean, default=False, comment="是否重复")
    recurring_pattern = Column(String(50), nullable=True, comment="重复模式：yearly, monthly等")
    
    # 促销设置
    has_promotion = Column(Boolean, default=False, comment="是否有促销")
    promotion_id = Column(UUID(as_uuid=True), ForeignKey("promotions.id"), nullable=True, comment="关联促销ID")
    discount_percentage = Column(Float, nullable=True, comment="折扣百分比")
    
    # 显示设置
    display_order = Column(Integer, default=0, comment="显示顺序")
    is_featured = Column(Boolean, default=False, comment="是否特色")
    homepage_visible = Column(Boolean, default=True, comment="是否首页可见")
    
    # 内容设置
    slogan = Column(String(255), nullable=True, comment="口号")
    story_content = Column(Text, nullable=True, comment="故事内容")
    
    # SEO设置
    seo_title = Column(String(100), nullable=True, comment="SEO标题")
    seo_description = Column(String(255), nullable=True, comment="SEO描述")
    seo_keywords = Column(ARRAY(String), nullable=True, comment="SEO关键词")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    sale_count = Column(Integer, default=0, comment="销售次数")
    revenue = Column(Float, default=0, comment="产生收入")
    
    # 额外信息
    tags = Column(ARRAY(String), nullable=True, comment="标签列表")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    promotion = relationship("Promotion")
    creator = relationship("User")
    collection_products = relationship("CollectionProduct", back_populates="collection", cascade="all, delete-orphan")


class CollectionProduct(Base):
    """集合中的产品，包含排序和特色设置"""
    __tablename__ = "collection_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("seasonal_collections.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    
    # 产品设置
    display_order = Column(Integer, default=0, comment="显示顺序")
    is_featured = Column(Boolean, default=False, comment="是否特色")
    
    # 自定义描述
    custom_title = Column(String(255), nullable=True, comment="自定义标题")
    custom_description = Column(Text, nullable=True, comment="自定义描述")
    
    # 自定义展示
    custom_image_url = Column(String(255), nullable=True, comment="自定义图片URL")
    
    # 季节特殊关联
    seasonal_relevance = Column(String(255), nullable=True, comment="季节相关性描述")
    cultural_significance = Column(Text, nullable=True, comment="文化意义")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    click_count = Column(Integer, default=0, comment="点击次数")
    purchase_count = Column(Integer, default=0, comment="购买次数")
    
    # 定价信息
    original_price = Column(Float, nullable=True, comment="原价")
    seasonal_price = Column(Float, nullable=True, comment="季节价")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    collection = relationship("SeasonalCollection", back_populates="collection_products")
    product = relationship("Product")


class SeasonalLandingPage(Base):
    """季节性落地页配置"""
    __tablename__ = "seasonal_landing_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("seasonal_collections.id", ondelete="CASCADE"), nullable=False)
    
    # 基本信息
    title = Column(String(255), nullable=False, comment="标题")
    subtitle = Column(String(255), nullable=True, comment="副标题")
    slug = Column(String(100), nullable=False, unique=True, comment="URL slug")
    
    # 内容设置
    hero_banner_url = Column(String(255), nullable=True, comment="主横幅URL")
    video_url = Column(String(255), nullable=True, comment="视频URL")
    
    # 页面结构
    sections = Column(JSON, nullable=True, comment="页面区块")
    
    # 链接设置
    primary_cta_text = Column(String(100), nullable=True, comment="主要行动召唤文本")
    primary_cta_url = Column(String(255), nullable=True, comment="主要行动召唤URL")
    
    # SEO设置
    meta_title = Column(String(100), nullable=True, comment="Meta标题")
    meta_description = Column(String(255), nullable=True, comment="Meta描述")
    
    # 状态设置
    is_published = Column(Boolean, default=False, comment="是否已发布")
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    bounce_rate = Column(Float, nullable=True, comment="跳出率")
    average_time_on_page = Column(Integer, nullable=True, comment="平均停留时间（秒）")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    collection = relationship("SeasonalCollection")
    creator = relationship("User")
