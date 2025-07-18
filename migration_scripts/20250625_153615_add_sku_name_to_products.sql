-- Migration Script: Add sku_name column to products and product_skus tables
-- Generated at: 2025-06-25 15:36:15
-- Purpose: Add sku_name field for consumer-facing SKU names

BEGIN;

-- Add sku_name column to products table
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS sku_name VARCHAR(255);

-- Update existing products to use sku_code as default sku_name where null
UPDATE products 
SET sku_name = sku_code 
WHERE sku_name IS NULL;

-- Add sku_name column to product_skus table
ALTER TABLE product_skus 
ADD COLUMN IF NOT EXISTS sku_name VARCHAR(255);

-- Update existing product_skus to use sku_code as default sku_name where null
UPDATE product_skus 
SET sku_name = sku_code 
WHERE sku_name IS NULL;

-- Add comment to describe the column purpose
COMMENT ON COLUMN products.sku_name IS 'Consumer-facing SKU name, defaults to sku_code if not specified';
COMMENT ON COLUMN product_skus.sku_name IS 'Consumer-facing SKU name, defaults to sku_code if not specified';

COMMIT;