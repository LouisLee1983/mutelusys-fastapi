import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

# 引入子模块的模型
from app.payment.method.models import PaymentMethod
from app.payment.transaction.models import PaymentTransaction
from app.payment.gateway.models import PaymentGateway
from app.payment.status.models import PaymentStatus
from app.payment.cod.models import CashOnDelivery
from app.payment.installment.models import InstallmentPlan
from app.payment.currency.models import Currency, CurrencyRate


# 支付模块的其他核心模型可以在这里定义
class PaymentLog(Base):
    """支付操作日志表"""
    __tablename__ = "payment_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("payment_transactions.id"), nullable=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # 日志信息
    action = Column(String(50), nullable=False, comment="操作类型")
    status = Column(String(50), nullable=False, comment="操作状态")
    message = Column(Text, nullable=True, comment="日志消息")
    details = Column(JSON, nullable=True, comment="详细信息")
    
    # IP和设备信息
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(String(255), nullable=True, comment="User Agent")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    transaction = relationship("PaymentTransaction")
    order = relationship("Order")
    user = relationship("User")
