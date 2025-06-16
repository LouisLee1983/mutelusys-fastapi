import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class MaterialPopularity(ReportBase):
    """材质流行度分析表，追踪不同材质的受欢迎程度"""
    __tablename__ = "material_popularities"

    total_materials = Column(Integer, nullable=True, comment="材质总数")
    top_materials = Column(JSONB, nullable=True, comment="热门材质列表")
    material_product_distribution = Column(JSONB, nullable=True, comment="材质产品分布")
    material_customer_distribution = Column(JSONB, nullable=True, comment="材质客户分布")
    material_view_counts = Column(JSONB, nullable=True, comment="材质浏览次数")
    material_purchase_counts = Column(JSONB, nullable=True, comment="材质购买次数")
    material_conversion_rates = Column(JSONB, nullable=True, comment="材质转化率")
    material_average_order_values = Column(JSONB, nullable=True, comment="材质平均订单价值")
    material_revenue_contribution = Column(JSONB, nullable=True, comment="材质收入贡献")
    material_growth_rates = Column(JSONB, nullable=True, comment="材质增长率")
    material_seasonal_trends = Column(JSONB, nullable=True, comment="材质季节性趋势")
    material_geographic_distribution = Column(JSONB, nullable=True, comment="材质地理分布")
    material_demographic_distribution = Column(JSONB, nullable=True, comment="材质人口统计分布")
    material_cross_selling_patterns = Column(JSONB, nullable=True, comment="材质交叉销售模式")
    material_search_frequency = Column(JSONB, nullable=True, comment="材质搜索频率")
    material_content_engagement = Column(JSONB, nullable=True, comment="材质内容互动")
    material_customer_satisfaction = Column(JSONB, nullable=True, comment="材质客户满意度")
    material_price_sensitivity = Column(JSONB, nullable=True, comment="材质价格敏感度")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")


class MaterialPerformanceMetric(Base):
    """材质表现指标表，记录特定材质的详细表现数据"""
    __tablename__ = "material_performance_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("material_popularities.id", ondelete="CASCADE"), nullable=False)
    material_id = Column(UUID(as_uuid=True), ForeignKey("product_materials.id"), nullable=False, comment="材质ID")
    date = Column(Date, nullable=False, comment="统计日期")
    material_name = Column(String(100), nullable=False, comment="材质名称")
    material_type = Column(String(50), nullable=True, comment="材质类型")
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
    price_range = Column(JSONB, nullable=True, comment="价格范围")
    average_rating = Column(Float, nullable=True, comment="平均评分")
    content_view_count = Column(Integer, nullable=True, comment="相关内容浏览次数")
    related_materials = Column(JSONB, nullable=True, comment="相关材质")
    popular_products = Column(JSONB, nullable=True, comment="热门产品")
    related_intents = Column(JSONB, nullable=True, comment="相关意图")
    related_symbols = Column(JSONB, nullable=True, comment="相关符号")
    customer_segments = Column(JSONB, nullable=True, comment="客户细分")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    report = relationship("MaterialPopularity")
    material = relationship("ProductMaterial")
