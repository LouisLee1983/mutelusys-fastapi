import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class AffiliateStatus(str, enum.Enum):
    PENDING = "pending"       # 待审核
    APPROVED = "approved"     # 已批准
    REJECTED = "rejected"     # 已拒绝
    SUSPENDED = "suspended"   # 已暂停
    TERMINATED = "terminated" # 已终止


class AffiliateLevel(str, enum.Enum):
    BASIC = "basic"           # 基础级别
    SILVER = "silver"         # 银级
    GOLD = "gold"             # 金级
    PLATINUM = "platinum"     # 白金级
    DIAMOND = "diamond"       # 钻石级


class Affiliate(Base):
    """分销员信息，包含佣金率、结算方式等"""
    __tablename__ = "affiliates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("affiliate_programs.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="关联的客户ID，可以为空")
    
    # 基本信息
    code = Column(String(50), nullable=False, unique=True, comment="推广代码，用于跟踪")
    name = Column(String(100), nullable=False, comment="分销员名称")
    email = Column(String(255), nullable=False, comment="联系邮箱")
    phone = Column(String(50), nullable=True, comment="联系电话")
    company_name = Column(String(100), nullable=True, comment="公司名称")
    website = Column(String(255), nullable=True, comment="网站")
    
    # 状态信息
    status = Column(Enum(AffiliateStatus), default=AffiliateStatus.PENDING, nullable=False, comment="状态")
    level = Column(Enum(AffiliateLevel), default=AffiliateLevel.BASIC, nullable=False, comment="级别")
    
    # 佣金设置
    commission_rate = Column(Float, nullable=False, comment="佣金率（百分比）")
    override_program_rate = Column(Boolean, default=False, comment="是否覆盖项目佣金率")
    cookie_days = Column(Integer, default=30, comment="Cookie有效天数")
    
    # 支付设置
    payment_method = Column(String(50), nullable=True, comment="支付方式")
    payment_details = Column(JSON, nullable=True, comment="支付详情，如银行账号等")
    payment_threshold = Column(Float, default=100, comment="支付阈值")
    tax_id = Column(String(50), nullable=True, comment="税务ID")
    
    # 统计信息
    clicks_count = Column(Integer, default=0, comment="点击次数")
    conversions_count = Column(Integer, default=0, comment="转化次数")
    total_earnings = Column(Float, default=0, comment="总收入")
    unpaid_earnings = Column(Float, default=0, comment="未付收入")
    last_click_at = Column(DateTime, nullable=True, comment="最后点击时间")
    last_conversion_at = Column(DateTime, nullable=True, comment="最后转化时间")
    
    # 自定义域
    custom_domain = Column(String(255), nullable=True, comment="自定义域名")
    landing_page = Column(String(255), nullable=True, comment="落地页")
    
    # 跟踪设置
    tracking_code = Column(Text, nullable=True, comment="跟踪代码")
    utm_parameters = Column(JSON, nullable=True, comment="UTM参数设置")
    
    # 审核信息
    approval_date = Column(DateTime, nullable=True, comment="批准日期")
    rejection_reason = Column(Text, nullable=True, comment="拒绝原因")
    notes = Column(Text, nullable=True, comment="备注")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    program = relationship("AffiliateProgram", back_populates="affiliates")
    customer = relationship("Customer", back_populates="affiliate")
    commissions = relationship("AffiliateCommission", back_populates="affiliate", cascade="all, delete-orphan")
    clicks = relationship("AffiliateClick", back_populates="affiliate", cascade="all, delete-orphan")


class AffiliateClick(Base):
    """分销点击记录"""
    __tablename__ = "affiliate_clicks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affiliate_id = Column(UUID(as_uuid=True), ForeignKey("affiliates.id", ondelete="CASCADE"), nullable=False)
    
    # 点击信息
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    referrer = Column(String(255), nullable=True, comment="来源页面")
    landing_page = Column(String(255), nullable=True, comment="落地页面")
    
    # 追踪信息
    click_id = Column(String(100), nullable=False, unique=True, comment="点击ID")
    conversion_id = Column(UUID(as_uuid=True), ForeignKey("affiliate_conversions.id"), nullable=True, comment="关联的转化ID")
    session_id = Column(String(100), nullable=True, comment="会话ID")
    
    # 设备信息
    device_type = Column(String(20), nullable=True, comment="设备类型")
    browser = Column(String(50), nullable=True, comment="浏览器")
    operating_system = Column(String(50), nullable=True, comment="操作系统")
    country_code = Column(String(2), nullable=True, comment="国家代码")
    
    # 时间信息
    clicked_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="点击时间")
    expiry_date = Column(DateTime, nullable=True, comment="过期日期")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    affiliate = relationship("Affiliate", back_populates="clicks")
    conversion = relationship("AffiliateConversion", back_populates="click")


class AffiliateConversion(Base):
    """分销转化记录"""
    __tablename__ = "affiliate_conversions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affiliate_id = Column(UUID(as_uuid=True), ForeignKey("affiliates.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, comment="关联订单ID")
    
    # 转化信息
    amount = Column(Float, nullable=False, comment="订单金额")
    commission_amount = Column(Float, nullable=False, comment="佣金金额")
    currency_code = Column(String(3), default="USD", comment="货币代码")
    
    # 状态信息
    status = Column(String(20), default="pending", comment="状态：pending, approved, rejected, paid")
    approved_at = Column(DateTime, nullable=True, comment="批准时间")
    rejected_at = Column(DateTime, nullable=True, comment="拒绝时间")
    rejection_reason = Column(Text, nullable=True, comment="拒绝原因")
    
    # 关联点击
    click_id = Column(String(100), nullable=True, comment="关联的点击ID")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    affiliate = relationship("Affiliate")
    order = relationship("Order")
    click = relationship("AffiliateClick", back_populates="conversion")
    commission = relationship("AffiliateCommission", back_populates="conversion", uselist=False)
