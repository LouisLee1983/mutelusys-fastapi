from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class StaticPageType(str, Enum):
    """Static page type enumeration"""
    ABOUT = "about"
    PRIVACY = "privacy"
    TERMS = "terms"
    FAQ = "faq"
    CONTACT = "contact"
    SHIPPING = "shipping"
    REFUND = "refund"

# Placeholder schemas - to be implemented
class PageCreate(BaseModel):
    """Page creation schema"""
    title: str = Field(..., description="Page title")
    content: str = Field(..., description="Page content")
    slug: str = Field(..., description="Page slug")


class PageUpdate(BaseModel):
    """Page update schema"""
    title: Optional[str] = Field(None, description="Page title")
    content: Optional[str] = Field(None, description="Page content")
    slug: Optional[str] = Field(None, description="Page slug")


class PageResponse(BaseModel):
    """Page response schema"""
    id: str
    title: str
    content: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PageListQuery(BaseModel):
    """Page list query schema"""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Page size")
    search: Optional[str] = Field(None, description="Search term")


class PageBatchUpdate(BaseModel):
    """Page batch update schema"""
    page_ids: List[str] = Field(..., description="Page IDs to update")
    is_published: Optional[bool] = Field(None, description="Publish status")


class PageListResponse(BaseModel):
    """Page list response schema"""
    items: List[PageResponse] = Field(..., description="Page items")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total pages")


class PageTranslationCreate(BaseModel):
    """Page translation creation schema"""
    language_code: str = Field(..., description="Language code")
    title: str = Field(..., description="Translated title")
    content: str = Field(..., description="Translated content")
    meta_title: Optional[str] = Field(None, description="Meta title")
    meta_description: Optional[str] = Field(None, description="Meta description")


class PageTranslationUpdate(BaseModel):
    """Page translation update schema"""
    title: Optional[str] = Field(None, description="Translated title")
    content: Optional[str] = Field(None, description="Translated content")
    meta_title: Optional[str] = Field(None, description="Meta title")
    meta_description: Optional[str] = Field(None, description="Meta description")


class PageTranslationResponse(BaseModel):
    """Page translation response schema"""
    id: str
    page_id: str
    language_code: str
    title: str
    content: str
    meta_title: Optional[str]
    meta_description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PageStatistics(BaseModel):
    """Page statistics schema"""
    total_pages: int = Field(..., description="Total number of pages")
    published_pages: int = Field(..., description="Number of published pages")
    draft_pages: int = Field(..., description="Number of draft pages")
    total_views: int = Field(..., description="Total page views")


class PublicPageResponse(BaseModel):
    """Public page response schema"""
    id: str
    title: str
    content: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True