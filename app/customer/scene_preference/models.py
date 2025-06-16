import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class CustomerScenePreference(Base):
    """场景偏好，记录用户对不同生活场景产品的兴趣"""
    __tablename__ = "customer_scene_preference_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("product_scenes.id", ondelete="CASCADE"), nullable=False)
    
    # 偏好相关信息
    preference_level = Column(Integer, default=1, comment="偏好程度，1-5级")
    confidence_score = Column(Float, default=0.0, comment="置信度分数，0-1之间")
    engagement_count = Column(Integer, default=0, comment="互动次数")
    last_engagement_at = Column(DateTime, nullable=True, comment="最后互动时间")
    notes = Column(Text, nullable=True, comment="备注")
    source = Column(String(50), nullable=True, comment="偏好来源，如browse, survey, purchase等")
    
    # 扩展信息
    frequency_of_use = Column(String(50), nullable=True, comment="使用频率，如daily, weekly, monthly")
    expertise_level = Column(String(50), nullable=True, comment="专业程度，如beginner, intermediate, expert")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    customer = relationship("Customer", backref="scene_preference_details")
    scene = relationship("ProductScene")
    
    # 联合唯一约束，确保每个客户对每个场景只有一条详细记录
    __table_args__ = (
        {},
    )
