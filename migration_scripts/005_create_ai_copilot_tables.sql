-- AI助手相关数据表迁移脚本
-- 创建时间：2024-01-01
-- 作者：AI Assistant

BEGIN;

-- 创建AI服务提供商枚举类型
CREATE TYPE ai_service_provider AS ENUM (
    'alibaba_bailian',
    'openai', 
    'anthropic',
    'tencent_hunyuan',
    'baidu_qianfan'
);

-- 创建AI调用状态枚举类型
CREATE TYPE ai_call_status AS ENUM (
    'pending',
    'processing', 
    'success',
    'failed',
    'cancelled'
);

-- 创建AI调用类型枚举类型
CREATE TYPE ai_call_type AS ENUM (
    'product_analysis',
    'content_generation',
    'translation',
    'image_recognition',
    'text_analysis'
);

-- 创建AI调用记录表
CREATE TABLE ai_call_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider ai_service_provider NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    call_type ai_call_type NOT NULL,
    status ai_call_status DEFAULT 'pending',
    
    -- 请求相关字段
    image_urls TEXT[],
    prompt TEXT,
    request_data JSONB,
    business_context JSONB,
    
    -- 响应相关字段
    response_data JSONB,
    parsed_result JSONB,
    error_message TEXT,
    
    -- 性能和成本字段
    tokens_used INTEGER,
    cost DECIMAL(10, 6),
    duration_ms INTEGER,
    confidence_score DECIMAL(3, 2),
    
    -- 关联字段
    user_id UUID,
    product_id UUID,
    
    -- 时间字段
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建商品AI分析结果表
CREATE TABLE product_ai_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    call_record_id UUID NOT NULL REFERENCES ai_call_records(id) ON DELETE CASCADE,
    product_id UUID,
    
    -- AI分析建议字段
    suggested_name VARCHAR(255),
    suggested_description TEXT,
    suggested_category_ids UUID[],
    suggested_attributes JSONB,
    suggested_materials TEXT[],
    suggested_colors TEXT[],
    suggested_sizes TEXT[],
    suggested_prices JSONB,
    suggested_tags TEXT[],
    suggested_scenes TEXT[],
    suggested_target_groups TEXT[],
    
    -- 分析置信度
    analysis_confidence DECIMAL(3, 2),
    
    -- 原始分析结果
    raw_analysis JSONB,
    
    -- 应用状态
    is_applied BOOLEAN DEFAULT FALSE,
    applied_at TIMESTAMP WITH TIME ZONE,
    applied_by UUID,
    
    -- 时间字段
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_ai_call_records_provider ON ai_call_records(provider);
CREATE INDEX idx_ai_call_records_status ON ai_call_records(status);
CREATE INDEX idx_ai_call_records_call_type ON ai_call_records(call_type);
CREATE INDEX idx_ai_call_records_user_id ON ai_call_records(user_id);
CREATE INDEX idx_ai_call_records_product_id ON ai_call_records(product_id);
CREATE INDEX idx_ai_call_records_created_at ON ai_call_records(created_at DESC);

CREATE INDEX idx_product_ai_analyses_call_record_id ON product_ai_analyses(call_record_id);
CREATE INDEX idx_product_ai_analyses_product_id ON product_ai_analyses(product_id);
CREATE INDEX idx_product_ai_analyses_is_applied ON product_ai_analyses(is_applied);
CREATE INDEX idx_product_ai_analyses_created_at ON product_ai_analyses(created_at DESC);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器
CREATE TRIGGER update_ai_call_records_updated_at 
    BEFORE UPDATE ON ai_call_records 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_ai_analyses_updated_at 
    BEFORE UPDATE ON product_ai_analyses 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 添加注释
COMMENT ON TABLE ai_call_records IS 'AI调用记录表，存储所有AI服务调用的详细信息';
COMMENT ON TABLE product_ai_analyses IS '商品AI分析结果表，存储商品图片分析的结果和建议';

COMMENT ON COLUMN ai_call_records.provider IS 'AI服务提供商';
COMMENT ON COLUMN ai_call_records.model_name IS '使用的AI模型名称';
COMMENT ON COLUMN ai_call_records.call_type IS 'AI调用类型';
COMMENT ON COLUMN ai_call_records.status IS 'AI调用状态';
COMMENT ON COLUMN ai_call_records.image_urls IS '图片URL列表';
COMMENT ON COLUMN ai_call_records.prompt IS '请求提示词';
COMMENT ON COLUMN ai_call_records.business_context IS '业务上下文信息';
COMMENT ON COLUMN ai_call_records.tokens_used IS '使用的token数量';
COMMENT ON COLUMN ai_call_records.cost IS '调用成本';
COMMENT ON COLUMN ai_call_records.duration_ms IS '调用耗时（毫秒）';

COMMENT ON COLUMN product_ai_analyses.suggested_name IS 'AI建议的商品名称';
COMMENT ON COLUMN product_ai_analyses.suggested_description IS 'AI建议的商品描述';
COMMENT ON COLUMN product_ai_analyses.suggested_attributes IS 'AI建议的商品属性（JSON格式）';
COMMENT ON COLUMN product_ai_analyses.analysis_confidence IS 'AI分析的置信度';
COMMENT ON COLUMN product_ai_analyses.is_applied IS '建议是否已被应用';

COMMIT; 