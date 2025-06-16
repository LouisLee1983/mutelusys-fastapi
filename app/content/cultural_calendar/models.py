import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 事件类型枚举
class EventType(str, enum.Enum):
    FESTIVAL = "festival"              # 节日
    RELIGIOUS = "religious"            # 宗教活动
    CULTURAL = "cultural"              # 文化活动
    LUNAR = "lunar"                    # 农历事件
    ZODIAC = "zodiac"                  # 生肖相关
    SEASONAL = "seasonal"              # 季节相关
    HISTORICAL = "historical"          # 历史事件
    OTHER = "other"                    # 其他


# 重复类型枚举
class RecurrenceType(str, enum.Enum):
    YEARLY = "yearly"                  # 每年
    LUNAR_YEARLY = "lunar_yearly"      # 农历每年
    MONTHLY = "monthly"                # 每月
    NONE = "none"                      # 不重复


# 文化日历与产品的多对多关联表
cultural_calendar_product = Table(
    "cultural_calendar_product",
    Base.metadata,
    Column("calendar_id", UUID(as_uuid=True), ForeignKey("cultural_calendars.id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class CulturalCalendar(Base):
    """文化日历表，追踪不同文化的重要节日和活动"""
    __tablename__ = "cultural_calendars"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="事件标题")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="别名，用于URL")
    description = Column(Text, nullable=True, comment="事件描述")
    event_type = Column(Enum(EventType), nullable=False, comment="事件类型")
    cultural_region = Column(String(100), nullable=True, comment="文化区域")
    start_date = Column(Date, nullable=False, comment="开始日期")
    end_date = Column(Date, nullable=True, comment="结束日期")
    is_lunar_date = Column(Boolean, default=False, comment="是否农历日期")
    recurrence_type = Column(Enum(RecurrenceType), nullable=False, default=RecurrenceType.YEARLY, comment="重复类型")
    recurrence_details = Column(JSON, nullable=True, comment="重复细节")
    significance = Column(Text, nullable=True, comment="重要性和意义")
    traditions = Column(Text, nullable=True, comment="传统习俗")
    symbols = Column(Text, nullable=True, comment="相关符号")
    featured_image = Column(String(255), nullable=True, comment="特色图片URL")
    external_link = Column(String(255), nullable=True, comment="外部链接")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.PUBLISHED, comment="状态")
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    view_count = Column(Integer, default=0, comment="浏览次数")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("CulturalCalendarTranslation", back_populates="calendar", cascade="all, delete-orphan")
    products = relationship("Product", secondary=cultural_calendar_product, back_populates="cultural_calendars")


class CulturalCalendarTranslation(Base):
    """文化日历多语言翻译表"""
    __tablename__ = "cultural_calendar_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calendar_id = Column(UUID(as_uuid=True), ForeignKey("cultural_calendars.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(255), nullable=False, comment="事件标题")
    description = Column(Text, nullable=True, comment="事件描述")
    cultural_region = Column(String(100), nullable=True, comment="文化区域")
    significance = Column(Text, nullable=True, comment="重要性和意义")
    traditions = Column(Text, nullable=True, comment="传统习俗")
    symbols = Column(Text, nullable=True, comment="相关符号")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    calendar = relationship("CulturalCalendar", back_populates="translations")

    # 联合索引确保每个日历事件对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
