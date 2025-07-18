-- 数据库模型同步SQL语句
-- 生成时间: 2025-06-24 14:58:02.481140
-- 注意: 执行前请备份数据库!


-- ========== 模块: analytics ==========

-- 表: ai_call_records (模型: AICallRecord)
ALTER TABLE ai_call_records ALTER COLUMN cost TYPE REAL;
ALTER TABLE ai_call_records ALTER COLUMN confidence_score TYPE REAL;
ALTER TABLE ai_call_records ALTER COLUMN created_at SET NOT NULL;
ALTER TABLE ai_call_records ALTER COLUMN updated_at SET NOT NULL;

-- 表: behavior_funnels (模型: BehaviorFunnel)
CREATE TABLE behavior_funnels (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    funnel_steps JSONB NOT NULL,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    date_range VARCHAR(50),
    step_conversion_rates JSONB,
    overall_conversion_rate REAL,
    average_time_to_convert REAL,
    dropoff_analysis JSONB,
    segment_performance JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: campaign_performance_metrics (模型: CampaignPerformanceMetric)
CREATE TABLE campaign_performance_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    campaign_id UUID NOT NULL,
    campaign_name VARCHAR(100) NOT NULL,
    campaign_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget REAL,
    spend REAL,
    revenue REAL,
    roi REAL,
    impressions INTEGER,
    clicks INTEGER,
    conversions INTEGER,
    conversion_rate REAL,
    cost_per_click REAL,
    cost_per_acquisition REAL,
    target_audience VARCHAR(100),
    channels ARRAY,
    performance_metrics JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_element_trends (模型: CulturalElementTrend)
CREATE TABLE cultural_element_trends (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    element_type VARCHAR(50) NOT NULL,
    element_id UUID,
    element_name VARCHAR(100) NOT NULL,
    trend_period VARCHAR(50) NOT NULL,
    trend_score REAL NOT NULL,
    trend_direction VARCHAR(20) NOT NULL,
    growth_rate REAL,
    view_count_trend JSONB,
    search_count_trend JSONB,
    purchase_count_trend JSONB,
    engagement_rate_trend JSONB,
    related_elements JSONB,
    audience_segments JSONB,
    regional_popularity JSONB,
    seasonal_factors JSONB,
    trend_prediction JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_trend_reports (模型: CulturalTrendReport)
CREATE TABLE cultural_trend_reports (
    trending_symbols JSONB,
    trending_cultural_stories JSONB,
    trending_cultural_regions JSONB,
    trending_cultural_elements JSONB,
    trend_correlations JSONB,
    search_trend_analysis JSONB,
    view_trend_analysis JSONB,
    purchase_trend_analysis JSONB,
    geographic_trend_distribution JSONB,
    demographic_trend_distribution JSONB,
    season_based_trends JSONB,
    cultural_calendar_correlation JSONB,
    content_engagement_trends JSONB,
    rising_cultural_interests JSONB,
    declining_cultural_interests JSONB,
    trending_cross_cultural_combinations JSONB,
    predicted_future_trends JSONB,
    comparison_period_data JSONB,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: customer_reports (模型: CustomerReport)
CREATE TABLE customer_reports (
    total_customers INTEGER,
    new_customers INTEGER,
    active_customers INTEGER,
    inactive_customers INTEGER,
    returning_customers INTEGER,
    average_order_frequency REAL,
    average_customer_lifetime_value REAL,
    churn_rate REAL,
    retention_rate REAL,
    conversion_rate REAL,
    top_customer_segments JSONB,
    customer_acquisition_cost REAL,
    customers_by_region JSONB,
    customers_by_age JSONB,
    customers_by_gender JSONB,
    customers_by_intent JSONB,
    customers_by_cultural_preference JSONB,
    customers_by_purchase_value JSONB,
    comparison_period_data JSONB,
    growth_rate REAL,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: customer_segment_analyses (模型: CustomerSegmentAnalysis)
CREATE TABLE customer_segment_analyses (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    segment_name VARCHAR(100) NOT NULL,
    segment_description VARCHAR(255),
    customer_count INTEGER,
    average_order_value REAL,
    purchase_frequency REAL,
    preferred_products JSONB,
    preferred_categories JSONB,
    preferred_intents JSONB,
    preferred_cultural_elements JSONB,
    engagement_metrics JSONB,
    lifetime_value REAL,
    potential_value REAL,
    marketing_recommendations TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: daily_ad_performance (模型: DailyAdPerformance)
CREATE TABLE daily_ad_performance (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_date DATE NOT NULL,
    channel VARCHAR(50) NOT NULL,
    campaign_name VARCHAR(200),
    campaign_id VARCHAR(100),
    impressions INTEGER DEFAULT ScalarElementColumnDefault(0),
    clicks INTEGER DEFAULT ScalarElementColumnDefault(0),
    click_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    cost NUMERIC(15, 2) DEFAULT ScalarElementColumnDefault(0),
    cost_per_click NUMERIC(10, 4) DEFAULT ScalarElementColumnDefault(0),
    cost_per_acquisition NUMERIC(10, 2) DEFAULT ScalarElementColumnDefault(0),
    conversions INTEGER DEFAULT ScalarElementColumnDefault(0),
    conversion_value NUMERIC(15, 2) DEFAULT ScalarElementColumnDefault(0),
    conversion_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    roi NUMERIC(8, 4) DEFAULT ScalarElementColumnDefault(0),
    roas NUMERIC(8, 4) DEFAULT ScalarElementColumnDefault(0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: daily_product_performance (模型: DailyProductPerformance)
CREATE TABLE daily_product_performance (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_date DATE NOT NULL,
    product_id UUID NOT NULL,
    product_name VARCHAR(500),
    sku_code VARCHAR(100),
    category_name VARCHAR(200),
    views INTEGER DEFAULT ScalarElementColumnDefault(0),
    unique_views INTEGER DEFAULT ScalarElementColumnDefault(0),
    cart_additions INTEGER DEFAULT ScalarElementColumnDefault(0),
    purchases INTEGER DEFAULT ScalarElementColumnDefault(0),
    quantity_sold INTEGER DEFAULT ScalarElementColumnDefault(0),
    revenue NUMERIC(15, 2) DEFAULT ScalarElementColumnDefault(0),
    avg_selling_price NUMERIC(10, 2) DEFAULT ScalarElementColumnDefault(0),
    view_to_cart_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    cart_to_purchase_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    overall_conversion_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    stock_level INTEGER DEFAULT ScalarElementColumnDefault(0),
    low_stock_alert INTEGER DEFAULT ScalarElementColumnDefault(0),
    is_out_of_stock INTEGER DEFAULT ScalarElementColumnDefault(0),
    sales_rank INTEGER,
    view_rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: daily_sales_summary (模型: DailySalesSummary)
CREATE TABLE daily_sales_summary (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_date DATE NOT NULL,
    total_orders INTEGER DEFAULT ScalarElementColumnDefault(0),
    total_revenue NUMERIC(15, 2) DEFAULT ScalarElementColumnDefault(0),
    total_items_sold INTEGER DEFAULT ScalarElementColumnDefault(0),
    avg_order_value NUMERIC(10, 2) DEFAULT ScalarElementColumnDefault(0),
    new_customers INTEGER DEFAULT ScalarElementColumnDefault(0),
    returning_customers INTEGER DEFAULT ScalarElementColumnDefault(0),
    total_customers INTEGER DEFAULT ScalarElementColumnDefault(0),
    conversion_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    refund_amount NUMERIC(15, 2) DEFAULT ScalarElementColumnDefault(0),
    refund_orders INTEGER DEFAULT ScalarElementColumnDefault(0),
    by_currency JSONB,
    by_country JSONB,
    by_payment_method JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: daily_user_behavior (模型: DailyUserBehavior)
CREATE TABLE daily_user_behavior (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_date DATE NOT NULL,
    total_sessions INTEGER DEFAULT ScalarElementColumnDefault(0),
    unique_visitors INTEGER DEFAULT ScalarElementColumnDefault(0),
    page_views INTEGER DEFAULT ScalarElementColumnDefault(0),
    bounce_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    avg_session_duration INTEGER DEFAULT ScalarElementColumnDefault(0),
    avg_pages_per_session NUMERIC(5, 2) DEFAULT ScalarElementColumnDefault(0),
    cart_additions INTEGER DEFAULT ScalarElementColumnDefault(0),
    cart_abandonment_rate NUMERIC(5, 4) DEFAULT ScalarElementColumnDefault(0),
    checkout_starts INTEGER DEFAULT ScalarElementColumnDefault(0),
    top_viewed_products JSONB,
    top_search_keywords JSONB,
    top_pages JSONB,
    by_device_type JSONB,
    by_traffic_source JSONB,
    by_country JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: intent_analytics (模型: IntentAnalytics)
CREATE TABLE intent_analytics (
    total_intents INTEGER,
    top_intents JSONB,
    intent_product_distribution JSONB,
    intent_customer_distribution JSONB,
    intent_view_counts JSONB,
    intent_purchase_counts JSONB,
    intent_conversion_rates JSONB,
    intent_average_order_values JSONB,
    intent_revenue_contribution JSONB,
    intent_growth_rates JSONB,
    intent_seasonal_trends JSONB,
    intent_geographic_distribution JSONB,
    intent_demographic_distribution JSONB,
    intent_cross_selling_patterns JSONB,
    intent_search_frequency JSONB,
    intent_return_rates JSONB,
    intent_customer_satisfaction JSONB,
    comparison_period_data JSONB,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: intent_performance_metrics (模型: IntentPerformanceMetric)
CREATE TABLE intent_performance_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    intent_id UUID NOT NULL,
    date DATE NOT NULL,
    intent_name VARCHAR(100) NOT NULL,
    product_count INTEGER,
    view_count INTEGER,
    search_count INTEGER,
    add_to_cart_count INTEGER,
    purchase_count INTEGER,
    revenue REAL,
    conversion_rate REAL,
    average_order_value REAL,
    customer_count INTEGER,
    new_customer_percentage REAL,
    return_rate REAL,
    repurchase_rate REAL,
    average_rating REAL,
    related_intents JSONB,
    popular_products JSONB,
    customer_segments JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: inventory_alerts (模型: InventoryAlert)
CREATE TABLE inventory_alerts (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    sku_id UUID,
    warehouse_id UUID,
    alert_type VARCHAR(50) NOT NULL,
    alert_level VARCHAR(20) NOT NULL,
    current_quantity INTEGER NOT NULL,
    threshold INTEGER,
    message VARCHAR(255) NOT NULL,
    is_resolved BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    resolved_at TIMESTAMP,
    resolved_by UUID,
    resolution_note TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: inventory_reports (模型: InventoryReport)
CREATE TABLE inventory_reports (
    total_stock_value REAL,
    total_stock_items INTEGER,
    total_sku_count INTEGER,
    out_of_stock_items INTEGER,
    low_stock_items INTEGER,
    overstocked_items INTEGER,
    healthy_stock_items INTEGER,
    inventory_turnover_rate REAL,
    average_days_on_hand REAL,
    stock_level_changes JSONB,
    top_selling_items JSONB,
    slow_moving_items JSONB,
    aging_inventory JSONB,
    inventory_by_category JSONB,
    inventory_by_warehouse JSONB,
    inventory_by_supplier JSONB,
    restock_recommendations JSONB,
    inventory_value_trend JSONB,
    comparison_period_data JSONB,
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: marketing_reports (模型: MarketingReport)
CREATE TABLE marketing_reports (
    total_marketing_spend REAL,
    total_revenue_generated REAL,
    total_roi REAL,
    total_impressions INTEGER,
    total_clicks INTEGER,
    total_conversions INTEGER,
    conversion_rate REAL,
    cost_per_click REAL,
    cost_per_acquisition REAL,
    campaign_performance JSONB,
    channel_performance JSONB,
    coupon_performance JSONB,
    thematic_campaign_performance JSONB,
    intent_based_marketing_performance JSONB,
    cultural_content_performance JSONB,
    affiliate_performance JSONB,
    promotional_effectiveness JSONB,
    marketing_spend_by_channel JSONB,
    marketing_spend_by_campaign JSONB,
    marketing_spend_by_period JSONB,
    top_performing_campaigns JSONB,
    customer_acquisition_by_channel JSONB,
    comparison_period_data JSONB,
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: material_performance_metrics (模型: MaterialPerformanceMetric)
CREATE TABLE material_performance_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    material_id UUID NOT NULL,
    date DATE NOT NULL,
    material_name VARCHAR(100) NOT NULL,
    material_type VARCHAR(50),
    product_count INTEGER,
    view_count INTEGER,
    search_count INTEGER,
    add_to_cart_count INTEGER,
    purchase_count INTEGER,
    revenue REAL,
    conversion_rate REAL,
    average_order_value REAL,
    customer_count INTEGER,
    new_customer_percentage REAL,
    price_range JSONB,
    average_rating REAL,
    content_view_count INTEGER,
    related_materials JSONB,
    popular_products JSONB,
    related_intents JSONB,
    related_symbols JSONB,
    customer_segments JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: material_popularities (模型: MaterialPopularity)
CREATE TABLE material_popularities (
    total_materials INTEGER,
    top_materials JSONB,
    material_product_distribution JSONB,
    material_customer_distribution JSONB,
    material_view_counts JSONB,
    material_purchase_counts JSONB,
    material_conversion_rates JSONB,
    material_average_order_values JSONB,
    material_revenue_contribution JSONB,
    material_growth_rates JSONB,
    material_seasonal_trends JSONB,
    material_geographic_distribution JSONB,
    material_demographic_distribution JSONB,
    material_cross_selling_patterns JSONB,
    material_search_frequency JSONB,
    material_content_engagement JSONB,
    material_customer_satisfaction JSONB,
    material_price_sensitivity JSONB,
    comparison_period_data JSONB,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: page_view_stats (模型: PageViewStats)
CREATE TABLE page_view_stats (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    page_url VARCHAR(255) NOT NULL,
    page_title VARCHAR(255),
    page_type VARCHAR(50),
    object_id UUID,
    views INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    unique_views INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    average_time_on_page REAL,
    bounce_rate REAL,
    exit_rate REAL,
    device_breakdown JSONB,
    referrer_breakdown JSONB,
    conversion_rate REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: product_ai_analyses (模型: ProductAIAnalysis)
ALTER TABLE product_ai_analyses ALTER COLUMN analysis_confidence TYPE REAL;
ALTER TABLE product_ai_analyses ALTER COLUMN created_at SET NOT NULL;
ALTER TABLE product_ai_analyses ALTER COLUMN updated_at SET NOT NULL;

-- 表: sales_report_snapshots (模型: SalesReportSnapshot)
CREATE TABLE sales_report_snapshots (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    snapshot_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    period_value VARCHAR(20) NOT NULL,
    revenue REAL,
    cost REAL,
    profit REAL,
    order_count INTEGER,
    item_count INTEGER,
    data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: sales_reports (模型: SalesReport)
CREATE TABLE sales_reports (
    revenue REAL,
    cost REAL,
    profit REAL,
    order_count INTEGER,
    item_count INTEGER,
    average_order_value REAL,
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    top_products JSONB,
    top_categories JSONB,
    top_regions JSONB,
    sales_by_time JSONB,
    sales_by_product JSONB,
    sales_by_category JSONB,
    sales_by_region JSONB,
    sales_by_payment_method JSONB,
    comparison_period_data JSONB,
    growth_rate REAL,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: scenario_conversions (模型: ScenarioConversion)
CREATE TABLE scenario_conversions (
    total_scenes INTEGER,
    top_scenes JSONB,
    scene_product_distribution JSONB,
    scene_customer_distribution JSONB,
    scene_view_counts JSONB,
    scene_purchase_counts JSONB,
    scene_conversion_rates JSONB,
    scene_average_order_values JSONB,
    scene_revenue_contribution JSONB,
    scene_growth_rates JSONB,
    scene_seasonal_trends JSONB,
    scene_geographic_distribution JSONB,
    scene_demographic_distribution JSONB,
    scene_cross_selling_patterns JSONB,
    scene_search_frequency JSONB,
    scene_content_engagement JSONB,
    scene_customer_satisfaction JSONB,
    comparison_period_data JSONB,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: scene_performance_metrics (模型: ScenePerformanceMetric)
CREATE TABLE scene_performance_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    scene_id UUID NOT NULL,
    date DATE NOT NULL,
    scene_name VARCHAR(100) NOT NULL,
    product_count INTEGER,
    view_count INTEGER,
    search_count INTEGER,
    add_to_cart_count INTEGER,
    purchase_count INTEGER,
    revenue REAL,
    conversion_rate REAL,
    average_order_value REAL,
    customer_count INTEGER,
    new_customer_percentage REAL,
    return_rate REAL,
    content_view_count INTEGER,
    related_scenes JSONB,
    popular_products JSONB,
    related_intents JSONB,
    related_symbols JSONB,
    customer_segments JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: search_queries (模型: SearchQuery)
CREATE TABLE search_queries (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    customer_id UUID,
    session_id VARCHAR(100) NOT NULL,
    query_text VARCHAR(255) NOT NULL,
    query_language VARCHAR(10),
    result_count INTEGER,
    clicked_results INTEGER DEFAULT ScalarElementColumnDefault(0),
    filters_applied JSONB,
    sort_applied VARCHAR(50),
    category_id UUID,
    page_number INTEGER DEFAULT ScalarElementColumnDefault(1),
    per_page INTEGER DEFAULT ScalarElementColumnDefault(20),
    device_type VARCHAR(7),
    ip_address VARCHAR(50),
    geo_location JSONB,
    is_successful BOOLEAN,
    has_result BOOLEAN,
    search_time REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: search_query_metrics (模型: SearchQueryMetric)
CREATE TABLE search_query_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    date TIMESTAMP NOT NULL,
    total_searches INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    unique_queries INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    successful_searches INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    zero_result_searches INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    average_results REAL,
    average_search_time REAL,
    click_through_rate REAL,
    conversion_rate REAL,
    popular_queries JSONB,
    trending_queries JSONB,
    zero_result_queries JSONB,
    top_filters JSONB,
    popular_categories JSONB,
    search_abandonment_rate REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: search_suggestions (模型: SearchSuggestion)
CREATE TABLE search_suggestions (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    query_text VARCHAR(255) NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    suggestion_type VARCHAR(50) NOT NULL,
    priority INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    search_count INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    click_through_rate REAL,
    conversion_rate REAL,
    related_categories ARRAY,
    related_intents ARRAY,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: symbol_performance_metrics (模型: SymbolPerformanceMetric)
CREATE TABLE symbol_performance_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    symbol_id UUID NOT NULL,
    date DATE NOT NULL,
    symbol_name VARCHAR(100) NOT NULL,
    product_count INTEGER,
    view_count INTEGER,
    search_count INTEGER,
    add_to_cart_count INTEGER,
    purchase_count INTEGER,
    revenue REAL,
    conversion_rate REAL,
    average_order_value REAL,
    customer_count INTEGER,
    new_customer_percentage REAL,
    cultural_regions JSONB,
    content_view_count INTEGER,
    related_symbols JSONB,
    popular_products JSONB,
    related_intents JSONB,
    customer_segments JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: symbol_performances (模型: SymbolPerformance)
CREATE TABLE symbol_performances (
    total_symbols INTEGER,
    top_symbols JSONB,
    symbol_product_distribution JSONB,
    symbol_customer_distribution JSONB,
    symbol_view_counts JSONB,
    symbol_purchase_counts JSONB,
    symbol_conversion_rates JSONB,
    symbol_average_order_values JSONB,
    symbol_revenue_contribution JSONB,
    symbol_growth_rates JSONB,
    symbol_seasonal_trends JSONB,
    symbol_geographic_distribution JSONB,
    symbol_demographic_distribution JSONB,
    symbol_cultural_preference_correlation JSONB,
    symbol_search_frequency JSONB,
    symbol_content_engagement JSONB,
    symbol_customer_satisfaction JSONB,
    comparison_period_data JSONB,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: theme_performance_metrics (模型: ThemePerformanceMetric)
CREATE TABLE theme_performance_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL,
    theme_id UUID NOT NULL,
    date DATE NOT NULL,
    theme_name VARCHAR(100) NOT NULL,
    theme_type VARCHAR(50),
    is_seasonal BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    season_info VARCHAR(50),
    launch_date DATE,
    end_date DATE,
    product_count INTEGER,
    bundle_count INTEGER,
    view_count INTEGER,
    search_count INTEGER,
    add_to_cart_count INTEGER,
    purchase_count INTEGER,
    revenue REAL,
    conversion_rate REAL,
    average_order_value REAL,
    customer_count INTEGER,
    new_customer_percentage REAL,
    marketing_spend REAL,
    marketing_roi REAL,
    popular_products JSONB,
    customer_segments JSONB,
    related_themes JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: theme_performances (模型: ThemePerformance)
CREATE TABLE theme_performances (
    total_themes INTEGER,
    active_themes INTEGER,
    top_themes JSONB,
    theme_product_distribution JSONB,
    theme_customer_distribution JSONB,
    theme_view_counts JSONB,
    theme_purchase_counts JSONB,
    theme_conversion_rates JSONB,
    theme_average_order_values JSONB,
    theme_revenue_contribution JSONB,
    theme_growth_rates JSONB,
    theme_seasonal_performance JSONB,
    theme_geographic_distribution JSONB,
    theme_demographic_distribution JSONB,
    theme_marketing_effectiveness JSONB,
    theme_bundle_performance JSONB,
    theme_cross_selling_patterns JSONB,
    theme_customer_retention JSONB,
    comparison_period_data JSONB,
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    report_type VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportType.DAILY: 'daily'>),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<ReportStatus.PENDING: 'pending'>),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    dimensions ARRAY,
    filters JSONB,
    data JSONB,
    file_url VARCHAR(255),
    scheduled BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    schedule_config JSONB,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: user_behavior_logs (模型: UserBehaviorLog)
CREATE TABLE user_behavior_logs (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    customer_id UUID,
    session_id VARCHAR(100) NOT NULL,
    behavior_type VARCHAR(15) NOT NULL,
    page_url VARCHAR(255),
    page_title VARCHAR(255),
    referrer_url VARCHAR(255),
    object_type VARCHAR(50),
    object_id UUID,
    device_type VARCHAR(7),
    device_info JSONB,
    ip_address VARCHAR(50),
    user_agent VARCHAR(255),
    geo_location JSONB,
    action_details JSONB,
    event_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: user_behavior_metrics (模型: UserBehaviorMetric)
CREATE TABLE user_behavior_metrics (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    date TIMESTAMP NOT NULL,
    behavior_type VARCHAR(15) NOT NULL,
    count INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    unique_users INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    unique_sessions INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    logged_in_ratio REAL,
    new_user_ratio REAL,
    average_duration REAL,
    conversion_rate REAL,
    bounce_rate REAL,
    top_objects JSONB,
    device_breakdown JSONB,
    geo_breakdown JSONB,
    referrer_breakdown JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: visit_sessions (模型: VisitSession)
CREATE TABLE visit_sessions (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) NOT NULL,
    customer_id UUID,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration REAL,
    is_bounce BOOLEAN,
    page_views INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    landing_page VARCHAR(255),
    exit_page VARCHAR(255),
    referrer_url VARCHAR(255),
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    device_type VARCHAR(7),
    browser VARCHAR(100),
    os VARCHAR(100),
    ip_address VARCHAR(50),
    geo_location JSONB,
    language VARCHAR(10),
    is_new_visitor BOOLEAN,
    has_conversion BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    conversion_type VARCHAR(50),
    conversion_value REAL,
    page_path_sequence ARRAY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: visit_stats (模型: VisitStats)
CREATE TABLE visit_stats (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    total_visits INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    unique_visitors INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    returning_visitors INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    new_visitors INTEGER NOT NULL DEFAULT ScalarElementColumnDefault(0),
    bounce_rate REAL,
    average_session_duration REAL,
    average_page_views REAL,
    top_entry_pages JSONB,
    top_exit_pages JSONB,
    traffic_sources JSONB,
    device_breakdown JSONB,
    browser_breakdown JSONB,
    geo_breakdown JSONB,
    language_breakdown JSONB,
    time_of_day_breakdown JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- ========== 模块: content ==========

-- 表: banner_translations (模型: BannerTranslation)
CREATE TABLE banner_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    banner_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    description TEXT,
    button_text VARCHAR(50),
    alt_text VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: banners (模型: Banner)
CREATE TABLE banners (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    type VARCHAR(15) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    mobile_image_url VARCHAR(255),
    link_url VARCHAR(255),
    position VARCHAR(50),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    alt_text VARCHAR(255),
    open_in_new_tab BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    additional_css TEXT,
    additional_info JSONB,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: blog_categories (模型: BlogCategory)
CREATE TABLE blog_categories (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id UUID,
    image_url VARCHAR(255),
    icon VARCHAR(100),
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: blog_category_translations (模型: BlogCategoryTranslation)
CREATE TABLE blog_category_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    category_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: blog_tag_translations (模型: BlogTagTranslation)
CREATE TABLE blog_tag_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    tag_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: blog_tags (模型: BlogTag)
CREATE TABLE blog_tags (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: blog_translations (模型: BlogTranslation)
CREATE TABLE blog_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    excerpt TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: blogs (模型: Blog)
CREATE TABLE blogs (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    slug VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    excerpt TEXT,
    category_id UUID,
    featured_image VARCHAR(255),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    is_commentable BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    author_id UUID,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    published_at TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_calendar_translations (模型: CulturalCalendarTranslation)
CREATE TABLE cultural_calendar_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    calendar_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    cultural_region VARCHAR(100),
    significance TEXT,
    traditions TEXT,
    symbols TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_calendars (模型: CulturalCalendar)
CREATE TABLE cultural_calendars (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    event_type VARCHAR(10) NOT NULL,
    cultural_region VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE,
    is_lunar_date BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    recurrence_type VARCHAR(12) NOT NULL DEFAULT ScalarElementColumnDefault(<RecurrenceType.YEARLY: 'yearly'>),
    recurrence_details JSONB,
    significance TEXT,
    traditions TEXT,
    symbols TEXT,
    featured_image VARCHAR(255),
    external_link VARCHAR(255),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.PUBLISHED: 'published'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_stories (模型: CulturalStory)
CREATE TABLE cultural_stories (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    cultural_region VARCHAR(14) NOT NULL,
    historical_period VARCHAR(100),
    featured_image VARCHAR(255),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    additional_media JSONB,
    published_at TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_story_translations (模型: CulturalStoryTranslation)
CREATE TABLE cultural_story_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    historical_period VARCHAR(100),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: faq_translations (模型: FAQTranslation)
CREATE TABLE faq_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    faq_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    question VARCHAR(500) NOT NULL,
    answer TEXT NOT NULL,
    custom_category VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: faqs (模型: FAQ)
CREATE TABLE faqs (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    question VARCHAR(500) NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(8) NOT NULL DEFAULT ScalarElementColumnDefault(<FAQCategory.GENERAL: 'general'>),
    custom_category VARCHAR(100),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.PUBLISHED: 'published'>),
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: intention_guide_translations (模型: IntentionGuideTranslation)
CREATE TABLE intention_guide_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    guide_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    usage_steps TEXT,
    ritual_description TEXT,
    placement_guidance TEXT,
    wearing_guidance TEXT,
    activation_method TEXT,
    maintenance_tips TEXT,
    best_practices TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: intention_guides (模型: IntentionGuide)
CREATE TABLE intention_guides (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    usage_steps TEXT,
    ritual_description TEXT,
    placement_guidance TEXT,
    wearing_guidance TEXT,
    activation_method TEXT,
    maintenance_tips TEXT,
    best_practices TEXT,
    featured_image VARCHAR(255),
    additional_images ARRAY,
    video_url VARCHAR(255),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    published_at TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: material_guide_translations (模型: MaterialGuideTranslation)
CREATE TABLE material_guide_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    guide_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    origin VARCHAR(100),
    physical_properties TEXT,
    spiritual_properties TEXT,
    care_instructions TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: material_guides (模型: MaterialGuide)
CREATE TABLE material_guides (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    material_type VARCHAR(7) NOT NULL,
    origin VARCHAR(100),
    physical_properties TEXT,
    spiritual_properties TEXT,
    care_instructions TEXT,
    featured_image VARCHAR(255),
    additional_images ARRAY,
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    video_url VARCHAR(255),
    published_at TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: meditation_guide_translations (模型: MeditationGuideTranslation)
CREATE TABLE meditation_guide_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    guide_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    benefits TEXT,
    instructions TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: meditation_guides (模型: MeditationGuide)
CREATE TABLE meditation_guides (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    meditation_type VARCHAR(15) NOT NULL,
    experience_level VARCHAR(12) NOT NULL DEFAULT ScalarElementColumnDefault(<ExperienceLevel.ALL_LEVELS: 'all_levels'>),
    duration_minutes INTEGER,
    benefits TEXT,
    instructions TEXT,
    audio_url VARCHAR(255),
    video_url VARCHAR(255),
    featured_image VARCHAR(255),
    additional_images ARRAY,
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    published_at TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: navigation_menu_item_translations (模型: NavigationMenuItemTranslation)
CREATE TABLE navigation_menu_item_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    menu_item_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: navigation_menu_items (模型: NavigationMenuItem)
CREATE TABLE navigation_menu_items (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    menu_id UUID NOT NULL,
    parent_id UUID,
    title VARCHAR(100) NOT NULL,
    type VARCHAR(8) NOT NULL DEFAULT ScalarElementColumnDefault(<MenuItemType.LINK: 'link'>),
    url VARCHAR(255),
    page_id UUID,
    category_id UUID,
    icon VARCHAR(100),
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    open_in_new_tab BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: navigation_menus (模型: NavigationMenu)
CREATE TABLE navigation_menus (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: page_translations (模型: PageTranslation)
CREATE TABLE page_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    page_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: pages (模型: Page)
CREATE TABLE pages (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    slug VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    template VARCHAR(100),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    is_homepage BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    featured_image VARCHAR(255),
    published_at TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: promotion_content_translations (模型: PromotionContentTranslation)
CREATE TABLE promotion_content_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    short_text VARCHAR(100),
    button_text VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: promotion_contents (模型: PromotionContent)
CREATE TABLE promotion_contents (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content_type VARCHAR(14) NOT NULL,
    promotion_id UUID,
    short_text VARCHAR(100),
    content TEXT,
    button_text VARCHAR(50),
    link_url VARCHAR(255),
    background_color VARCHAR(7),
    text_color VARCHAR(7),
    font_size VARCHAR(20),
    position VARCHAR(50),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    target_pages JSONB,
    target_countries JSONB,
    target_languages JSONB,
    additional_settings JSONB,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: promotion_text_templates (模型: PromotionTextTemplate)
CREATE TABLE promotion_text_templates (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    content_type VARCHAR(14) NOT NULL,
    template_title VARCHAR(255) NOT NULL,
    template_content TEXT,
    template_variables JSONB,
    default_styles JSONB,
    usage_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: scene_based_content_translations (模型: SceneBasedContentTranslation)
CREATE TABLE scene_based_content_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    excerpt TEXT,
    space_design TEXT,
    color_scheme TEXT,
    lighting_tips TEXT,
    product_placement TEXT,
    styling_tips TEXT,
    maintenance_guidance TEXT,
    mood_enhancement TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: scene_based_contents (模型: SceneBasedContent)
CREATE TABLE scene_based_contents (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    space_design TEXT,
    color_scheme TEXT,
    lighting_tips TEXT,
    product_placement TEXT,
    styling_tips TEXT,
    maintenance_guidance TEXT,
    mood_enhancement TEXT,
    featured_image VARCHAR(255),
    additional_images ARRAY,
    video_url VARCHAR(255),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.DRAFT: 'draft'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    published_at TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: seo_setting_translations (模型: SEOSettingTranslation)
CREATE TABLE seo_setting_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    seo_setting_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    keywords VARCHAR(255),
    og_title VARCHAR(255),
    og_description VARCHAR(500),
    twitter_title VARCHAR(255),
    twitter_description VARCHAR(500),
    schema_markup TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: seo_settings (模型: SEOSetting)
CREATE TABLE seo_settings (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    entity_type VARCHAR(13) NOT NULL,
    entity_id UUID,
    page_path VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    keywords VARCHAR(255),
    canonical_url VARCHAR(255),
    robots VARCHAR(50) DEFAULT ScalarElementColumnDefault('index,follow'),
    og_title VARCHAR(255),
    og_description VARCHAR(500),
    og_image VARCHAR(255),
    twitter_card VARCHAR(20) DEFAULT ScalarElementColumnDefault('summary'),
    twitter_title VARCHAR(255),
    twitter_description VARCHAR(500),
    twitter_image VARCHAR(255),
    schema_markup TEXT,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: symbol_dictionaries (模型: SymbolDictionary)
CREATE TABLE symbol_dictionaries (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    symbol_type VARCHAR(12) NOT NULL,
    origin VARCHAR(100),
    cultural_significance TEXT,
    spiritual_meaning TEXT,
    image_url VARCHAR(255),
    additional_images ARRAY,
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ContentStatus.PUBLISHED: 'published'>),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    related_product_symbol_id UUID,
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: symbol_dictionary_translations (模型: SymbolDictionaryTranslation)
CREATE TABLE symbol_dictionary_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    symbol_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    origin VARCHAR(100),
    cultural_significance TEXT,
    spiritual_meaning TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- ========== 模块: customer ==========

-- 表: customer_addresses (模型: CustomerAddress)
ALTER TABLE customer_addresses ALTER COLUMN latitude TYPE REAL;
ALTER TABLE customer_addresses ALTER COLUMN longitude TYPE REAL;

-- 表: customer_cultural_preference_details (模型: CustomerCulturalPreference)
ALTER TABLE customer_cultural_preference_details ALTER COLUMN confidence_score TYPE REAL;

-- 表: customer_intent_details (模型: CustomerIntent)
ALTER TABLE customer_intent_details ALTER COLUMN confidence_score TYPE REAL;

-- 表: customer_points (模型: CustomerPoints)
ALTER TABLE customer_points ALTER COLUMN transaction_type TYPE VARCHAR(14);

-- 表: customer_scene_preference_details (模型: CustomerScenePreference)
ALTER TABLE customer_scene_preference_details ALTER COLUMN confidence_score TYPE REAL;

-- 表: customers (模型: Customer)
ALTER TABLE customers ADD COLUMN role VARCHAR(7);
UPDATE customers SET role = ScalarElementColumnDefault(<CustomerRole.REGULAR: 'regular'>) WHERE role IS NULL;
ALTER TABLE customers ALTER COLUMN role SET NOT NULL;
ALTER TABLE customers ADD COLUMN country_id INTEGER;

-- ========== 模块: duty ==========

-- 表: duty_rules (模型: DutyRule)
CREATE TABLE duty_rules (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    zone_id UUID NOT NULL,
    category_id UUID,
    tax_free_amount REAL DEFAULT ScalarElementColumnDefault(0.0),
    tax_rate REAL NOT NULL,
    min_tax_amount REAL DEFAULT ScalarElementColumnDefault(0.0),
    max_tax_amount REAL,
    priority INTEGER DEFAULT ScalarElementColumnDefault(1),
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('active'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: duty_zone_countries (模型: DutyZoneCountry)
CREATE TABLE duty_zone_countries (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    zone_id UUID NOT NULL,
    country_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: duty_zone_translations (模型: DutyZoneTranslation)
CREATE TABLE duty_zone_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    zone_id UUID NOT NULL,
    language VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: duty_zones (模型: DutyZone)
CREATE TABLE duty_zones (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    tax_free_threshold REAL DEFAULT ScalarElementColumnDefault(0.0),
    default_tax_rate REAL DEFAULT ScalarElementColumnDefault(0.0),
    currency VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('active'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: order_duty_charges (模型: OrderDutyCharge)
CREATE TABLE order_duty_charges (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    country_id UUID NOT NULL,
    duty_zone_id UUID NOT NULL,
    taxable_amount REAL NOT NULL,
    tax_rate REAL NOT NULL,
    duty_amount REAL NOT NULL,
    currency VARCHAR(3) NOT NULL,
    calculation_details TEXT,
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('pending'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: product_duty_categories (模型: ProductDutyCategory)
CREATE TABLE product_duty_categories (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    tax_rate REAL,
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('active'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: product_duty_category_translations (模型: ProductDutyCategoryTranslation)
CREATE TABLE product_duty_category_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    category_id UUID NOT NULL,
    language VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- ========== 模块: fortune ==========

-- 表: fortune_profiles (模型: FortuneProfile)
CREATE TABLE fortune_profiles (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    birth_year INTEGER NOT NULL,
    birth_month INTEGER NOT NULL,
    birth_day INTEGER NOT NULL,
    birth_hour INTEGER,
    gender VARCHAR(10) NOT NULL,
    birth_location VARCHAR(100),
    bazi_analysis JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: fortune_readings (模型: FortuneReading)
CREATE TABLE fortune_readings (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    profile_id UUID,
    reading_type VARCHAR(5) NOT NULL,
    input_data JSONB NOT NULL,
    ai_analysis TEXT NOT NULL,
    recommended_products JSONB,
    reading_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- ========== 模块: localization ==========

-- 表: country_regions (模型: CountryRegion)
CREATE TABLE country_regions (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    code VARCHAR(3) NOT NULL,
    name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100),
    flag_image VARCHAR(255),
    phone_code VARCHAR(10),
    tax_rate REAL,
    timezone VARCHAR(50),
    continent VARCHAR(20),
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_localization_translations (模型: CulturalLocalizationTranslation)
CREATE TABLE cultural_localization_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    cultural_localization_id UUID NOT NULL,
    language_id UUID NOT NULL,
    element_name VARCHAR(100) NOT NULL,
    local_meaning TEXT NOT NULL,
    usage_context TEXT,
    local_taboos TEXT,
    recommendations TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_localizations (模型: CulturalLocalization)
CREATE TABLE cultural_localizations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    country_region_id UUID NOT NULL,
    symbol_id UUID,
    element_name VARCHAR(100) NOT NULL,
    local_meaning TEXT NOT NULL,
    usage_context TEXT,
    local_taboos TEXT,
    recommendations TEXT,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: currencies (模型: Currency)
ALTER TABLE currencies ADD COLUMN exchange_rate REAL DEFAULT ScalarElementColumnDefault(1.0);
ALTER TABLE currencies ADD COLUMN sort_order INTEGER DEFAULT ScalarElementColumnDefault(0);
ALTER TABLE currencies ALTER COLUMN name TYPE VARCHAR(50);
ALTER TABLE currencies ALTER COLUMN symbol SET NOT NULL;
-- ALTER TABLE currencies DROP COLUMN format_pattern; -- 请手动确认是否删除
-- ALTER TABLE currencies DROP COLUMN is_base_currency; -- 请手动确认是否删除
-- ALTER TABLE currencies DROP COLUMN countries; -- 请手动确认是否删除

-- 表: languages (模型: Language)
CREATE TABLE languages (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    code VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    native_name VARCHAR(50),
    flag_image VARCHAR(255),
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    is_default BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: locale_preferences (模型: LocalePreference)
CREATE TABLE locale_preferences (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    user_id UUID,
    language_id UUID NOT NULL,
    currency_id UUID NOT NULL,
    country_region_id UUID NOT NULL,
    date_format VARCHAR(20) DEFAULT ScalarElementColumnDefault('YYYY-MM-DD'),
    time_format VARCHAR(20) DEFAULT ScalarElementColumnDefault('HH:mm:ss'),
    number_format VARCHAR(20) DEFAULT ScalarElementColumnDefault('#,##0.00'),
    first_day_of_week INTEGER DEFAULT ScalarElementColumnDefault(1),
    measurement_unit VARCHAR(10) DEFAULT ScalarElementColumnDefault('metric'),
    timezone VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: translation_keys (模型: TranslationKey)
CREATE TABLE translation_keys (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    key VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    module VARCHAR(50),
    is_system BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: translation_values (模型: TranslationValue)
CREATE TABLE translation_values (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    translation_key_id UUID NOT NULL,
    language_id UUID NOT NULL,
    value TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- ========== 模块: marketing ==========

-- 表: abandoned_cart_reminders (模型: AbandonedCartReminder)
CREATE TABLE abandoned_cart_reminders (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    cart_id UUID NOT NULL,
    reminder_type VARCHAR(20) DEFAULT ScalarElementColumnDefault('email'),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<ReminderStatus.SCHEDULED: 'scheduled'>),
    scheduled_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,
    template_id VARCHAR(100),
    subject VARCHAR(255),
    content TEXT,
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: abandoned_carts (模型: AbandonedCart)
CREATE TABLE abandoned_carts (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    session_id VARCHAR(255),
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<CartStatus.ACTIVE: 'active'>),
    abandoned_at TIMESTAMP,
    recovered_at TIMESTAMP,
    items_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    total_value REAL DEFAULT ScalarElementColumnDefault(0),
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    cart_items JSONB,
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    coupon_issued BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    coupon_id UUID,
    discount_amount REAL,
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    recovery_url VARCHAR(255),
    recovery_token VARCHAR(100),
    recovery_expires_at TIMESTAMP,
    device_type VARCHAR(50),
    ip_address VARCHAR(50),
    user_agent TEXT,
    meta_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: activity_participations (模型: ActivityParticipation)
CREATE TABLE activity_participations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    activity_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    participation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    result VARCHAR(50),
    reward_type VARCHAR(50),
    reward_id UUID,
    reward_details JSONB,
    is_claimed BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    claimed_at TIMESTAMP,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: affiliate_applications (模型: AffiliateApplication)
CREATE TABLE affiliate_applications (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    program_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    website VARCHAR(255),
    company VARCHAR(100),
    promotion_methods ARRAY,
    expected_sales INTEGER,
    answers JSONB,
    additional_info TEXT,
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('pending'),
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by UUID,
    feedback TEXT,
    rejection_reason TEXT,
    approved_commission_rate REAL,
    affiliate_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: affiliate_clicks (模型: AffiliateClick)
CREATE TABLE affiliate_clicks (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    affiliate_id UUID NOT NULL,
    ip_address VARCHAR(50),
    user_agent TEXT,
    referrer VARCHAR(255),
    landing_page VARCHAR(255),
    click_id VARCHAR(100) NOT NULL,
    conversion_id UUID,
    session_id VARCHAR(100),
    device_type VARCHAR(20),
    browser VARCHAR(50),
    operating_system VARCHAR(50),
    country_code VARCHAR(2),
    clicked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: affiliate_commissions (模型: AffiliateCommission)
CREATE TABLE affiliate_commissions (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    affiliate_id UUID NOT NULL,
    conversion_id UUID,
    payment_id UUID,
    amount REAL NOT NULL,
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    commission_type VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<CommissionType.PERCENTAGE: 'percentage'>),
    commission_rate REAL,
    order_id UUID,
    order_amount REAL,
    order_date TIMESTAMP,
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<CommissionStatus.PENDING: 'pending'>),
    approval_date TIMESTAMP,
    rejection_date TIMESTAMP,
    rejection_reason TEXT,
    payment_date TIMESTAMP,
    payment_method VARCHAR(13),
    payment_reference VARCHAR(100),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    is_locked BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    lock_reason VARCHAR(255),
    locked_at TIMESTAMP,
    locked_by UUID,
    approved_by UUID,
    rejected_by UUID,
    notes TEXT,
    admin_notes TEXT,
    meta_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: affiliate_conversions (模型: AffiliateConversion)
CREATE TABLE affiliate_conversions (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    affiliate_id UUID NOT NULL,
    order_id UUID NOT NULL,
    amount REAL NOT NULL,
    commission_amount REAL NOT NULL,
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('pending'),
    approved_at TIMESTAMP,
    rejected_at TIMESTAMP,
    rejection_reason TEXT,
    click_id VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: affiliate_payments (模型: AffiliatePayment)
CREATE TABLE affiliate_payments (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    affiliate_id UUID NOT NULL,
    amount REAL NOT NULL,
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    payment_method VARCHAR(13) NOT NULL,
    reference_number VARCHAR(100),
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('pending'),
    payment_date TIMESTAMP,
    transaction_id VARCHAR(100),
    payment_details JSONB,
    fee_amount REAL DEFAULT ScalarElementColumnDefault(0),
    period_start TIMESTAMP,
    period_end TIMESTAMP,
    commissions_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    notes TEXT,
    receipt_url VARCHAR(255),
    processed_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: affiliate_programs (模型: AffiliateProgram)
CREATE TABLE affiliate_programs (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(8) NOT NULL DEFAULT ScalarElementColumnDefault(<ProgramStatus.ACTIVE: 'active'>),
    is_public BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    requires_approval BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    auto_approval BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    commission_structure VARCHAR(17) NOT NULL DEFAULT ScalarElementColumnDefault(<CommissionStructure.FLAT: 'flat'>),
    default_commission_rate REAL DEFAULT ScalarElementColumnDefault(10.0),
    min_commission_rate REAL DEFAULT ScalarElementColumnDefault(5.0),
    max_commission_rate REAL DEFAULT ScalarElementColumnDefault(30.0),
    tiered_commissions JSONB,
    category_commissions JSONB,
    product_commissions JSONB,
    cookie_days INTEGER DEFAULT ScalarElementColumnDefault(30),
    excluded_products ARRAY,
    excluded_categories ARRAY,
    min_payout REAL DEFAULT ScalarElementColumnDefault(50.0),
    payout_schedule VARCHAR(50) DEFAULT ScalarElementColumnDefault('monthly'),
    terms_conditions TEXT,
    banner_url VARCHAR(255),
    logo_url VARCHAR(255),
    marketing_materials JSONB,
    tracking_domain VARCHAR(255),
    tracking_parameters JSONB,
    application_form JSONB,
    application_questions JSONB,
    max_affiliates INTEGER,
    country_restrictions ARRAY,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    contact_email VARCHAR(255),
    support_email VARCHAR(255),
    support_phone VARCHAR(50),
    total_affiliates INTEGER DEFAULT ScalarElementColumnDefault(0),
    active_affiliates INTEGER DEFAULT ScalarElementColumnDefault(0),
    total_sales REAL DEFAULT ScalarElementColumnDefault(0),
    total_commissions REAL DEFAULT ScalarElementColumnDefault(0),
    conversion_rate REAL DEFAULT ScalarElementColumnDefault(0),
    meta_data JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: affiliates (模型: Affiliate)
CREATE TABLE affiliates (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    program_id UUID NOT NULL,
    customer_id UUID,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    company_name VARCHAR(100),
    website VARCHAR(255),
    status VARCHAR(10) NOT NULL DEFAULT ScalarElementColumnDefault(<AffiliateStatus.PENDING: 'pending'>),
    level VARCHAR(8) NOT NULL DEFAULT ScalarElementColumnDefault(<AffiliateLevel.BASIC: 'basic'>),
    commission_rate REAL NOT NULL,
    override_program_rate BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    cookie_days INTEGER DEFAULT ScalarElementColumnDefault(30),
    payment_method VARCHAR(50),
    payment_details JSONB,
    payment_threshold REAL DEFAULT ScalarElementColumnDefault(100),
    tax_id VARCHAR(50),
    clicks_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    conversions_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    total_earnings REAL DEFAULT ScalarElementColumnDefault(0),
    unpaid_earnings REAL DEFAULT ScalarElementColumnDefault(0),
    last_click_at TIMESTAMP,
    last_conversion_at TIMESTAMP,
    custom_domain VARCHAR(255),
    landing_page VARCHAR(255),
    tracking_code TEXT,
    utm_parameters JSONB,
    approval_date TIMESTAMP,
    rejection_reason TEXT,
    notes TEXT,
    meta_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: campaign_events (模型: CampaignEvent)
CREATE TABLE campaign_events (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    details JSONB,
    customer_id UUID,
    PRIMARY KEY (id)
);

-- 表: collection_products (模型: CollectionProduct)
CREATE TABLE collection_products (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    collection_id UUID NOT NULL,
    product_id UUID NOT NULL,
    display_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    custom_title VARCHAR(255),
    custom_description TEXT,
    custom_image_url VARCHAR(255),
    seasonal_relevance VARCHAR(255),
    cultural_significance TEXT,
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    click_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    purchase_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    original_price REAL,
    seasonal_price REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: content_engagements (模型: ContentEngagement)
CREATE TABLE content_engagements (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    content_item_id UUID NOT NULL,
    customer_id UUID,
    engagement_type VARCHAR(20) NOT NULL,
    engagement_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comment_text TEXT,
    rating INTEGER,
    device_type VARCHAR(50),
    ip_address VARCHAR(50),
    user_agent TEXT,
    referrer VARCHAR(255),
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: coupons (模型: Coupon)
ALTER TABLE coupons ALTER COLUMN referrer_reward TYPE REAL;
ALTER TABLE coupons ALTER COLUMN conversion_rate TYPE REAL;

-- 表: cultural_content_campaigns (模型: CulturalContentCampaign)
CREATE TABLE cultural_content_campaigns (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    cultural_theme VARCHAR(100) NOT NULL,
    cultural_region VARCHAR(100),
    cultural_symbols ARRAY,
    main_story TEXT,
    storytelling_angle VARCHAR(255),
    content_keywords ARRAY,
    target_audience JSONB,
    target_channels ARRAY,
    media_files JSONB,
    cover_image_url VARCHAR(255),
    featured_video_url VARCHAR(255),
    related_products ARRAY,
    related_symbols ARRAY,
    related_materials ARRAY,
    seo_title VARCHAR(100),
    seo_description VARCHAR(255),
    seo_keywords ARRAY,
    publication_status VARCHAR(20) DEFAULT ScalarElementColumnDefault('draft'),
    publish_date TIMESTAMP,
    expiry_date TIMESTAMP,
    social_media_caption TEXT,
    social_media_hashtags ARRAY,
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    engagement_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    share_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    conversion_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    tags ARRAY,
    meta_data JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: cultural_content_items (模型: CulturalContentItem)
CREATE TABLE cultural_content_items (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    content_type VARCHAR(11) NOT NULL,
    content TEXT,
    featured_image_url VARCHAR(255),
    media_gallery JSONB,
    status VARCHAR(20) DEFAULT ScalarElementColumnDefault('draft'),
    publish_date TIMESTAMP,
    author VARCHAR(100),
    reading_time INTEGER,
    website_url VARCHAR(255),
    blog_url VARCHAR(255),
    social_media_urls JSONB,
    views INTEGER DEFAULT ScalarElementColumnDefault(0),
    likes INTEGER DEFAULT ScalarElementColumnDefault(0),
    comments INTEGER DEFAULT ScalarElementColumnDefault(0),
    shares INTEGER DEFAULT ScalarElementColumnDefault(0),
    call_to_action JSONB,
    related_product_ids ARRAY,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: customer_coupons (模型: CustomerCoupon)
ALTER TABLE customer_coupons ALTER COLUMN discount_amount TYPE REAL;

-- 表: discounts (模型: Discount)
CREATE TABLE discounts (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    promotion_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    rule_type VARCHAR(19) NOT NULL,
    min_cart_total REAL,
    max_cart_total REAL,
    min_quantity INTEGER,
    max_quantity INTEGER,
    required_products ARRAY,
    any_required_products ARRAY,
    required_categories ARRAY,
    discount_type VARCHAR(20) NOT NULL,
    discount_value REAL NOT NULL,
    max_discount_amount REAL,
    applies_to VARCHAR(20) DEFAULT ScalarElementColumnDefault('cart'),
    target_products ARRAY,
    target_categories ARRAY,
    repeat_times INTEGER DEFAULT ScalarElementColumnDefault(1),
    tier_rules JSONB,
    usage_limit INTEGER,
    usage_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    user_limit INTEGER,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    is_permanent BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    sort_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    label VARCHAR(50),
    label_color VARCHAR(7),
    is_test BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    test_group VARCHAR(50),
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    use_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    revenue_impact REAL DEFAULT ScalarElementColumnDefault(0),
    meta_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: intent_based_campaigns (模型: IntentBasedCampaign)
CREATE TABLE intent_based_campaigns (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    primary_intent VARCHAR(50) NOT NULL,
    secondary_intents ARRAY,
    intent_description TEXT,
    target_segments ARRAY,
    target_preferences JSONB,
    content_story TEXT,
    content_images ARRAY,
    video_url VARCHAR(255),
    product_ids ARRAY,
    bundle_ids ARRAY,
    featured_product_id UUID,
    promotion_id UUID,
    coupon_id UUID,
    email_template_id VARCHAR(100),
    landing_page_url VARCHAR(255),
    social_media_assets JSONB,
    push_title VARCHAR(100),
    push_body TEXT,
    push_image_url VARCHAR(255),
    cta_text VARCHAR(100),
    cta_url VARCHAR(255),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    click_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    conversion_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    revenue REAL DEFAULT ScalarElementColumnDefault(0),
    tags ARRAY,
    meta_data JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: intent_engagement_records (模型: IntentEngagementRecord)
CREATE TABLE intent_engagement_records (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL,
    customer_id UUID,
    session_id VARCHAR(100),
    engagement_type VARCHAR(50) NOT NULL,
    engagement_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content_id VARCHAR(100),
    content_type VARCHAR(50),
    product_id UUID,
    device_type VARCHAR(50),
    ip_address VARCHAR(50),
    user_agent TEXT,
    order_id UUID,
    order_value REAL,
    meta_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: marketing_campaigns (模型: Campaign)
CREATE TABLE marketing_campaigns (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(11) NOT NULL,
    status VARCHAR(9) NOT NULL DEFAULT ScalarElementColumnDefault(<CampaignStatus.DRAFT: 'draft'>),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    execution_time TIMESTAMP,
    target_audience VARCHAR(50) DEFAULT ScalarElementColumnDefault('all'),
    customer_segments ARRAY,
    target_customers ARRAY,
    exclusion_list ARRAY,
    audience_size INTEGER,
    budget REAL,
    actual_cost REAL DEFAULT ScalarElementColumnDefault(0),
    cost_per_acquisition REAL,
    currency_code VARCHAR(3) DEFAULT ScalarElementColumnDefault('USD'),
    content_template_id UUID,
    subject_line VARCHAR(200),
    sender_name VARCHAR(100),
    sender_email VARCHAR(100),
    reply_to VARCHAR(100),
    promotion_ids ARRAY,
    primary_channel VARCHAR(50) NOT NULL,
    secondary_channels ARRAY,
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    sent_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    delivered_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    open_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    click_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    conversion_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    bounce_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    unsubscribe_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    execution_status VARCHAR(50),
    revenue_generated REAL DEFAULT ScalarElementColumnDefault(0),
    roi REAL,
    conversion_rate REAL,
    open_rate REAL,
    click_rate REAL,
    is_ab_test BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    test_variants JSONB,
    winning_variant VARCHAR(50),
    parent_campaign_id UUID,
    tags ARRAY,
    cultural_theme VARCHAR(100),
    intention_focus VARCHAR(100),
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: personalized_recommendations (模型: PersonalizedRecommendation)
CREATE TABLE personalized_recommendations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    customer_id UUID,
    session_id VARCHAR(100),
    recommendation_type VARCHAR(9) NOT NULL,
    item_id UUID NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    algorithm VARCHAR(23) NOT NULL DEFAULT ScalarElementColumnDefault(<RecommendationAlgorithm.HYBRID: 'hybrid'>),
    context VARCHAR(50),
    position VARCHAR(50),
    section VARCHAR(50),
    related_intention VARCHAR(100),
    related_cultural_element VARCHAR(100),
    matching_score REAL DEFAULT ScalarElementColumnDefault(0),
    reason_code VARCHAR(50),
    reason_text VARCHAR(255),
    source_behavior VARCHAR(50),
    source_item_id UUID,
    source_item_type VARCHAR(50),
    was_shown BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    was_clicked BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    was_converted BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    shown_at TIMESTAMP,
    clicked_at TIMESTAMP,
    converted_at TIMESTAMP,
    meta_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: promotions (模型: Promotion)
ALTER TABLE promotions ALTER COLUMN discount_value TYPE REAL;
ALTER TABLE promotions ALTER COLUMN min_order_amount TYPE REAL;
ALTER TABLE promotions ALTER COLUMN max_discount_amount TYPE REAL;

-- 表: recommendation_models (模型: RecommendationModel)
CREATE TABLE recommendation_models (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    algorithm VARCHAR(23) NOT NULL,
    version VARCHAR(20) NOT NULL,
    parameters JSONB,
    training_date TIMESTAMP,
    training_duration INTEGER,
    training_data_size INTEGER,
    accuracy REAL,
    precision REAL,
    recall REAL,
    f1_score REAL,
    mean_average_precision REAL,
    model_path VARCHAR(255),
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    is_in_production BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    is_in_test BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    test_group VARCHAR(50),
    meta_data JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: recommendation_rules (模型: RecommendationRule)
CREATE TABLE recommendation_rules (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    rule_type VARCHAR(50) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    source_id UUID,
    target_type VARCHAR(50) NOT NULL,
    target_ids ARRAY,
    strength REAL DEFAULT ScalarElementColumnDefault(1.0),
    priority INTEGER DEFAULT ScalarElementColumnDefault(0),
    is_bidirectional BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    conditions JSONB,
    reason_text VARCHAR(255),
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    meta_data JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: seasonal_collections (模型: SeasonalCollection)
CREATE TABLE seasonal_collections (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    season_type VARCHAR(9) NOT NULL,
    custom_season_name VARCHAR(100),
    cultural_context TEXT,
    target_regions ARRAY,
    target_audience JSONB,
    products ARRAY,
    categories ARRAY,
    theme_color VARCHAR(7),
    accent_color VARCHAR(7),
    design_elements JSONB,
    banner_url VARCHAR(255),
    cover_image_url VARCHAR(255),
    lookbook_images ARRAY,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    is_recurring BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    recurring_pattern VARCHAR(50),
    has_promotion BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    promotion_id UUID,
    discount_percentage REAL,
    display_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    is_featured BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    homepage_visible BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    slogan VARCHAR(255),
    story_content TEXT,
    seo_title VARCHAR(100),
    seo_description VARCHAR(255),
    seo_keywords ARRAY,
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    sale_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    revenue REAL DEFAULT ScalarElementColumnDefault(0),
    tags ARRAY,
    meta_data JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: seasonal_landing_pages (模型: SeasonalLandingPage)
CREATE TABLE seasonal_landing_pages (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    collection_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    slug VARCHAR(100) NOT NULL,
    hero_banner_url VARCHAR(255),
    video_url VARCHAR(255),
    sections JSONB,
    primary_cta_text VARCHAR(100),
    primary_cta_url VARCHAR(255),
    meta_title VARCHAR(100),
    meta_description VARCHAR(255),
    is_published BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    published_at TIMESTAMP,
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    bounce_rate REAL,
    average_time_on_page INTEGER,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: thematic_campaigns (模型: ThematicCampaign)
CREATE TABLE thematic_campaigns (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    theme_type VARCHAR(9) NOT NULL,
    theme_name VARCHAR(100) NOT NULL,
    theme_description TEXT,
    cultural_background TEXT,
    target_regions ARRAY,
    featured_products ARRAY,
    featured_categories ARRAY,
    featured_bundles ARRAY,
    featured_symbols ARRAY,
    featured_materials ARRAY,
    promotion_ids ARRAY,
    discount_code VARCHAR(50),
    banner_url VARCHAR(255),
    landing_page_url VARCHAR(255),
    main_image_url VARCHAR(255),
    video_url VARCHAR(255),
    theme_color VARCHAR(7),
    theme_font VARCHAR(100),
    theme_elements JSONB,
    slogan VARCHAR(255),
    story_content TEXT,
    content_sections JSONB,
    featured_blog_posts ARRAY,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    is_recurring BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    recurring_pattern VARCHAR(50),
    channels ARRAY,
    social_media_assets JSONB,
    email_template_id VARCHAR(100),
    seo_title VARCHAR(100),
    seo_description VARCHAR(255),
    seo_keywords ARRAY,
    view_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    participation_count INTEGER DEFAULT ScalarElementColumnDefault(0),
    revenue REAL DEFAULT ScalarElementColumnDefault(0),
    tags ARRAY,
    meta_data JSONB,
    created_by UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: theme_activities (模型: ThemeActivity)
CREATE TABLE theme_activities (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    activity_type VARCHAR(50) NOT NULL,
    rules TEXT,
    rewards JSONB,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    participation_limit INTEGER,
    total_participants INTEGER DEFAULT ScalarElementColumnDefault(0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: theme_sections (模型: ThemeSection)
CREATE TABLE theme_sections (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    section_type VARCHAR(50) NOT NULL,
    display_order INTEGER DEFAULT ScalarElementColumnDefault(0),
    is_visible BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    title VARCHAR(255),
    subtitle VARCHAR(255),
    content TEXT,
    background_url VARCHAR(255),
    image_url VARCHAR(255),
    button_text VARCHAR(100),
    button_url VARCHAR(255),
    product_ids ARRAY,
    category_ids ARRAY,
    style_settings JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- ========== 模块: order ==========

-- 表: carriers (模型: Carrier)
CREATE TABLE carriers (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL,
    contact_phone VARCHAR(30),
    contact_email VARCHAR(100),
    website VARCHAR(255),
    tracking_url_template VARCHAR(500),
    supported_countries JSONB,
    service_types JSONB,
    api_endpoint VARCHAR(255),
    api_key VARCHAR(255),
    api_config JSONB,
    is_active BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    priority INTEGER DEFAULT ScalarElementColumnDefault(0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: order_items (模型: OrderItem)
ALTER TABLE order_items ALTER COLUMN weight TYPE REAL;
ALTER TABLE order_items ALTER COLUMN width TYPE REAL;
ALTER TABLE order_items ALTER COLUMN height TYPE REAL;
ALTER TABLE order_items ALTER COLUMN length TYPE REAL;
ALTER TABLE order_items ALTER COLUMN discount_percentage TYPE REAL;

-- 表: order_notes (模型: OrderNote)
CREATE TABLE order_notes (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    note TEXT NOT NULL,
    is_customer_notified BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    is_visible_to_customer BOOLEAN DEFAULT ScalarElementColumnDefault(False),
    author_id UUID,
    author_name VARCHAR(100),
    author_type VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: order_payments (模型: OrderPayment)
CREATE TABLE order_payments (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    payment_method_id UUID,
    payment_type VARCHAR(13) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    currency_code VARCHAR(3) NOT NULL,
    result VARCHAR(18) NOT NULL,
    transaction_id VARCHAR(100),
    transaction_reference VARCHAR(100),
    payment_method_name VARCHAR(100),
    payment_details JSONB,
    authorization_code VARCHAR(100),
    authorization_transaction_id VARCHAR(100),
    is_refunded INTEGER DEFAULT ScalarElementColumnDefault(0),
    refunded_amount NUMERIC(10, 2) DEFAULT ScalarElementColumnDefault(0),
    refund_transaction_id VARCHAR(100),
    notes TEXT,
    ip_address VARCHAR(50),
    error_code VARCHAR(50),
    error_message TEXT,
    response_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    refunded_at TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: order_shipments (模型: OrderShipment)
CREATE TABLE order_shipments (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    shipment_code VARCHAR(50) NOT NULL,
    order_id UUID NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT ScalarElementColumnDefault(<ShipmentStatus.PENDING: 'PENDING'>),
    carrier_name VARCHAR(100) NOT NULL,
    tracking_number VARCHAR(100),
    shipping_method VARCHAR(50) NOT NULL,
    recipient_name VARCHAR(100) NOT NULL,
    recipient_phone VARCHAR(30) NOT NULL,
    recipient_email VARCHAR(100),
    shipping_address1 VARCHAR(255) NOT NULL,
    shipping_city VARCHAR(100) NOT NULL,
    shipping_country VARCHAR(100) NOT NULL,
    shipping_postcode VARCHAR(20) NOT NULL,
    weight REAL NOT NULL,
    shipping_cost NUMERIC(10, 2) NOT NULL DEFAULT ScalarElementColumnDefault(0),
    estimated_delivery_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: order_status_history (模型: OrderStatusHistory)
CREATE TABLE order_status_history (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    previous_status VARCHAR(18),
    new_status VARCHAR(18) NOT NULL,
    previous_payment_status VARCHAR(18),
    new_payment_status VARCHAR(18),
    previous_shipping_status VARCHAR(17),
    new_shipping_status VARCHAR(17),
    comment TEXT,
    operator_id UUID,
    operator_name VARCHAR(100),
    is_customer_notified INTEGER DEFAULT ScalarElementColumnDefault(0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: orders (模型: Order)
ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50);
UPDATE orders SET payment_method = ScalarElementColumnDefault('CREDIT_CARD') WHERE payment_method IS NULL;
ALTER TABLE orders ALTER COLUMN payment_method SET NOT NULL;
ALTER TABLE orders ADD COLUMN points_used INTEGER;
UPDATE orders SET points_used = ScalarElementColumnDefault(0) WHERE points_used IS NULL;
ALTER TABLE orders ALTER COLUMN points_used SET NOT NULL;

-- 表: shipment_items (模型: ShipmentItem)
CREATE TABLE shipment_items (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    shipment_id UUID NOT NULL,
    order_item_id UUID NOT NULL,
    product_id UUID NOT NULL,
    sku_id UUID,
    product_name VARCHAR(255) NOT NULL,
    sku_code VARCHAR(50),
    quantity_shipped INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    attributes JSONB,
    image_url VARCHAR(255),
    weight_per_unit REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: shipment_tracking (模型: ShipmentTracking)
CREATE TABLE shipment_tracking (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    shipment_id UUID NOT NULL,
    tracking_status VARCHAR(19) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    operator_name VARCHAR(100),
    timestamp TIMESTAMP NOT NULL,
    is_auto_generated BOOLEAN DEFAULT ScalarElementColumnDefault(True),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- ========== 模块: payment ==========

-- 表: cash_on_delivery_settings (模型: CashOnDelivery)
ALTER TABLE cash_on_delivery_settings ALTER COLUMN min_order_amount TYPE REAL;
ALTER TABLE cash_on_delivery_settings ALTER COLUMN max_order_amount TYPE REAL;
ALTER TABLE cash_on_delivery_settings ALTER COLUMN fee_amount TYPE REAL;
ALTER TABLE cash_on_delivery_settings ALTER COLUMN fee_percentage TYPE REAL;
ALTER TABLE cash_on_delivery_settings ALTER COLUMN min_fee TYPE REAL;
ALTER TABLE cash_on_delivery_settings ALTER COLUMN max_fee TYPE REAL;
ALTER TABLE cash_on_delivery_settings ALTER COLUMN max_product_weight TYPE REAL;

-- 表: installment_plans (模型: InstallmentPlan)
ALTER TABLE installment_plans ALTER COLUMN min_down_payment_percentage TYPE REAL;
ALTER TABLE installment_plans ALTER COLUMN interest_rate TYPE REAL;
ALTER TABLE installment_plans ALTER COLUMN fee_fixed TYPE REAL;
ALTER TABLE installment_plans ALTER COLUMN fee_percentage TYPE REAL;
ALTER TABLE installment_plans ALTER COLUMN min_order_amount TYPE REAL;
ALTER TABLE installment_plans ALTER COLUMN max_order_amount TYPE REAL;

-- 表: payment_methods (模型: PaymentMethod)
ALTER TABLE payment_methods ALTER COLUMN fee_fixed TYPE REAL;
ALTER TABLE payment_methods ALTER COLUMN fee_percentage TYPE REAL;
ALTER TABLE payment_methods ALTER COLUMN min_fee TYPE REAL;
ALTER TABLE payment_methods ALTER COLUMN max_fee TYPE REAL;
ALTER TABLE payment_methods ALTER COLUMN min_amount TYPE REAL;
ALTER TABLE payment_methods ALTER COLUMN max_amount TYPE REAL;

-- 表: payment_transactions (模型: PaymentTransaction)
ALTER TABLE payment_transactions ALTER COLUMN amount TYPE REAL;
ALTER TABLE payment_transactions ALTER COLUMN fee_amount TYPE REAL;
ALTER TABLE payment_transactions ALTER COLUMN refunded_amount TYPE REAL;

-- ========== 模块: product ==========

-- 表: bundle_items (模型: BundleItem)
ALTER TABLE bundle_items ALTER COLUMN discount_value TYPE REAL;

-- 表: product_bundles (模型: ProductBundle)
ALTER TABLE product_bundles ALTER COLUMN discount_value TYPE REAL;

-- 表: product_images (模型: ProductImage)
ALTER TABLE product_images ALTER COLUMN is_video DROP NOT NULL;

-- 表: product_prices (模型: ProductPrice)
ALTER TABLE product_prices ALTER COLUMN regular_price TYPE REAL;
ALTER TABLE product_prices ALTER COLUMN sale_price TYPE REAL;
ALTER TABLE product_prices ALTER COLUMN discount_percentage TYPE REAL;
ALTER TABLE product_prices ALTER COLUMN special_price TYPE REAL;

-- 表: product_sku_translations (模型: ProductSkuTranslation)
CREATE TABLE product_sku_translations (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    sku_id UUID NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    sku_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 表: product_skus (模型: ProductSku)
ALTER TABLE product_skus ADD COLUMN sku_name VARCHAR(255);
ALTER TABLE product_skus ADD COLUMN stock_quantity INTEGER;
UPDATE product_skus SET stock_quantity = ScalarElementColumnDefault(0) WHERE stock_quantity IS NULL;
ALTER TABLE product_skus ALTER COLUMN stock_quantity SET NOT NULL;
ALTER TABLE product_skus ADD COLUMN low_stock_threshold INTEGER;
UPDATE product_skus SET low_stock_threshold = ScalarElementColumnDefault(10) WHERE low_stock_threshold IS NULL;
ALTER TABLE product_skus ALTER COLUMN low_stock_threshold SET NOT NULL;
ALTER TABLE product_skus ALTER COLUMN price_adjustment TYPE REAL;
ALTER TABLE product_skus ALTER COLUMN weight_adjustment TYPE REAL;
ALTER TABLE product_skus ALTER COLUMN width_adjustment TYPE REAL;
ALTER TABLE product_skus ALTER COLUMN height_adjustment TYPE REAL;
ALTER TABLE product_skus ALTER COLUMN length_adjustment TYPE REAL;

-- 表: product_translations (模型: ProductTranslation)
ALTER TABLE product_translations ADD COLUMN sku_name VARCHAR(255);

-- 表: products (模型: Product)
ALTER TABLE products ADD COLUMN sku_name VARCHAR(255);
ALTER TABLE products ALTER COLUMN weight TYPE REAL;
ALTER TABLE products ALTER COLUMN width TYPE REAL;
ALTER TABLE products ALTER COLUMN height TYPE REAL;
ALTER TABLE products ALTER COLUMN length TYPE REAL;

-- 表: stock_logs (模型: StockLog)
CREATE TABLE stock_logs (
    id INTEGER NOT NULL,
    sku_id UUID NOT NULL,
    change_type VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    balance INTEGER NOT NULL,
    order_id UUID,
    remark VARCHAR(200),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    PRIMARY KEY (id)
);
