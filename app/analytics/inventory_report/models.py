import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import ReportBase, ReportType, ReportStatus


class InventoryReport(ReportBase):
    """库存报表表，跟踪库存变动和预警"""
    __tablename__ = "inventory_reports"

    total_stock_value = Column(Float, nullable=True, comment="总库存价值")
    total_stock_items = Column(Integer, nullable=True, comment="总库存项数")
    total_sku_count = Column(Integer, nullable=True, comment="总SKU数量")
    out_of_stock_items = Column(Integer, nullable=True, comment="缺货商品数")
    low_stock_items = Column(Integer, nullable=True, comment="低库存商品数")
    overstocked_items = Column(Integer, nullable=True, comment="超额库存商品数")
    healthy_stock_items = Column(Integer, nullable=True, comment="健康库存商品数")
    inventory_turnover_rate = Column(Float, nullable=True, comment="库存周转率")
    average_days_on_hand = Column(Float, nullable=True, comment="平均库存周期")
    stock_level_changes = Column(JSONB, nullable=True, comment="库存水平变化")
    top_selling_items = Column(JSONB, nullable=True, comment="热销商品")
    slow_moving_items = Column(JSONB, nullable=True, comment="滞销商品")
    aging_inventory = Column(JSONB, nullable=True, comment="老化库存")
    inventory_by_category = Column(JSONB, nullable=True, comment="按分类的库存情况")
    inventory_by_warehouse = Column(JSONB, nullable=True, comment="按仓库的库存情况")
    inventory_by_supplier = Column(JSONB, nullable=True, comment="按供应商的库存情况")
    restock_recommendations = Column(JSONB, nullable=True, comment="补货建议")
    inventory_value_trend = Column(JSONB, nullable=True, comment="库存价值趋势")
    comparison_period_data = Column(JSONB, nullable=True, comment="对比周期数据")
    currency_code = Column(String(3), nullable=True, default="USD", comment="货币代码")


class InventoryAlert(Base):
    """库存预警表，记录库存异常情况"""
    __tablename__ = "inventory_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, comment="商品ID")
    sku_id = Column(UUID(as_uuid=True), ForeignKey("product_skus.id"), nullable=True, comment="SKU ID")
    warehouse_id = Column(UUID(as_uuid=True), nullable=True, comment="仓库ID（简化处理，不使用外键）")
    alert_type = Column(String(50), nullable=False, comment="预警类型，如out_of_stock, low_stock, overstock")
    alert_level = Column(String(20), nullable=False, comment="预警级别，如normal, warning, critical")
    current_quantity = Column(Integer, nullable=False, comment="当前库存数量")
    threshold = Column(Integer, nullable=True, comment="预警阈值")
    message = Column(String(255), nullable=False, comment="预警消息")
    is_resolved = Column(Boolean, default=False, comment="是否已解决")
    resolved_at = Column(DateTime, nullable=True, comment="解决时间")
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="解决者ID")
    resolution_note = Column(Text, nullable=True, comment="解决说明")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    product = relationship("Product")
    sku = relationship("ProductSku")
    # warehouse = relationship("Warehouse")  # 仓库功能已简化
    resolver = relationship("User", foreign_keys=[resolved_by])
