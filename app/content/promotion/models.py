import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


class PromotionContentType(str, enum.Enum):
    """促销内容类型"""
    BANNER_TEXT = "banner_text"        # 横幅文字
    NOTIFICATION = "notification"      # 通知文本
    POPUP_TEXT = "popup_text"         # 弹窗文本
    EMAIL_TEMPLATE = "email_template"  # 邮件模板
    SMS_TEMPLATE = "sms_template"     # 短信模板
    PRODUCT_BADGE = "product_badge"   # 产品徽章
    ANNOUNCEMENT = "announcement"     # 公告


class PromotionContent(Base):
    """促销活动内容管理表"""
    __tablename__ = "promotion_contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="内容标题")
    content_type = Column(Enum(PromotionContentType), nullable=False, comment="内容类型")
    
    # 关联到具体的促销活动（可选）
    promotion_id = Column(UUID(as_uuid=True), nullable=True, comment="关联的促销活动ID")
    
    # 内容信息
    short_text = Column(String(100), nullable=True, comment="短文本（如徽章文字）")
    content = Column(Text, nullable=True, comment="主要内容")
    button_text = Column(String(50), nullable=True, comment="按钮文字")
    link_url = Column(String(255), nullable=True, comment="链接URL")
    
    # 显示设置
    background_color = Column(String(7), nullable=True, comment="背景颜色")
    text_color = Column(String(7), nullable=True, comment="文字颜色")
    font_size = Column(String(20), nullable=True, comment="字体大小")
    position = Column(String(50), nullable=True, comment="显示位置")
    
    # 状态和时间
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, comment="内容状态")
    start_date = Column(DateTime, nullable=True, comment="开始时间")
    end_date = Column(DateTime, nullable=True, comment="结束时间")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
    # 目标设置
    target_pages = Column(JSON, nullable=True, comment="目标页面列表")
    target_countries = Column(JSON, nullable=True, comment="目标国家")
    target_languages = Column(JSON, nullable=True, comment="目标语言")
    
    # 额外设置
    additional_settings = Column(JSON, nullable=True, comment="额外设置")
    
    # 审计字段
    created_by = Column(UUID(as_uuid=True), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("PromotionContentTranslation", back_populates="content", cascade="all, delete-orphan")


class PromotionContentTranslation(Base):
    """促销内容多语言翻译表"""
    __tablename__ = "promotion_content_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("promotion_contents.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码")
    
    # 翻译内容
    title = Column(String(255), nullable=False, comment="标题")
    short_text = Column(String(100), nullable=True, comment="短文本")
    content = Column(Text, nullable=True, comment="主要内容")
    button_text = Column(String(50), nullable=True, comment="按钮文字")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    content = relationship("PromotionContent", back_populates="translations")

    # 联合索引确保每个内容对每种语言只有一个翻译
    __table_args__ = (
        {},
    )


class PromotionTextTemplate(Base):
    """促销文本模板表"""
    __tablename__ = "promotion_text_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="模板名称")
    content_type = Column(Enum(PromotionContentType), nullable=False, comment="内容类型")
    
    # 模板内容
    template_title = Column(String(255), nullable=False, comment="模板标题")
    template_content = Column(Text, nullable=True, comment="模板内容（支持变量占位符）")
    template_variables = Column(JSON, nullable=True, comment="模板变量定义")
    
    # 预设样式
    default_styles = Column(JSON, nullable=True, comment="默认样式设置")
    
    # 使用统计
    usage_count = Column(Integer, default=0, comment="使用次数")
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)