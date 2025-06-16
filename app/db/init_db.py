"""
数据库初始化脚本
用于创建数据库表和初始数据
"""
import logging
from app.db.base import Base
from app.db.session import engine
from app.security.models import User, Role, Permission
from app.security.user.service import get_password_hash
from sqlalchemy.orm import Session
from uuid import uuid4

# 导入所有模型以确保创建表时都被包含
from app.security.models import (
    User, Role, Permission, UserRole, RolePermission, 
    LoginLog, OperationLog, DataBackup, SystemSetting
)

# 导入商品模块相关模型
from app.product.models import (
    Product, ProductCategory, ProductTranslation, ProductCategoryTranslation,
    product_tag, product_scene, product_intent, product_symbol,
    product_material, product_theme, product_target_group
)
from app.product.models import (
    ProductTag,
    ProductScene,
    ProductIntent,
    ProductSymbol,
    ProductMaterial,
    ProductTheme,
    ProductTargetGroup,
    ProductImage,
    ProductPrice,
    ProductInventory,
    InventoryOperation,
    InventoryHistory,
    ProductSku,
    sku_attribute_value,
    ProductAttribute,
    ProductAttributeValue,
    ProductBundle
)

# 物流模块已删除，使用order.shipment模块代替

# 导入订单模块相关模型
from app.order.models import (
    Order, OrderItem, OrderPayment, OrderStatusHistory, OrderNote,
    OrderStatus, PaymentStatus, ShippingStatus, OrderItemStatus, PaymentType, PaymentResult
)
from app.order.shipment.models import OrderShipment, shipment_item, ShipmentStatus, ShipmentTracking
from app.order.return_.models import OrderReturn, ReturnStatus, ReturnReason, ReturnAction, return_item
from app.order.gift.models import GiftOrder, GiftWrapType

# 导入客户模块相关模型
from app.customer.models import (
    Customer, CustomerStatus, MembershipLevel, RegistrationSource, AddressType,
    customer_group, customer_intent, customer_cultural_preference, customer_scene_preference,
    CustomerAddress, CustomerGroup, CustomerBehavior, CustomerPoints, BlackList
)
from app.customer.segment.models import CustomerSegment, segment_customer
from app.customer.intent.models import CustomerIntent
from app.customer.cultural_preference.models import CustomerCulturalPreference
from app.customer.scene_preference.models import CustomerScenePreference
from app.customer.gift_registry.models import GiftRegistry, RegistryType, RegistryStatus

# 导入营销模块相关模型
from app.marketing.coupon.models import Coupon, CouponStatus, CouponBatch
from app.marketing.customer_coupon.models import CustomerCoupon, CustomerCouponStatus, IssueMethod

# 导入支付模块相关模型
from app.payment.models import PaymentLog
from app.payment.method.models import PaymentMethod, PaymentMethodStatus
from app.payment.gateway.models import PaymentGateway, GatewayStatus
from app.payment.transaction.models import PaymentTransaction, TransactionType, TransactionStatus
from app.payment.status.models import PaymentStatus, PaymentStatusEnum
from app.payment.cod.models import CashOnDelivery
from app.payment.installment.models import InstallmentPlan, InstallmentPlanStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    # 创建所有表
    logger.info("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成")

def create_initial_data(db: Session):
    # 检查是否已存在超级管理员
    if db.query(User).filter(User.is_superuser == True).first():
        logger.info("超级管理员已存在，跳过初始数据创建")
        return
    
    # 创建初始超级管理员
    logger.info("正在创建超级管理员账号...")
    admin_user = User(
        username="admin",
        email="admin@mutelusys.com",
        hashed_password=get_password_hash("Admin123!"),
        full_name="系统管理员",
        is_active=True,
        is_superuser=True
    )
    db.add(admin_user)
    
    # 创建基本角色
    logger.info("正在创建基本角色...")
    admin_role = Role(
        name="管理员",
        description="系统管理员，拥有所有权限",
        is_default=False
    )
    
    operator_role = Role(
        name="运营",
        description="系统运营人员，负责内容和产品管理",
        is_default=False
    )
    
    customer_service_role = Role(
        name="客服",
        description="客服人员，负责处理订单和客户问题",
        is_default=True
    )
    
    db.add_all([admin_role, operator_role, customer_service_role])
    db.commit()
    
    logger.info("初始数据创建完成")

if __name__ == "__main__":
    # 初始化数据库
    init_db()
    
    # 创建会话并添加初始数据
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        db.close() 