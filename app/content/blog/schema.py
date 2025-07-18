from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

from app.content.models import ContentStatus


class BlogTranslationCreate(BaseModel):
    """Blog translation creation schema"""
    language_code: str = Field(..., description="Language code", example="zh-CN")
    title: str = Field(..., description="Title", example="Blog Title")
    content: Optional[str] = Field(None, description="Content")
    excerpt: Optional[str] = Field(None, description="Excerpt")
    meta_title: Optional[str] = Field(None, description="Meta title")
    meta_description: Optional[str] = Field(None, description="Meta description")
    meta_keywords: Optional[str] = Field(None, description="Meta keywords")


class BlogTranslationUpdate(BaseModel):
    """Blog translation update schema"""
    title: Optional[str] = Field(None, description="Title")
    content: Optional[str] = Field(None, description="Content")
    excerpt: Optional[str] = Field(None, description="Excerpt")
    meta_title: Optional[str] = Field(None, description="Meta title")
    meta_description: Optional[str] = Field(None, description="Meta description")
    meta_keywords: Optional[str] = Field(None, description="Meta keywords")


class BlogCreate(BaseModel):
    """Blog creation schema"""
    slug: str = Field(..., description="Blog slug", example="my-blog-post")
    title: str = Field(..., description="Blog title", example="My Blog Post")
    content: str = Field(..., description="Blog content")
    excerpt: Optional[str] = Field(None, description="Blog excerpt")
    category_id: Optional[str] = Field(None, description="Category ID")
    featured_image: Optional[str] = Field(None, description="Featured image URL")
    is_featured: bool = Field(False, description="Is featured")
    is_commentable: bool = Field(True, description="Allow comments")
    meta_title: Optional[str] = Field(None, description="Meta title")
    meta_description: Optional[str] = Field(None, description="Meta description")
    meta_keywords: Optional[str] = Field(None, description="Meta keywords")
    published_at: Optional[datetime] = Field(None, description="Publish date")
    tag_ids: Optional[List[str]] = Field([], description="Tag IDs")
    translations: List[BlogTranslationCreate] = Field([], description="Translations")


class BlogUpdate(BaseModel):
    """Blog update schema"""
    slug: Optional[str] = Field(None, description="Blog slug")
    title: Optional[str] = Field(None, description="Blog title")
    content: Optional[str] = Field(None, description="Blog content")
    excerpt: Optional[str] = Field(None, description="Blog excerpt")
    category_id: Optional[str] = Field(None, description="Category ID")
    featured_image: Optional[str] = Field(None, description="Featured image URL")
    is_featured: Optional[bool] = Field(None, description="Is featured")
    is_commentable: Optional[bool] = Field(None, description="Allow comments")
    meta_title: Optional[str] = Field(None, description="Meta title")
    meta_description: Optional[str] = Field(None, description="Meta description")
    meta_keywords: Optional[str] = Field(None, description="Meta keywords")
    published_at: Optional[datetime] = Field(None, description="Publish date")
    status: Optional[ContentStatus] = Field(None, description="Status")
    tag_ids: Optional[List[str]] = Field(None, description="Tag IDs")


class BlogListQuery(BaseModel):
    """Blog list query schema"""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Page size")
    status: Optional[ContentStatus] = Field(None, description="Filter by status")
    category_id: Optional[str] = Field(None, description="Filter by category")
    tag_id: Optional[str] = Field(None, description="Filter by tag")
    is_featured: Optional[bool] = Field(None, description="Filter by featured")
    author_id: Optional[str] = Field(None, description="Filter by author")
    search: Optional[str] = Field(None, description="Search term")


class BlogBatchUpdate(BaseModel):
    """Blog batch update schema"""
    blog_ids: List[str] = Field(..., description="Blog IDs to update")
    status: Optional[ContentStatus] = Field(None, description="New status")
    is_featured: Optional[bool] = Field(None, description="Is featured")
    category_id: Optional[str] = Field(None, description="Category ID")


class BlogTagCreate(BaseModel):
    """Blog tag creation schema"""
    name: str = Field(..., description="Tag name", example="Technology")
    slug: str = Field(..., description="Tag slug", example="technology")
    description: Optional[str] = Field(None, description="Tag description")


class BlogTagUpdate(BaseModel):
    """Blog tag update schema"""
    name: Optional[str] = Field(None, description="Tag name")
    slug: Optional[str] = Field(None, description="Tag slug")
    description: Optional[str] = Field(None, description="Tag description")


class BlogCategoryCreate(BaseModel):
    """Blog category creation schema"""
    name: str = Field(..., description="Category name", example="Technology")
    slug: str = Field(..., description="Category slug", example="technology")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[str] = Field(None, description="Parent category ID")


class BlogCategoryUpdate(BaseModel):
    """Blog category update schema"""
    name: Optional[str] = Field(None, description="Category name")
    slug: Optional[str] = Field(None, description="Category slug")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[str] = Field(None, description="Parent category ID")


class BlogStatistics(BaseModel):
    """Blog statistics schema"""
    total_blogs: int = Field(..., description="Total number of blogs")
    published_blogs: int = Field(..., description="Number of published blogs")
    draft_blogs: int = Field(..., description="Number of draft blogs")
    featured_blogs: int = Field(..., description="Number of featured blogs")
    total_views: int = Field(..., description="Total views")
    total_categories: int = Field(..., description="Total categories")
    total_tags: int = Field(..., description="Total tags")


class BlogResponse(BaseModel):
    """Blog response schema"""
    id: str
    slug: str
    title: str
    content: str
    excerpt: Optional[str]
    category_id: Optional[str]
    featured_image: Optional[str]
    is_featured: bool
    is_commentable: bool
    meta_title: Optional[str]
    meta_description: Optional[str]
    meta_keywords: Optional[str]
    published_at: Optional[datetime]
    status: ContentStatus
    view_count: int
    created_at: datetime
    updated_at: datetime
    author_id: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[str]

    class Config:
        from_attributes = True


class BlogTranslationResponse(BaseModel):
    """Blog translation response schema"""
    id: str
    blog_id: str
    language_code: str
    title: str
    content: str
    excerpt: Optional[str]
    meta_title: Optional[str]
    meta_description: Optional[str]
    meta_keywords: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlogTagResponse(BaseModel):
    """Blog tag response schema"""
    id: str
    name: str
    slug: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlogCategoryResponse(BaseModel):
    """Blog category response schema"""
    id: str
    name: str
    slug: str
    description: Optional[str]
    parent_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlogListResponse(BaseModel):
    """Blog list response schema"""
    items: List[BlogResponse] = Field(..., description="Blog items")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total pages")


class PublicBlogResponse(BaseModel):
    """Public blog response schema"""
    id: str
    slug: str
    title: str
    content: str
    excerpt: Optional[str]
    featured_image: Optional[str]
    is_featured: bool
    meta_title: Optional[str]
    meta_description: Optional[str]
    meta_keywords: Optional[str]
    published_at: Optional[datetime]
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True