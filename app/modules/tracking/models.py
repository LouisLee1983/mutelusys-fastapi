from sqlalchemy import Column, Integer, String, DateTime, Text, DECIMAL, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class TrackingCampaign(Base):
    """推广活动表"""
    __tablename__ = "tracking_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_code = Column(String(50), unique=True, index=True, nullable=False)
    campaign_name = Column(String(200), nullable=False)
    platform = Column(String(50), nullable=False)  # facebook/instagram/tiktok/google
    advertiser_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    budget = Column(DECIMAL(10, 2), nullable=True)
    status = Column(String(20), default="active")  # active/paused/ended
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    advertiser = relationship("User", backref="campaigns")
    product = relationship("Product", backref="campaigns")
    visits = relationship("TrackingVisit", back_populates="campaign")


class TrackingVisit(Base):
    """访问记录表"""
    __tablename__ = "tracking_visits"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("tracking_campaigns.id"), nullable=True)
    visitor_id = Column(String(100), index=True)  # Cookie/Session ID
    user_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    source_url = Column(Text)
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_content = Column(String(100))
    utm_term = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    landing_page = Column(String(500))
    referrer = Column(String(500))
    visit_time = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100), index=True)
    
    # Relationships
    campaign = relationship("TrackingCampaign", back_populates="visits")
    user = relationship("Customer", backref="tracking_visits")
    behaviors = relationship("TrackingBehavior", back_populates="visit")


class TrackingBehavior(Base):
    """用户行为记录表"""
    __tablename__ = "tracking_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(Integer, ForeignKey("tracking_visits.id"))
    user_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    event_type = Column(String(50), nullable=False)  # view_product/add_cart/checkout/purchase
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    page_url = Column(String(500))
    duration = Column(Integer)  # 停留时长(秒)
    event_data = Column(JSONB)  # 额外事件数据
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    visit = relationship("TrackingVisit", back_populates="behaviors")
    user = relationship("Customer", backref="tracking_behaviors")
    product = relationship("Product", backref="tracking_behaviors")


class ProductViewHistory(Base):
    """商品浏览历史表"""
    __tablename__ = "product_view_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    session_id = Column(String(100), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    view_count = Column(Integer, default=1)
    last_viewed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("Customer", backref="view_history")
    product = relationship("Product", backref="view_history")