"""
订单关税集成服务
将关税计算集成到订单创建和管理流程中
"""

import uuid
from typing import List, Optional, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session

from app.order.models import Order, OrderItem
from app.order.schema import OrderCreate
from app.duty.service import DutyCalculationService
from app.duty.models import OrderDutyCharge
from app.duty.schema import (
    DutyCalculationRequest, 
    DutyCalculationItem, 
    OrderDutyChargeCreate
)


class OrderDutyIntegrationService:
    """订单关税集成服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.duty_service = DutyCalculationService(db)
    
    def calculate_and_apply_duty(self, order_data: OrderCreate) -> Dict[str, Any]:
        """
        计算并应用关税到订单数据
        
        Args:
            order_data: 订单创建数据
            
        Returns:
            Dict: 包含更新后的订单数据和关税计算结果
        """
        # 检查是否需要计算关税（跨境订单）
        if not self._needs_duty_calculation(order_data):
            return {
                "order_data": order_data,
                "duty_result": None,
                "duty_applied": False
            }
        
        # 准备关税计算请求
        duty_request = self._prepare_duty_calculation_request(order_data)
        
        # 执行关税计算
        duty_result = self.duty_service.calculate_duty(duty_request)
        
        # 应用关税到订单数据
        updated_order_data = self._apply_duty_to_order(order_data, duty_result)
        
        return {
            "order_data": updated_order_data,
            "duty_result": duty_result,
            "duty_applied": True
        }
    
    def create_duty_charge_record(self, order: Order, duty_result, order_data: OrderCreate) -> Optional[OrderDutyCharge]:
        """
        创建订单关税记录
        
        Args:
            order: 已创建的订单
            duty_result: 关税计算结果
            order_data: 原始订单数据
            
        Returns:
            OrderDutyCharge: 关税记录，如果无需关税则返回None
        """
        if not duty_result or duty_result.is_tax_free:
            return None
        
        # 获取国家信息
        country = self._get_country_by_code(duty_result.country_code)
        if not country:
            return None
        
        # 创建关税记录
        duty_charge = OrderDutyCharge(
            id=uuid.uuid4(),
            order_id=order.id,
            country_id=country.id,
            duty_zone_id=uuid.UUID(duty_result.duty_zone_id) if duty_result.duty_zone_id else None,
            taxable_amount=duty_result.taxable_amount,
            tax_rate=duty_result.tax_rate,
            duty_amount=duty_result.duty_amount,
            currency=duty_result.currency,
            calculation_details=duty_result.calculation_details,
            status='calculated'
        )
        
        self.db.add(duty_charge)
        self.db.commit()
        self.db.refresh(duty_charge)
        
        return duty_charge
    
    def update_duty_status(self, order_id: uuid.UUID, status: str) -> Optional[OrderDutyCharge]:
        """
        更新订单关税状态
        
        Args:
            order_id: 订单ID
            status: 新状态 (calculated, confirmed, paid, disputed)
            
        Returns:
            OrderDutyCharge: 更新后的关税记录
        """
        duty_charge = (
            self.db.query(OrderDutyCharge)
            .filter(OrderDutyCharge.order_id == order_id)
            .first()
        )
        
        if duty_charge:
            duty_charge.status = status
            if status == 'paid':
                duty_charge.paid_at = self.db.execute("SELECT NOW()").scalar()
            
            self.db.commit()
            self.db.refresh(duty_charge)
        
        return duty_charge
    
    def get_order_duty_info(self, order_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        获取订单关税信息
        
        Args:
            order_id: 订单ID
            
        Returns:
            Dict: 关税信息，包括计算结果和记录
        """
        duty_charge = (
            self.db.query(OrderDutyCharge)
            .filter(OrderDutyCharge.order_id == order_id)
            .first()
        )
        
        if not duty_charge:
            return None
        
        return {
            "duty_charge_id": str(duty_charge.id),
            "taxable_amount": float(duty_charge.taxable_amount),
            "tax_rate": float(duty_charge.tax_rate),
            "duty_amount": float(duty_charge.duty_amount),
            "currency": duty_charge.currency,
            "status": duty_charge.status,
            "calculation_details": duty_charge.calculation_details,
            "created_at": duty_charge.created_at.isoformat(),
            "paid_at": duty_charge.paid_at.isoformat() if duty_charge.paid_at else None
        }
    
    def recalculate_duty_for_order(self, order: Order) -> Dict[str, Any]:
        """
        重新计算订单关税（订单修改时使用）
        
        Args:
            order: 订单对象
            
        Returns:
            Dict: 重新计算的结果
        """
        # 构建关税计算请求
        duty_items = []
        for item in order.items:
            duty_items.append(DutyCalculationItem(
                product_id=str(item.product_id),
                category_id=str(item.category_id) if hasattr(item, 'category_id') and item.category_id else None,
                quantity=item.quantity,
                price=float(item.unit_price)
            ))
        
        duty_request = DutyCalculationRequest(
            country_code=self._extract_country_code(order.shipping_country),
            items=duty_items,
            shipping_cost=float(order.shipping_amount),
            currency=order.currency_code
        )
        
        # 执行重新计算
        duty_result = self.duty_service.calculate_duty(duty_request)
        
        # 更新现有关税记录
        duty_charge = (
            self.db.query(OrderDutyCharge)
            .filter(OrderDutyCharge.order_id == order.id)
            .first()
        )
        
        if duty_charge and not duty_result.is_tax_free:
            # 更新现有记录
            duty_charge.taxable_amount = duty_result.taxable_amount
            duty_charge.tax_rate = duty_result.tax_rate
            duty_charge.duty_amount = duty_result.duty_amount
            duty_charge.calculation_details = duty_result.calculation_details
            duty_charge.status = 'recalculated'
            self.db.commit()
        elif not duty_charge and not duty_result.is_tax_free:
            # 创建新记录
            country = self._get_country_by_code(duty_result.country_code)
            if country:
                duty_charge = OrderDutyCharge(
                    id=uuid.uuid4(),
                    order_id=order.id,
                    country_id=country.id,
                    duty_zone_id=uuid.UUID(duty_result.duty_zone_id) if duty_result.duty_zone_id else None,
                    taxable_amount=duty_result.taxable_amount,
                    tax_rate=duty_result.tax_rate,
                    duty_amount=duty_result.duty_amount,
                    currency=duty_result.currency,
                    calculation_details=duty_result.calculation_details,
                    status='recalculated'
                )
                self.db.add(duty_charge)
                self.db.commit()
        
        # 更新订单税费字段
        order.tax_amount = duty_result.duty_amount if not duty_result.is_tax_free else 0
        order.total_amount = order.subtotal + order.shipping_amount + order.tax_amount - order.discount_amount
        self.db.commit()
        
        return {
            "duty_result": duty_result,
            "duty_charge": duty_charge,
            "order_updated": True
        }
    
    def _needs_duty_calculation(self, order_data: OrderCreate) -> bool:
        """检查是否需要关税计算"""
        # 检查收货地址是否为跨境
        if not order_data.shipping_address.country:
            return False
        
        # 这里可以添加更多逻辑，比如检查是否为本国订单
        # 暂时假设所有国际订单都需要关税计算
        country_code = self._extract_country_code(order_data.shipping_address.country)
        
        # 检查是否支持该国家的关税计算
        duty_zone = self.duty_service._find_duty_zone_by_country(country_code)
        return duty_zone is not None
    
    def _prepare_duty_calculation_request(self, order_data: OrderCreate) -> DutyCalculationRequest:
        """准备关税计算请求"""
        duty_items = []
        
        for item in order_data.items:
            duty_items.append(DutyCalculationItem(
                product_id=str(item.product_id),
                category_id=str(item.category_id) if hasattr(item, 'category_id') and item.category_id else None,
                quantity=item.quantity,
                price=float(item.unit_price)
            ))
        
        return DutyCalculationRequest(
            country_code=self._extract_country_code(order_data.shipping_address.country),
            items=duty_items,
            shipping_cost=float(order_data.shipping_amount),
            currency=order_data.currency_code
        )
    
    def _apply_duty_to_order(self, order_data: OrderCreate, duty_result) -> OrderCreate:
        """将关税应用到订单数据"""
        # 创建订单数据副本
        updated_data = order_data.copy()
        
        # 更新税费和总金额
        if not duty_result.is_tax_free:
            updated_data.tax_amount = Decimal(str(duty_result.duty_amount))
            updated_data.total_amount = (
                updated_data.subtotal + 
                updated_data.shipping_amount + 
                updated_data.tax_amount - 
                updated_data.discount_amount
            )
        
        return updated_data
    
    def _extract_country_code(self, country_name: str) -> str:
        """从国家名称提取国家代码"""
        # 这里可以实现更复杂的逻辑来处理国家名称到代码的转换
        # 暂时假设传入的就是国家代码或能直接映射
        country_mapping = {
            "United States": "US",
            "Singapore": "SG",
            "Malaysia": "MY",
            "Thailand": "TH",
            "China": "CN",
            "Japan": "JP",
            "South Korea": "KR",
            "United Kingdom": "GB",
            "Australia": "AU",
            "Canada": "CA"
        }
        
        return country_mapping.get(country_name, country_name.upper()[:2])
    
    def _get_country_by_code(self, country_code: str):
        """根据国家代码获取国家信息"""
        from app.localization.country.models import Country
        return (
            self.db.query(Country)
            .filter(Country.code == country_code.upper())
            .first()
        )