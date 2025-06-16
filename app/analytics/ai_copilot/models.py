# -*- coding: utf-8 -*-
"""
AI助手相关数据模型
包含AI调用记录、分析结果等
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class AIServiceProvider(str, enum.Enum):
    """AI服务提供商枚举"""
    ALIBABA_BAILIAN = "ALIBABA_BAILIAN"  # 阿里云百炼
    OPENAI = "OPENAI"                    # OpenAI
    ANTHROPIC = "ANTHROPIC"              # Anthropic
    TENCENT_HUNYUAN = "TENCENT_HUNYUAN"  # 腾讯混元
    BAIDU_QIANFAN = "BAIDU_QIANFAN"      # 百度千帆


class AICallStatus(str, enum.Enum):
    """AI调用状态枚举"""
    PENDING = "PENDING"      # 待处理
    PROCESSING = "PROCESSING" # 处理中
    SUCCESS = "SUCCESS"      # 成功
    FAILED = "FAILED"        # 失败
    TIMEOUT = "TIMEOUT"      # 超时


class AICallType(str, enum.Enum):
    """AI调用类型枚举"""
    PRODUCT_ANALYSIS = "PRODUCT_ANALYSIS"        # 商品分析
    IMAGE_RECOGNITION = "IMAGE_RECOGNITION"      # 图像识别
    TEXT_GENERATION = "TEXT_GENERATION"          # 文本生成
    TRANSLATION = "TRANSLATION"                  # 翻译
    CATEGORY_CLASSIFICATION = "CATEGORY_CLASSIFICATION"  # 分类识别


class AICallRecord(Base):
    """AI调用记录表"""
    __tablename__ = "ai_call_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 基础信息
    provider = Column(Enum(AIServiceProvider), nullable=False, comment="AI服务提供商")
    model_name = Column(String(100), nullable=False, comment="使用的模型名称")
    call_type = Column(Enum(AICallType), nullable=False, comment="调用类型")
    status = Column(Enum(AICallStatus), nullable=False, default=AICallStatus.PENDING, comment="调用状态")
    
    # 请求信息
    request_data = Column(JSON, nullable=True, comment="请求数据")
    image_urls = Column(JSON, nullable=True, comment="图片URL列表")
    prompt = Column(Text, nullable=True, comment="请求提示词")
    
    # 响应信息
    response_data = Column(JSON, nullable=True, comment="响应数据")
    parsed_result = Column(JSON, nullable=True, comment="解析后的结果")
    error_message = Column(Text, nullable=True, comment="错误信息")
    
    # 成本和性能信息
    tokens_used = Column(Integer, nullable=True, comment="使用的token数")
    cost = Column(Float, nullable=True, comment="调用成本")
    duration_ms = Column(Integer, nullable=True, comment="调用耗时(毫秒)")
    
    # 关联信息
    user_id = Column(UUID(as_uuid=True), nullable=True, comment="操作用户ID")
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True, comment="关联的商品ID")
    
    # 业务信息
    business_context = Column(JSON, nullable=True, comment="业务上下文信息")
    confidence_score = Column(Float, nullable=True, comment="置信度分数")
    
    # 时间信息
    started_at = Column(DateTime, nullable=True, comment="开始时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    product = relationship("Product", foreign_keys=[product_id])


class ProductAIAnalysis(Base):
    """商品AI分析结果表"""
    __tablename__ = "product_ai_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_record_id = Column(UUID(as_uuid=True), ForeignKey("ai_call_records.id"), nullable=False, comment="AI调用记录ID")
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True, comment="关联的商品ID")
    
    # 分析结果
    suggested_name = Column(String(255), nullable=True, comment="建议的商品名称")
    suggested_description = Column(Text, nullable=True, comment="建议的商品描述")
    suggested_category_ids = Column(Text, nullable=True, comment="建议的分类ID列表(JSON格式)")
    suggested_attributes = Column(Text, nullable=True, comment="建议的属性信息(JSON格式)")
    suggested_materials = Column(Text, nullable=True, comment="建议的材质信息(JSON格式)")
    suggested_colors = Column(Text, nullable=True, comment="建议的颜色信息(JSON格式)")
    suggested_sizes = Column(Text, nullable=True, comment="建议的尺寸信息(JSON格式)")
    suggested_prices = Column(Text, nullable=True, comment="建议的价格信息(JSON格式)")
    suggested_tags = Column(Text, nullable=True, comment="建议的标签(JSON格式)")
    suggested_scenes = Column(Text, nullable=True, comment="建议的使用场景(JSON格式)")
    suggested_target_groups = Column(Text, nullable=True, comment="建议的目标人群(JSON格式)")
    
    # 分析详情
    analysis_confidence = Column(Float, nullable=True, comment="分析置信度")
    raw_analysis = Column(Text, nullable=True, comment="原始分析结果(JSON格式)")
    
    # 状态信息
    is_applied = Column(Boolean, default=False, comment="是否已应用到商品")
    applied_at = Column(DateTime, nullable=True, comment="应用时间")
    applied_by = Column(UUID(as_uuid=True), nullable=True, comment="应用操作者ID")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    call_record = relationship("AICallRecord", foreign_keys=[call_record_id])
    product = relationship("Product", foreign_keys=[product_id]) 