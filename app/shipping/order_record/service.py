# -*- coding: utf-8 -*-
"""
订单运费记录服务层
包含订单收费项目和运费记录的业务逻辑
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from .models import OrderChargeItem, OrderShippingInfo
from .schema import (
    OrderChargeItemCreate, OrderChargeItemUpdate, OrderChargeItemResponse,
    OrderShippingInfoCreate, OrderShippingInfoUpdate, OrderShippingInfoResponse,
    CreateOrderShippingRequest, OrderShippingStatsResponse
)
from ..calculation.service import ShippingCalculationService
from ..calculation.schema import ShippingCalculationRequest
from ..method.models import ShippingMethod
from ..zone.models import ShippingZone


class OrderRecordService:
    """订单运费记录服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.calculation_service = ShippingCalculationService(db)

    # ==================== 订单收费项目操作 ====================

    def create_charge_item(self, item_data: OrderChargeItemCreate) -> OrderChargeItem:
        """创建订单收费项目"""
        charge_item = OrderChargeItem(**item_data.dict())
        self.db.add(charge_item)
        self.db.commit()
        self.db.refresh(charge_item)
        return charge_item

    def get_charge_items_by_order(self, order_id: str) -> List[OrderChargeItem]:
        """获取订单的所有收费项目"""
        return self.db.query(OrderChargeItem).filter(
            and_(
                OrderChargeItem.order_id == order_id,
                OrderChargeItem.is_active == True
            )
        ).all()

    def update_charge_item(self, item_id: UUID, item_data: OrderChargeItemUpdate) -> Optional[OrderChargeItem]:
        """更新订单收费项目"""
        charge_item = self.db.query(OrderChargeItem).filter(OrderChargeItem.id == item_id).first()
        if not charge_item:
            return None

        for field, value in item_data.dict(exclude_unset=True).items():
            setattr(charge_item, field, value)

        self.db.commit()
        self.db.refresh(charge_item)
        return charge_item

    def delete_charge_item(self, item_id: UUID) -> bool:
        """删除订单收费项目（软删除）"""
        charge_item = self.db.query(OrderChargeItem).filter(OrderChargeItem.id == item_id).first()
        if not charge_item:
            return False

        charge_item.is_active = False
        self.db.commit()
        return True

    # ==================== 订单运费记录操作 ====================

    def create_shipping_info(self, shipping_data: OrderShippingInfoCreate) -> OrderShippingInfo:
        """创建订单运费记录"""
        shipping_info = OrderShippingInfo(**shipping_data.dict())
        self.db.add(shipping_info)
        self.db.commit()
        self.db.refresh(shipping_info)
        
        # 同时创建运费收费项目
        if shipping_info.final_shipping_cost > 0:
            charge_item_data = OrderChargeItemCreate(
                order_id=shipping_info.order_id,
                item_type="shipping",
                item_code=shipping_info.shipping_method_code,
                item_name=f"运费 - {shipping_info.shipping_method_name}",
                item_description=f"发往 {shipping_info.country_code} 的运费",
                amount=shipping_info.final_shipping_cost,
                currency_code=shipping_info.currency_code,
                shipping_method_id=shipping_info.shipping_method_id,
                shipping_zone_id=shipping_info.shipping_zone_id,
                free_shipping_rule_id=shipping_info.free_shipping_rule_id,
                metadata={
                    "base_cost": str(shipping_info.base_shipping_cost),
                    "discount": str(shipping_info.discount_amount),
                    "is_free_shipping": shipping_info.is_free_shipping
                }
            )
            self.create_charge_item(charge_item_data)
        
        return shipping_info

    def get_shipping_info_by_order(self, order_id: str) -> Optional[OrderShippingInfo]:
        """根据订单号获取运费记录"""
        return self.db.query(OrderShippingInfo).filter(
            OrderShippingInfo.order_id == order_id
        ).first()

    def update_shipping_info(self, order_id: str, shipping_data: OrderShippingInfoUpdate) -> Optional[OrderShippingInfo]:
        """更新订单运费记录"""
        shipping_info = self.get_shipping_info_by_order(order_id)
        if not shipping_info:
            return None

        for field, value in shipping_data.dict(exclude_unset=True).items():
            setattr(shipping_info, field, value)

        self.db.commit()
        self.db.refresh(shipping_info)
        return shipping_info

    def create_order_shipping_from_calculation(self, request: CreateOrderShippingRequest) -> OrderShippingInfo:
        """根据计算请求创建订单运费记录"""
        # 1. 进行运费计算
        calc_request = ShippingCalculationRequest(
            country_code=request.country_code,
            state_province=request.state_province,
            city=request.city,
            postal_code=request.postal_code,
            total_quantity=request.total_quantity,
            total_amount=request.total_amount,
            currency_code=request.currency_code,
            member_level=request.member_level,
            promotion_codes=request.promotion_codes,
            language_code=request.language_code
        )

        calc_result = self.calculation_service.calculate_shipping(calc_request)
        if not calc_result.success:
            raise ValueError(f"运费计算失败: {calc_result.message}")

        # 2. 查找指定的快递方式
        selected_estimate = None
        for estimate in calc_result.estimates:
            if estimate.method.method_code == request.shipping_method_code:
                selected_estimate = estimate
                break

        if not selected_estimate:
            raise ValueError(f"指定的快递方式 '{request.shipping_method_code}' 不可用")

        # 3. 获取快递方式和地区信息
        method = self.db.query(ShippingMethod).filter(
            ShippingMethod.code == request.shipping_method_code
        ).first()
        
        if not method:
            raise ValueError(f"快递方式 '{request.shipping_method_code}' 不存在")

        zone = self.db.query(ShippingZone).filter(
            ShippingZone.id == calc_result.zone_id
        ).first()

        # 4. 构建运费记录数据
        shipping_data = OrderShippingInfoCreate(
            order_id=request.order_id,
            country_code=request.country_code,
            state_province=request.state_province,
            city=request.city,
            postal_code=request.postal_code,
            full_address=request.full_address,
            total_quantity=request.total_quantity,
            total_amount=request.total_amount,
            currency_code=request.currency_code,
            
            # 快递信息
            shipping_method_id=method.id,
            shipping_method_code=method.code,
            shipping_method_name=selected_estimate.method.method_name,
            shipping_company=selected_estimate.method.company_name,
            transport_type=selected_estimate.method.transport_type,
            
            # 地区信息
            shipping_zone_id=zone.id if zone else None,
            shipping_zone_name=calc_result.zone_name or "",
            
            # 运费计算结果
            base_shipping_cost=selected_estimate.breakdown.base_shipping_cost,
            discount_amount=selected_estimate.breakdown.discount_amount,
            final_shipping_cost=selected_estimate.breakdown.final_shipping_cost,
            
            # 免运费信息
            is_free_shipping=selected_estimate.breakdown.is_free_shipping,
            free_shipping_rule_id=UUID(selected_estimate.breakdown.free_shipping_rule_id) if selected_estimate.breakdown.free_shipping_rule_id else None,
            free_shipping_rule_name=selected_estimate.breakdown.free_shipping_rule_name,
            free_shipping_reason=selected_estimate.breakdown.free_shipping_reason,
            savings_amount=selected_estimate.breakdown.savings_amount,
            
            # 配送时间
            estimated_delivery_days=selected_estimate.method.min_delivery_days,
            min_delivery_days=selected_estimate.method.min_delivery_days,
            max_delivery_days=selected_estimate.method.max_delivery_days,
            delivery_time_text=selected_estimate.method.delivery_time_text,
            
            # 计算详情
            calculation_details={
                "calculation_id": str(calc_result.calculated_at),
                "all_estimates": len(calc_result.estimates),
                "is_recommended": selected_estimate.is_recommended,
                "zone_id": calc_result.zone_id,
                "zone_name": calc_result.zone_name
            },
            calculation_metadata={
                "calculation_time": calc_result.calculation_time,
                "request_params": calc_request.dict(),
                "member_level": request.member_level,
                "promotion_codes": request.promotion_codes
            }
        )

        # 5. 创建运费记录
        return self.create_shipping_info(shipping_data)

    # ==================== 发货和跟踪管理 ====================

    def update_tracking_info(self, order_id: str, tracking_number: str, tracking_url: Optional[str] = None) -> Optional[OrderShippingInfo]:
        """更新快递跟踪信息"""
        update_data = OrderShippingInfoUpdate(
            tracking_number=tracking_number,
            tracking_url=tracking_url,
            shipping_status="shipped",
            shipped_at=datetime.utcnow()
        )
        return self.update_shipping_info(order_id, update_data)

    def mark_as_delivered(self, order_id: str, delivered_at: Optional[datetime] = None) -> Optional[OrderShippingInfo]:
        """标记订单为已签收"""
        update_data = OrderShippingInfoUpdate(
            shipping_status="delivered",
            delivered_at=delivered_at or datetime.utcnow()
        )
        return self.update_shipping_info(order_id, update_data)

    def update_shipping_status(self, order_id: str, status: str) -> Optional[OrderShippingInfo]:
        """更新发货状态"""
        update_data = OrderShippingInfoUpdate(shipping_status=status)
        return self.update_shipping_info(order_id, update_data)

    # ==================== 统计和分析 ====================

    def get_shipping_stats(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> OrderShippingStatsResponse:
        """获取运费统计数据"""
        query = self.db.query(OrderShippingInfo)
        
        if start_date:
            query = query.filter(OrderShippingInfo.created_at >= start_date)
        if end_date:
            query = query.filter(OrderShippingInfo.created_at <= end_date)

        shipping_records = query.all()
        
        if not shipping_records:
            return OrderShippingStatsResponse(
                total_orders=0,
                free_shipping_orders=0,
                free_shipping_rate=0.0,
                total_shipping_revenue=Decimal("0"),
                total_savings=Decimal("0")
            )

        total_orders = len(shipping_records)
        free_shipping_orders = sum(1 for r in shipping_records if r.is_free_shipping)
        free_shipping_rate = free_shipping_orders / total_orders if total_orders > 0 else 0.0
        
        total_revenue = sum(r.final_shipping_cost for r in shipping_records)
        total_savings = sum(r.savings_amount or Decimal("0") for r in shipping_records)
        
        # 计算平均运费（仅包含付费订单）
        paid_orders = [r for r in shipping_records if not r.is_free_shipping]
        average_shipping_cost = None
        if paid_orders:
            average_shipping_cost = sum(r.final_shipping_cost for r in paid_orders) / len(paid_orders)

        # 最受欢迎的快递方式
        method_counts = {}
        for record in shipping_records:
            method_counts[record.shipping_method_code] = method_counts.get(record.shipping_method_code, 0) + 1
        most_popular_method = max(method_counts.items(), key=lambda x: x[1])[0] if method_counts else None

        # 最受欢迎的地区
        zone_counts = {}
        for record in shipping_records:
            zone_counts[record.shipping_zone_name] = zone_counts.get(record.shipping_zone_name, 0) + 1
        most_popular_zone = max(zone_counts.items(), key=lambda x: x[1])[0] if zone_counts else None

        return OrderShippingStatsResponse(
            total_orders=total_orders,
            free_shipping_orders=free_shipping_orders,
            free_shipping_rate=round(free_shipping_rate, 4),
            average_shipping_cost=average_shipping_cost,
            total_shipping_revenue=total_revenue,
            total_savings=total_savings,
            most_popular_method=most_popular_method,
            most_popular_zone=most_popular_zone
        )

    def get_orders_by_shipping_method(self, method_code: str, limit: int = 50) -> List[OrderShippingInfo]:
        """获取使用指定快递方式的订单"""
        return self.db.query(OrderShippingInfo).filter(
            OrderShippingInfo.shipping_method_code == method_code
        ).order_by(desc(OrderShippingInfo.created_at)).limit(limit).all()

    def get_orders_by_zone(self, zone_name: str, limit: int = 50) -> List[OrderShippingInfo]:
        """获取指定地区的订单"""
        return self.db.query(OrderShippingInfo).filter(
            OrderShippingInfo.shipping_zone_name == zone_name
        ).order_by(desc(OrderShippingInfo.created_at)).limit(limit).all()

    def get_free_shipping_orders(self, limit: int = 50) -> List[OrderShippingInfo]:
        """获取免运费订单列表"""
        return self.db.query(OrderShippingInfo).filter(
            OrderShippingInfo.is_free_shipping == True
        ).order_by(desc(OrderShippingInfo.created_at)).limit(limit).all() 