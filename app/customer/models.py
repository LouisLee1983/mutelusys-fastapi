import uuid
from typing import List, Optional
from datetime import datetime
import enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


# 客户状态枚举
class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"        # 活跃
    INACTIVE = "inactive"    # 不活跃
    LOCKED = "locked"        # 锁定
    DELETED = "deleted"      # 已删除


# 客户等级枚举
class MembershipLevel(str, enum.Enum):
    REGULAR = "regular"      # 普通会员
    SILVER = "silver"        # 银卡会员
    GOLD = "gold"            # 金卡会员
    PLATINUM = "platinum"    # 白金会员
    DIAMOND = "diamond"      # 钻石会员


# 客户注册来源枚举
class RegistrationSource(str, enum.Enum):
    WEBSITE = "website"        # 网站注册
    MOBILE_APP = "mobile_app"  # 移动应用注册
    FACEBOOK = "facebook"      # Facebook登录
    GOOGLE = "google"          # Google登录
    APPLE = "apple"            # Apple登录
    OFFLINE = "offline"        # 线下注册
    ADMIN = "admin"            # 管理员添加


# 客户角色枚举
class CustomerRole(str, enum.Enum):
    REGULAR = "regular"        # 普通客户
    KOL = "kol"               # KOL/网红/达人
    VIP = "vip"               # VIP客户（高消费客户）


# 地址类型枚举
class AddressType(str, enum.Enum):
    SHIPPING = "shipping"    # 收货地址
    BILLING = "billing"      # 账单地址
    BOTH = "both"            # 两者都是


# 积分交易类型枚举
class PointsTransactionType(str, enum.Enum):
    EARN_ORDER = "earn_order"              # 订单获得
    EARN_REGISTER = "earn_register"        # 注册奖励
    EARN_REFERRAL = "earn_referral"        # 推荐奖励
    EARN_BIRTHDAY = "earn_birthday"        # 生日礼物
    EARN_REVIEW = "earn_review"            # 评价奖励
    EARN_PROMOTION = "earn_promotion"      # 促销活动
    REDEEM_PRODUCT = "redeem_product"      # 兑换商品
    EXPIRE = "expire"                      # 过期
    REFUND = "refund"                      # 退款返还
    DEDUCT_REFUND = "deduct_refund"        # 退款扣除
    ADMIN_ADJUST = "admin_adjust"          # 管理员调整


# 客户与客户分组的多对多关联表
customer_group = Table(
    "customer_group",
    Base.metadata,
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", UUID(as_uuid=True), ForeignKey("customer_groups.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


# 客户与意图的多对多关联表
customer_intent = Table(
    "customer_intent",
    Base.metadata,
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True),
    Column("intent_id", UUID(as_uuid=True), ForeignKey("product_intents.id", ondelete="CASCADE"), primary_key=True),
    Column("preference_level", Integer, default=1, comment="偏好程度，1-5"),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
)


# 客户与文化偏好的多对多关联表
customer_cultural_preference = Table(
    "customer_cultural_preference",
    Base.metadata,
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True),
    Column("symbol_id", UUID(as_uuid=True), ForeignKey("product_symbols.id", ondelete="CASCADE"), primary_key=True),
    Column("preference_level", Integer, default=1, comment="偏好程度，1-5"),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
)


# 客户与场景偏好的多对多关联表
customer_scene_preference = Table(
    "customer_scene_preference",
    Base.metadata,
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True),
    Column("scene_id", UUID(as_uuid=True), ForeignKey("product_scenes.id", ondelete="CASCADE"), primary_key=True),
    Column("preference_level", Integer, default=1, comment="偏好程度，1-5"),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
)


class Customer(Base):
    """客户信息表，包含基本信息、账户状态、会员等级、积分、注册来源等,由于注册的时候只要求用户提供email，连密码都可以不要，通过email发送验证码验证也可以，所以密码也可以留空，只需要记录用户的email即可注册通过。"""
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # 允许第三方登录的用户没有密码
    first_name = Column(String(100), nullable=True) # 名
    last_name = Column(String(100), nullable=True) # 姓
    phone_number = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    status = Column(Enum(CustomerStatus), default=CustomerStatus.ACTIVE, nullable=False)  # 客户状态
    membership_level = Column(Enum(MembershipLevel), default=MembershipLevel.REGULAR, nullable=False)   # 会员等级
    role = Column(Enum(CustomerRole), default=CustomerRole.REGULAR, nullable=False, comment="客户角色")  # 客户角色
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True, comment="所属国家")  # 所属国家
    current_points = Column(Integer, default=0, nullable=False, comment="当前可用积分")
    total_points_earned = Column(Integer, default=0, nullable=False, comment="累计获得的积分")
    registration_source = Column(Enum(RegistrationSource), default=RegistrationSource.WEBSITE, nullable=False)  # 注册来源
    registration_ip = Column(String(50), nullable=True)  # 注册IP
    last_login_at = Column(DateTime, nullable=True)  # 最后登录时间
    last_login_ip = Column(String(50), nullable=True)  # 最后登录IP
    notes = Column(Text, nullable=True, comment="管理员备注")  # 管理员备注
    preferences = Column(JSON, nullable=True, comment="用户偏好设置，如通知设置、隐私设置等")  # 用户偏好设置
    language_preference = Column(String(10), nullable=True, comment="语言偏好，如en-US")  # 语言偏好
    currency_preference = Column(String(3), nullable=True, comment="货币偏好，如USD")  # 货币偏好
    is_verified = Column(Boolean, default=False, comment="电子邮件或手机是否已验证")  # 电子邮件或手机是否已验证
    referral_code = Column(String(20), nullable=True, unique=True, comment="推荐码")  # 推荐码
    referred_by = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="推荐人ID")  # 推荐人ID
    verification_token = Column(String(100), nullable=True)  # 验证令牌, 用于验证邮箱或手机
    verification_token_expires_at = Column(DateTime, nullable=True)  # 验证令牌过期时间, 用于验证邮箱或手机
    reset_password_token = Column(String(100), nullable=True)  # 重置密码令牌, 用于重置密码
    reset_password_token_expires_at = Column(DateTime, nullable=True)  # 重置密码令牌过期时间, 用于重置密码
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 创建时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # 更新时间

    # 关联关系
    addresses = relationship("CustomerAddress", back_populates="customer", cascade="all, delete-orphan")
    groups = relationship("CustomerGroup", secondary=customer_group, back_populates="customers")
    behaviors = relationship("CustomerBehavior", back_populates="customer", cascade="all, delete-orphan")
    points_history = relationship("CustomerPoints", back_populates="customer", cascade="all, delete-orphan")
    country = relationship("Country", foreign_keys=[country_id])  # 关联国家
    # orders = relationship("Order", back_populates="customer")  # 暂时注释，避免循环导入
    
    # 多对多关系（暂时注释，等Product模型完善后再启用）
    # intents = relationship("ProductIntent", secondary="customer_intent", back_populates="customers")
    # scene_preferences = relationship("ProductScene", secondary="customer_scene_preference", back_populates="interested_customers")
    # cultural_preferences = relationship("ProductSymbol", secondary="customer_cultural_preference", back_populates="interested_customers")
    
    # 定义反向引用，用于获取被此客户推荐的其他客户
    referrals = relationship("Customer", backref="referrer", remote_side=[id])

    # 一对多关系
    gift_registries = relationship("GiftRegistry", back_populates="customer")
    coupons = relationship("CustomerCoupon", foreign_keys="CustomerCoupon.customer_id", back_populates="customer", cascade="all, delete-orphan")


class CustomerAddress(Base):
    """客户地址信息表，支持多地址管理"""
    __tablename__ = "customer_addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    address_type = Column(Enum(AddressType), default=AddressType.SHIPPING, nullable=False)
    is_default = Column(Boolean, default=False, comment="是否为默认地址")
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=False)
    country_code = Column(String(2), nullable=False, comment="ISO国家代码，如US")
    delivery_notes = Column(Text, nullable=True, comment="送货注意事项")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer", back_populates="addresses")


class CustomerGroup(Base):
    """客户分组，如新客、老客、VIP等"""
    __tablename__ = "customer_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, comment="是否系统预定义分组")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    customers = relationship("Customer", secondary=customer_group, back_populates="groups")


class CustomerBehavior(Base):
    """客户行为记录，如浏览历史、购买记录等"""
    __tablename__ = "customer_behaviors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    behavior_type = Column(String(50), nullable=False, comment="行为类型，如view_product, add_to_cart等")
    entity_type = Column(String(50), nullable=False, comment="实体类型，如product, category等")
    entity_id = Column(UUID(as_uuid=True), nullable=False, comment="实体ID")
    meta_data = Column(JSON, nullable=True, comment="元数据，如停留时间、点击位置等")
    user_agent = Column(String(255), nullable=True, comment="用户代理")
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer", back_populates="behaviors")


class CustomerPoints(Base):
    """客户积分记录，包含获取和使用历史"""
    __tablename__ = "customer_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False, comment="积分数量，正数为获取，负数为使用")
    description = Column(String(255), nullable=False, comment="积分描述，如购物获得、积分兑换等")
    transaction_type = Column(Enum(PointsTransactionType), nullable=False, comment="交易类型")
    reference_type = Column(String(50), nullable=True, comment="关联类型，如order, promotion等")
    reference_id = Column(UUID(as_uuid=True), nullable=True, comment="关联ID")
    expiry_date = Column(DateTime, nullable=True, comment="过期时间")
    is_expired = Column(Boolean, default=False, comment="是否已过期")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    customer = relationship("Customer", back_populates="points_history")


class BlackList(Base):
    """黑名单信息，包含电话、邮箱、地址等，用于拦截恶意下单"""
    __tablename__ = "blacklists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blacklist_type = Column(String(20), nullable=False, comment="黑名单类型，如email, phone, address, ip")
    value = Column(String(255), nullable=False, comment="黑名单值")
    reason = Column(Text, nullable=True, comment="拉黑原因")
    notes = Column(Text, nullable=True, comment="备注")
    is_active = Column(Boolean, default=True, comment="是否生效")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 联合唯一约束，确保同一类型的黑名单值不重复
    __table_args__ = (
        {},
    )


class EmailVerificationCode(Base):
    """邮箱验证码表，用于存储注册、登录、重置密码等场景的验证码"""
    __tablename__ = "email_verification_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, index=True, comment="邮箱地址")
    verification_code = Column(String(6), nullable=False, comment="6位验证码")
    purpose = Column(String(20), nullable=False, comment="验证码用途：register, login, reset_password")
    is_used = Column(Boolean, default=False, comment="是否已使用")
    used_at = Column(DateTime, nullable=True, comment="使用时间")
    expires_at = Column(DateTime, nullable=False, comment="过期时间")
    ip_address = Column(String(50), nullable=True, comment="请求IP地址")
    user_agent = Column(String(255), nullable=True, comment="用户代理")
    attempts = Column(Integer, default=0, comment="验证尝试次数")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 联合索引，用于查询特定邮箱的有效验证码
    __table_args__ = (
        {},
    )
