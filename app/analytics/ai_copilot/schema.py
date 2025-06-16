# -*- coding: utf-8 -*-
"""
AI助手相关数据结构定义
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from app.analytics.ai_copilot.models import AIServiceProvider, AICallStatus, AICallType


class AICallRecordBase(BaseModel):
    """AI调用记录基础模型"""
    provider: AIServiceProvider = Field(..., description="AI服务提供商")
    model_name: str = Field(..., description="使用的模型名称")
    call_type: AICallType = Field(..., description="调用类型")
    image_urls: Optional[List[str]] = Field(None, description="图片URL列表")
    prompt: Optional[str] = Field(None, description="请求提示词")
    business_context: Optional[Dict[str, Any]] = Field(None, description="业务上下文信息")


class AICallRecordCreate(AICallRecordBase):
    """创建AI调用记录"""
    pass


class AICallRecord(AICallRecordBase):
    """AI调用记录响应模型"""
    id: UUID
    status: AICallStatus
    request_data: Optional[Dict[str, Any]] = None
    response_data: Optional[Dict[str, Any]] = None
    parsed_result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    duration_ms: Optional[int] = None
    user_id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    confidence_score: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductAIAnalysisBase(BaseModel):
    """商品AI分析基础模型"""
    suggested_name: Optional[str] = Field(None, description="建议的商品名称")
    suggested_description: Optional[str] = Field(None, description="建议的商品描述")
    suggested_category_ids: Optional[List[UUID]] = Field(None, description="建议的分类ID列表")
    suggested_attributes: Optional[Dict[str, Any]] = Field(None, description="建议的属性信息")
    suggested_materials: Optional[List[str]] = Field(None, description="建议的材质信息")
    suggested_colors: Optional[List[str]] = Field(None, description="建议的颜色信息")
    suggested_sizes: Optional[List[str]] = Field(None, description="建议的尺寸信息")
    suggested_prices: Optional[Dict[str, Any]] = Field(None, description="建议的价格信息")
    suggested_tags: Optional[List[str]] = Field(None, description="建议的标签")
    suggested_scenes: Optional[List[str]] = Field(None, description="建议的使用场景")
    suggested_target_groups: Optional[List[str]] = Field(None, description="建议的目标人群")
    analysis_confidence: Optional[float] = Field(None, description="分析置信度")


class ProductAIAnalysisCreate(ProductAIAnalysisBase):
    """创建商品AI分析"""
    call_record_id: UUID = Field(..., description="AI调用记录ID")
    raw_analysis: Optional[Dict[str, Any]] = Field(None, description="原始分析结果")


class ProductAIAnalysis(ProductAIAnalysisBase):
    """商品AI分析响应模型"""
    id: UUID
    call_record_id: UUID
    product_id: Optional[UUID] = None
    raw_analysis: Optional[Dict[str, Any]] = None
    is_applied: bool = False
    applied_at: Optional[datetime] = None
    applied_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_model(cls, db_obj):
        """从数据库模型转换，处理JSON字符串字段"""
        import json
        
        if not db_obj:
            raise ValueError("数据库对象不能为空")
        
        data = {}
        
        # 确保从数据库对象中正确提取数据
        if hasattr(db_obj, '__dict__'):
            obj_dict = db_obj.__dict__
        else:
            # 如果不是SQLAlchemy对象，可能是字典
            obj_dict = db_obj if isinstance(db_obj, dict) else {}
        
        for field_name, field_value in obj_dict.items():
            if field_name.startswith('_'):
                continue
                
            # 处理JSON字符串字段，转换回Python对象
            if field_name in [
                'suggested_category_ids', 'suggested_attributes', 'suggested_materials',
                'suggested_colors', 'suggested_sizes', 'suggested_prices',
                'suggested_tags', 'suggested_scenes', 'suggested_target_groups',
                'raw_analysis'
            ]:
                if field_value and isinstance(field_value, str):
                    try:
                        data[field_name] = json.loads(field_value)
                    except (json.JSONDecodeError, TypeError):
                        data[field_name] = field_value
                else:
                    data[field_name] = field_value
            else:
                data[field_name] = field_value
        
        # 确保必需字段存在
        if 'id' not in data:
            raise ValueError("缺少必需字段: id")
        if 'call_record_id' not in data:
            raise ValueError("缺少必需字段: call_record_id")
        if 'created_at' not in data:
            raise ValueError("缺少必需字段: created_at")
        if 'updated_at' not in data:
            raise ValueError("缺少必需字段: updated_at")
        
        return cls(**data)


class ProductAnalysisRequest(BaseModel):
    """商品分析请求"""
    image_urls: List[str] = Field(..., description="商品图片URL列表")
    additional_context: Optional[str] = Field(None, description="额外上下文信息")
    language: Optional[str] = Field("zh-CN", description="分析语言")


class ProductAnalysisResponse(BaseModel):
    """商品分析响应"""
    call_record_id: UUID = Field(..., description="调用记录ID")
    analysis_id: UUID = Field(..., description="分析结果ID")
    analysis: ProductAIAnalysis = Field(..., description="分析结果")
    suggestions: Dict[str, Any] = Field(..., description="建议信息")


class ApplyAnalysisRequest(BaseModel):
    """应用分析结果请求"""
    analysis_id: UUID = Field(..., description="分析结果ID")
    selected_suggestions: Dict[str, Any] = Field(..., description="选择的建议项")
    create_product: bool = Field(True, description="是否创建新商品")
    product_id: Optional[UUID] = Field(None, description="更新现有商品ID（如果不创建新商品）") 