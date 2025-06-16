import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, JSON, Table
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


# 客户细分与客户的多对多关联表
segment_customer = Table(
    "segment_customer",
    Base.metadata,
    Column("segment_id", UUID(as_uuid=True), ForeignKey("customer_segments.id", ondelete="CASCADE"), primary_key=True),
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class CustomerSegment(Base):
    """客户细分，用于精准营销"""
    __tablename__ = "customer_segments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="细分名称")
    description = Column(Text, nullable=True, comment="细分描述")
    
    # 细分类型和条件
    segment_type = Column(String(50), nullable=False, comment="细分类型，如dynamic, static, hybrid")
    is_dynamic = Column(Boolean, default=True, comment="是否动态细分，根据条件自动更新")
    conditions = Column(JSON, nullable=True, comment="细分条件，用于动态细分")
    
    # 属性和标签
    attributes = Column(JSON, nullable=True, comment="细分属性")
    tags = Column(ARRAY(String), nullable=True, comment="标签")
    
    # 细分状态信息
    is_active = Column(Boolean, default=True, comment="是否激活")
    customer_count = Column(Integer, default=0, comment="客户数量")
    last_updated_at = Column(DateTime, nullable=True, comment="最后更新时间")
    last_campaign_at = Column(DateTime, nullable=True, comment="最后营销活动时间")
    
    # 创建和管理信息
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    customers = relationship("Customer", secondary=segment_customer)
    
    __table_args__ = (
        {},
    )
