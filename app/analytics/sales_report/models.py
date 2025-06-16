import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class SalesReport(ReportBase):
    """销售报表表，包含时间、商品、区域等维度的销售数据"""
    __tablename__ = "sales_reports"

    revenue = Column(Float, nullable=True, comment="总收入")
    cost = Column(Float, nullable=True, comment="总成本")
    profit = Column(Float, nullable=True, comment="总利润")
    order_count = Column(Integer, nullable=True, comment="订单总数")
    item_count = Column(Integer, nullable=True, comment="销售商品总数")
    average_order_value = Column(Float, nullable=True, comment="平均订单价值")
    currency_code = Column(String(3), nullable=True, default="USD", comment="货币代码")
    top_products = Column(JSONB, nullable=True, comment="热销商品列表")
    top_categories = Column(JSONB, nullable=True, comment="热销分类列表")
    top_regions = Column(JSONB, nullable=True, comment="热销地区列表")
    sales_by_time = Column(JSONB, nullable=True, comment="按时间分布的销售数据")
    sales_by_product = Column(JSONB, nullable=True, comment="按商品分布的销售数据")
    sales_by_category = Column(JSONB, nullable=True, comment="按分类分布的销售数据")
    sales_by_region = Column(JSONB, nullable=True, comment="按地区分布的销售数据")
    sales_by_payment_method = Column(JSONB, nullable=True, comment="按支付方式分布的销售数据")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")
    growth_rate = Column(Float, nullable=True, comment="增长率")


class SalesReportSnapshot(Base):
    """销售报表快照，用于保存历史报表数据以便快速访问"""
    __tablename__ = "sales_report_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("sales_reports.id", ondelete="CASCADE"), nullable=False)
    snapshot_date = Column(Date, nullable=False, comment="快照日期")
    period_type = Column(String(20), nullable=False, comment="周期类型，如day, week, month, quarter, year")
    period_value = Column(String(20), nullable=False, comment="周期值，如2023-01, 2023-Q1等")
    revenue = Column(Float, nullable=True, comment="总收入")
    cost = Column(Float, nullable=True, comment="总成本")
    profit = Column(Float, nullable=True, comment="总利润")
    order_count = Column(Integer, nullable=True, comment="订单总数")
    item_count = Column(Integer, nullable=True, comment="销售商品总数")
    data = Column(JSONB, nullable=True, comment="详细数据")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("SalesReport")
