-- 在products表中添加main_image_url字段
-- 执行时间：请在低峰期执行此脚本
-- 用途：为Product模型添加主图URL字段，优化商品列表查询性能

-- Step 1: 添加列
ALTER TABLE products 
ADD COLUMN main_image_url VARCHAR(512);

-- Step 2: 添加列注释（PostgreSQL语法）
COMMENT ON COLUMN products.main_image_url IS '商品主图URL，用于列表展示和快速访问';

-- 可选：创建索引以优化查询性能（如果经常根据是否有主图进行筛选）
-- CREATE INDEX idx_products_main_image_url ON products(main_image_url) WHERE main_image_url IS NOT NULL;

-- 可选：批量更新现有商品的主图URL（如果你想从ProductImage表同步现有数据）
/*
UPDATE products 
SET main_image_url = (
    SELECT pi.image_url 
    FROM product_images pi 
    WHERE pi.product_id = products.id 
    AND pi.image_type = 'main' 
    AND pi.is_active = true
    ORDER BY pi.sort_order ASC, pi.created_at ASC 
    LIMIT 1
)
WHERE EXISTS (
    SELECT 1 
    FROM product_images pi 
    WHERE pi.product_id = products.id 
    AND pi.image_type = 'main' 
    AND pi.is_active = true
);
*/

-- 验证字段添加成功
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default,
    character_maximum_length
FROM information_schema.columns 
WHERE table_name = 'products' 
AND column_name = 'main_image_url';

-- 验证列注释（PostgreSQL方式）
SELECT 
    c.column_name,
    pgd.description as column_comment
FROM pg_catalog.pg_statio_all_tables st
RIGHT JOIN pg_catalog.pg_description pgd ON (pgd.objoid = st.relid)
RIGHT JOIN information_schema.columns c ON (pgd.objsubid = c.ordinal_position AND c.table_name = st.relname)
WHERE c.table_name = 'products' AND c.column_name = 'main_image_url'; 