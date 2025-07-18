-- Migration Script: Add role column to customers table
-- Generated at: 2025-06-27
-- Description: Add the missing 'role' column to customers table

BEGIN;

-- Create CustomerRole enum type if it doesn't exist
DO $$ BEGIN
    CREATE TYPE customerrole AS ENUM ('regular', 'kol', 'vip');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Add role column to customers table
ALTER TABLE customers 
ADD COLUMN IF NOT EXISTS role customerrole NOT NULL DEFAULT 'regular';

-- Add comment for the role column
COMMENT ON COLUMN customers.role IS '客户角色';

COMMIT;