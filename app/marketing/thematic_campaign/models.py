import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ThemeType(str, enum.Enum):
    CULTURAL = "cultural"         # 文化主题（如中国新年、泰国宋干节）
    SEASONAL = "seasonal"         # 季节性主题（如夏季、冬季）
    ZODIAC = "zodiac"             # 生肖主题（如龙年、虎年）
    HOLIDAY = "holiday"           # 节日主题（如情人节、感恩节）
    SPIRITUAL = "spiritual"       # 精神主题（如冥想、瑜伽）
    INTENTION = "intention"       # 意图主题（如健康、爱情）
    CUSTOM = "custom"             # 自定义主题


class ThematicCampaign(Base):
    """主题营销活动，围绕文化节日、年度生肖等文化元素开展"""
    __tablename__ = "thematic_campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="活动名称")
    description = Column(Text, nullable=True, comment="活动描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 主题相关
    theme_type = Column(Enum(ThemeType), nullable=False, comment="主题类型")
    theme_name = Column(String(100), nullable=False, comment="主题名称")
    theme_description = Column(Text, nullable=True, comment="主题描述")
    
    # 文化和区域相关
    cultural_background = Column(Text, nullable=True, comment="文化背景")
    target_regions = Column(ARRAY(String), nullable=True, comment="目标区域")
    
    # 产品和内容关联
    featured_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="特色产品ID列表")
    featured_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="特色分类ID列表")
    featured_bundles = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="特色套装ID列表")
    featured_symbols = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="特色符号ID列表")
    featured_materials = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="特色材质ID列表")
    
    # 促销关联
    promotion_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="关联促销ID列表")
    discount_code = Column(String(50), nullable=True, comment="折扣代码")
    
    # 内容和媒体设置
    banner_url = Column(String(255), nullable=True, comment="横幅URL")
    landing_page_url = Column(String(255), nullable=True, comment="落地页URL")
    main_image_url = Column(String(255), nullable=True, comment="主图URL")
    video_url = Column(String(255), nullable=True, comment="视频URL")
    
    # 主题配置
    theme_color = Column(String(7), nullable=True, comment="主题颜色（HEX）")
    theme_font = Column(String(100), nullable=True, comment="主题字体")
    theme_elements = Column(JSON, nullable=True, comment="主题元素")
    
    # 内容设置
    slogan = Column(String(255), nullable=True, comment="主题口号")
    story_content = Column(Text, nullable=True, comment="故事内容")
    content_sections = Column(JSON, nullable=True, comment="内容区块")
    featured_blog_posts = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="特色博客文章ID列表")
    
    # 时间设置
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    is_recurring = Column(Boolean, default=False, comment="是否重复")
    recurring_pattern = Column(String(50), nullable=True, comment="重复模式：yearly, monthly等")
    
    # 营销渠道
    channels = Column(ARRAY(String), nullable=True, comment="营销渠道列表")
    social_media_assets = Column(JSON, nullable=True, comment="社交媒体资源")
    email_template_id = Column(String(100), nullable=True, comment="邮件模板ID")
    
    # SEO设置
    seo_title = Column(String(100), nullable=True, comment="SEO标题")
    seo_description = Column(String(255), nullable=True, comment="SEO描述")
    seo_keywords = Column(ARRAY(String), nullable=True, comment="SEO关键词")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    participation_count = Column(Integer, default=0, comment="参与次数")
    revenue = Column(Float, default=0, comment="产生收入")
    
    # 额外信息
    tags = Column(ARRAY(String), nullable=True, comment="标签列表")
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    creator = relationship("User")
    theme_sections = relationship("ThemeSection", back_populates="campaign", cascade="all, delete-orphan")
    theme_activities = relationship("ThemeActivity", back_populates="campaign", cascade="all, delete-orphan")


class ThemeSection(Base):
    """主题区块，一个主题活动可包含多个主题区块"""
    __tablename__ = "theme_sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("thematic_campaigns.id", ondelete="CASCADE"), nullable=False)
    
    # 区块信息
    name = Column(String(100), nullable=False, comment="区块名称")
    description = Column(Text, nullable=True, comment="区块描述")
    section_type = Column(String(50), nullable=False, comment="区块类型：product_list, story, banner等")
    
    # 排序和显示
    display_order = Column(Integer, default=0, comment="显示顺序")
    is_visible = Column(Boolean, default=True, comment="是否可见")
    
    # 内容设置
    title = Column(String(255), nullable=True, comment="标题")
    subtitle = Column(String(255), nullable=True, comment="副标题")
    content = Column(Text, nullable=True, comment="内容")
    
    # 媒体设置
    background_url = Column(String(255), nullable=True, comment="背景URL")
    image_url = Column(String(255), nullable=True, comment="图片URL")
    
    # 链接设置
    button_text = Column(String(100), nullable=True, comment="按钮文本")
    button_url = Column(String(255), nullable=True, comment="按钮URL")
    
    # 产品关联
    product_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="产品ID列表")
    category_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="分类ID列表")
    
    # 样式设置
    style_settings = Column(JSON, nullable=True, comment="样式设置")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    campaign = relationship("ThematicCampaign", back_populates="theme_sections")


class ThemeActivity(Base):
    """主题活动，如抽奖、签到、分享等互动活动"""
    __tablename__ = "theme_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("thematic_campaigns.id", ondelete="CASCADE"), nullable=False)
    
    # 活动信息
    name = Column(String(100), nullable=False, comment="活动名称")
    description = Column(Text, nullable=True, comment="活动描述")
    activity_type = Column(String(50), nullable=False, comment="活动类型：lottery, checkin, share等")
    
    # 活动规则
    rules = Column(Text, nullable=True, comment="活动规则")
    rewards = Column(JSON, nullable=True, comment="奖励设置")
    
    # 时间设置
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    
    # 参与限制
    participation_limit = Column(Integer, nullable=True, comment="参与次数限制")
    
    # 统计信息
    total_participants = Column(Integer, default=0, comment="总参与人数")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    campaign = relationship("ThematicCampaign", back_populates="theme_activities")
    participations = relationship("ActivityParticipation", back_populates="activity", cascade="all, delete-orphan")


class ActivityParticipation(Base):
    """活动参与记录"""
    __tablename__ = "activity_participations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("theme_activities.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    
    # 参与信息
    participation_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="参与时间")
    result = Column(String(50), nullable=True, comment="参与结果")
    
    # 奖励信息
    reward_type = Column(String(50), nullable=True, comment="奖励类型")
    reward_id = Column(UUID(as_uuid=True), nullable=True, comment="奖励ID")
    reward_details = Column(JSON, nullable=True, comment="奖励详情")
    is_claimed = Column(Boolean, default=False, comment="是否已领取")
    claimed_at = Column(DateTime, nullable=True, comment="领取时间")
    
    # 设备信息
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    activity = relationship("ThemeActivity", back_populates="participations")
    customer = relationship("Customer")
