import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_, and_
import random
import string

from app.order.shipment.models import (
    OrderShipment, ShipmentItem, ShipmentTracking, Carrier,
    ShipmentStatus, TrackingStatus
)
from app.order.shipment.schema import (
    ShipmentCreate, ShipmentUpdate, ShipmentStatusUpdate,
    TrackingRecordCreate, ShipmentListParams, CarrierCreate
)
from app.order.models import Order, OrderItem


class ShipmentService:
    @staticmethod
    def generate_shipment_code() -> str:
        """生成发货单号，格式为：SH+年月日+6位随机数字"""
        date_prefix = datetime.now().strftime("%Y%m%d")
        random_suffix = ''.join(random.choices(string.digits, k=6))
        return f"SH{date_prefix}{random_suffix}"

    @staticmethod
    def create_shipment(db: Session, shipment_data: ShipmentCreate) -> OrderShipment:
        """创建发货记录"""
        shipment_code = ShipmentService.generate_shipment_code()
        
        # 验证订单是否存在
        order = db.query(Order).filter(Order.id == shipment_data.order_id).first()
        if not order:
            raise ValueError("订单不存在")
        
        # 创建简化的发货记录（专注于快递公司和基本信息）
        shipment = OrderShipment(
            shipment_code=shipment_code,
            order_id=shipment_data.order_id,
            status=ShipmentStatus.PENDING,
            carrier_name=shipment_data.carrier_name,
            tracking_number=shipment_data.tracking_number,
            shipping_method=shipment_data.shipping_method,
            recipient_name=shipment_data.recipient_name,
            recipient_phone=shipment_data.recipient_phone,
            recipient_email=shipment_data.recipient_email,
            shipping_address1=shipment_data.shipping_address1,
            shipping_city=shipment_data.shipping_city,
            shipping_country=shipment_data.shipping_country,
            shipping_postcode=shipment_data.shipping_postcode,
            weight=shipment_data.weight,
            shipping_cost=shipment_data.shipping_cost,
            estimated_delivery_date=shipment_data.estimated_delivery_date,
            notes=shipment_data.notes
        )
        
        db.add(shipment)
        db.flush()  # 获取发货记录ID
        
        # 创建发货商品明细
        for item_data in shipment_data.items:
            # 验证订单商品是否存在
            order_item = db.query(OrderItem).filter(
                OrderItem.id == item_data.order_item_id,
                OrderItem.order_id == shipment_data.order_id
            ).first()
            if not order_item:
                raise ValueError(f"订单商品不存在: {item_data.order_item_id}")
            
            shipment_item = ShipmentItem(
                shipment_id=shipment.id,
                order_item_id=item_data.order_item_id,
                product_id=item_data.product_id,
                sku_id=item_data.sku_id,
                product_name=item_data.product_name,
                sku_code=item_data.sku_code,
                quantity_shipped=item_data.quantity_shipped,
                unit_price=item_data.unit_price,
                attributes=item_data.attributes,
                image_url=item_data.image_url,
                weight_per_unit=item_data.weight_per_unit
            )
            db.add(shipment_item)
        
        # 创建初始跟踪记录
        initial_tracking = ShipmentTracking(
            shipment_id=shipment.id,
            tracking_status=TrackingStatus.CREATED,
            location="发货仓库",
            description="发货记录已创建，准备打包发货",
            timestamp=datetime.utcnow(),
            is_auto_generated=True
        )
        db.add(initial_tracking)
        
        db.commit()
        db.refresh(shipment)
        
        return shipment

    @staticmethod
    def get_shipment_by_id(db: Session, shipment_id: uuid.UUID) -> Optional[OrderShipment]:
        """通过ID获取发货记录"""
        from sqlalchemy.orm import joinedload
        return db.query(OrderShipment).options(
            joinedload(OrderShipment.items),
            joinedload(OrderShipment.tracking_records)
        ).filter(OrderShipment.id == shipment_id).first()

    @staticmethod
    def get_shipment_by_code(db: Session, shipment_code: str) -> Optional[OrderShipment]:
        """通过发货单号获取发货记录"""
        from sqlalchemy.orm import joinedload
        return db.query(OrderShipment).options(
            joinedload(OrderShipment.items),
            joinedload(OrderShipment.tracking_records)
        ).filter(OrderShipment.shipment_code == shipment_code).first()

    @staticmethod
    def get_shipments(db: Session, params: ShipmentListParams) -> Tuple[List[OrderShipment], int]:
        """获取发货记录列表"""
        from sqlalchemy.orm import joinedload
        
        query = db.query(OrderShipment).options(
            joinedload(OrderShipment.items),
            joinedload(OrderShipment.tracking_records)
        )
        
        # 应用过滤条件
        if params.filters:
            filters = params.filters
            if filters.order_id:
                query = query.filter(OrderShipment.order_id == filters.order_id)
            if filters.shipment_code:
                query = query.filter(OrderShipment.shipment_code.ilike(f"%{filters.shipment_code}%"))
            if filters.status:
                query = query.filter(OrderShipment.status == filters.status)
            if filters.carrier_id:
                query = query.filter(OrderShipment.carrier_id == filters.carrier_id)
            if filters.tracking_number:
                query = query.filter(OrderShipment.tracking_number.ilike(f"%{filters.tracking_number}%"))
            if filters.date_from:
                query = query.filter(OrderShipment.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(OrderShipment.created_at <= filters.date_to)
            if filters.recipient_name:
                query = query.filter(OrderShipment.recipient_name.ilike(f"%{filters.recipient_name}%"))
            if filters.recipient_phone:
                query = query.filter(OrderShipment.recipient_phone.ilike(f"%{filters.recipient_phone}%"))
        
        # 获取总数
        total = query.count()
        
        # 应用排序
        if params.sort_desc:
            query = query.order_by(desc(getattr(OrderShipment, params.sort_by)))
        else:
            query = query.order_by(asc(getattr(OrderShipment, params.sort_by)))
        
        # 应用分页
        offset = (params.page - 1) * params.page_size
        shipments = query.offset(offset).limit(params.page_size).all()
        
        return shipments, total

    @staticmethod
    def update_shipment(db: Session, shipment_id: uuid.UUID, update_data: ShipmentUpdate) -> Optional[OrderShipment]:
        """更新发货记录"""
        shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
        if not shipment:
            return None
        
        # 更新字段
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(shipment, field) and value is not None:
                setattr(shipment, field, value)
        
        db.commit()
        db.refresh(shipment)
        return shipment

    @staticmethod
    def update_shipment_status(db: Session, shipment_id: uuid.UUID, status_data: ShipmentStatusUpdate) -> Optional[OrderShipment]:
        """更新发货状态"""
        shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
        if not shipment:
            return None
        
        old_status = shipment.status
        shipment.status = status_data.status
        
        # 更新时间戳
        if status_data.status == ShipmentStatus.SHIPPED and not shipment.shipped_at:
            shipment.shipped_at = datetime.utcnow()
        elif status_data.status == ShipmentStatus.DELIVERED and not shipment.delivered_at:
            shipment.delivered_at = datetime.utcnow()
        
        # 添加跟踪记录
        tracking_status_map = {
            ShipmentStatus.PREPARING: TrackingStatus.CREATED,
            ShipmentStatus.SHIPPED: TrackingStatus.PICKED_UP,
            ShipmentStatus.IN_TRANSIT: TrackingStatus.IN_TRANSIT,
            ShipmentStatus.OUT_FOR_DELIVERY: TrackingStatus.OUT_FOR_DELIVERY,
            ShipmentStatus.DELIVERED: TrackingStatus.DELIVERED,
        }
        
        tracking_status = tracking_status_map.get(status_data.status, TrackingStatus.IN_TRANSIT)
        description = f"状态更新：{old_status} -> {status_data.status}"
        if status_data.notes:
            description += f"，备注：{status_data.notes}"
        
        tracking_record = ShipmentTracking(
            shipment_id=shipment.id,
            tracking_status=tracking_status,
            location="更新位置",
            description=description,
            timestamp=datetime.utcnow(),
            is_auto_generated=True
        )
        db.add(tracking_record)
        
        db.commit()
        db.refresh(shipment)
        return shipment

    @staticmethod
    def add_tracking_record(db: Session, shipment_id: uuid.UUID, tracking_data: TrackingRecordCreate) -> Optional[ShipmentTracking]:
        """添加物流跟踪记录"""
        shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
        if not shipment:
            return None
        
        tracking_record = ShipmentTracking(
            shipment_id=shipment_id,
            tracking_status=tracking_data.tracking_status,
            location=tracking_data.location,
            description=tracking_data.description,
            operator_name=tracking_data.operator_name,
            timestamp=tracking_data.timestamp,
            is_auto_generated=tracking_data.is_auto_generated
        )
        
        db.add(tracking_record)
        db.commit()
        db.refresh(tracking_record)
        
        return tracking_record

    @staticmethod
    def get_tracking_records(db: Session, shipment_id: uuid.UUID) -> List[ShipmentTracking]:
        """获取物流跟踪记录"""
        return db.query(ShipmentTracking).filter(
            ShipmentTracking.shipment_id == shipment_id
        ).order_by(desc(ShipmentTracking.timestamp)).all()

    @staticmethod
    def get_tracking_updates(db: Session, shipment_id: uuid.UUID) -> List[ShipmentTracking]:
        """获取物流跟踪更新记录（与get_tracking_records相同，为API兼容性）"""
        return ShipmentService.get_tracking_records(db, shipment_id)

    @staticmethod
    def add_tracking_update(db: Session, shipment_id: uuid.UUID, tracking_data) -> Optional[ShipmentTracking]:
        """添加物流跟踪更新（适配API层的TrackingUpdateCreate）"""
        from app.order.shipment.schema import TrackingRecordCreate
        
        # 检查发货记录是否存在
        shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
        if not shipment:
            return None
        
        # 如果没有提供时间戳，使用当前时间
        timestamp = tracking_data.timestamp if tracking_data.timestamp else datetime.utcnow()
        
        # 转换为TrackingRecordCreate格式
        tracking_record_data = TrackingRecordCreate(
            tracking_status=tracking_data.tracking_status,
            location=tracking_data.location,
            description=tracking_data.description,
            operator_name=tracking_data.operator_name,
            timestamp=timestamp,
            is_auto_generated=False  # 手动添加的记录
        )
        
        return ShipmentService.add_tracking_record(db, shipment_id, tracking_record_data)

    @staticmethod
    def delete_shipment(db: Session, shipment_id: uuid.UUID) -> bool:
        """删除发货记录"""
        shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
        if not shipment:
            return False
        
        # 只允许删除待处理或准备中的发货记录
        if shipment.status not in [ShipmentStatus.PENDING, ShipmentStatus.PREPARING]:
            raise ValueError("只能删除待处理或准备中的发货记录")
        
        db.delete(shipment)
        db.commit()
        return True

    @staticmethod
    def get_order_shipments(db: Session, order_id: uuid.UUID) -> List[OrderShipment]:
        """获取订单的所有发货记录"""
        from sqlalchemy.orm import joinedload
        return db.query(OrderShipment).options(
            joinedload(OrderShipment.items),
            joinedload(OrderShipment.tracking_records)
        ).filter(OrderShipment.order_id == order_id).order_by(desc(OrderShipment.created_at)).all()

    @staticmethod
    def get_shipments_by_order_id(db: Session, order_id: uuid.UUID) -> List[OrderShipment]:
        """根据订单ID获取发货记录（与get_order_shipments相同，为API兼容性）"""
        return ShipmentService.get_order_shipments(db, order_id)

    @staticmethod
    def search_shipment_by_tracking(db: Session, tracking_number: str) -> Optional[OrderShipment]:
        """根据物流单号搜索发货记录"""
        from sqlalchemy.orm import joinedload
        return db.query(OrderShipment).options(
            joinedload(OrderShipment.items),
            joinedload(OrderShipment.tracking_records)
        ).filter(
            or_(
                OrderShipment.tracking_number.ilike(f"%{tracking_number}%"),
                OrderShipment.shipment_code.ilike(f"%{tracking_number}%")
            )
        ).first()

    @staticmethod
    def mark_as_shipped(db: Session, shipment_id: uuid.UUID, tracking_number: Optional[str] = None, tracking_url: Optional[str] = None) -> Optional[OrderShipment]:
        """标记发货记录为已发货状态"""
        shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
        if not shipment:
            return None
        
        # 更新发货状态
        shipment.status = ShipmentStatus.SHIPPED
        shipment.shipped_at = datetime.utcnow()
        
        # 更新跟踪号
        if tracking_number:
            shipment.tracking_number = tracking_number
        
        # 添加跟踪记录
        tracking_record = ShipmentTracking(
            shipment_id=shipment.id,
            tracking_status=TrackingStatus.PICKED_UP,
            location="发货地",
            description=f"包裹已发货",
            timestamp=datetime.utcnow(),
            is_auto_generated=True
        )
        
        if tracking_number:
            tracking_record.description += f"，物流单号：{tracking_number}"
        if tracking_url:
            tracking_record.description += f"，查询链接：{tracking_url}"
        
        db.add(tracking_record)
        db.commit()
        db.refresh(shipment)
        
        return shipment

    @staticmethod
    def count_shipments_by_status(db: Session) -> Dict[str, int]:
        """统计各状态的发货记录数量"""
        result = {}
        for status in ShipmentStatus:
            count = db.query(OrderShipment).filter(OrderShipment.status == status).count()
            result[status.value] = count
        return result


class CarrierService:
    @staticmethod
    def create_carrier(db: Session, carrier_data: CarrierCreate) -> Carrier:
        """创建承运商"""
        carrier = Carrier(**carrier_data.dict())
        db.add(carrier)
        db.commit()
        db.refresh(carrier)
        return carrier

    @staticmethod
    def get_carrier_by_id(db: Session, carrier_id: uuid.UUID) -> Optional[Carrier]:
        """通过ID获取承运商"""
        return db.query(Carrier).filter(Carrier.id == carrier_id).first()

    @staticmethod
    def get_carriers(db: Session, active_only: bool = True) -> List[Carrier]:
        """获取承运商列表"""
        query = db.query(Carrier)
        if active_only:
            query = query.filter(Carrier.is_active == True)
        return query.order_by(desc(Carrier.priority), Carrier.name).all()

    @staticmethod
    def get_carrier_by_code(db: Session, code: str) -> Optional[Carrier]:
        """通过代码获取承运商"""
        return db.query(Carrier).filter(Carrier.code == code).first()

    @staticmethod
    def update_carrier(db: Session, carrier_id: uuid.UUID, update_data: Dict[str, Any]) -> Optional[Carrier]:
        """更新承运商"""
        carrier = CarrierService.get_carrier_by_id(db, carrier_id)
        if not carrier:
            return None
        
        for field, value in update_data.items():
            if hasattr(carrier, field):
                setattr(carrier, field, value)
        
        db.commit()
        db.refresh(carrier)
        return carrier

    @staticmethod
    def delete_carrier(db: Session, carrier_id: uuid.UUID) -> bool:
        """删除承运商"""
        carrier = CarrierService.get_carrier_by_id(db, carrier_id)
        if not carrier:
            return False
        
        # 检查是否有关联的发货记录
        shipment_count = db.query(OrderShipment).filter(OrderShipment.carrier_id == carrier_id).count()
        if shipment_count > 0:
            raise ValueError("无法删除有发货记录的承运商")
        
        db.delete(carrier)
        db.commit()
        return True
