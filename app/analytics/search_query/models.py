import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.analytics.models import DeviceType


class SearchQuery(Base):
    """搜索查询记录表，用于优化搜索体验"""
    __tablename__ = "search_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, comment="客户ID，未登录用户为NULL")
    session_id = Column(String(100), nullable=False, comment="会话ID")
    query_text = Column(String(255), nullable=False, comment="搜索文本")
    query_language = Column(String(10), nullable=True, comment="搜索语言代码")
    result_count = Column(Integer, nullable=True, comment="结果数量")
    clicked_results = Column(Integer, nullable=True, default=0, comment="点击结果数量")
    filters_applied = Column(JSONB, nullable=True, comment="应用的筛选条件")
    sort_applied = Column(String(50), nullable=True, comment="应用的排序")
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=True, comment="搜索的分类ID")
    page_number = Column(Integer, nullable=True, default=1, comment="页码")
    per_page = Column(Integer, nullable=True, default=20, comment="每页项数")
    device_type = Column(Enum(DeviceType), nullable=True, comment="设备类型")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    geo_location = Column(JSONB, nullable=True, comment="地理位置")
    is_successful = Column(Boolean, nullable=True, comment="是否成功搜索")
    has_result = Column(Boolean, nullable=True, comment="是否有结果")
    search_time = Column(Float, nullable=True, comment="搜索耗时(秒)")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer")
    category = relationship("ProductCategory")


class SearchQueryMetric(Base):
    """搜索查询指标表，汇总分析搜索数据"""
    __tablename__ = "search_query_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, comment="统计日期")
    total_searches = Column(Integer, nullable=False, default=0, comment="总搜索次数")
    unique_queries = Column(Integer, nullable=False, default=0, comment="独立查询数")
    successful_searches = Column(Integer, nullable=False, default=0, comment="成功搜索次数")
    zero_result_searches = Column(Integer, nullable=False, default=0, comment="零结果搜索次数")
    average_results = Column(Float, nullable=True, comment="平均结果数")
    average_search_time = Column(Float, nullable=True, comment="平均搜索时间(秒)")
    click_through_rate = Column(Float, nullable=True, comment="点击率")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    popular_queries = Column(JSONB, nullable=True, comment="热门查询")
    trending_queries = Column(JSONB, nullable=True, comment="趋势查询")
    zero_result_queries = Column(JSONB, nullable=True, comment="零结果查询")
    top_filters = Column(JSONB, nullable=True, comment="热门筛选条件")
    popular_categories = Column(JSONB, nullable=True, comment="热门搜索分类")
    search_abandonment_rate = Column(Float, nullable=True, comment="搜索放弃率")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SearchSuggestion(Base):
    """搜索建议表，基于历史搜索优化搜索体验"""
    __tablename__ = "search_suggestions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(String(255), nullable=False, comment="查询文本")
    language_code = Column(String(10), nullable=False, comment="语言代码")
    suggestion_type = Column(String(50), nullable=False, comment="建议类型，如popular, trending, related, autocomplete")
    priority = Column(Integer, nullable=False, default=0, comment="优先级")
    search_count = Column(Integer, nullable=False, default=0, comment="搜索次数")
    click_through_rate = Column(Float, nullable=True, comment="点击率")
    conversion_rate = Column(Float, nullable=True, comment="转化率")
    related_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="相关分类ID")
    related_intents = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="相关意图ID")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
