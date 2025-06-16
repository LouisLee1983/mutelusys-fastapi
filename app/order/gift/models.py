import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, Enum, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class GiftWrapType(str, enum.Enum):
    STANDARD = "standard"          # 标准包装
    PREMIUM = "premium"            # 高级包装
    DELUXE = "deluxe"              # 豪华包装
    FESTIVE = "festive"            # 节日包装
    BIRTHDAY = "birthday"          # 生日包装
    ANNIVERSARY = "anniversary"    # 纪念日包装
    CUSTOM = "custom"              # 自定义包装


class GiftOrder(Base):
    """礼品订单，包含赠言、包装选项、送达日期等特殊属性"""
    __tablename__ = "gift_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # 礼品信息
    sender_name = Column(String(100), nullable=True, comment="送礼人姓名")
    sender_email = Column(String(100), nullable=True, comment="送礼人邮箱")
    sender_phone = Column(String(30), nullable=True, comment="送礼人电话")
    recipient_name = Column(String(100), nullable=False, comment="收礼人姓名")
    recipient_email = Column(String(100), nullable=True, comment="收礼人邮箱")
    recipient_phone = Column(String(30), nullable=True, comment="收礼人电话")
    
    # 礼品卡信息
    gift_message = Column(Text, nullable=True, comment="礼品留言")
    is_gift_message_printed = Column(Boolean, default=True, comment="是否打印礼品留言")
    is_price_hidden = Column(Boolean, default=True, comment="是否隐藏价格")
    
    # 礼品包装信息
    gift_wrap_type = Column(Enum(GiftWrapType), nullable=True, comment="礼品包装类型")
    gift_wrap_color = Column(String(50), nullable=True, comment="礼品包装颜色")
    gift_wrap_note = Column(Text, nullable=True, comment="礼品包装备注")
    gift_wrap_price = Column(Integer, default=0, comment="礼品包装价格")
    
    # 送达安排
    is_scheduled_delivery = Column(Boolean, default=False, comment="是否预约送达")
    scheduled_delivery_date = Column(Date, nullable=True, comment="预约送达日期")
    scheduled_delivery_time_slot = Column(String(50), nullable=True, comment="预约送达时间段")
    delivery_instructions = Column(Text, nullable=True, comment="送达说明")
    
    # 特殊情况
    is_surprise = Column(Boolean, default=False, comment="是否是惊喜")
    is_registry_order = Column(Boolean, default=False, comment="是否礼品登记订单")
    registry_id = Column(UUID(as_uuid=True), ForeignKey("gift_registries.id"), nullable=True)
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    # order = relationship("Order", back_populates="gift_info")  # 暂时注释，避免循环导入
