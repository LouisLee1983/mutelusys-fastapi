-- 更新商品分类默认图片脚本
-- 将所有image_url和icon_url为NULL或空字符串的记录更新为默认值
-- 执行时间：$(date '+%Y-%m-%d %H:%M:%S')

-- 开始事务
BEGIN;

-- 显示更新前的统计
SELECT 
    '更新前统计' as stage,
    COUNT(*) as total_categories,
    COUNT(CASE WHEN image_url IS NULL OR image_url = '' THEN 1 END) as null_hero_images,
    COUNT(CASE WHEN icon_url IS NULL OR icon_url = '' THEN 1 END) as null_icon_images
FROM product_categories;

-- 更新image_url为空的记录
UPDATE product_categories 
SET image_url = '/static/uploads/category-hero-images/category-default-hero-image.jpg'
WHERE image_url IS NULL OR image_url = '';

-- 获取更新的hero图片数量
SELECT ROW_COUNT() as updated_hero_images;

-- 更新icon_url为空的记录
UPDATE product_categories 
SET icon_url = '/static/uploads/category-hero-images/category-default-icon.jpg'
WHERE icon_url IS NULL OR icon_url = '';

-- 获取更新的icon图片数量
SELECT ROW_COUNT() as updated_icon_images;

-- 更新updated_at字段到当前时间
UPDATE product_categories 
SET updated_at = CURRENT_TIMESTAMP
WHERE image_url = '/static/uploads/category-hero-images/category-default-hero-image.jpg' 
   OR icon_url = '/static/uploads/category-hero-images/category-default-icon.jpg';

-- 显示更新后的统计
SELECT 
    '更新后统计' as stage,
    COUNT(*) as total_categories,
    COUNT(CASE WHEN image_url = '/static/uploads/category-hero-images/category-default-hero-image.jpg' THEN 1 END) as default_hero_images,
    COUNT(CASE WHEN icon_url = '/static/uploads/category-hero-images/category-default-icon.jpg' THEN 1 END) as default_icon_images,
    COUNT(CASE WHEN image_url IS NULL OR image_url = '' THEN 1 END) as remaining_null_hero_images,
    COUNT(CASE WHEN icon_url IS NULL OR icon_url = '' THEN 1 END) as remaining_null_icon_images
FROM product_categories;

-- 显示具体更新的分类信息
SELECT 
    id,
    name,
    slug,
    image_url,
    icon_url,
    updated_at
FROM product_categories 
WHERE image_url = '/static/uploads/category-hero-images/category-default-hero-image.jpg' 
   OR icon_url = '/static/uploads/category-hero-images/category-default-icon.jpg'
ORDER BY updated_at DESC;

-- 提交事务
COMMIT;

-- 输出完成信息
SELECT 'Category default images update completed successfully!' as status; 