import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class SymbolPerformance(ReportBase):
    """符号表现分析表，追踪不同文化符号商品的市场表现"""
    __tablename__ = "symbol_performances"

    total_symbols = Column(Integer, nullable=True, comment="符号总数")
    top_symbols = Column(JSONB, nullable=True, comment="热门符号列表")
    symbol_product_distribution = Column(JSONB, nullable=True, comment="符号产品分布")
    symbol_customer_distribution = Column(JSONB, nullable=True, comment="符号客户分布")
    symbol_view_counts = Column(JSONB, nullable=True, comment="符号浏览次数")
    symbol_purchase_counts = Column(JSONB, nullable=True, comment="符号购买次数")
    symbol_conversion_rates = Column(JSONB, nullable=True, comment="符号转化率")
    symbol_average_order_values = Column(JSONB, nullable=True, comment="符号平均订单价值")
    symbol_revenue_contribution = Column(JSONB, nullable=True, comment="符号收入贡献")
    symbol_growth_rates = Column(JSONB, nullable=True, comment="符号增长率")
    symbol_seasonal_trends = Column(JSONB, nullable=True, comment="符号季节性趋势")
    symbol_geographic_distribution = Column(JSONB, nullable=True, comment="符号地理分布")
    symbol_demographic_distribution = Column(JSONB, nullable=True, comment="符号人口统计分布")
    symbol_cultural_preference_correlation = Column(JSONB, nullable=True, comment="符号文化偏好相关性")
    symbol_search_frequency = Column(JSONB, nullable=True, comment="符号搜索频率")
    symbol_content_engagement = Column(JSONB, nullable=True, comment="符号内容互动")
    symbol_customer_satisfaction = Column(JSONB, nullable=True, comment="符号客户满意度")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")


class SymbolPerformanceMetric(Base):
    """符号表现指标表，记录特定符号的详细表现数据"""
    __tablename__ = "symbol_performance_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("symbol_performances.id", ondelete="CASCADE"), nullable=False)
    symbol_id = Column(UUID(as_uuid=True), ForeignKey("product_symbols.id"), nullable=False, comment="符号ID")
    date = Column(Date, nullable=False, comment="统计日期")
    symbol_name = Column(String(100), nullable=False, comment="符号名称")
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
    cultural_regions = Column(JSONB, nullable=True, comment="文化区域分布")
    content_view_count = Column(Integer, nullable=True, comment="相关内容浏览次数")
    related_symbols = Column(JSONB, nullable=True, comment="相关符号")
    popular_products = Column(JSONB, nullable=True, comment="热门产品")
    related_intents = Column(JSONB, nullable=True, comment="相关意图")
    customer_segments = Column(JSONB, nullable=True, comment="客户细分")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("SymbolPerformance")
    symbol = relationship("ProductSymbol")
