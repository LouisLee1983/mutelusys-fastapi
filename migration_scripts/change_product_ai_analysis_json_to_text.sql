-- 修改商品AI分析结果表的JSON字段为Text字段
-- 解决PostgreSQL JSON类型转换问题
-- 执行时间: 2024-06-11

-- 开始事务
BEGIN;

-- 修改字段类型从JSON到TEXT
ALTER TABLE product_ai_analyses 
    ALTER COLUMN suggested_category_ids TYPE TEXT USING suggested_category_ids::TEXT,
    ALTER COLUMN suggested_attributes TYPE TEXT USING suggested_attributes::TEXT,
    ALTER COLUMN suggested_materials TYPE TEXT USING suggested_materials::TEXT,
    ALTER COLUMN suggested_colors TYPE TEXT USING suggested_colors::TEXT,
    ALTER COLUMN suggested_sizes TYPE TEXT USING suggested_sizes::TEXT,
    ALTER COLUMN suggested_prices TYPE TEXT USING suggested_prices::TEXT,
    ALTER COLUMN suggested_tags TYPE TEXT USING suggested_tags::TEXT,
    ALTER COLUMN suggested_scenes TYPE TEXT USING suggested_scenes::TEXT,
    ALTER COLUMN suggested_target_groups TYPE TEXT USING suggested_target_groups::TEXT,
    ALTER COLUMN raw_analysis TYPE TEXT USING raw_analysis::TEXT;

-- 更新字段注释
COMMENT ON COLUMN product_ai_analyses.suggested_category_ids IS '建议的分类ID列表(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_attributes IS '建议的属性信息(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_materials IS '建议的材质信息(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_colors IS '建议的颜色信息(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_sizes IS '建议的尺寸信息(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_prices IS '建议的价格信息(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_tags IS '建议的标签(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_scenes IS '建议的使用场景(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.suggested_target_groups IS '建议的目标人群(JSON格式)';
COMMENT ON COLUMN product_ai_analyses.raw_analysis IS '原始分析结果(JSON格式)';

-- 提交事务
COMMIT; 