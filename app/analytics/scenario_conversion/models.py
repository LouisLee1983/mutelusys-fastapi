import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class ScenarioConversion(ReportBase):
    """场景转化率表，分析不同生活场景分类的销售效果"""
    __tablename__ = "scenario_conversions"

    total_scenes = Column(Integer, nullable=True, comment="场景总数")
    top_scenes = Column(JSONB, nullable=True, comment="热门场景列表")
    scene_product_distribution = Column(JSONB, nullable=True, comment="场景产品分布")
    scene_customer_distribution = Column(JSONB, nullable=True, comment="场景客户分布")
    scene_view_counts = Column(JSONB, nullable=True, comment="场景浏览次数")
    scene_purchase_counts = Column(JSONB, nullable=True, comment="场景购买次数")
    scene_conversion_rates = Column(JSONB, nullable=True, comment="场景转化率")
    scene_average_order_values = Column(JSONB, nullable=True, comment="场景平均订单价值")
    scene_revenue_contribution = Column(JSONB, nullable=True, comment="场景收入贡献")
    scene_growth_rates = Column(JSONB, nullable=True, comment="场景增长率")
    scene_seasonal_trends = Column(JSONB, nullable=True, comment="场景季节性趋势")
    scene_geographic_distribution = Column(JSONB, nullable=True, comment="场景地理分布")
    scene_demographic_distribution = Column(JSONB, nullable=True, comment="场景人口统计分布")
    scene_cross_selling_patterns = Column(JSONB, nullable=True, comment="场景交叉销售模式")
    scene_search_frequency = Column(JSONB, nullable=True, comment="场景搜索频率")
    scene_content_engagement = Column(JSONB, nullable=True, comment="场景内容互动")
    scene_customer_satisfaction = Column(JSONB, nullable=True, comment="场景客户满意度")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")


class ScenePerformanceMetric(Base):
    """场景表现指标表，记录特定场景的详细表现数据"""
    __tablename__ = "scene_performance_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("scenario_conversions.id", ondelete="CASCADE"), nullable=False)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("product_scenes.id"), nullable=False, comment="场景ID")
    date = Column(Date, nullable=False, comment="统计日期")
    scene_name = Column(String(100), nullable=False, comment="场景名称")
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
    content_view_count = Column(Integer, nullable=True, comment="相关内容浏览次数")
    related_scenes = Column(JSONB, nullable=True, comment="相关场景")
    popular_products = Column(JSONB, nullable=True, comment="热门产品")
    related_intents = Column(JSONB, nullable=True, comment="相关意图")
    related_symbols = Column(JSONB, nullable=True, comment="相关符号")
    customer_segments = Column(JSONB, nullable=True, comment="客户细分")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("ScenarioConversion")
    scene = relationship("ProductScene")
