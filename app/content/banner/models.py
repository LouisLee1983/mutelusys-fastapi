import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 横幅类型枚举
class BannerType(str, enum.Enum):
    HOME_SLIDER = "home_slider"        # 首页轮播
    PROMO_BANNER = "promo_banner"      # 促销横幅
    CATEGORY_BANNER = "category_banner"  # 分类页横幅
    SIDEBAR_BANNER = "sidebar_banner"  # 侧边栏横幅
    POPUP = "popup"                    # 弹窗广告


class Banner(Base):
    """广告横幅表，包含图片、链接、排序等"""
    __tablename__ = "banners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="横幅标题")
    type = Column(Enum(BannerType), nullable=False, comment="横幅类型")
    image_url = Column(String(255), nullable=False, comment="图片URL")
    mobile_image_url = Column(String(255), nullable=True, comment="移动端图片URL")
    link_url = Column(String(255), nullable=True, comment="链接URL")
    position = Column(String(50), nullable=True, comment="位置标识")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, comment="横幅状态")
    start_date = Column(DateTime, nullable=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    alt_text = Column(String(255), nullable=True, comment="图片替代文本")
    open_in_new_tab = Column(Boolean, default=False, comment="是否在新标签页打开")
    additional_css = Column(Text, nullable=True, comment="额外CSS样式")
    additional_info = Column(JSON, nullable=True, comment="额外信息，如按钮文本、动画类型等")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("BannerTranslation", back_populates="banner", cascade="all, delete-orphan")


class BannerTranslation(Base):
    """横幅多语言翻译表"""
    __tablename__ = "banner_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    banner_id = Column(UUID(as_uuid=True), ForeignKey("banners.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="横幅标题")
    subtitle = Column(String(255), nullable=True, comment="副标题")
    description = Column(Text, nullable=True, comment="描述文本")
    button_text = Column(String(50), nullable=True, comment="按钮文本")
    alt_text = Column(String(255), nullable=True, comment="图片替代文本")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    banner = relationship("Banner", back_populates="translations")

    # 联合索引确保每个横幅对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
