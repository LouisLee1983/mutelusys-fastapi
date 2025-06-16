import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ProgramStatus(str, enum.Enum):
    ACTIVE = "active"        # 激活
    INACTIVE = "inactive"    # 未激活
    PAUSED = "paused"        # 暂停
    ENDED = "ended"          # 已结束


class CommissionStructure(str, enum.Enum):
    FLAT = "flat"                   # 统一佣金
    TIERED = "tiered"               # 阶梯佣金
    CATEGORY_BASED = "category"     # 分类佣金
    PRODUCT_BASED = "product"       # 产品佣金
    PERFORMANCE_BASED = "performance"  # 性能佣金


class AffiliateProgram(Base):
    """联盟营销项目设置"""
    __tablename__ = "affiliate_programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="项目名称")
    description = Column(Text, nullable=True, comment="项目描述")
    status = Column(Enum(ProgramStatus), default=ProgramStatus.ACTIVE, nullable=False, comment="状态")
    
    # 基本设置
    is_public = Column(Boolean, default=True, comment="是否公开(允许自助申请)")
    requires_approval = Column(Boolean, default=True, comment="是否需要审核")
    auto_approval = Column(Boolean, default=False, comment="是否自动审核")
    
    # 佣金设置
    commission_structure = Column(Enum(CommissionStructure), default=CommissionStructure.FLAT, nullable=False, comment="佣金结构")
    default_commission_rate = Column(Float, default=10.0, comment="默认佣金率（百分比）")
    min_commission_rate = Column(Float, default=5.0, comment="最低佣金率")
    max_commission_rate = Column(Float, default=30.0, comment="最高佣金率")
    tiered_commissions = Column(JSON, nullable=True, comment="阶梯佣金结构")
    category_commissions = Column(JSON, nullable=True, comment="分类佣金结构")
    product_commissions = Column(JSON, nullable=True, comment="产品佣金结构")
    
    # 规则设置
    cookie_days = Column(Integer, default=30, comment="Cookie有效天数")
    excluded_products = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除产品")
    excluded_categories = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="排除分类")
    min_payout = Column(Float, default=50.0, comment="最低支付金额")
    payout_schedule = Column(String(50), default="monthly", comment="支付周期：weekly, biweekly, monthly, quarterly")
    
    # 内容设置
    terms_conditions = Column(Text, nullable=True, comment="条款和条件")
    banner_url = Column(String(255), nullable=True, comment="横幅URL")
    logo_url = Column(String(255), nullable=True, comment="徽标URL")
    marketing_materials = Column(JSON, nullable=True, comment="营销材料")
    
    # 追踪设置
    tracking_domain = Column(String(255), nullable=True, comment="跟踪域名")
    tracking_parameters = Column(JSON, nullable=True, comment="跟踪参数")
    
    # 应用设置
    application_form = Column(JSON, nullable=True, comment="申请表单配置")
    application_questions = Column(JSON, nullable=True, comment="申请问题")
    
    # 限制设置
    max_affiliates = Column(Integer, nullable=True, comment="最大分销员数量")
    country_restrictions = Column(ARRAY(String), nullable=True, comment="国家限制")
    
    # 时间设置
    start_date = Column(DateTime, nullable=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    
    # 联系信息
    contact_email = Column(String(255), nullable=True, comment="联系邮箱")
    support_email = Column(String(255), nullable=True, comment="支持邮箱")
    support_phone = Column(String(50), nullable=True, comment="支持电话")
    
    # 统计信息
    total_affiliates = Column(Integer, default=0, comment="总分销员数量")
    active_affiliates = Column(Integer, default=0, comment="活跃分销员数量")
    total_sales = Column(Float, default=0, comment="总销售额")
    total_commissions = Column(Float, default=0, comment="总佣金额")
    conversion_rate = Column(Float, default=0, comment="转化率")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    affiliates = relationship("Affiliate", back_populates="program")
    creator = relationship("User")


class AffiliateApplication(Base):
    """联盟项目申请记录"""
    __tablename__ = "affiliate_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("affiliate_programs.id", ondelete="CASCADE"), nullable=False)
    
    # 申请者信息
    name = Column(String(100), nullable=False, comment="申请者名称")
    email = Column(String(255), nullable=False, comment="申请者邮箱")
    phone = Column(String(50), nullable=True, comment="申请者电话")
    website = Column(String(255), nullable=True, comment="申请者网站")
    company = Column(String(100), nullable=True, comment="申请者公司")
    
    # 申请信息
    promotion_methods = Column(ARRAY(String), nullable=True, comment="推广方式")
    expected_sales = Column(Integer, nullable=True, comment="预期销售量")
    answers = Column(JSON, nullable=True, comment="问题回答")
    additional_info = Column(Text, nullable=True, comment="附加信息")
    
    # 状态信息
    status = Column(String(20), default="pending", comment="状态：pending, approved, rejected")
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="提交时间")
    reviewed_at = Column(DateTime, nullable=True, comment="审核时间")
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="审核人")
    
    # 审核结果
    feedback = Column(Text, nullable=True, comment="反馈意见")
    rejection_reason = Column(Text, nullable=True, comment="拒绝原因")
    approved_commission_rate = Column(Float, nullable=True, comment="批准的佣金率")
    
    # 成功申请后的关联分销员
    affiliate_id = Column(UUID(as_uuid=True), ForeignKey("affiliates.id"), nullable=True, comment="关联分销员ID")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    program = relationship("AffiliateProgram")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    affiliate = relationship("Affiliate", foreign_keys=[affiliate_id])
