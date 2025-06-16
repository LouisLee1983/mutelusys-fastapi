import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import DeviceType


class VisitStats(Base):
    """访问统计表，包含来源、设备、停留时间等"""
    __tablename__ = "visit_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False, comment="统计日期")
    total_visits = Column(Integer, nullable=False, default=0, comment="总访问次数")
    unique_visitors = Column(Integer, nullable=False, default=0, comment="独立访客数")
    returning_visitors = Column(Integer, nullable=False, default=0, comment="回访访客数")
    new_visitors = Column(Integer, nullable=False, default=0, comment="新访客数")
    bounce_rate = Column(Float, nullable=True, comment="跳出率")
    average_session_duration = Column(Float, nullable=True, comment="平均会话时长(秒)")
    average_page_views = Column(Float, nullable=True, comment="平均页面浏览量")
    top_entry_pages = Column(JSONB, nullable=True, comment="热门入口页面")
    top_exit_pages = Column(JSONB, nullable=True, comment="热门退出页面")
    traffic_sources = Column(JSONB, nullable=True, comment="流量来源")
    device_breakdown = Column(JSONB, nullable=True, comment="设备分布")
    browser_breakdown = Column(JSONB, nullable=True, comment="浏览器分布")
    geo_breakdown = Column(JSONB, nullable=True, comment="地理分布")
    language_breakdown = Column(JSONB, nullable=True, comment="语言分布")
    time_of_day_breakdown = Column(JSONB, nullable=True, comment="一天中时间分布")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class PageViewStats(Base):
    """页面浏览统计表，记录各页面的访问情况"""
    __tablename__ = "page_view_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False, comment="统计日期")
    page_url = Column(String(255), nullable=False, comment="页面URL")
    page_title = Column(String(255), nullable=True, comment="页面标题")
    page_type = Column(String(50), nullable=True, comment="页面类型，如homepage, product, category, blog等")
    object_id = Column(UUID(as_uuid=True), nullable=True, comment="对象ID，如商品ID、分类ID等")
    views = Column(Integer, nullable=False, default=0, comment="浏览量")
    unique_views = Column(Integer, nullable=False, default=0, comment="独立浏览量")
    average_time_on_page = Column(Float, nullable=True, comment="平均页面停留时间(秒)")
    bounce_rate = Column(Float, nullable=True, comment="跳出率")
    exit_rate = Column(Float, nullable=True, comment="退出率")
    device_breakdown = Column(JSONB, nullable=True, comment="设备分布")
    referrer_breakdown = Column(JSONB, nullable=True, comment="来源分布")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class VisitSession(Base):
    """访问会话表，记录用户访问会话的详细信息"""
    __tablename__ = "visit_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), nullable=False, unique=True, comment="会话ID")
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, comment="客户ID，未登录用户为NULL")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=True, comment="结束时间")
    duration = Column(Float, nullable=True, comment="持续时间(秒)")
    is_bounce = Column(Boolean, nullable=True, comment="是否跳出")
    page_views = Column(Integer, nullable=False, default=0, comment="页面浏览量")
    landing_page = Column(String(255), nullable=True, comment="着陆页面")
    exit_page = Column(String(255), nullable=True, comment="退出页面")
    referrer_url = Column(String(255), nullable=True, comment="来源URL")
    utm_source = Column(String(100), nullable=True, comment="UTM来源")
    utm_medium = Column(String(100), nullable=True, comment="UTM媒介")
    utm_campaign = Column(String(100), nullable=True, comment="UTM活动")
    device_type = Column(Enum(DeviceType), nullable=True, comment="设备类型")
    browser = Column(String(100), nullable=True, comment="浏览器")
    os = Column(String(100), nullable=True, comment="操作系统")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    geo_location = Column(JSONB, nullable=True, comment="地理位置")
    language = Column(String(10), nullable=True, comment="语言")
    is_new_visitor = Column(Boolean, nullable=True, comment="是否新访客")
    has_conversion = Column(Boolean, default=False, comment="是否有转化")
    conversion_type = Column(String(50), nullable=True, comment="转化类型")
    conversion_value = Column(Float, nullable=True, comment="转化价值")
    page_path_sequence = Column(ARRAY(String), nullable=True, comment="页面路径序列")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer")
