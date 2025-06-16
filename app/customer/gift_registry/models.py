import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, JSON, Date, Enum, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class RegistryType(str, enum.Enum):
    WEDDING = "wedding"          # 婚礼
    BABY_SHOWER = "baby_shower"  # 迎婴派对
    BIRTHDAY = "birthday"        # 生日
    ANNIVERSARY = "anniversary"  # 周年纪念
    HOUSEWARMING = "housewarming"  # 乔迁
    GRADUATION = "graduation"    # 毕业
    OTHER = "other"              # 其他


class RegistryStatus(str, enum.Enum):
    ACTIVE = "active"            # 活跃
    INACTIVE = "inactive"        # 不活跃
    COMPLETED = "completed"      # 已完成
    EXPIRED = "expired"          # 已过期
    ARCHIVED = "archived"        # 已归档


class GiftRegistry(Base):
    """礼品登记，用户可创建愿望清单供他人购买礼物"""
    __tablename__ = "gift_registries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False, comment="登记标题")
    description = Column(Text, nullable=True, comment="登记描述")
    registry_type = Column(Enum(RegistryType), nullable=False, comment="登记类型")
    status = Column(Enum(RegistryStatus), default=RegistryStatus.ACTIVE, nullable=False, comment="状态")
    
    # 日期信息
    event_date = Column(Date, nullable=True, comment="活动日期")
    end_date = Column(Date, nullable=True, comment="结束日期")
    
    # 分享与隐私设置
    is_public = Column(Boolean, default=False, comment="是否公开")
    access_code = Column(String(20), nullable=True, comment="访问代码，用于非公开登记")
    sharing_url = Column(String(255), nullable=True, comment="分享URL")
    
    # 额外信息
    message_to_guests = Column(Text, nullable=True, comment="给宾客的留言")
    co_registrant_name = Column(String(100), nullable=True, comment="共同登记人姓名")
    shipping_address_id = Column(UUID(as_uuid=True), ForeignKey("customer_addresses.id"), nullable=True)
    custom_theme = Column(String(50), nullable=True, comment="自定义主题")
    thank_you_message_template = Column(Text, nullable=True, comment="感谢信息模板")
    
    # 统计信息
    total_items = Column(Integer, default=0, comment="总项目数")
    total_purchased = Column(Integer, default=0, comment="已购买项目数")
    views_count = Column(Integer, default=0, comment="查看次数")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    customer = relationship("Customer")
    shipping_address = relationship("CustomerAddress")
    items = relationship("GiftRegistryItem", back_populates="registry", cascade="all, delete-orphan")


class GiftRegistryItem(Base):
    """礼品登记项目，包含商品、数量、优先级等信息"""
    __tablename__ = "gift_registry_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registry_id = Column(UUID(as_uuid=True), ForeignKey("gift_registries.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    sku_id = Column(UUID(as_uuid=True), ForeignKey("product_skus.id"), nullable=True)
    
    # 商品信息（快照）
    name = Column(String(255), nullable=False, comment="商品名称")
    sku_code = Column(String(50), nullable=True, comment="SKU编码")
    image_url = Column(String(255), nullable=True, comment="商品图片URL")
    unit_price = Column(Numeric(10, 2), nullable=False, comment="单价")
    
    # 数量和状态
    desired_quantity = Column(Integer, nullable=False, default=1, comment="期望数量")
    purchased_quantity = Column(Integer, default=0, comment="已购买数量")
    remaining_quantity = Column(Integer, default=0, comment="剩余数量")
    priority = Column(Integer, default=0, comment="优先级，0-最高")
    
    # 其他信息
    notes = Column(Text, nullable=True, comment="备注")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_private = Column(Boolean, default=False, comment="是否私密，不显示给其他人")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    registry = relationship("GiftRegistry", back_populates="items")
    product = relationship("Product")
    sku = relationship("ProductSku")
    purchases = relationship("GiftRegistryPurchase", back_populates="registry_item", cascade="all, delete-orphan")


class GiftRegistryPurchase(Base):
    """礼品登记购买记录表"""
    __tablename__ = "gift_registry_purchases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registry_item_id = Column(UUID(as_uuid=True), ForeignKey("gift_registry_items.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey("order_items.id"), nullable=True)
    
    # 购买信息
    purchaser_name = Column(String(100), nullable=True, comment="购买人姓名")
    purchaser_email = Column(String(255), nullable=True, comment="购买人邮箱")
    quantity = Column(Integer, default=1, nullable=False, comment="购买数量")
    message = Column(Text, nullable=True, comment="留言")
    is_anonymous = Column(Boolean, default=False, comment="是否匿名购买")
    
    # 状态信息
    status = Column(String(50), default="pending", nullable=False, comment="状态：pending, fulfilled, cancelled")
    is_thank_you_sent = Column(Boolean, default=False, comment="是否已发送感谢信息")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    registry_item = relationship("GiftRegistryItem", back_populates="purchases")
    order = relationship("Order")
    # order_item = relationship("OrderItem", back_populates="registry_purchase")  # 暂时注释，避免循环导入
