from datetime import date, datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from decimal import Decimal


class DailySalesSummaryBase(BaseModel):
    """每日销售汇总基础模型"""
    report_date: date
    total_orders: int = 0
    total_revenue: Decimal = Field(default=0, decimal_places=2)
    total_items_sold: int = 0
    avg_order_value: Decimal = Field(default=0, decimal_places=2)
    new_customers: int = 0
    returning_customers: int = 0
    total_customers: int = 0
    conversion_rate: Decimal = Field(default=0, decimal_places=4)
    refund_amount: Decimal = Field(default=0, decimal_places=2)
    refund_orders: int = 0
    by_currency: Optional[Dict[str, Any]] = None
    by_country: Optional[Dict[str, Any]] = None
    by_payment_method: Optional[Dict[str, Any]] = None


class DailySalesSummaryCreate(DailySalesSummaryBase):
    """创建每日销售汇总"""
    pass


class DailySalesSummaryResponse(DailySalesSummaryBase):
    """每日销售汇总响应"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DailyAdPerformanceBase(BaseModel):
    """每日广告投放效果基础模型"""
    report_date: date
    channel: str
    campaign_name: Optional[str] = None
    campaign_id: Optional[str] = None
    impressions: int = 0
    clicks: int = 0
    click_rate: Decimal = Field(default=0, decimal_places=4)
    cost: Decimal = Field(default=0, decimal_places=2)
    cost_per_click: Decimal = Field(default=0, decimal_places=4)
    cost_per_acquisition: Decimal = Field(default=0, decimal_places=2)
    conversions: int = 0
    conversion_value: Decimal = Field(default=0, decimal_places=2)
    conversion_rate: Decimal = Field(default=0, decimal_places=4)
    roi: Decimal = Field(default=0, decimal_places=4)
    roas: Decimal = Field(default=0, decimal_places=4)


class DailyAdPerformanceCreate(DailyAdPerformanceBase):
    """创建每日广告投放效果"""
    pass


class DailyAdPerformanceResponse(DailyAdPerformanceBase):
    """每日广告投放效果响应"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DailyUserBehaviorBase(BaseModel):
    """每日用户行为基础模型"""
    report_date: date
    total_sessions: int = 0
    unique_visitors: int = 0
    page_views: int = 0
    bounce_rate: Decimal = Field(default=0, decimal_places=4)
    avg_session_duration: int = 0
    avg_pages_per_session: Decimal = Field(default=0, decimal_places=2)
    cart_additions: int = 0
    cart_abandonment_rate: Decimal = Field(default=0, decimal_places=4)
    checkout_starts: int = 0
    top_viewed_products: Optional[List[Dict[str, Any]]] = None
    top_search_keywords: Optional[List[Dict[str, Any]]] = None
    top_pages: Optional[List[Dict[str, Any]]] = None
    by_device_type: Optional[Dict[str, Any]] = None
    by_traffic_source: Optional[Dict[str, Any]] = None
    by_country: Optional[Dict[str, Any]] = None


class DailyUserBehaviorCreate(DailyUserBehaviorBase):
    """创建每日用户行为"""
    pass


class DailyUserBehaviorResponse(DailyUserBehaviorBase):
    """每日用户行为响应"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DailyProductPerformanceBase(BaseModel):
    """每日商品表现基础模型"""
    report_date: date
    product_id: str
    product_name: Optional[str] = None
    sku_code: Optional[str] = None
    category_name: Optional[str] = None
    views: int = 0
    unique_views: int = 0
    cart_additions: int = 0
    purchases: int = 0
    quantity_sold: int = 0
    revenue: Decimal = Field(default=0, decimal_places=2)
    avg_selling_price: Decimal = Field(default=0, decimal_places=2)
    view_to_cart_rate: Decimal = Field(default=0, decimal_places=4)
    cart_to_purchase_rate: Decimal = Field(default=0, decimal_places=4)
    overall_conversion_rate: Decimal = Field(default=0, decimal_places=4)
    stock_level: int = 0
    low_stock_alert: int = 0
    is_out_of_stock: int = 0
    sales_rank: Optional[int] = None
    view_rank: Optional[int] = None


class DailyProductPerformanceCreate(DailyProductPerformanceBase):
    """创建每日商品表现"""
    pass


class DailyProductPerformanceResponse(DailyProductPerformanceBase):
    """每日商品表现响应"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DailySummaryRequest(BaseModel):
    """每日汇总请求"""
    target_date: Optional[date] = None
    force_refresh: bool = False


class DailySummaryResponse(BaseModel):
    """每日汇总响应"""
    date: date
    sales_summary: DailySalesSummaryResponse
    behavior_summary: DailyUserBehaviorResponse
    product_performances_count: int
    generated_at: datetime


class DateRangeRequest(BaseModel):
    """日期范围请求"""
    start_date: date
    end_date: date
    limit: Optional[int] = 100


class SalesReportResponse(BaseModel):
    """销售报表响应"""
    date_range: Dict[str, date]
    total_orders: int
    total_revenue: Decimal
    avg_order_value: Decimal
    total_customers: int
    conversion_rate: Decimal
    daily_data: List[DailySalesSummaryResponse]
    trends: Dict[str, Any]


class UserBehaviorReportResponse(BaseModel):
    """用户行为报表响应"""
    date_range: Dict[str, date]
    total_sessions: int
    unique_visitors: int
    page_views: int
    avg_session_duration: int
    daily_data: List[DailyUserBehaviorResponse]
    top_products: List[Dict[str, Any]]
    top_keywords: List[Dict[str, Any]]


class ProductPerformanceReportResponse(BaseModel):
    """商品表现报表响应"""
    date_range: Dict[str, date]
    total_products: int
    top_performers: List[DailyProductPerformanceResponse]
    category_performance: Dict[str, Any]
    stock_alerts: List[Dict[str, Any]]


class AdPerformanceReportResponse(BaseModel):
    """广告表现报表响应"""
    date_range: Dict[str, date]
    total_cost: Decimal
    total_conversions: int
    avg_roi: Decimal
    daily_data: List[DailyAdPerformanceResponse]
    channel_performance: Dict[str, Any]


class DashboardSummaryResponse(BaseModel):
    """仪表板汇总响应"""
    today: DailySalesSummaryResponse
    yesterday: DailySalesSummaryResponse
    this_week: Dict[str, Any]
    this_month: Dict[str, Any]
    key_metrics: Dict[str, Any]
    alerts: List[Dict[str, Any]]
    charts_data: Dict[str, Any]