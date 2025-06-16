import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class ThemePerformance(ReportBase):
    """主题表现报告表，分析不同主题系列的市场表现"""
    __tablename__ = "theme_performances"

    total_themes = Column(Integer, nullable=True, comment="主题总数")
    active_themes = Column(Integer, nullable=True, comment="活跃主题数")
    top_themes = Column(JSONB, nullable=True, comment="热门主题列表")
    theme_product_distribution = Column(JSONB, nullable=True, comment="主题产品分布")
    theme_customer_distribution = Column(JSONB, nullable=True, comment="主题客户分布")
    theme_view_counts = Column(JSONB, nullable=True, comment="主题浏览次数")
    theme_purchase_counts = Column(JSONB, nullable=True, comment="主题购买次数")
    theme_conversion_rates = Column(JSONB, nullable=True, comment="主题转化率")
    theme_average_order_values = Column(JSONB, nullable=True, comment="主题平均订单价值")
    theme_revenue_contribution = Column(JSONB, nullable=True, comment="主题收入贡献")
    theme_growth_rates = Column(JSONB, nullable=True, comment="主题增长率")
    theme_seasonal_performance = Column(JSONB, nullable=True, comment="主题季节性表现")
    theme_geographic_distribution = Column(JSONB, nullable=True, comment="主题地理分布")
    theme_demographic_distribution = Column(JSONB, nullable=True, comment="主题人口统计分布")
    theme_marketing_effectiveness = Column(JSONB, nullable=True, comment="主题营销效果")
    theme_bundle_performance = Column(JSONB, nullable=True, comment="主题套装表现")
    theme_cross_selling_patterns = Column(JSONB, nullable=True, comment="主题交叉销售模式")
    theme_customer_retention = Column(JSONB, nullable=True, comment="主题客户留存")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")


class ThemePerformanceMetric(Base):
    """主题表现指标表，记录特定主题的详细表现数据"""
    __tablename__ = "theme_performance_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("theme_performances.id", ondelete="CASCADE"), nullable=False)
    theme_id = Column(UUID(as_uuid=True), ForeignKey("product_themes.id"), nullable=False, comment="主题ID")
    date = Column(Date, nullable=False, comment="统计日期")
    theme_name = Column(String(100), nullable=False, comment="主题名称")
    theme_type = Column(String(50), nullable=True, comment="主题类型")
    is_seasonal = Column(Boolean, default=False, comment="是否季节性主题")
    season_info = Column(String(50), nullable=True, comment="季节信息")
    launch_date = Column(Date, nullable=True, comment="发布日期")
    end_date = Column(Date, nullable=True, comment="结束日期")
    product_count = Column(Integer, nullable=True, comment="产品数量")
    bundle_count = Column(Integer, nullable=True, comment="套装数量")
    view_count = Column(Integer, nullable=True, comment="浏览次数")
    search_count = Column(Integer, nullable=True, comment="搜索次数")
    add_to_cart_count = Column(Integer, nullable=True, comment="加入购物车次数")
    purchase_count = Column(Integer, nullable=True, comment="购买次数")
    revenue = Column(Float, nullable=True, comment="收入")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    average_order_value = Column(Float, nullable=True, comment="平均订单价值")
    customer_count = Column(Integer, nullable=True, comment="客户数量")
    new_customer_percentage = Column(Float, nullable=True, comment="新客户百分比")
    marketing_spend = Column(Float, nullable=True, comment="营销支出")
    marketing_roi = Column(Float, nullable=True, comment="营销ROI")
    popular_products = Column(JSONB, nullable=True, comment="热门产品")
    customer_segments = Column(JSONB, nullable=True, comment="客户细分")
    related_themes = Column(JSONB, nullable=True, comment="相关主题")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("ThemePerformance")
    theme = relationship("ProductTheme")
