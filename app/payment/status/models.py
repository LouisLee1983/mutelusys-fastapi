import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class PaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"              # 等待处理
    PROCESSING = "processing"        # 处理中
    AUTHORIZED = "authorized"        # 已授权
    COMPLETED = "completed"          # 已完成
    CANCELLED = "cancelled"          # 已取消
    DECLINED = "declined"            # 已拒绝
    REFUNDED = "refunded"            # 已退款
    PARTIALLY_REFUNDED = "partially_refunded"  # 部分退款
    FAILED = "failed"                # 失败
    EXPIRED = "expired"              # 已过期
    WAITING = "waiting"              # 等待中(如银行转账等)


class PaymentStatus(Base):
    """支付状态枚举表"""
    __tablename__ = "payment_statuses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(Enum(PaymentStatusEnum), nullable=False, unique=True, comment="状态代码")
    name = Column(String(100), nullable=False, comment="状态名称")
    description = Column(Text, nullable=True, comment="状态描述")
    
    # 显示设置
    color = Column(String(20), nullable=True, comment="状态颜色代码")
    icon = Column(String(50), nullable=True, comment="状态图标")
    
    # 工作流设置
    is_final = Column(Boolean, default=False, comment="是否终态")
    allowed_next_statuses = Column(JSON, nullable=True, comment="允许的下一个状态")
    requires_approval = Column(Boolean, default=False, comment="是否需要审批")
    triggers_action = Column(String(50), nullable=True, comment="触发的动作")
    
    # 通知设置
    notify_customer = Column(Boolean, default=False, comment="是否通知客户")
    notify_admin = Column(Boolean, default=False, comment="是否通知管理员")
    customer_message_template = Column(Text, nullable=True, comment="客户通知模板")
    admin_message_template = Column(Text, nullable=True, comment="管理员通知模板")
    
    # 排序和系统设置
    sort_order = Column(Integer, default=0, comment="排序顺序")
    is_system = Column(Boolean, default=True, comment="是否系统预设状态")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
