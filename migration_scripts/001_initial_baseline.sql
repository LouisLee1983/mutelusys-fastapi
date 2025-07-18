-- ========================================
-- 初始化迁移脚本
-- ========================================
-- 基于当前数据库状态: 88 个表
-- 生成时间: 2025-06-24 15:08:50
-- 此脚本记录了数据库同步后的基准状态

-- ========================================
-- 当前数据库表列表 (基准状态)
-- ========================================
--  1. ai_call_records
--  2. blacklists
--  3. bundle_intent
--  4. bundle_items
--  5. bundle_theme
--  6. cash_on_delivery_settings
--  7. coupon_batches
--  8. coupons
--  9. currencies
-- 10. currency_rates
-- 11. customer_addresses
-- 12. customer_behaviors
-- 13. customer_coupons
-- 14. customer_cultural_preference
-- 15. customer_cultural_preference_details
-- 16. customer_group
-- 17. customer_groups
-- 18. customer_intent
-- 19. customer_intent_details
-- 20. customer_points
-- 21. customer_scene_preference
-- 22. customer_scene_preference_details
-- 23. customer_segments
-- 24. customers
-- 25. data_backups
-- 26. email_verification_codes
-- 27. gift_orders
-- 28. gift_registries
-- 29. gift_registry_items
-- 30. gift_registry_purchases
-- 31. gift_wrappings
-- 32. installment_plans
-- 33. inventory_history
-- 34. login_logs
-- 35. operation_logs
-- 36. order_items
-- 37. order_returns
-- 38. orders
-- 39. payment_gateways
-- 40. payment_logs
-- 41. payment_methods
-- 42. payment_statuses
-- 43. payment_transactions
-- 44. permissions
-- 45. product_ai_analyses
-- 46. product_attribute_values
-- 47. product_attributes
-- 48. product_bundles
-- 49. product_categories
-- 50. product_category
-- 51. product_category_translations
-- 52. product_images
-- 53. product_intent
-- 54. product_intents
-- 55. product_inventories
-- 56. product_material
-- 57. product_materials
-- 58. product_prices
-- 59. product_scene
-- 60. product_scenes
-- 61. product_skus
-- 62. product_symbol
-- 63. product_symbols
-- 64. product_tag
-- 65. product_tags
-- 66. product_target_group
-- 67. product_target_groups
-- 68. product_theme
-- 69. product_themes
-- 70. product_translations
-- 71. products
-- 72. promotions
-- 73. return_item
-- 74. role_permissions
-- 75. roles
-- 76. segment_customer
-- 77. shipment_item
-- 78. shipping_addresses
-- 79. shipping_carriers
-- 80. shipping_methods
-- 81. shipping_order_shipments
-- 82. shipping_tracking_events
-- 83. shipping_trackings
-- 84. shipping_zone_method
-- 85. sku_attribute_value
-- 86. system_settings
-- 87. user_roles
-- 88. users

-- ========================================
-- 迁移历史跟踪表
-- ========================================
-- 创建迁移历史跟踪表，用于记录所有执行的迁移
CREATE TABLE IF NOT EXISTS migration_history (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL UNIQUE,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    sql_checksum VARCHAR(64),
    execution_time_ms INTEGER
);

-- ========================================
-- 基准状态标记
-- ========================================
-- 插入基准迁移记录
INSERT INTO migration_history (migration_name, description, execution_time_ms) VALUES
('001_initial_baseline', '基于模型同步后的数据库基准状态，包含88个表', 0)
ON CONFLICT (migration_name) DO NOTHING;

-- ========================================
-- 索引优化建议
-- ========================================
-- 基于当前表结构，添加一些常用的索引

-- 产品相关索引
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_product_skus_product_id ON product_skus(product_id);
CREATE INDEX IF NOT EXISTS idx_product_prices_sku_id ON product_prices(sku_id);

-- 订单相关索引
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_sku_id ON order_items(sku_id);

-- 客户相关索引
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);
CREATE INDEX IF NOT EXISTS idx_customer_addresses_customer_id ON customer_addresses(customer_id);

-- 支付相关索引
CREATE INDEX IF NOT EXISTS idx_payment_transactions_order_id ON payment_transactions(order_id);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_status ON payment_transactions(status);

-- 时间戳索引（用于查询和统计）
CREATE INDEX IF NOT EXISTS idx_ai_call_records_created_at ON ai_call_records(created_at);
CREATE INDEX IF NOT EXISTS idx_login_logs_created_at ON login_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_operation_logs_created_at ON operation_logs(created_at);

-- ========================================
-- 基准状态确认完成
-- ========================================
-- 此迁移标记数据库已达到基准状态
-- 后续所有的模型变更都应通过新的迁移脚本来处理