import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text, Float, Enum, Numeric, JSON, Table
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ShipmentStatus(str, enum.Enum):
    """发货状态"""
    PENDING = "PENDING"                    # 待处理
    PREPARING = "PREPARING"                # 准备中
    READY_TO_SHIP = "READY_TO_SHIP"       # 准备发货
    SHIPPED = "SHIPPED"                    # 已发货
    IN_TRANSIT = "IN_TRANSIT"             # 运输中
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY" # 派送中
    DELIVERED = "DELIVERED"                # 已送达
    FAILED = "FAILED"                      # 配送失败
    RETURNED = "RETURNED"                  # 已退回
    CANCELLED = "CANCELLED"                # 已取消


class TrackingStatus(str, enum.Enum):
    """物流跟踪状态"""
    CREATED = "CREATED"                    # 运单创建
    PICKED_UP = "PICKED_UP"               # 已取件
    IN_TRANSIT = "IN_TRANSIT"             # 运输中
    ARRIVED_AT_FACILITY = "ARRIVED_AT_FACILITY"  # 到达分拣中心
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY" # 派送中
    DELIVERED = "DELIVERED"                # 已送达
    DELIVERY_FAILED = "DELIVERY_FAILED"   # 派送失败
    RETURNED = "RETURNED"                  # 已退回


class PackageType(str, enum.Enum):
    """包裹类型"""
    ENVELOPE = "ENVELOPE"              # 信封
    SMALL_BOX = "SMALL_BOX"           # 小包装盒
    MEDIUM_BOX = "MEDIUM_BOX"         # 中等包装盒
    LARGE_BOX = "LARGE_BOX"           # 大包装盒
    TUBE = "TUBE"                     # 圆筒包装
    FLAT_PACK = "FLAT_PACK"           # 平板包装
    CUSTOM = "CUSTOM"                 # 自定义包装


# 物流包裹与订单项的多对多关联表
shipment_item = Table(
    "shipment_item",
    Base.metadata,
    Column("shipment_id", UUID(as_uuid=True), ForeignKey("order_shipments.id", ondelete="CASCADE"), primary_key=True),
    Column("order_item_id", UUID(as_uuid=True), ForeignKey("order_items.id", ondelete="CASCADE"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1, comment="发货数量"),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class OrderShipment(Base):
    """简化的订单发货记录表（专注于快递公司和基本追踪信息）"""
    __tablename__ = "order_shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_code = Column(String(50), nullable=False, unique=True, index=True, comment="发货单号")
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, comment="订单ID")
    
    # 发货状态
    status = Column(Enum(ShipmentStatus), nullable=False, default=ShipmentStatus.PENDING, comment="发货状态")
    
    # 快递公司信息（简化）
    carrier_name = Column(String(100), nullable=False, comment="快递公司名称")
    tracking_number = Column(String(100), nullable=True, comment="快递单号")
    shipping_method = Column(String(50), nullable=False, comment="配送方式")
    
    # 收货地址（基本信息）
    recipient_name = Column(String(100), nullable=False, comment="收件人姓名")
    recipient_phone = Column(String(30), nullable=False, comment="收件人电话")
    recipient_email = Column(String(100), nullable=True, comment="收件人邮箱")
    shipping_address1 = Column(String(255), nullable=False, comment="收货地址")
    shipping_city = Column(String(100), nullable=False, comment="城市")
    shipping_country = Column(String(100), nullable=False, comment="国家")
    shipping_postcode = Column(String(20), nullable=False, comment="邮编")
    
    # 包裹基本信息
    weight = Column(Float, nullable=False, comment="重量(kg)")
    shipping_cost = Column(Numeric(10, 2), nullable=False, default=0, comment="运费")
    
    # 预计时间
    estimated_delivery_date = Column(DateTime, nullable=True, comment="预计送达时间")
    
    # 备注
    notes = Column(Text, nullable=True, comment="发货备注")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    shipped_at = Column(DateTime, nullable=True, comment="发货时间")
    delivered_at = Column(DateTime, nullable=True, comment="送达时间")
    
    # 关联关系
    order = relationship("Order", back_populates="shipments")
    items = relationship("ShipmentItem", back_populates="shipment", cascade="all, delete-orphan")
    tracking_records = relationship("ShipmentTracking", back_populates="shipment", cascade="all, delete-orphan")


class ShipmentItem(Base):
    """发货商品明细表"""
    __tablename__ = "shipment_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("order_shipments.id", ondelete="CASCADE"), nullable=False)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey("order_items.id"), nullable=False, comment="订单商品ID")
    
    # 商品信息快照
    product_id = Column(UUID(as_uuid=True), nullable=False, comment="商品ID")
    sku_id = Column(UUID(as_uuid=True), nullable=True, comment="SKU ID")
    product_name = Column(String(255), nullable=False, comment="商品名称")
    sku_code = Column(String(50), nullable=True, comment="SKU编码")
    
    # 发货数量
    quantity_shipped = Column(Integer, nullable=False, comment="发货数量")
    unit_price = Column(Numeric(10, 2), nullable=False, comment="单价")
    
    # 商品属性快照
    attributes = Column(JSON, nullable=True, comment="商品属性")
    image_url = Column(String(255), nullable=True, comment="商品图片")
    
    # 物理属性
    weight_per_unit = Column(Float, nullable=True, comment="单件重量(kg)")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    shipment = relationship("OrderShipment", back_populates="items")
    order_item = relationship("OrderItem")


class ShipmentTracking(Base):
    """简化的物流跟踪记录表（专注于货运位置信息）"""
    __tablename__ = "shipment_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("order_shipments.id", ondelete="CASCADE"), nullable=False)
    
    # 跟踪信息
    tracking_status = Column(Enum(TrackingStatus), nullable=False, comment="跟踪状态")
    location = Column(String(255), nullable=False, comment="当前位置，如：北京分拣中心、上海派送中心")
    description = Column(Text, nullable=False, comment="状态描述，如：已发货、运输中、派送中")
    
    # 操作信息
    operator_name = Column(String(100), nullable=True, comment="操作员或快递员姓名")
    
    # 时间
    timestamp = Column(DateTime, nullable=False, comment="跟踪时间")
    
    # 其他信息
    is_auto_generated = Column(Boolean, default=True, comment="是否系统自动生成")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关联关系
    shipment = relationship("OrderShipment", back_populates="tracking_records")


class Carrier(Base):
    """承运商信息表"""
    __tablename__ = "carriers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="承运商名称")
    code = Column(String(20), nullable=False, unique=True, comment="承运商代码")
    
    # 联系信息
    contact_phone = Column(String(30), nullable=True, comment="联系电话")
    contact_email = Column(String(100), nullable=True, comment="联系邮箱")
    website = Column(String(255), nullable=True, comment="官方网站")
    
    # 服务信息
    tracking_url_template = Column(String(500), nullable=True, comment="跟踪链接模板")
    supported_countries = Column(JSON, nullable=True, comment="支持的国家列表")
    service_types = Column(JSON, nullable=True, comment="服务类型列表")
    
    # 配置信息
    api_endpoint = Column(String(255), nullable=True, comment="API接口地址")
    api_key = Column(String(255), nullable=True, comment="API密钥")
    api_config = Column(JSON, nullable=True, comment="API配置")
    
    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    priority = Column(Integer, default=0, comment="优先级")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
