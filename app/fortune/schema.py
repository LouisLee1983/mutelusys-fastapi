from typing import Optional, List, Dict, Any, Generic, TypeVar
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from app.fortune.models import ReadingType

T = TypeVar('T')


# 八字命理请求
class BaziAnalysisRequest(BaseModel):
    customer_id: UUID = Field(..., description="客户ID")
    birth_year: int = Field(..., ge=1900, le=2030, description="出生年份")
    birth_month: int = Field(..., ge=1, le=12, description="出生月份")
    birth_day: int = Field(..., ge=1, le=31, description="出生日期")
    birth_hour: Optional[int] = Field(None, ge=0, le=23, description="出生时辰（0-23）")
    gender: str = Field(..., pattern="^(male|female)$", description="性别")
    birth_location: Optional[str] = Field(None, max_length=100, description="出生地点")

    @validator('birth_day')
    def validate_birth_day(cls, v, values):
        if 'birth_month' in values:
            month = values['birth_month']
            if month in [4, 6, 9, 11] and v > 30:
                raise ValueError('该月份最多30天')
            elif month == 2 and v > 29:
                raise ValueError('2月最多29天')
        return v


# 塔罗牌分析请求
class TarotAnalysisRequest(BaseModel):
    customer_id: UUID = Field(..., description="客户ID")
    selected_cards: List[int] = Field(..., min_items=1, max_items=3, description="选择的塔罗牌编号")
    question_type: str = Field(..., description="占卜问题类型：love/career/health/general")
    
    @validator('selected_cards')
    def validate_cards(cls, v):
        if not all(1 <= card <= 78 for card in v):
            raise ValueError('塔罗牌编号必须在1-78之间')
        return v


# 算命档案响应
class FortuneProfileResponse(BaseModel):
    id: str
    customer_id: str
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: Optional[int]
    gender: str
    birth_location: Optional[str]
    bazi_analysis: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 算命记录响应
class FortuneReadingResponse(BaseModel):
    id: str
    customer_id: str
    profile_id: Optional[str]
    reading_type: ReadingType
    input_data: Dict[str, Any]
    ai_analysis: str
    recommended_products: Optional[List[Dict[str, Any]]]
    reading_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# 分析结果响应
class AnalysisResultResponse(BaseModel):
    reading_id: str
    analysis: str
    summary: str
    recommendations: List[str]
    recommended_products: Optional[List[Dict[str, Any]]]
    created_at: datetime


# 算命历史列表响应
class FortuneHistoryResponse(BaseModel):
    readings: List[FortuneReadingResponse]
    total_count: int
    has_profile: bool
    profile: Optional[FortuneProfileResponse]


# 算命档案创建请求
class FortuneProfileCreateRequest(BaseModel):
    customer_id: UUID = Field(..., description="客户ID")
    birth_year: int = Field(..., ge=1900, le=2030, description="出生年份")
    birth_month: int = Field(..., ge=1, le=12, description="出生月份")
    birth_day: int = Field(..., ge=1, le=31, description="出生日期")
    birth_hour: Optional[int] = Field(None, ge=0, le=23, description="出生时辰（0-23）")
    gender: str = Field(..., pattern="^(male|female)$", description="性别")
    birth_location: Optional[str] = Field(None, max_length=100, description="出生地点")
    timezone: Optional[str] = Field(None, description="时区")

    @validator('birth_day')
    def validate_birth_day(cls, v, values):
        if 'birth_month' in values:
            month = values['birth_month']
            if month in [4, 6, 9, 11] and v > 30:
                raise ValueError('该月份最多30天')
            elif month == 2 and v > 29:
                raise ValueError('2月最多29天')
        return v


# 算命档案更新请求
class FortuneProfileUpdateRequest(BaseModel):
    birth_year: Optional[int] = Field(None, ge=1900, le=2030, description="出生年份")
    birth_month: Optional[int] = Field(None, ge=1, le=12, description="出生月份")
    birth_day: Optional[int] = Field(None, ge=1, le=31, description="出生日期")
    birth_hour: Optional[int] = Field(None, ge=0, le=23, description="出生时辰（0-23）")
    gender: Optional[str] = Field(None, pattern="^(male|female)$", description="性别")
    birth_location: Optional[str] = Field(None, max_length=100, description="出生地点")
    timezone: Optional[str] = Field(None, description="时区")

    @validator('birth_day')
    def validate_birth_day(cls, v, values):
        if v and 'birth_month' in values and values['birth_month']:
            month = values['birth_month']
            if month in [4, 6, 9, 11] and v > 30:
                raise ValueError('该月份最多30天')
            elif month == 2 and v > 29:
                raise ValueError('2月最多29天')
        return v


# 算命统计分析响应
class FortuneAnalyticsResponse(BaseModel):
    total_profiles: int = Field(..., description="总档案数")
    total_readings: int = Field(..., description="总算命记录数")
    bazi_readings: int = Field(..., description="八字算命记录数")
    tarot_readings: int = Field(..., description="塔罗算命记录数")
    popular_questions: List[Dict[str, Any]] = Field(..., description="热门问题统计")
    user_engagement: Dict[str, Any] = Field(..., description="用户参与度统计")


# 分页响应
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T] = Field(..., description="数据项列表")
    total: int = Field(..., description="总数据量")
    page: int = Field(..., description="当前页码")
    limit: int = Field(..., description="每页数据量")
    pages: int = Field(..., description="总页数")