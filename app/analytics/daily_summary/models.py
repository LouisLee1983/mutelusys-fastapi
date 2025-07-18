from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid
from datetime import datetime


class DailySalesSummary(Base):
    """每日销售汇总表 - 存储每日销售核心指标"""
    __tablename__ = "daily_sales_summary"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_date = Column(Date, nullable=False, index=True, comment="报表日期")
    
    # 订单相关指标
    total_orders = Column(Integer, default=0, comment="总订单数")
    total_revenue = Column(Numeric(15, 2), default=0, comment="总销售额")
    total_items_sold = Column(Integer, default=0, comment="总销售商品数")
    avg_order_value = Column(Numeric(10, 2), default=0, comment="平均订单价值")
    
    # 客户相关指标
    new_customers = Column(Integer, default=0, comment="新客户数")
    returning_customers = Column(Integer, default=0, comment="回头客数")
    total_customers = Column(Integer, default=0, comment="总客户数")
    
    # 转化相关指标
    conversion_rate = Column(Numeric(5, 4), default=0, comment="转化率")
    refund_amount = Column(Numeric(15, 2), default=0, comment="退款金额")
    refund_orders = Column(Integer, default=0, comment="退款订单数")
    
    # 按维度分组的数据 (JSON格式存储)
    by_currency = Column(JSON, comment="按货币分组的销售数据")
    by_country = Column(JSON, comment="按国家分组的销售数据")
    by_payment_method = Column(JSON, comment="按支付方式分组")
    
    # 系统字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True


class DailyAdPerformance(Base):
    """每日广告投放效果汇总表"""
    __tablename__ = "daily_ad_performance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_date = Column(Date, nullable=False, index=True, comment="报表日期")
    
    # 广告渠道信息
    channel = Column(String(50), nullable=False, comment="广告渠道")
    campaign_name = Column(String(200), comment="推广活动名称")
    campaign_id = Column(String(100), comment="推广活动ID")
    
    # 展示和点击数据
    impressions = Column(Integer, default=0, comment="展示次数")
    clicks = Column(Integer, default=0, comment="点击次数")
    click_rate = Column(Numeric(5, 4), default=0, comment="点击率")
    
    # 成本数据
    cost = Column(Numeric(15, 2), default=0, comment="广告费用")
    cost_per_click = Column(Numeric(10, 4), default=0, comment="单次点击成本")
    cost_per_acquisition = Column(Numeric(10, 2), default=0, comment="获客成本")
    
    # 转化数据
    conversions = Column(Integer, default=0, comment="转化次数")
    conversion_value = Column(Numeric(15, 2), default=0, comment="转化价值")
    conversion_rate = Column(Numeric(5, 4), default=0, comment="转化率")
    
    # ROI数据
    roi = Column(Numeric(8, 4), default=0, comment="投资回报率")
    roas = Column(Numeric(8, 4), default=0, comment="广告支出回报率")
    
    # 系统字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True


class DailyUserBehavior(Base):
    """每日用户行为汇总表"""
    __tablename__ = "daily_user_behavior"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_date = Column(Date, nullable=False, index=True, comment="报表日期")
    
    # 访问统计
    total_sessions = Column(Integer, default=0, comment="总会话数")
    unique_visitors = Column(Integer, default=0, comment="独立访客数")
    page_views = Column(Integer, default=0, comment="总页面浏览量")
    
    # 行为统计
    bounce_rate = Column(Numeric(5, 4), default=0, comment="跳出率")
    avg_session_duration = Column(Integer, default=0, comment="平均会话时长(秒)")
    avg_pages_per_session = Column(Numeric(5, 2), default=0, comment="平均页面/会话")
    
    # 购物行为
    cart_additions = Column(Integer, default=0, comment="加购物车次数")
    cart_abandonment_rate = Column(Numeric(5, 4), default=0, comment="购物车放弃率")
    checkout_starts = Column(Integer, default=0, comment="开始结账次数")
    
    # 热门内容 (JSON格式存储)
    top_viewed_products = Column(JSON, comment="热门浏览商品")
    top_search_keywords = Column(JSON, comment="热门搜索词")
    top_pages = Column(JSON, comment="热门页面")
    
    # 按维度分组的数据
    by_device_type = Column(JSON, comment="按设备类型分组")
    by_traffic_source = Column(JSON, comment="按流量来源分组")
    by_country = Column(JSON, comment="按国家分组")
    
    # 系统字段  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True


class DailyProductPerformance(Base):
    """每日商品表现汇总表"""
    __tablename__ = "daily_product_performance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_date = Column(Date, nullable=False, index=True, comment="报表日期")
    
    # 商品信息
    product_id = Column(UUID(as_uuid=True), nullable=False, index=True, comment="商品ID")
    product_name = Column(String(500), comment="商品名称")
    sku_code = Column(String(100), comment="商品编码")
    category_name = Column(String(200), comment="分类名称")
    
    # 浏览数据
    views = Column(Integer, default=0, comment="浏览次数")
    unique_views = Column(Integer, default=0, comment="独立浏览数")
    
    # 购买行为
    cart_additions = Column(Integer, default=0, comment="加购次数")
    purchases = Column(Integer, default=0, comment="购买次数")
    quantity_sold = Column(Integer, default=0, comment="销售数量")
    
    # 收入数据
    revenue = Column(Numeric(15, 2), default=0, comment="销售收入")
    avg_selling_price = Column(Numeric(10, 2), default=0, comment="平均售价")
    
    # 转化数据
    view_to_cart_rate = Column(Numeric(5, 4), default=0, comment="浏览到加购转化率")
    cart_to_purchase_rate = Column(Numeric(5, 4), default=0, comment="加购到购买转化率")
    overall_conversion_rate = Column(Numeric(5, 4), default=0, comment="总转化率")
    
    # 库存数据
    stock_level = Column(Integer, default=0, comment="库存水平")
    low_stock_alert = Column(Integer, default=0, comment="低库存预警阈值")
    is_out_of_stock = Column(Integer, default=0, comment="是否缺货 0:有库存 1:缺货")
    
    # 排名数据
    sales_rank = Column(Integer, comment="销售排名")
    view_rank = Column(Integer, comment="浏览排名")
    
    # 系统字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True