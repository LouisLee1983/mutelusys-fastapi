import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class MarketingReport(ReportBase):
    """营销报表表，分析广告效果和ROI"""
    __tablename__ = "marketing_reports"

    total_marketing_spend = Column(Float, nullable=True, comment="总营销支出")
    total_revenue_generated = Column(Float, nullable=True, comment="总带来收入")
    total_roi = Column(Float, nullable=True, comment="总投资回报率")
    total_impressions = Column(Integer, nullable=True, comment="总展示次数")
    total_clicks = Column(Integer, nullable=True, comment="总点击次数")
    total_conversions = Column(Integer, nullable=True, comment="总转化次数")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    cost_per_click = Column(Float, nullable=True, comment="每次点击成本")
    cost_per_acquisition = Column(Float, nullable=True, comment="每次获取成本")
    campaign_performance = Column(JSONB, nullable=True, comment="活动表现数据")
    channel_performance = Column(JSONB, nullable=True, comment="渠道表现数据")
    coupon_performance = Column(JSONB, nullable=True, comment="优惠券表现数据")
    thematic_campaign_performance = Column(JSONB, nullable=True, comment="主题活动表现数据")
    intent_based_marketing_performance = Column(JSONB, nullable=True, comment="基于意图的营销表现数据")
    cultural_content_performance = Column(JSONB, nullable=True, comment="文化内容营销表现数据")
    affiliate_performance = Column(JSONB, nullable=True, comment="联盟营销表现数据")
    promotional_effectiveness = Column(JSONB, nullable=True, comment="促销效果数据")
    marketing_spend_by_channel = Column(JSONB, nullable=True, comment="按渠道的营销支出")
    marketing_spend_by_campaign = Column(JSONB, nullable=True, comment="按活动的营销支出")
    marketing_spend_by_period = Column(JSONB, nullable=True, comment="按期间的营销支出")
    top_performing_campaigns = Column(JSONB, nullable=True, comment="表现最佳的活动")
    customer_acquisition_by_channel = Column(JSONB, nullable=True, comment="按渠道的客户获取")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")
    currency_code = Column(String(3), nullable=True, default="USD", comment="货币代码")


class CampaignPerformanceMetric(Base):
    """活动表现指标表，针对特定营销活动的详细分析"""
    __tablename__ = "campaign_performance_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("marketing_reports.id", ondelete="CASCADE"), nullable=False)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("marketing_campaigns.id"), nullable=False, comment="活动ID")
    campaign_name = Column(String(100), nullable=False, comment="活动名称")
    campaign_type = Column(String(50), nullable=False, comment="活动类型")
    start_date = Column(Date, nullable=False, comment="开始日期")
    end_date = Column(Date, nullable=True, comment="结束日期")
    budget = Column(Float, nullable=True, comment="预算")
    spend = Column(Float, nullable=True, comment="实际支出")
    revenue = Column(Float, nullable=True, comment="带来收入")
    roi = Column(Float, nullable=True, comment="投资回报率")
    impressions = Column(Integer, nullable=True, comment="展示次数")
    clicks = Column(Integer, nullable=True, comment="点击次数")
    conversions = Column(Integer, nullable=True, comment="转化次数")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    cost_per_click = Column(Float, nullable=True, comment="每次点击成本")
    cost_per_acquisition = Column(Float, nullable=True, comment="每次获取成本")
    target_audience = Column(String(100), nullable=True, comment="目标受众")
    channels = Column(ARRAY(String), nullable=True, comment="使用渠道")
    performance_metrics = Column(JSONB, nullable=True, comment="表现指标详情")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("MarketingReport")
    campaign = relationship("MarketingCampaign")
