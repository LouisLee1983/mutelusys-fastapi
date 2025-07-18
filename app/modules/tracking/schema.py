from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID


# Campaign Schemas
class CampaignBase(BaseModel):
    campaign_code: str = Field(..., max_length=50)
    campaign_name: str = Field(..., max_length=200)
    platform: str = Field(..., max_length=50)
    advertiser_id: Optional[UUID] = None
    product_id: Optional[int] = None
    budget: Optional[Decimal] = None
    status: str = Field(default="active", max_length=20)


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    campaign_name: Optional[str] = None
    platform: Optional[str] = None
    product_id: Optional[int] = None
    budget: Optional[Decimal] = None
    status: Optional[str] = None


class CampaignInDB(CampaignBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Visit Tracking Schemas
class TrackingVisitBase(BaseModel):
    visitor_id: str
    session_id: str
    source_url: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    landing_page: Optional[str] = None
    referrer: Optional[str] = None


class TrackingVisitCreate(TrackingVisitBase):
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class TrackingVisitInDB(TrackingVisitBase):
    id: int
    campaign_id: Optional[int] = None
    user_id: Optional[int] = None
    visit_time: datetime
    
    class Config:
        from_attributes = True


# Behavior Tracking Schemas
class TrackingBehaviorBase(BaseModel):
    event_type: str
    page_url: Optional[str] = None
    duration: Optional[int] = None
    event_data: Optional[Dict[str, Any]] = None


class TrackingBehaviorCreate(TrackingBehaviorBase):
    visit_id: Optional[int] = None
    session_id: Optional[str] = None
    product_id: Optional[int] = None


class TrackingBehaviorInDB(TrackingBehaviorBase):
    id: int
    visit_id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Product View History Schemas
class ProductViewBase(BaseModel):
    product_id: int
    session_id: str


class ProductViewCreate(ProductViewBase):
    pass


class ProductViewInDB(ProductViewBase):
    id: int
    user_id: Optional[int] = None
    view_count: int
    last_viewed_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecentlyViewedProduct(BaseModel):
    product_id: int
    product_name: str
    product_image: Optional[str] = None
    price: Decimal
    view_count: int
    last_viewed_at: datetime


# Analytics Response Schemas
class CampaignStats(BaseModel):
    campaign_id: int
    campaign_code: str
    campaign_name: str
    platform: str
    total_visits: int
    unique_visitors: int
    registered_users: int
    total_purchases: int
    conversion_rate: float
    total_revenue: Decimal
    roi: Optional[float] = None


class VisitorJourney(BaseModel):
    visit_id: int
    visitor_id: str
    user_id: Optional[int] = None
    source: str
    landing_time: datetime
    total_duration: int
    pages_viewed: int
    products_viewed: List[int]
    added_to_cart: bool
    completed_purchase: bool
    purchase_value: Optional[Decimal] = None