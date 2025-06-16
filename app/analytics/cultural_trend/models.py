import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class CulturalTrendReport(ReportBase):
    """文化趋势报告表，识别不同文化元素的流行趋势"""
    __tablename__ = "cultural_trend_reports"

    trending_symbols = Column(JSONB, nullable=True, comment="趋势符号")
    trending_cultural_stories = Column(JSONB, nullable=True, comment="趋势文化故事")
    trending_cultural_regions = Column(JSONB, nullable=True, comment="趋势文化区域")
    trending_cultural_elements = Column(JSONB, nullable=True, comment="趋势文化元素")
    trend_correlations = Column(JSONB, nullable=True, comment="趋势相关性")
    search_trend_analysis = Column(JSONB, nullable=True, comment="搜索趋势分析")
    view_trend_analysis = Column(JSONB, nullable=True, comment="浏览趋势分析")
    purchase_trend_analysis = Column(JSONB, nullable=True, comment="购买趋势分析")
    geographic_trend_distribution = Column(JSONB, nullable=True, comment="地理趋势分布")
    demographic_trend_distribution = Column(JSONB, nullable=True, comment="人口统计趋势分布")
    season_based_trends = Column(JSONB, nullable=True, comment="基于季节的趋势")
    cultural_calendar_correlation = Column(JSONB, nullable=True, comment="文化日历相关性")
    content_engagement_trends = Column(JSONB, nullable=True, comment="内容互动趋势")
    rising_cultural_interests = Column(JSONB, nullable=True, comment="上升文化兴趣")
    declining_cultural_interests = Column(JSONB, nullable=True, comment="下降文化兴趣")
    trending_cross_cultural_combinations = Column(JSONB, nullable=True, comment="趋势跨文化组合")
    predicted_future_trends = Column(JSONB, nullable=True, comment="预测未来趋势")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")


class CulturalElementTrend(Base):
    """文化元素趋势表，记录特定文化元素的趋势数据"""
    __tablename__ = "cultural_element_trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("cultural_trend_reports.id", ondelete="CASCADE"), nullable=False)
    element_type = Column(String(50), nullable=False, comment="元素类型，如symbol, story, region, tradition等")
    element_id = Column(UUID(as_uuid=True), nullable=True, comment="元素ID，如符号ID")
    element_name = Column(String(100), nullable=False, comment="元素名称")
    trend_period = Column(String(50), nullable=False, comment="趋势周期，如last_week, last_month, last_quarter等")
    trend_score = Column(Float, nullable=False, comment="趋势得分，表示趋势强度")
    trend_direction = Column(String(20), nullable=False, comment="趋势方向，如rising, stable, declining")
    growth_rate = Column(Float, nullable=True, comment="增长率")
    view_count_trend = Column(JSONB, nullable=True, comment="浏览量趋势")
    search_count_trend = Column(JSONB, nullable=True, comment="搜索量趋势")
    purchase_count_trend = Column(JSONB, nullable=True, comment="购买量趋势")
    engagement_rate_trend = Column(JSONB, nullable=True, comment="互动率趋势")
    related_elements = Column(JSONB, nullable=True, comment="相关元素")
    audience_segments = Column(JSONB, nullable=True, comment="受众细分")
    regional_popularity = Column(JSONB, nullable=True, comment="区域流行度")
    seasonal_factors = Column(JSONB, nullable=True, comment="季节因素")
    trend_prediction = Column(JSONB, nullable=True, comment="趋势预测")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("CulturalTrendReport")
