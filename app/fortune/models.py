import uuid
from typing import Optional
from datetime import datetime
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ReadingType(str, enum.Enum):
    BAZI = "bazi"        # 八字命理
    TAROT = "tarot"      # 塔罗牌


class FortuneProfile(Base):
    """用户算命档案表，存储用户的基本信息和八字档案"""
    __tablename__ = "fortune_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    birth_year = Column(Integer, nullable=False, comment="出生年份")
    birth_month = Column(Integer, nullable=False, comment="出生月份") 
    birth_day = Column(Integer, nullable=False, comment="出生日期")
    birth_hour = Column(Integer, nullable=True, comment="出生时辰（0-23）")
    gender = Column(String(10), nullable=False, comment="性别：male/female")
    birth_location = Column(String(100), nullable=True, comment="出生地点")
    bazi_analysis = Column(JSON, nullable=True, comment="八字分析结果JSON")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer", foreign_keys=[customer_id])
    readings = relationship("FortuneReading", back_populates="profile", cascade="all, delete-orphan")


class FortuneReading(Base):
    """算命记录表，存储每次算命的详细记录"""
    __tablename__ = "fortune_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("fortune_profiles.id", ondelete="CASCADE"), nullable=True)
    reading_type = Column(Enum(ReadingType), nullable=False, comment="算命类型")
    question_type = Column(String(50), nullable=True, comment="问题类型：love/career/health/general")
    input_data = Column(JSON, nullable=False, comment="输入数据JSON")
    ai_analysis = Column(Text, nullable=False, comment="AI分析结果")
    recommended_products = Column(JSON, nullable=True, comment="推荐商品JSON")
    reading_date = Column(DateTime, default=datetime.utcnow, nullable=False, comment="算命日期")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer", foreign_keys=[customer_id])
    profile = relationship("FortuneProfile", back_populates="readings")