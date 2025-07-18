from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

from app.content.promotion.models import PromotionContentType
from app.content.models import ContentStatus


class PromotionContentTranslationCreate(BaseModel):
    """促销内容翻译创建模型"""
    language_code: str = Field(..., description="语言代码", example="zh-CN")
    title: str = Field(..., description="内容标题", example="春节大促销")
    short_text: Optional[str] = Field(None, description="短文本", example="8折起")
    content: Optional[str] = Field(None, description="主要内容")
    button_text: Optional[str] = Field(None, description="按钮文字", example="立即抢购")


class PromotionContentTranslationUpdate(BaseModel):
    """促销内容翻译更新模型"""
    title: Optional[str] = Field(None, description="内容标题")
    short_text: Optional[str] = Field(None, description="短文本")
    content: Optional[str] = Field(None, description="主要内容")
    button_text: Optional[str] = Field(None, description="按钮文字")


class PromotionContentTranslationResponse(BaseModel):
    """促销内容翻译响应模型"""
    id: str
    language_code: str
    title: str
    short_text: Optional[str] = None
    content: Optional[str] = None
    button_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PromotionContentCreate(BaseModel):
    """促销内容创建模型"""
    title: str = Field(..., description="内容标题", example="春节促销横幅")
    content_type: PromotionContentType = Field(..., description="内容类型")
    promotion_id: Optional[str] = Field(None, description="关联的促销活动ID")
    
    # 内容信息
    short_text: Optional[str] = Field(None, description="短文本", example="限时8折")
    content: Optional[str] = Field(None, description="主要内容")
    button_text: Optional[str] = Field(None, description="按钮文字", example="立即购买")
    link_url: Optional[str] = Field(None, description="链接URL")
    
    # 显示设置
    background_color: Optional[str] = Field(None, description="背景颜色", example="#FF6B6B")
    text_color: Optional[str] = Field(None, description="文字颜色", example="#FFFFFF")
    font_size: Optional[str] = Field(None, description="字体大小", example="16px")
    position: Optional[str] = Field(None, description="显示位置", example="top-banner")
    
    # 时间设置
    start_date: Optional[datetime] = Field(None, description="开始时间")
    end_date: Optional[datetime] = Field(None, description="结束时间")
    sort_order: int = Field(0, description="排序顺序")
    
    # 目标设置
    target_pages: Optional[List[str]] = Field(None, description="目标页面")
    target_countries: Optional[List[str]] = Field(None, description="目标国家")
    target_languages: Optional[List[str]] = Field(None, description="目标语言")
    
    # 额外设置
    additional_settings: Optional[Dict[str, Any]] = Field(None, description="额外设置")
    
    # 多语言翻译
    translations: List[PromotionContentTranslationCreate] = Field([], description="多语言翻译")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('结束时间必须晚于开始时间')
        return v


class PromotionContentUpdate(BaseModel):
    """促销内容更新模型"""
    title: Optional[str] = Field(None, description="内容标题")
    content_type: Optional[PromotionContentType] = Field(None, description="内容类型")
    promotion_id: Optional[str] = Field(None, description="关联的促销活动ID")
    
    # 内容信息
    short_text: Optional[str] = Field(None, description="短文本")
    content: Optional[str] = Field(None, description="主要内容")
    button_text: Optional[str] = Field(None, description="按钮文字")
    link_url: Optional[str] = Field(None, description="链接URL")
    
    # 显示设置
    background_color: Optional[str] = Field(None, description="背景颜色")
    text_color: Optional[str] = Field(None, description="文字颜色")
    font_size: Optional[str] = Field(None, description="字体大小")
    position: Optional[str] = Field(None, description="显示位置")
    
    # 状态和时间
    status: Optional[ContentStatus] = Field(None, description="内容状态")
    start_date: Optional[datetime] = Field(None, description="开始时间")
    end_date: Optional[datetime] = Field(None, description="结束时间")
    sort_order: Optional[int] = Field(None, description="排序顺序")
    
    # 目标设置
    target_pages: Optional[List[str]] = Field(None, description="目标页面")
    target_countries: Optional[List[str]] = Field(None, description="目标国家")
    target_languages: Optional[List[str]] = Field(None, description="目标语言")
    
    # 额外设置
    additional_settings: Optional[Dict[str, Any]] = Field(None, description="额外设置")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('结束时间必须晚于开始时间')
        return v


class PromotionContentResponse(BaseModel):
    """促销内容响应模型"""
    id: str
    title: str
    content_type: PromotionContentType
    promotion_id: Optional[str] = None
    
    # 内容信息
    short_text: Optional[str] = None
    content: Optional[str] = None
    button_text: Optional[str] = None
    link_url: Optional[str] = None
    
    # 显示设置
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    font_size: Optional[str] = None
    position: Optional[str] = None
    
    # 状态和时间
    status: ContentStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_order: int
    
    # 目标设置
    target_pages: Optional[List[str]] = None
    target_countries: Optional[List[str]] = None
    target_languages: Optional[List[str]] = None
    
    # 额外设置
    additional_settings: Optional[Dict[str, Any]] = None
    
    # 多语言翻译
    translations: List[PromotionContentTranslationResponse] = []
    
    # 时间戳
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PromotionContentListQuery(BaseModel):
    """促销内容列表查询参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    content_type: Optional[PromotionContentType] = Field(None, description="内容类型筛选")
    status: Optional[ContentStatus] = Field(None, description="状态筛选")
    position: Optional[str] = Field(None, description="位置筛选")
    promotion_id: Optional[str] = Field(None, description="促销活动ID筛选")
    search: Optional[str] = Field(None, description="搜索关键词")


class PromotionContentListResponse(BaseModel):
    """促销内容列表响应模型"""
    items: List[PromotionContentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class PromotionContentBatchUpdate(BaseModel):
    """促销内容批量更新模型"""
    content_ids: List[str] = Field(..., description="内容ID列表")
    status: Optional[ContentStatus] = Field(None, description="状态")
    sort_orders: Optional[Dict[str, int]] = Field(None, description="排序顺序映射")


class PublicPromotionContentResponse(BaseModel):
    """公开促销内容响应模型（前端使用）"""
    id: str
    title: str
    content_type: PromotionContentType
    short_text: Optional[str] = None
    content: Optional[str] = None
    button_text: Optional[str] = None
    link_url: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    font_size: Optional[str] = None
    position: Optional[str] = None
    sort_order: int
    additional_settings: Optional[Dict[str, Any]] = None
    translations: List[PromotionContentTranslationResponse] = []

    class Config:
        from_attributes = True


class PromotionTextTemplateCreate(BaseModel):
    """促销文本模板创建模型"""
    name: str = Field(..., description="模板名称", example="春节促销模板")
    content_type: PromotionContentType = Field(..., description="内容类型")
    template_title: str = Field(..., description="模板标题", example="{promotion_name}限时特惠")
    template_content: Optional[str] = Field(None, description="模板内容")
    template_variables: Optional[Dict[str, Any]] = Field(None, description="模板变量定义")
    default_styles: Optional[Dict[str, Any]] = Field(None, description="默认样式设置")


class PromotionTextTemplateUpdate(BaseModel):
    """促销文本模板更新模型"""
    name: Optional[str] = Field(None, description="模板名称")
    template_title: Optional[str] = Field(None, description="模板标题")
    template_content: Optional[str] = Field(None, description="模板内容")
    template_variables: Optional[Dict[str, Any]] = Field(None, description="模板变量定义")
    default_styles: Optional[Dict[str, Any]] = Field(None, description="默认样式设置")


class PromotionTextTemplateResponse(BaseModel):
    """促销文本模板响应模型"""
    id: str
    name: str
    content_type: PromotionContentType
    template_title: str
    template_content: Optional[str] = None
    template_variables: Optional[Dict[str, Any]] = None
    default_styles: Optional[Dict[str, Any]] = None
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True