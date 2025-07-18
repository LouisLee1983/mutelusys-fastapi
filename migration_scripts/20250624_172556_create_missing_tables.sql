-- Migration Script: Create Missing Tables
-- Generated at: 2025-06-24 17:25:56
-- Missing tables: 185

BEGIN;

-- Table: abandoned_cart_reminders
-- Class: ReminderStatus
-- File: app/marketing/abandoned_cart/models.py

CREATE TABLE IF NOT EXISTS abandoned_cart_reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_abandoned_cart_reminders_updated_at BEFORE UPDATE
ON abandoned_cart_reminders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: abandoned_carts
-- Class: CartStatus
-- File: app/marketing/abandoned_cart/models.py

CREATE TABLE IF NOT EXISTS abandoned_carts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_abandoned_carts_updated_at BEFORE UPDATE
ON abandoned_carts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: activity_participations
-- Class: ThemeActivity
-- File: app/marketing/thematic_campaign/models.py

CREATE TABLE IF NOT EXISTS activity_participations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_activity_participations_updated_at BEFORE UPDATE
ON activity_participations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: affiliate_applications
-- Class: CommissionStructure
-- File: app/marketing/affiliate_program/models.py

CREATE TABLE IF NOT EXISTS affiliate_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_affiliate_applications_updated_at BEFORE UPDATE
ON affiliate_applications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: affiliate_clicks
-- Class: AffiliateLevel
-- File: app/marketing/affiliate/models.py

CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_affiliate_clicks_updated_at BEFORE UPDATE
ON affiliate_clicks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: affiliate_commissions
-- Class: CommissionStatus
-- File: app/marketing/affiliate_commission/models.py

CREATE TABLE IF NOT EXISTS affiliate_commissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_affiliate_commissions_updated_at BEFORE UPDATE
ON affiliate_commissions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: affiliate_conversions
-- Class: Affiliate
-- File: app/marketing/affiliate/models.py

CREATE TABLE IF NOT EXISTS affiliate_conversions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_affiliate_conversions_updated_at BEFORE UPDATE
ON affiliate_conversions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: affiliate_payments
-- Class: CommissionType
-- File: app/marketing/affiliate_commission/models.py

CREATE TABLE IF NOT EXISTS affiliate_payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_affiliate_payments_updated_at BEFORE UPDATE
ON affiliate_payments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: affiliate_programs
-- Class: ProgramStatus
-- File: app/marketing/affiliate_program/models.py

CREATE TABLE IF NOT EXISTS affiliate_programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_affiliate_programs_updated_at BEFORE UPDATE
ON affiliate_programs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: affiliates
-- Class: AffiliateStatus
-- File: app/marketing/affiliate/models.py

CREATE TABLE IF NOT EXISTS affiliates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_affiliates_updated_at BEFORE UPDATE
ON affiliates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: ai_call_records
-- Class: AIServiceProvider
-- File: app/analytics/ai_copilot/models.py

CREATE TABLE IF NOT EXISTS ai_call_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ai_call_records_updated_at BEFORE UPDATE
ON ai_call_records FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: banner_translations
-- Class: Banner
-- File: app/content/banner/models.py

CREATE TABLE IF NOT EXISTS banner_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_banner_translations_updated_at BEFORE UPDATE
ON banner_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: banners
-- Class: BannerType
-- File: app/content/banner/models.py

CREATE TABLE IF NOT EXISTS banners (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_banners_updated_at BEFORE UPDATE
ON banners FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: behavior_funnels
-- Class: BehaviorFunnel
-- File: app/analytics/user_behavior_log/models.py

CREATE TABLE IF NOT EXISTS behavior_funnels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_behavior_funnels_updated_at BEFORE UPDATE
ON behavior_funnels FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: blacklists
-- Class: PointsTransactionType
-- File: app/customer/models.py

CREATE TABLE IF NOT EXISTS blacklists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blacklists_updated_at BEFORE UPDATE
ON blacklists FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: blog_categories
-- Class: BlogCategory
-- File: app/content/blog_category/models.py

CREATE TABLE IF NOT EXISTS blog_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blog_categories_updated_at BEFORE UPDATE
ON blog_categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: blog_category_translations
-- Class: BlogCategoryTranslation
-- File: app/content/blog_category/models.py

CREATE TABLE IF NOT EXISTS blog_category_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blog_category_translations_updated_at BEFORE UPDATE
ON blog_category_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: blog_tag_translations
-- Class: BlogTagTranslation
-- File: app/content/blog/models.py

CREATE TABLE IF NOT EXISTS blog_tag_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blog_tag_translations_updated_at BEFORE UPDATE
ON blog_tag_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: blog_tags
-- Class: BlogTag
-- File: app/content/blog/models.py

CREATE TABLE IF NOT EXISTS blog_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blog_tags_updated_at BEFORE UPDATE
ON blog_tags FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: blog_translations
-- Class: BlogTranslation
-- File: app/content/blog/models.py

CREATE TABLE IF NOT EXISTS blog_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blog_translations_updated_at BEFORE UPDATE
ON blog_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: blogs
-- Class: Blog
-- File: app/content/blog/models.py

CREATE TABLE IF NOT EXISTS blogs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blogs_updated_at BEFORE UPDATE
ON blogs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: bundle_items
-- Class: ProductTag
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS bundle_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_bundle_items_updated_at BEFORE UPDATE
ON bundle_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: bundle_recommendations
-- Class: BundleItem
-- File: app/marketing/intention_bundle/models.py

CREATE TABLE IF NOT EXISTS bundle_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_bundle_recommendations_updated_at BEFORE UPDATE
ON bundle_recommendations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: campaign_events
-- Class: CampaignStatus
-- File: app/marketing/campaign/models.py

CREATE TABLE IF NOT EXISTS campaign_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_campaign_events_updated_at BEFORE UPDATE
ON campaign_events FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: campaign_performance_metrics
-- Class: CampaignPerformanceMetric
-- File: app/analytics/marketing_report/models.py

CREATE TABLE IF NOT EXISTS campaign_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_campaign_performance_metrics_updated_at BEFORE UPDATE
ON campaign_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: carriers
-- Class: OrderShipment
-- File: app/order/shipment/models.py

CREATE TABLE IF NOT EXISTS carriers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_carriers_updated_at BEFORE UPDATE
ON carriers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cash_on_delivery_settings
-- Class: CashOnDelivery
-- File: app/payment/cod/models.py

CREATE TABLE IF NOT EXISTS cash_on_delivery_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cash_on_delivery_settings_updated_at BEFORE UPDATE
ON cash_on_delivery_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: collection_products
-- Class: SeasonalCollection
-- File: app/marketing/seasonal_collection/models.py

CREATE TABLE IF NOT EXISTS collection_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_collection_products_updated_at BEFORE UPDATE
ON collection_products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: content_engagements
-- Class: CulturalContentItem
-- File: app/marketing/cultural_content/models.py

CREATE TABLE IF NOT EXISTS content_engagements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_content_engagements_updated_at BEFORE UPDATE
ON content_engagements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: country_regions
-- Class: CountryRegion
-- File: app/localization/models.py

CREATE TABLE IF NOT EXISTS country_regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_country_regions_updated_at BEFORE UPDATE
ON country_regions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: country_translations
-- Class: CountryTranslation
-- File: app/localization/country/models.py

CREATE TABLE IF NOT EXISTS country_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_country_translations_updated_at BEFORE UPDATE
ON country_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: coupon_batches
-- Class: CouponFormat
-- File: app/marketing/coupon/models.py

CREATE TABLE IF NOT EXISTS coupon_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_coupon_batches_updated_at BEFORE UPDATE
ON coupon_batches FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_calendar_translations
-- Class: RecurrenceType
-- File: app/content/cultural_calendar/models.py

CREATE TABLE IF NOT EXISTS cultural_calendar_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_calendar_translations_updated_at BEFORE UPDATE
ON cultural_calendar_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_calendars
-- Class: EventType
-- File: app/content/cultural_calendar/models.py

CREATE TABLE IF NOT EXISTS cultural_calendars (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_calendars_updated_at BEFORE UPDATE
ON cultural_calendars FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_content_campaigns
-- Class: ContentType
-- File: app/marketing/cultural_content/models.py

CREATE TABLE IF NOT EXISTS cultural_content_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_content_campaigns_updated_at BEFORE UPDATE
ON cultural_content_campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_content_items
-- Class: CulturalContentCampaign
-- File: app/marketing/cultural_content/models.py

CREATE TABLE IF NOT EXISTS cultural_content_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_content_items_updated_at BEFORE UPDATE
ON cultural_content_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_element_trends
-- Class: CulturalElementTrend
-- File: app/analytics/cultural_trend/models.py

CREATE TABLE IF NOT EXISTS cultural_element_trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_element_trends_updated_at BEFORE UPDATE
ON cultural_element_trends FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_localization_translations
-- Class: CulturalLocalizationTranslation
-- File: app/localization/models.py

CREATE TABLE IF NOT EXISTS cultural_localization_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_localization_translations_updated_at BEFORE UPDATE
ON cultural_localization_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_localizations
-- Class: CulturalLocalization
-- File: app/localization/models.py

CREATE TABLE IF NOT EXISTS cultural_localizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_localizations_updated_at BEFORE UPDATE
ON cultural_localizations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_stories
-- Class: CulturalRegion
-- File: app/content/cultural_story/models.py

CREATE TABLE IF NOT EXISTS cultural_stories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_stories_updated_at BEFORE UPDATE
ON cultural_stories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_story_translations
-- Class: CulturalStory
-- File: app/content/cultural_story/models.py

CREATE TABLE IF NOT EXISTS cultural_story_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_story_translations_updated_at BEFORE UPDATE
ON cultural_story_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: cultural_trend_reports
-- Class: CulturalTrendReport
-- File: app/analytics/cultural_trend/models.py

CREATE TABLE IF NOT EXISTS cultural_trend_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cultural_trend_reports_updated_at BEFORE UPDATE
ON cultural_trend_reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: currency_rates
-- Class: CurrencyRate
-- File: app/payment/currency/models.py

CREATE TABLE IF NOT EXISTS currency_rates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_currency_rates_updated_at BEFORE UPDATE
ON currency_rates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_behaviors
-- Class: CustomerRole
-- File: app/customer/models.py

CREATE TABLE IF NOT EXISTS customer_behaviors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_behaviors_updated_at BEFORE UPDATE
ON customer_behaviors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_coupons
-- Class: CustomerCouponStatus
-- File: app/marketing/customer_coupon/models.py

CREATE TABLE IF NOT EXISTS customer_coupons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_coupons_updated_at BEFORE UPDATE
ON customer_coupons FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_cultural_preference_details
-- Class: CustomerCulturalPreference
-- File: app/customer/cultural_preference/models.py

CREATE TABLE IF NOT EXISTS customer_cultural_preference_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_cultural_preference_details_updated_at BEFORE UPDATE
ON customer_cultural_preference_details FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_groups
-- Class: RegistrationSource
-- File: app/customer/models.py

CREATE TABLE IF NOT EXISTS customer_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_groups_updated_at BEFORE UPDATE
ON customer_groups FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_intent_details
-- Class: CustomerIntent
-- File: app/customer/intent/models.py

CREATE TABLE IF NOT EXISTS customer_intent_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_intent_details_updated_at BEFORE UPDATE
ON customer_intent_details FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_points
-- Class: AddressType
-- File: app/customer/models.py

CREATE TABLE IF NOT EXISTS customer_points (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_points_updated_at BEFORE UPDATE
ON customer_points FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_promotion_usage
-- Class: DiscountType
-- File: app/marketing/simple_promotion/models.py

CREATE TABLE IF NOT EXISTS customer_promotion_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_promotion_usage_updated_at BEFORE UPDATE
ON customer_promotion_usage FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_reports
-- Class: CustomerReport
-- File: app/analytics/customer_report/models.py

CREATE TABLE IF NOT EXISTS customer_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_reports_updated_at BEFORE UPDATE
ON customer_reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_scene_preference_details
-- Class: CustomerScenePreference
-- File: app/customer/scene_preference/models.py

CREATE TABLE IF NOT EXISTS customer_scene_preference_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_scene_preference_details_updated_at BEFORE UPDATE
ON customer_scene_preference_details FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_segment_analyses
-- Class: CustomerSegmentAnalysis
-- File: app/analytics/customer_report/models.py

CREATE TABLE IF NOT EXISTS customer_segment_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_segment_analyses_updated_at BEFORE UPDATE
ON customer_segment_analyses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: customer_segments
-- Class: CustomerSegment
-- File: app/customer/segment/models.py

CREATE TABLE IF NOT EXISTS customer_segments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_segments_updated_at BEFORE UPDATE
ON customer_segments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: daily_ad_performance
-- Class: DailyAdPerformance
-- File: app/analytics/daily_summary/models.py

CREATE TABLE IF NOT EXISTS daily_ad_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_daily_ad_performance_updated_at BEFORE UPDATE
ON daily_ad_performance FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: daily_product_performance
-- Class: DailyProductPerformance
-- File: app/analytics/daily_summary/models.py

CREATE TABLE IF NOT EXISTS daily_product_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_daily_product_performance_updated_at BEFORE UPDATE
ON daily_product_performance FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: daily_sales_summary
-- Class: DailySalesSummary
-- File: app/analytics/daily_summary/models.py

CREATE TABLE IF NOT EXISTS daily_sales_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_daily_sales_summary_updated_at BEFORE UPDATE
ON daily_sales_summary FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: daily_user_behavior
-- Class: DailyUserBehavior
-- File: app/analytics/daily_summary/models.py

CREATE TABLE IF NOT EXISTS daily_user_behavior (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_daily_user_behavior_updated_at BEFORE UPDATE
ON daily_user_behavior FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: data_backups
-- Class: DataBackup
-- File: app/security/models.py

CREATE TABLE IF NOT EXISTS data_backups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_data_backups_updated_at BEFORE UPDATE
ON data_backups FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: discounts
-- Class: DiscountRuleType
-- File: app/marketing/discount/models.py

CREATE TABLE IF NOT EXISTS discounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_discounts_updated_at BEFORE UPDATE
ON discounts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: duty_rules
-- Class: DutyRule
-- File: app/duty/models.py

CREATE TABLE IF NOT EXISTS duty_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_duty_rules_updated_at BEFORE UPDATE
ON duty_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: duty_zone_countries
-- Class: DutyZoneCountry
-- File: app/duty/models.py

CREATE TABLE IF NOT EXISTS duty_zone_countries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_duty_zone_countries_updated_at BEFORE UPDATE
ON duty_zone_countries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: duty_zone_translations
-- Class: DutyZoneTranslation
-- File: app/duty/models.py

CREATE TABLE IF NOT EXISTS duty_zone_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_duty_zone_translations_updated_at BEFORE UPDATE
ON duty_zone_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: duty_zones
-- Class: DutyZone
-- File: app/duty/models.py

CREATE TABLE IF NOT EXISTS duty_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_duty_zones_updated_at BEFORE UPDATE
ON duty_zones FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: email_verification_codes
-- Class: Customer
-- File: app/customer/models.py

CREATE TABLE IF NOT EXISTS email_verification_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_email_verification_codes_updated_at BEFORE UPDATE
ON email_verification_codes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: faq_translations
-- Class: FAQ
-- File: app/content/faq/models.py

CREATE TABLE IF NOT EXISTS faq_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_faq_translations_updated_at BEFORE UPDATE
ON faq_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: faqs
-- Class: FAQCategory
-- File: app/content/faq/models.py

CREATE TABLE IF NOT EXISTS faqs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_faqs_updated_at BEFORE UPDATE
ON faqs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: fortune_profiles
-- Class: ReadingType
-- File: app/fortune/models.py

CREATE TABLE IF NOT EXISTS fortune_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_fortune_profiles_updated_at BEFORE UPDATE
ON fortune_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: fortune_readings
-- Class: FortuneProfile
-- File: app/fortune/models.py

CREATE TABLE IF NOT EXISTS fortune_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_fortune_readings_updated_at BEFORE UPDATE
ON fortune_readings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: free_shipping_rule_translations
-- Class: FreeShippingRule
-- File: app/shipping/free_rule/models.py

CREATE TABLE IF NOT EXISTS free_shipping_rule_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_free_shipping_rule_translations_updated_at BEFORE UPDATE
ON free_shipping_rule_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: free_shipping_rules
-- Class: FreeShippingRuleType
-- File: app/shipping/free_rule/models.py

CREATE TABLE IF NOT EXISTS free_shipping_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_free_shipping_rules_updated_at BEFORE UPDATE
ON free_shipping_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: gift_orders
-- Class: GiftWrapType
-- File: app/order/gift/models.py

CREATE TABLE IF NOT EXISTS gift_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_gift_orders_updated_at BEFORE UPDATE
ON gift_orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: gift_registries
-- Class: RegistryType
-- File: app/customer/gift_registry/models.py

CREATE TABLE IF NOT EXISTS gift_registries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_gift_registries_updated_at BEFORE UPDATE
ON gift_registries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: gift_registry_items
-- Class: RegistryStatus
-- File: app/customer/gift_registry/models.py

CREATE TABLE IF NOT EXISTS gift_registry_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_gift_registry_items_updated_at BEFORE UPDATE
ON gift_registry_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: gift_registry_purchases
-- Class: GiftRegistry
-- File: app/customer/gift_registry/models.py

CREATE TABLE IF NOT EXISTS gift_registry_purchases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_gift_registry_purchases_updated_at BEFORE UPDATE
ON gift_registry_purchases FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: installment_plans
-- Class: InstallmentPlanStatus
-- File: app/payment/installment/models.py

CREATE TABLE IF NOT EXISTS installment_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_installment_plans_updated_at BEFORE UPDATE
ON installment_plans FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: intent_analytics
-- Class: IntentAnalytics
-- File: app/analytics/intent_analytics/models.py

CREATE TABLE IF NOT EXISTS intent_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_intent_analytics_updated_at BEFORE UPDATE
ON intent_analytics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: intent_based_campaigns
-- Class: IntentBasedCampaign
-- File: app/marketing/intent_based/models.py

CREATE TABLE IF NOT EXISTS intent_based_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_intent_based_campaigns_updated_at BEFORE UPDATE
ON intent_based_campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: intent_engagement_records
-- Class: IntentEngagementRecord
-- File: app/marketing/intent_based/models.py

CREATE TABLE IF NOT EXISTS intent_engagement_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_intent_engagement_records_updated_at BEFORE UPDATE
ON intent_engagement_records FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: intent_performance_metrics
-- Class: IntentPerformanceMetric
-- File: app/analytics/intent_analytics/models.py

CREATE TABLE IF NOT EXISTS intent_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_intent_performance_metrics_updated_at BEFORE UPDATE
ON intent_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: intention_bundles
-- Class: IntentionBundleStatus
-- File: app/marketing/intention_bundle/models.py

CREATE TABLE IF NOT EXISTS intention_bundles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_intention_bundles_updated_at BEFORE UPDATE
ON intention_bundles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: intention_guide_translations
-- Class: IntentionGuideTranslation
-- File: app/content/intention_guide/models.py

CREATE TABLE IF NOT EXISTS intention_guide_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_intention_guide_translations_updated_at BEFORE UPDATE
ON intention_guide_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: intention_guides
-- Class: IntentionGuide
-- File: app/content/intention_guide/models.py

CREATE TABLE IF NOT EXISTS intention_guides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_intention_guides_updated_at BEFORE UPDATE
ON intention_guides FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: inventory_alerts
-- Class: InventoryAlert
-- File: app/analytics/inventory_report/models.py

CREATE TABLE IF NOT EXISTS inventory_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_inventory_alerts_updated_at BEFORE UPDATE
ON inventory_alerts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: inventory_history
-- Class: ProductPrice
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS inventory_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_inventory_history_updated_at BEFORE UPDATE
ON inventory_history FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: inventory_reports
-- Class: InventoryReport
-- File: app/analytics/inventory_report/models.py

CREATE TABLE IF NOT EXISTS inventory_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_inventory_reports_updated_at BEFORE UPDATE
ON inventory_reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: locale_preferences
-- Class: LocalePreference
-- File: app/localization/models.py

CREATE TABLE IF NOT EXISTS locale_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_locale_preferences_updated_at BEFORE UPDATE
ON locale_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: login_logs
-- Class: LoginLog
-- File: app/security/models.py

CREATE TABLE IF NOT EXISTS login_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_login_logs_updated_at BEFORE UPDATE
ON login_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: marketing_campaigns
-- Class: CampaignType
-- File: app/marketing/campaign/models.py

CREATE TABLE IF NOT EXISTS marketing_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_marketing_campaigns_updated_at BEFORE UPDATE
ON marketing_campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: marketing_reports
-- Class: MarketingReport
-- File: app/analytics/marketing_report/models.py

CREATE TABLE IF NOT EXISTS marketing_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_marketing_reports_updated_at BEFORE UPDATE
ON marketing_reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: material_guide_translations
-- Class: MaterialGuide
-- File: app/content/material_guide/models.py

CREATE TABLE IF NOT EXISTS material_guide_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_material_guide_translations_updated_at BEFORE UPDATE
ON material_guide_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: material_guides
-- Class: MaterialType
-- File: app/content/material_guide/models.py

CREATE TABLE IF NOT EXISTS material_guides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_material_guides_updated_at BEFORE UPDATE
ON material_guides FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: material_performance_metrics
-- Class: MaterialPerformanceMetric
-- File: app/analytics/material_popularity/models.py

CREATE TABLE IF NOT EXISTS material_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_material_performance_metrics_updated_at BEFORE UPDATE
ON material_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: material_popularities
-- Class: MaterialPopularity
-- File: app/analytics/material_popularity/models.py

CREATE TABLE IF NOT EXISTS material_popularities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_material_popularities_updated_at BEFORE UPDATE
ON material_popularities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: media_files
-- Class: MediaType
-- File: app/content/media/models.py

CREATE TABLE IF NOT EXISTS media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_media_files_updated_at BEFORE UPDATE
ON media_files FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: media_folders
-- Class: MediaCategory
-- File: app/content/media/models.py

CREATE TABLE IF NOT EXISTS media_folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_media_folders_updated_at BEFORE UPDATE
ON media_folders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: media_processing_jobs
-- Class: MediaFile
-- File: app/content/media/models.py

CREATE TABLE IF NOT EXISTS media_processing_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_media_processing_jobs_updated_at BEFORE UPDATE
ON media_processing_jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: media_usage
-- Class: MediaStatus
-- File: app/content/media/models.py

CREATE TABLE IF NOT EXISTS media_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_media_usage_updated_at BEFORE UPDATE
ON media_usage FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: meditation_guide_translations
-- Class: ExperienceLevel
-- File: app/content/meditation_guide/models.py

CREATE TABLE IF NOT EXISTS meditation_guide_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_meditation_guide_translations_updated_at BEFORE UPDATE
ON meditation_guide_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: meditation_guides
-- Class: MeditationType
-- File: app/content/meditation_guide/models.py

CREATE TABLE IF NOT EXISTS meditation_guides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_meditation_guides_updated_at BEFORE UPDATE
ON meditation_guides FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: navigation_menu_item_translations
-- Class: NavigationMenuItem
-- File: app/content/navigation_menu/models.py

CREATE TABLE IF NOT EXISTS navigation_menu_item_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_navigation_menu_item_translations_updated_at BEFORE UPDATE
ON navigation_menu_item_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: navigation_menu_items
-- Class: NavigationMenu
-- File: app/content/navigation_menu/models.py

CREATE TABLE IF NOT EXISTS navigation_menu_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_navigation_menu_items_updated_at BEFORE UPDATE
ON navigation_menu_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: navigation_menus
-- Class: MenuItemType
-- File: app/content/navigation_menu/models.py

CREATE TABLE IF NOT EXISTS navigation_menus (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_navigation_menus_updated_at BEFORE UPDATE
ON navigation_menus FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: operation_logs
-- Class: OperationLog
-- File: app/security/models.py

CREATE TABLE IF NOT EXISTS operation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_operation_logs_updated_at BEFORE UPDATE
ON operation_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_charge_items
-- Class: OrderChargeItem
-- File: app/shipping/order_record/models.py

CREATE TABLE IF NOT EXISTS order_charge_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_charge_items_updated_at BEFORE UPDATE
ON order_charge_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_duty_charges
-- Class: OrderDutyCharge
-- File: app/duty/models.py

CREATE TABLE IF NOT EXISTS order_duty_charges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_duty_charges_updated_at BEFORE UPDATE
ON order_duty_charges FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_notes
-- Class: PaymentType
-- File: app/order/models.py

CREATE TABLE IF NOT EXISTS order_notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_notes_updated_at BEFORE UPDATE
ON order_notes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_payments
-- Class: ShippingStatus
-- File: app/order/models.py

CREATE TABLE IF NOT EXISTS order_payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_payments_updated_at BEFORE UPDATE
ON order_payments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_returns
-- Class: ReturnStatus
-- File: app/order/return_/models.py

CREATE TABLE IF NOT EXISTS order_returns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_returns_updated_at BEFORE UPDATE
ON order_returns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_shipments
-- Class: ShipmentStatus
-- File: app/order/shipment/models.py

CREATE TABLE IF NOT EXISTS order_shipments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_shipments_updated_at BEFORE UPDATE
ON order_shipments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_shipping_info
-- Class: OrderShippingInfo
-- File: app/shipping/order_record/models.py

CREATE TABLE IF NOT EXISTS order_shipping_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_shipping_info_updated_at BEFORE UPDATE
ON order_shipping_info FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: order_status_history
-- Class: OrderItemStatus
-- File: app/order/models.py

CREATE TABLE IF NOT EXISTS order_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_order_status_history_updated_at BEFORE UPDATE
ON order_status_history FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: page_translations
-- Class: PageTranslation
-- File: app/content/page_translation/models.py

CREATE TABLE IF NOT EXISTS page_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_page_translations_updated_at BEFORE UPDATE
ON page_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: page_view_stats
-- Class: PageViewStats
-- File: app/analytics/visit_stats/models.py

CREATE TABLE IF NOT EXISTS page_view_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_page_view_stats_updated_at BEFORE UPDATE
ON page_view_stats FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: pages
-- Class: Page
-- File: app/content/page/models.py

CREATE TABLE IF NOT EXISTS pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_pages_updated_at BEFORE UPDATE
ON pages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: payment_gateways
-- Class: GatewayStatus
-- File: app/payment/gateway/models.py

CREATE TABLE IF NOT EXISTS payment_gateways (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_payment_gateways_updated_at BEFORE UPDATE
ON payment_gateways FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: payment_logs
-- Class: PaymentLog
-- File: app/payment/models.py

CREATE TABLE IF NOT EXISTS payment_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_payment_logs_updated_at BEFORE UPDATE
ON payment_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: payment_methods
-- Class: PaymentMethodStatus
-- File: app/payment/method/models.py

CREATE TABLE IF NOT EXISTS payment_methods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_payment_methods_updated_at BEFORE UPDATE
ON payment_methods FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: payment_statuses
-- Class: PaymentStatusEnum
-- File: app/payment/status/models.py

CREATE TABLE IF NOT EXISTS payment_statuses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_payment_statuses_updated_at BEFORE UPDATE
ON payment_statuses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: payment_transactions
-- Class: TransactionType
-- File: app/payment/transaction/models.py

CREATE TABLE IF NOT EXISTS payment_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_payment_transactions_updated_at BEFORE UPDATE
ON payment_transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: personalized_recommendations
-- Class: RecommendationType
-- File: app/marketing/personalized_recommendation/models.py

CREATE TABLE IF NOT EXISTS personalized_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_personalized_recommendations_updated_at BEFORE UPDATE
ON personalized_recommendations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_ai_analyses
-- Class: AICallStatus
-- File: app/analytics/ai_copilot/models.py

CREATE TABLE IF NOT EXISTS product_ai_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_ai_analyses_updated_at BEFORE UPDATE
ON product_ai_analyses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_attribute_values
-- Class: GenderType
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_attribute_values (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_attribute_values_updated_at BEFORE UPDATE
ON product_attribute_values FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_attributes
-- Class: MaterialType
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_attributes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_attributes_updated_at BEFORE UPDATE
ON product_attributes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_bundles
-- Class: InventoryHistory
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_bundles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_bundles_updated_at BEFORE UPDATE
ON product_bundles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_category_translations
-- Class: ProductCategory
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_category_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_category_translations_updated_at BEFORE UPDATE
ON product_category_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_duty_categories
-- Class: ProductDutyCategory
-- File: app/duty/models.py

CREATE TABLE IF NOT EXISTS product_duty_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_duty_categories_updated_at BEFORE UPDATE
ON product_duty_categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_duty_category_translations
-- Class: ProductDutyCategoryTranslation
-- File: app/duty/models.py

CREATE TABLE IF NOT EXISTS product_duty_category_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_duty_category_translations_updated_at BEFORE UPDATE
ON product_duty_category_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_intents
-- Class: ProductAttribute
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_intents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_intents_updated_at BEFORE UPDATE
ON product_intents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_inventories
-- Class: AttributeType
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_inventories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_inventories_updated_at BEFORE UPDATE
ON product_inventories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_materials
-- Class: ProductSku
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_materials_updated_at BEFORE UPDATE
ON product_materials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_prices
-- Class: ProductTranslation
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_prices_updated_at BEFORE UPDATE
ON product_prices FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_scenes
-- Class: ProductImage
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_scenes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_scenes_updated_at BEFORE UPDATE
ON product_scenes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_sku_translations
-- Class: InventoryOperation
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_sku_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_sku_translations_updated_at BEFORE UPDATE
ON product_sku_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_symbols
-- Class: ProductAttributeValue
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_symbols (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_symbols_updated_at BEFORE UPDATE
ON product_symbols FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_tags
-- Class: ImageType
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_tags_updated_at BEFORE UPDATE
ON product_tags FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_target_groups
-- Class: ProductInventory
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_target_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_target_groups_updated_at BEFORE UPDATE
ON product_target_groups FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_themes
-- Class: ProductSkuTranslation
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_themes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_themes_updated_at BEFORE UPDATE
ON product_themes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_translations
-- Class: Product
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS product_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_translations_updated_at BEFORE UPDATE
ON product_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: product_view_history
-- Class: ProductViewHistory
-- File: app/modules/tracking/models.py

CREATE TABLE IF NOT EXISTS product_view_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    sku VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_product_view_history_updated_at BEFORE UPDATE
ON product_view_history FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: promotion_content_translations
-- Class: PromotionContent
-- File: app/content/promotion/models.py

CREATE TABLE IF NOT EXISTS promotion_content_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_promotion_content_translations_updated_at BEFORE UPDATE
ON promotion_content_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: promotion_contents
-- Class: PromotionContentType
-- File: app/content/promotion/models.py

CREATE TABLE IF NOT EXISTS promotion_contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_promotion_contents_updated_at BEFORE UPDATE
ON promotion_contents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: promotion_text_templates
-- Class: PromotionContentTranslation
-- File: app/content/promotion/models.py

CREATE TABLE IF NOT EXISTS promotion_text_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_promotion_text_templates_updated_at BEFORE UPDATE
ON promotion_text_templates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: recommendation_models
-- Class: PersonalizedRecommendation
-- File: app/marketing/personalized_recommendation/models.py

CREATE TABLE IF NOT EXISTS recommendation_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_recommendation_models_updated_at BEFORE UPDATE
ON recommendation_models FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: recommendation_rules
-- Class: RecommendationAlgorithm
-- File: app/marketing/personalized_recommendation/models.py

CREATE TABLE IF NOT EXISTS recommendation_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_recommendation_rules_updated_at BEFORE UPDATE
ON recommendation_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: region_translations
-- Class: RegionTranslation
-- File: app/localization/country/models.py

CREATE TABLE IF NOT EXISTS region_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_region_translations_updated_at BEFORE UPDATE
ON region_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: regions
-- Class: Region
-- File: app/localization/country/models.py

CREATE TABLE IF NOT EXISTS regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_regions_updated_at BEFORE UPDATE
ON regions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: sales_report_snapshots
-- Class: SalesReportSnapshot
-- File: app/analytics/sales_report/models.py

CREATE TABLE IF NOT EXISTS sales_report_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_sales_report_snapshots_updated_at BEFORE UPDATE
ON sales_report_snapshots FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: sales_reports
-- Class: SalesReport
-- File: app/analytics/sales_report/models.py

CREATE TABLE IF NOT EXISTS sales_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_sales_reports_updated_at BEFORE UPDATE
ON sales_reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: scenario_conversions
-- Class: ScenarioConversion
-- File: app/analytics/scenario_conversion/models.py

CREATE TABLE IF NOT EXISTS scenario_conversions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_scenario_conversions_updated_at BEFORE UPDATE
ON scenario_conversions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: scene_based_content_translations
-- Class: SceneBasedContentTranslation
-- File: app/content/scene_based/models.py

CREATE TABLE IF NOT EXISTS scene_based_content_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_scene_based_content_translations_updated_at BEFORE UPDATE
ON scene_based_content_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: scene_based_contents
-- Class: SceneBasedContent
-- File: app/content/scene_based/models.py

CREATE TABLE IF NOT EXISTS scene_based_contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_scene_based_contents_updated_at BEFORE UPDATE
ON scene_based_contents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: scene_performance_metrics
-- Class: ScenePerformanceMetric
-- File: app/analytics/scenario_conversion/models.py

CREATE TABLE IF NOT EXISTS scene_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_scene_performance_metrics_updated_at BEFORE UPDATE
ON scene_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: search_queries
-- Class: SearchQuery
-- File: app/analytics/search_query/models.py

CREATE TABLE IF NOT EXISTS search_queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_search_queries_updated_at BEFORE UPDATE
ON search_queries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: search_query_metrics
-- Class: SearchQueryMetric
-- File: app/analytics/search_query/models.py

CREATE TABLE IF NOT EXISTS search_query_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_search_query_metrics_updated_at BEFORE UPDATE
ON search_query_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: search_suggestions
-- Class: SearchSuggestion
-- File: app/analytics/search_query/models.py

CREATE TABLE IF NOT EXISTS search_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_search_suggestions_updated_at BEFORE UPDATE
ON search_suggestions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: seasonal_collections
-- Class: SeasonType
-- File: app/marketing/seasonal_collection/models.py

CREATE TABLE IF NOT EXISTS seasonal_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_seasonal_collections_updated_at BEFORE UPDATE
ON seasonal_collections FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: seasonal_landing_pages
-- Class: CollectionProduct
-- File: app/marketing/seasonal_collection/models.py

CREATE TABLE IF NOT EXISTS seasonal_landing_pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_seasonal_landing_pages_updated_at BEFORE UPDATE
ON seasonal_landing_pages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: seo_setting_translations
-- Class: SEOSetting
-- File: app/content/seo_setting/models.py

CREATE TABLE IF NOT EXISTS seo_setting_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_seo_setting_translations_updated_at BEFORE UPDATE
ON seo_setting_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: seo_settings
-- Class: SEOEntityType
-- File: app/content/seo_setting/models.py

CREATE TABLE IF NOT EXISTS seo_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_seo_settings_updated_at BEFORE UPDATE
ON seo_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: shipment_items
-- Class: TrackingStatus
-- File: app/order/shipment/models.py

CREATE TABLE IF NOT EXISTS shipment_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_shipment_items_updated_at BEFORE UPDATE
ON shipment_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: shipment_tracking
-- Class: PackageType
-- File: app/order/shipment/models.py

CREATE TABLE IF NOT EXISTS shipment_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_shipment_tracking_updated_at BEFORE UPDATE
ON shipment_tracking FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: shipping_method_translations
-- Class: ShippingMethod
-- File: app/shipping/method/models.py

CREATE TABLE IF NOT EXISTS shipping_method_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_shipping_method_translations_updated_at BEFORE UPDATE
ON shipping_method_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: shipping_zone_translations
-- Class: ShippingZoneTranslation
-- File: app/shipping/zone/models.py

CREATE TABLE IF NOT EXISTS shipping_zone_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_shipping_zone_translations_updated_at BEFORE UPDATE
ON shipping_zone_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: simple_promotions
-- Class: SimplePromotionType
-- File: app/marketing/simple_promotion/models.py

CREATE TABLE IF NOT EXISTS simple_promotions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_simple_promotions_updated_at BEFORE UPDATE
ON simple_promotions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: stock_logs
-- Class: ProductScene
-- File: app/product/models.py

CREATE TABLE IF NOT EXISTS stock_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_stock_logs_updated_at BEFORE UPDATE
ON stock_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: symbol_dictionaries
-- Class: SymbolType
-- File: app/content/symbol_dictionary/models.py

CREATE TABLE IF NOT EXISTS symbol_dictionaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_symbol_dictionaries_updated_at BEFORE UPDATE
ON symbol_dictionaries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: symbol_dictionary_translations
-- Class: SymbolDictionary
-- File: app/content/symbol_dictionary/models.py

CREATE TABLE IF NOT EXISTS symbol_dictionary_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_symbol_dictionary_translations_updated_at BEFORE UPDATE
ON symbol_dictionary_translations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: symbol_performance_metrics
-- Class: SymbolPerformanceMetric
-- File: app/analytics/symbol_performance/models.py

CREATE TABLE IF NOT EXISTS symbol_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_symbol_performance_metrics_updated_at BEFORE UPDATE
ON symbol_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: symbol_performances
-- Class: SymbolPerformance
-- File: app/analytics/symbol_performance/models.py

CREATE TABLE IF NOT EXISTS symbol_performances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_symbol_performances_updated_at BEFORE UPDATE
ON symbol_performances FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: system_settings
-- Class: SystemSetting
-- File: app/security/models.py

CREATE TABLE IF NOT EXISTS system_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_system_settings_updated_at BEFORE UPDATE
ON system_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: thematic_campaigns
-- Class: ThemeType
-- File: app/marketing/thematic_campaign/models.py

CREATE TABLE IF NOT EXISTS thematic_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_thematic_campaigns_updated_at BEFORE UPDATE
ON thematic_campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: theme_activities
-- Class: ThemeSection
-- File: app/marketing/thematic_campaign/models.py

CREATE TABLE IF NOT EXISTS theme_activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_theme_activities_updated_at BEFORE UPDATE
ON theme_activities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: theme_performance_metrics
-- Class: ThemePerformanceMetric
-- File: app/analytics/theme_performance/models.py

CREATE TABLE IF NOT EXISTS theme_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_theme_performance_metrics_updated_at BEFORE UPDATE
ON theme_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: theme_performances
-- Class: ThemePerformance
-- File: app/analytics/theme_performance/models.py

CREATE TABLE IF NOT EXISTS theme_performances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_theme_performances_updated_at BEFORE UPDATE
ON theme_performances FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: theme_sections
-- Class: ThematicCampaign
-- File: app/marketing/thematic_campaign/models.py

CREATE TABLE IF NOT EXISTS theme_sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_theme_sections_updated_at BEFORE UPDATE
ON theme_sections FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: tracking_behaviors
-- Class: TrackingBehavior
-- File: app/modules/tracking/models.py

CREATE TABLE IF NOT EXISTS tracking_behaviors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tracking_behaviors_updated_at BEFORE UPDATE
ON tracking_behaviors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: tracking_campaigns
-- Class: TrackingCampaign
-- File: app/modules/tracking/models.py

CREATE TABLE IF NOT EXISTS tracking_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tracking_campaigns_updated_at BEFORE UPDATE
ON tracking_campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: tracking_visits
-- Class: TrackingVisit
-- File: app/modules/tracking/models.py

CREATE TABLE IF NOT EXISTS tracking_visits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tracking_visits_updated_at BEFORE UPDATE
ON tracking_visits FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: translation_keys
-- Class: TranslationKey
-- File: app/localization/models.py

CREATE TABLE IF NOT EXISTS translation_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_translation_keys_updated_at BEFORE UPDATE
ON translation_keys FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: translation_values
-- Class: TranslationValue
-- File: app/localization/models.py

CREATE TABLE IF NOT EXISTS translation_values (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_code VARCHAR(10) NOT NULL,
    field_name VARCHAR(100),
    field_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_translation_values_updated_at BEFORE UPDATE
ON translation_values FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: user_behavior_logs
-- Class: UserBehaviorLog
-- File: app/analytics/user_behavior_log/models.py

CREATE TABLE IF NOT EXISTS user_behavior_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_behavior_logs_updated_at BEFORE UPDATE
ON user_behavior_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: user_behavior_metrics
-- Class: UserBehaviorMetric
-- File: app/analytics/user_behavior_log/models.py

CREATE TABLE IF NOT EXISTS user_behavior_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255),
    username VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_behavior_metrics_updated_at BEFORE UPDATE
ON user_behavior_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: visit_sessions
-- Class: VisitSession
-- File: app/analytics/visit_stats/models.py

CREATE TABLE IF NOT EXISTS visit_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_visit_sessions_updated_at BEFORE UPDATE
ON visit_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Table: visit_stats
-- Class: VisitStats
-- File: app/analytics/visit_stats/models.py

CREATE TABLE IF NOT EXISTS visit_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_visit_stats_updated_at BEFORE UPDATE
ON visit_stats FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


COMMIT;

-- Note: Please review and adjust the table structures based on the actual model definitions
-- Check the corresponding Python files for the exact column definitions
