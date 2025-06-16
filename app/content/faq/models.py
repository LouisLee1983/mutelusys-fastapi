import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# FAQ分类枚举
class FAQCategory(str, enum.Enum):
    GENERAL = "general"              # 一般问题
    PRODUCT = "product"              # 产品相关
    SHIPPING = "shipping"            # 配送相关
    PAYMENT = "payment"              # 支付相关
    RETURN = "return"                # 退换货相关
    ACCOUNT = "account"              # 账户相关
    CULTURAL = "cultural"            # 文化相关
    MATERIAL = "material"            # 材质相关
    CUSTOM = "custom"                # 自定义分类


class FAQ(Base):
    """常见问题表，包含问题、答案、分类等"""
    __tablename__ = "faqs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(String(500), nullable=False, comment="问题")
    answer = Column(Text, nullable=False, comment="答案")
    category = Column(Enum(FAQCategory), nullable=False, default=FAQCategory.GENERAL, comment="问题分类")
    custom_category = Column(String(100), nullable=True, comment="自定义分类")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.PUBLISHED, comment="状态")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    is_featured = Column(Boolean, default=False, comment="是否常见问题")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("FAQTranslation", back_populates="faq", cascade="all, delete-orphan")


class FAQTranslation(Base):
    """常见问题多语言翻译表"""
    __tablename__ = "faq_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faq_id = Column(UUID(as_uuid=True), ForeignKey("faqs.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    question = Column(String(500), nullable=False, comment="问题")
    answer = Column(Text, nullable=False, comment="答案")
    custom_category = Column(String(100), nullable=True, comment="自定义分类名称")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    faq = relationship("FAQ", back_populates="translations")

    # 联合索引确保每个FAQ对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
