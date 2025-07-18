-- 产品文章管理表创建脚本
-- 创建时间: 2025-06-26
-- 描述: 为产品添加可共享的图文介绍文章功能，支持多语种翻译

-- 1. 创建文章状态和类型的枚举类型
DO $$ 
BEGIN
    -- 创建文章状态枚举
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'articlestatus') THEN
        CREATE TYPE articlestatus AS ENUM ('draft', 'published', 'archived');
    END IF;
    
    -- 创建文章类型枚举
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'articletype') THEN
        CREATE TYPE articletype AS ENUM ('product_intro', 'material_guide', 'usage_guide', 'cultural_story', 'care_instruction');
    END IF;
END $$;

-- 2. 创建产品文章表
CREATE TABLE IF NOT EXISTS product_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    article_type articletype NOT NULL DEFAULT 'product_intro',
    status articlestatus NOT NULL DEFAULT 'draft',
    
    -- 内容字段
    summary TEXT,
    content TEXT,
    featured_image_url VARCHAR(512),
    
    -- 分类和标签
    category VARCHAR(100),
    tags VARCHAR(500),
    
    -- SEO字段
    seo_title VARCHAR(255),
    seo_description VARCHAR(500),
    seo_keywords VARCHAR(255),
    
    -- 管理字段
    author_id UUID REFERENCES users(id) ON DELETE SET NULL,
    is_featured BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    
    -- 自动分配规则
    auto_assign_materials VARCHAR(500),
    auto_assign_categories VARCHAR(500),
    auto_assign_tags VARCHAR(500),
    
    -- 时间字段
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 3. 创建产品文章翻译表
CREATE TABLE IF NOT EXISTS product_article_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES product_articles(id) ON DELETE CASCADE NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    
    -- 翻译内容
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    content TEXT,
    
    -- SEO翻译
    seo_title VARCHAR(255),
    seo_description VARCHAR(500),
    seo_keywords VARCHAR(255),
    
    -- 分类标签翻译
    category VARCHAR(100),
    tags VARCHAR(500),
    
    -- 管理字段
    is_auto_translated BOOLEAN DEFAULT FALSE,
    translator_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- 时间字段
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- 唯一约束：一个文章在同一语言下只能有一个翻译
    UNIQUE(article_id, language_code)
);

-- 4. 创建产品与文章的多对多关联表
CREATE TABLE IF NOT EXISTS product_article_associations (
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    article_id UUID REFERENCES product_articles(id) ON DELETE CASCADE,
    is_default BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    PRIMARY KEY (product_id, article_id)
);

-- 5. 创建产品文章模板表
CREATE TABLE IF NOT EXISTS product_article_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    article_type articletype NOT NULL,
    
    -- 模板内容
    title_template VARCHAR(255),
    summary_template TEXT,
    content_template TEXT,
    
    -- 自动填充规则
    auto_fill_rules TEXT,
    
    -- 管理字段
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 6. 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_product_articles_slug ON product_articles(slug);
CREATE INDEX IF NOT EXISTS idx_product_articles_status ON product_articles(status);
CREATE INDEX IF NOT EXISTS idx_product_articles_type ON product_articles(article_type);
CREATE INDEX IF NOT EXISTS idx_product_articles_created_at ON product_articles(created_at);
CREATE INDEX IF NOT EXISTS idx_product_articles_published_at ON product_articles(published_at);

CREATE INDEX IF NOT EXISTS idx_product_article_translations_article_id ON product_article_translations(article_id);
CREATE INDEX IF NOT EXISTS idx_product_article_translations_language ON product_article_translations(language_code);

CREATE INDEX IF NOT EXISTS idx_product_article_associations_product_id ON product_article_associations(product_id);
CREATE INDEX IF NOT EXISTS idx_product_article_associations_article_id ON product_article_associations(article_id);

-- 7. 添加注释
COMMENT ON TABLE product_articles IS '产品文章表 - 可被多个产品共享的介绍文章';
COMMENT ON TABLE product_article_translations IS '产品文章多语言翻译表';
COMMENT ON TABLE product_article_associations IS '产品与文章的多对多关联表';
COMMENT ON TABLE product_article_templates IS '产品文章模板表 - 用于快速创建标准化的产品文章';

COMMENT ON COLUMN product_articles.auto_assign_materials IS '自动分配给包含这些材质的产品，逗号分隔材质名称';
COMMENT ON COLUMN product_articles.auto_assign_categories IS '自动分配给这些分类的产品，逗号分隔分类名称';
COMMENT ON COLUMN product_articles.auto_assign_tags IS '自动分配给包含这些标签的产品，逗号分隔标签名称';

COMMENT ON COLUMN product_article_associations.is_default IS '是否为该产品的默认文章';
COMMENT ON COLUMN product_article_associations.sort_order IS '在该产品下的显示顺序';

-- 8. 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要的表创建触发器
DO $$
BEGIN
    -- product_articles表的更新触发器
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_product_articles_updated_at') THEN
        CREATE TRIGGER update_product_articles_updated_at
            BEFORE UPDATE ON product_articles
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    END IF;
    
    -- product_article_translations表的更新触发器
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_product_article_translations_updated_at') THEN
        CREATE TRIGGER update_product_article_translations_updated_at
            BEFORE UPDATE ON product_article_translations
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    END IF;
    
    -- product_article_templates表的更新触发器
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_product_article_templates_updated_at') THEN
        CREATE TRIGGER update_product_article_templates_updated_at
            BEFORE UPDATE ON product_article_templates
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;