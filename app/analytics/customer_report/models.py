import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class CustomerReport(ReportBase):
    """客户报表表，分析客户行为和转化情况"""
    __tablename__ = "customer_reports"

    total_customers = Column(Integer, nullable=True, comment="客户总数")
    new_customers = Column(Integer, nullable=True, comment="新客户数")
    active_customers = Column(Integer, nullable=True, comment="活跃客户数")
    inactive_customers = Column(Integer, nullable=True, comment="不活跃客户数")
    returning_customers = Column(Integer, nullable=True, comment="复购客户数")
    average_order_frequency = Column(Float, nullable=True, comment="平均订单频率")
    average_customer_lifetime_value = Column(Float, nullable=True, comment="平均客户终身价值")
    churn_rate = Column(Float, nullable=True, comment="客户流失率")
    retention_rate = Column(Float, nullable=True, comment="客户留存率")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    top_customer_segments = Column(JSONB, nullable=True, comment="主要客户细分")
    customer_acquisition_cost = Column(Float, nullable=True, comment="客户获取成本")
    customers_by_region = Column(JSONB, nullable=True, comment="按地区分布的客户数据")
    customers_by_age = Column(JSONB, nullable=True, comment="按年龄分布的客户数据")
    customers_by_gender = Column(JSONB, nullable=True, comment="按性别分布的客户数据")
    customers_by_intent = Column(JSONB, nullable=True, comment="按意图分布的客户数据")
    customers_by_cultural_preference = Column(JSONB, nullable=True, comment="按文化偏好分布的客户数据")
    customers_by_purchase_value = Column(JSONB, nullable=True, comment="按购买价值分布的客户数据")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")
    growth_rate = Column(Float, nullable=True, comment="增长率")


class CustomerSegmentAnalysis(Base):
    """客户细分分析表，针对特定客户细分的详细分析"""
    __tablename__ = "customer_segment_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("customer_reports.id", ondelete="CASCADE"), nullable=False)
    segment_name = Column(String(100), nullable=False, comment="细分名称")
    segment_description = Column(String(255), nullable=True, comment="细分描述")
    customer_count = Column(Integer, nullable=True, comment="客户数量")
    average_order_value = Column(Float, nullable=True, comment="平均订单价值")
    purchase_frequency = Column(Float, nullable=True, comment="购买频率")
    preferred_products = Column(JSONB, nullable=True, comment="偏好产品")
    preferred_categories = Column(JSONB, nullable=True, comment="偏好分类")
    preferred_intents = Column(JSONB, nullable=True, comment="偏好意图")
    preferred_cultural_elements = Column(JSONB, nullable=True, comment="偏好文化元素")
    engagement_metrics = Column(JSONB, nullable=True, comment="互动指标")
    lifetime_value = Column(Float, nullable=True, comment="终身价值")
    potential_value = Column(Float, nullable=True, comment="潜在价值")
    marketing_recommendations = Column(Text, nullable=True, comment="营销建议")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("CustomerReport")
