import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class IntentAnalytics(ReportBase):
    """意图分析表，了解不同意图产品的受欢迎程度和转化率"""
    __tablename__ = "intent_analytics"

    total_intents = Column(Integer, nullable=True, comment="意图总数")
    top_intents = Column(JSONB, nullable=True, comment="热门意图列表")
    intent_product_distribution = Column(JSONB, nullable=True, comment="意图产品分布")
    intent_customer_distribution = Column(JSONB, nullable=True, comment="意图客户分布")
    intent_view_counts = Column(JSONB, nullable=True, comment="意图浏览次数")
    intent_purchase_counts = Column(JSONB, nullable=True, comment="意图购买次数")
    intent_conversion_rates = Column(JSONB, nullable=True, comment="意图转化率")
    intent_average_order_values = Column(JSONB, nullable=True, comment="意图平均订单价值")
    intent_revenue_contribution = Column(JSONB, nullable=True, comment="意图收入贡献")
    intent_growth_rates = Column(JSONB, nullable=True, comment="意图增长率")
    intent_seasonal_trends = Column(JSONB, nullable=True, comment="意图季节性趋势")
    intent_geographic_distribution = Column(JSONB, nullable=True, comment="意图地理分布")
    intent_demographic_distribution = Column(JSONB, nullable=True, comment="意图人口统计分布")
    intent_cross_selling_patterns = Column(JSONB, nullable=True, comment="意图交叉销售模式")
    intent_search_frequency = Column(JSONB, nullable=True, comment="意图搜索频率")
    intent_return_rates = Column(JSONB, nullable=True, comment="意图退货率")
    intent_customer_satisfaction = Column(JSONB, nullable=True, comment="意图客户满意度")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")


class IntentPerformanceMetric(Base):
    """意图表现指标表，记录特定意图的详细表现数据"""
    __tablename__ = "intent_performance_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("intent_analytics.id", ondelete="CASCADE"), nullable=False)
    intent_id = Column(UUID(as_uuid=True), ForeignKey("product_intents.id"), nullable=False, comment="意图ID")
    date = Column(Date, nullable=False, comment="统计日期")
    intent_name = Column(String(100), nullable=False, comment="意图名称")
    product_count = Column(Integer, nullable=True, comment="产品数量")
    view_count = Column(Integer, nullable=True, comment="浏览次数")
    search_count = Column(Integer, nullable=True, comment="搜索次数")
    add_to_cart_count = Column(Integer, nullable=True, comment="加入购物车次数")
    purchase_count = Column(Integer, nullable=True, comment="购买次数")
    revenue = Column(Float, nullable=True, comment="收入")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    average_order_value = Column(Float, nullable=True, comment="平均订单价值")
    customer_count = Column(Integer, nullable=True, comment="客户数量")
    new_customer_percentage = Column(Float, nullable=True, comment="新客户百分比")
    return_rate = Column(Float, nullable=True, comment="退货率")
    repurchase_rate = Column(Float, nullable=True, comment="复购率")
    average_rating = Column(Float, nullable=True, comment="平均评分")
    related_intents = Column(JSONB, nullable=True, comment="相关意图")
    popular_products = Column(JSONB, nullable=True, comment="热门产品")
    customer_segments = Column(JSONB, nullable=True, comment="客户细分")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("IntentAnalytics")
    intent = relationship("ProductIntent")
