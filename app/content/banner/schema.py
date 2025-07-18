from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

from app.content.banner.models import BannerType
from app.content.models import ContentStatus


class BannerTranslationCreate(BaseModel):
    """*E���!�"""
    language_code: str = Field(..., description="� �", example="zh-CN")
    title: str = Field(..., description="*E�", example="�t� ;�")
    subtitle: Optional[str] = Field(None, description="o�", example="h:8�w")
    description: Optional[str] = Field(None, description="���,")
    button_text: Optional[str] = Field(None, description="	��,", example="�s�")
    alt_text: Optional[str] = Field(None, description="�G��,")


class BannerTranslationUpdate(BaseModel):
    """*E����!�"""
    title: Optional[str] = Field(None, description="*E�")
    subtitle: Optional[str] = Field(None, description="o�")
    description: Optional[str] = Field(None, description="���,")
    button_text: Optional[str] = Field(None, description="	��,")
    alt_text: Optional[str] = Field(None, description="�G��,")


class BannerTranslationResponse(BaseModel):
    """*E��͔!�"""
    id: str
    language_code: str
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    button_text: Optional[str] = None
    alt_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BannerCreate(BaseModel):
    """*E�!�"""
    title: str = Field(..., description="*E�", example="%�� *E")
    type: BannerType = Field(..., description="*E{�")
    image_url: str = Field(..., description="�GURL", example="/static/images/banner1.jpg")
    mobile_image_url: Optional[str] = Field(None, description="����GURL")
    link_url: Optional[str] = Field(None, description="��URL", example="/category/amulets")
    position: Optional[str] = Field(None, description="Mn�", example="home-top")
    start_date: Optional[datetime] = Field(None, description=" ��")
    end_date: Optional[datetime] = Field(None, description="�_�")
    sort_order: int = Field(0, description="��z�")
    alt_text: Optional[str] = Field(None, description="�G��,")
    open_in_new_tab: bool = Field(False, description="/&(�~uS ")
    additional_css: Optional[str] = Field(None, description="�CSS7")
    additional_info: Optional[Dict[str, Any]] = Field(None, description="��o")
    translations: List[BannerTranslationCreate] = Field([], description="� ��")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('�_��{Z� ��')
        return v


class BannerUpdate(BaseModel):
    """*E��!�"""
    title: Optional[str] = Field(None, description="*E�")
    type: Optional[BannerType] = Field(None, description="*E{�")
    image_url: Optional[str] = Field(None, description="�GURL")
    mobile_image_url: Optional[str] = Field(None, description="����GURL")
    link_url: Optional[str] = Field(None, description="��URL")
    position: Optional[str] = Field(None, description="Mn�")
    status: Optional[ContentStatus] = Field(None, description="*E�")
    start_date: Optional[datetime] = Field(None, description=" ��")
    end_date: Optional[datetime] = Field(None, description="�_�")
    sort_order: Optional[int] = Field(None, description="��z�")
    alt_text: Optional[str] = Field(None, description="�G��,")
    open_in_new_tab: Optional[bool] = Field(None, description="/&(�~uS ")
    additional_css: Optional[str] = Field(None, description="�CSS7")
    additional_info: Optional[Dict[str, Any]] = Field(None, description="��o")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('�_��{Z� ��')
        return v


class BannerResponse(BaseModel):
    """*E͔!�"""
    id: str
    title: str
    type: BannerType
    image_url: str
    mobile_image_url: Optional[str] = None
    link_url: Optional[str] = None
    position: Optional[str] = None
    status: ContentStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_order: int
    alt_text: Optional[str] = None
    open_in_new_tab: bool
    additional_css: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    translations: List[BannerTranslationResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BannerListQuery(BaseModel):
    """*Eh���p"""
    page: int = Field(1, ge=1, description="u")
    page_size: int = Field(20, ge=1, le=100, description="�up�")
    type: Optional[BannerType] = Field(None, description="*E{�[	")
    status: Optional[ContentStatus] = Field(None, description="�[	")
    position: Optional[str] = Field(None, description="Mn[	")
    search: Optional[str] = Field(None, description=""s.�")


class BannerListResponse(BaseModel):
    """*Eh͔!�"""
    items: List[BannerResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class BannerBatchUpdate(BaseModel):
    """*Ey���!�"""
    banner_ids: List[str] = Field(..., description="*EIDh")
    status: Optional[ContentStatus] = Field(None, description="�")
    sort_orders: Optional[Dict[str, int]] = Field(None, description="��z� ")


class BannerPositionResponse(BaseModel):
    """*EMn͔!�"""
    position: str
    banners: List[BannerResponse]


class PublicBannerResponse(BaseModel):
    """l *E͔!�M�(	"""
    id: str
    title: str
    type: BannerType
    image_url: str
    mobile_image_url: Optional[str] = None
    link_url: Optional[str] = None
    position: Optional[str] = None
    sort_order: int
    alt_text: Optional[str] = None
    open_in_new_tab: bool
    additional_css: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    translations: List[BannerTranslationResponse] = []

    class Config:
        from_attributes = True