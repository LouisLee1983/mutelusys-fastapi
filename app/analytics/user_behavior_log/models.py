import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import UserBehaviorType, DeviceType


class UserBehaviorLog(Base):
    """用户行为日志表，记录点击、浏览等行为"""
    __tablename__ = "user_behavior_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, comment="客户ID，未登录用户为NULL")
    session_id = Column(String(100), nullable=False, comment="会话ID")
    behavior_type = Column(Enum(UserBehaviorType), nullable=False, comment="行为类型")
    page_url = Column(String(255), nullable=True, comment="页面URL")
    page_title = Column(String(255), nullable=True, comment="页面标题")
    referrer_url = Column(String(255), nullable=True, comment="来源URL")
    object_type = Column(String(50), nullable=True, comment="对象类型，如product, category, blog等")
    object_id = Column(UUID(as_uuid=True), nullable=True, comment="对象ID")
    device_type = Column(Enum(DeviceType), nullable=True, comment="设备类型")
    device_info = Column(JSONB, nullable=True, comment="设备信息")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(String(255), nullable=True, comment="用户代理")
    geo_location = Column(JSONB, nullable=True, comment="地理位置")
    action_details = Column(JSONB, nullable=True, comment="行为详情")
    event_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="事件时间")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer")


class UserBehaviorMetric(Base):
    """用户行为指标表，汇总分析用户行为数据"""
    __tablename__ = "user_behavior_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, comment="统计日期")
    behavior_type = Column(Enum(UserBehaviorType), nullable=False, comment="行为类型")
    count = Column(Integer, nullable=False, default=0, comment="行为次数")
    unique_users = Column(Integer, nullable=False, default=0, comment="独立用户数")
    unique_sessions = Column(Integer, nullable=False, default=0, comment="独立会话数")
    logged_in_ratio = Column(Float, nullable=True, comment="登录用户比例")
    new_user_ratio = Column(Float, nullable=True, comment="新用户比例")
    average_duration = Column(Float, nullable=True, comment="平均持续时间(秒)")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    bounce_rate = Column(Float, nullable=True, comment="跳出率")
    top_objects = Column(JSONB, nullable=True, comment="热门对象")
    device_breakdown = Column(JSONB, nullable=True, comment="设备分布")
    geo_breakdown = Column(JSONB, nullable=True, comment="地理分布")
    referrer_breakdown = Column(JSONB, nullable=True, comment="来源分布")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BehaviorFunnel(Base):
    """行为漏斗表，分析用户行为转化路径"""
    __tablename__ = "behavior_funnels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="漏斗名称")
    description = Column(String(255), nullable=True, comment="漏斗描述")
    funnel_steps = Column(JSONB, nullable=False, comment="漏斗步骤定义")
    is_active = Column(Boolean, default=True, comment="是否激活")
    date_range = Column(String(50), nullable=True, comment="统计时间范围")
    step_conversion_rates = Column(JSONB, nullable=True, comment="步骤转化率")
    overall_conversion_rate = Column(Float, nullable=True, comment="整体转化率")
    average_time_to_convert = Column(Float, nullable=True, comment="平均转化时间(秒)")
    dropoff_analysis = Column(JSONB, nullable=True, comment="流失分析")
    segment_performance = Column(JSONB, nullable=True, comment="细分群体表现")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    creator = relationship("User")
