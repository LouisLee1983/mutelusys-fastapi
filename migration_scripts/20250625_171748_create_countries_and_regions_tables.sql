-- 创建国家和地区相关表
-- 执行时间: 2025-06-25 17:17:48

-- 创建countries表
CREATE TABLE IF NOT EXISTS countries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(2) UNIQUE NOT NULL,
    code3 VARCHAR(3) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100),
    currency VARCHAR(3),
    phone_code VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 为countries表添加注释
COMMENT ON TABLE countries IS '国家表';
COMMENT ON COLUMN countries.code IS 'ISO 3166-1 alpha-2 国家代码';
COMMENT ON COLUMN countries.code3 IS 'ISO 3166-1 alpha-3 国家代码';
COMMENT ON COLUMN countries.name IS '英文名称';
COMMENT ON COLUMN countries.native_name IS '本地名称';
COMMENT ON COLUMN countries.currency IS '默认货币代码';
COMMENT ON COLUMN countries.phone_code IS '电话区号';
COMMENT ON COLUMN countries.status IS '状态 active/inactive';
COMMENT ON COLUMN countries.created_at IS '创建时间';
COMMENT ON COLUMN countries.updated_at IS '更新时间';

-- 创建country_translations表
CREATE TABLE IF NOT EXISTS country_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_id UUID NOT NULL,
    language VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
);

-- 为country_translations表添加注释
COMMENT ON TABLE country_translations IS '国家翻译表';
COMMENT ON COLUMN country_translations.country_id IS '国家ID';
COMMENT ON COLUMN country_translations.language IS '语言代码 如 zh-CN, en-US, th-TH';
COMMENT ON COLUMN country_translations.name IS '翻译名称';
COMMENT ON COLUMN country_translations.created_at IS '创建时间';
COMMENT ON COLUMN country_translations.updated_at IS '更新时间';

-- 创建regions表（如果不存在）
CREATE TABLE IF NOT EXISTS regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(30) UNIQUE NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 为regions表添加注释
COMMENT ON TABLE regions IS '地区表 - 用于关税和运费的地区分组';
COMMENT ON COLUMN regions.name IS '地区名称';
COMMENT ON COLUMN regions.code IS '地区代码';
COMMENT ON COLUMN regions.description IS '地区描述';
COMMENT ON COLUMN regions.status IS '状态 active/inactive';
COMMENT ON COLUMN regions.created_at IS '创建时间';
COMMENT ON COLUMN regions.updated_at IS '更新时间';

-- 创建region_translations表
CREATE TABLE IF NOT EXISTS region_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_id UUID NOT NULL,
    language VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES regions(id) ON DELETE CASCADE
);

-- 为region_translations表添加注释
COMMENT ON TABLE region_translations IS '地区翻译表';
COMMENT ON COLUMN region_translations.region_id IS '地区ID';
COMMENT ON COLUMN region_translations.language IS '语言代码';
COMMENT ON COLUMN region_translations.name IS '翻译名称';
COMMENT ON COLUMN region_translations.description IS '翻译描述';
COMMENT ON COLUMN region_translations.created_at IS '创建时间';
COMMENT ON COLUMN region_translations.updated_at IS '更新时间';

-- 创建country_regions表（如果不存在）
CREATE TABLE IF NOT EXISTS country_regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_id UUID NOT NULL,
    region_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country_id, region_id)
);

-- 添加外键约束（如果不存在）
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'country_regions_country_id_fkey'
        AND table_name = 'country_regions'
    ) THEN
        ALTER TABLE country_regions 
        ADD CONSTRAINT country_regions_country_id_fkey 
        FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE;
    END IF;
    
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'country_regions_region_id_fkey'
        AND table_name = 'country_regions'
    ) THEN
        ALTER TABLE country_regions 
        ADD CONSTRAINT country_regions_region_id_fkey 
        FOREIGN KEY (region_id) REFERENCES regions(id) ON DELETE CASCADE;
    END IF;
END $$;

-- 为country_regions表添加注释
COMMENT ON TABLE country_regions IS '国家地区关联表';
COMMENT ON COLUMN country_regions.country_id IS '国家ID';
COMMENT ON COLUMN country_regions.region_id IS '地区ID';

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_countries_code ON countries(code);
CREATE INDEX IF NOT EXISTS idx_countries_code3 ON countries(code3);
CREATE INDEX IF NOT EXISTS idx_countries_status ON countries(status);
CREATE INDEX IF NOT EXISTS idx_country_translations_country_id ON country_translations(country_id);
CREATE INDEX IF NOT EXISTS idx_country_translations_language ON country_translations(language);
CREATE INDEX IF NOT EXISTS idx_regions_code ON regions(code);
CREATE INDEX IF NOT EXISTS idx_regions_status ON regions(status);
CREATE INDEX IF NOT EXISTS idx_region_translations_region_id ON region_translations(region_id);
CREATE INDEX IF NOT EXISTS idx_region_translations_language ON region_translations(language);
CREATE INDEX IF NOT EXISTS idx_country_regions_country_id ON country_regions(country_id);
CREATE INDEX IF NOT EXISTS idx_country_regions_region_id ON country_regions(region_id);

-- 创建或更新updated_at触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为所有表创建updated_at触发器
DROP TRIGGER IF EXISTS update_countries_updated_at ON countries;
CREATE TRIGGER update_countries_updated_at
    BEFORE UPDATE ON countries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_country_translations_updated_at ON country_translations;
CREATE TRIGGER update_country_translations_updated_at
    BEFORE UPDATE ON country_translations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_regions_updated_at ON regions;
CREATE TRIGGER update_regions_updated_at
    BEFORE UPDATE ON regions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_region_translations_updated_at ON region_translations;
CREATE TRIGGER update_region_translations_updated_at
    BEFORE UPDATE ON region_translations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();