from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.order.models import Order, OrderItem, OrderStatus, OrderItemStatus, PaymentStatus


class OrderItemService:
    """订单项服务层"""
    
    @staticmethod
    def get_order_item_by_id(db: Session, item_id: UUID) -> Optional[OrderItem]:
        """根据ID获取订单项"""
        return db.query(OrderItem).filter(OrderItem.id == item_id).first()
    
    @staticmethod
    def update_item_quantity(
        db: Session, 
        item_id: UUID, 
        new_quantity: int,
        customer_id: Optional[UUID] = None
    ) -> OrderItem:
        """更新订单项数量（仅限未支付订单）"""
        
        item = OrderItemService.get_order_item_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="订单项不存在"
            )
        
        # 检查订单权限
        if customer_id and item.order.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限修改此订单项"
            )
        
        # 检查订单状态是否允许修改
        if item.order.payment_status in [PaymentStatus.PAID, PaymentStatus.PARTIALLY_PAID]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="已支付订单无法修改商品数量"
            )
        
        if item.status not in [OrderItemStatus.PENDING, OrderItemStatus.CONFIRMED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前状态下无法修改数量"
            )
        
        if new_quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="数量必须大于0"
            )
        
        # 更新数量和价格
        old_quantity = item.quantity
        item.quantity = new_quantity
        item.subtotal = item.unit_price * new_quantity
        item.final_price = item.subtotal - item.discount_amount + item.tax_amount
        item.updated_at = datetime.utcnow()
        
        # 重新计算订单总金额
        OrderItemService._recalculate_order_total(db, item.order)
        
        db.commit()
        db.refresh(item)
        
        return item
    
    @staticmethod
    def remove_item_from_order(
        db: Session, 
        item_id: UUID,
        customer_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """从订单中移除商品（仅限未支付订单）"""
        
        item = OrderItemService.get_order_item_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="订单项不存在"
            )
        
        # 检查订单权限
        if customer_id and item.order.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限修改此订单项"
            )
        
        # 检查订单状态
        if item.order.payment_status in [PaymentStatus.PAID, PaymentStatus.PARTIALLY_PAID]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="已支付订单无法移除商品"
            )
        
        order = item.order
        
        # 检查是否是订单中最后一个商品
        remaining_items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id,
            OrderItem.id != item_id,
            OrderItem.status != OrderItemStatus.CANCELLED
        ).count()
        
        if remaining_items == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法移除最后一个商品，请取消整个订单"
            )
        
        # 删除订单项
        db.delete(item)
        
        # 重新计算订单总金额
        OrderItemService._recalculate_order_total(db, order)
        
        db.commit()
        
        return {"message": "商品已从订单中移除"}
    
    @staticmethod
    def cancel_item(
        db: Session, 
        item_id: UUID, 
        cancel_reason: str,
        customer_id: Optional[UUID] = None
    ) -> OrderItem:
        """取消订单项"""
        
        item = OrderItemService.get_order_item_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="订单项不存在"
            )
        
        # 检查权限
        if customer_id and item.order.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限取消此订单项"
            )
        
        # 检查是否可以取消
        if not item.can_cancel:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="此商品不允许取消"
            )
        
        if item.status in [OrderItemStatus.SHIPPED, OrderItemStatus.DELIVERED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="已发货商品无法取消，请申请退货"
            )
        
        # 更新状态
        item.status = OrderItemStatus.CANCELLED
        item.is_cancelled = True
        item.cancelled_quantity = item.quantity
        item.cancel_reason = cancel_reason
        item.cancelled_at = datetime.utcnow()
        item.updated_at = datetime.utcnow()
        
        # 重新计算订单总金额
        OrderItemService._recalculate_order_total(db, item.order)
        
        db.commit()
        db.refresh(item)
        
        return item
    
    @staticmethod
    def initiate_item_return(
        db: Session, 
        item_id: UUID, 
        return_quantity: int,
        return_reason: str,
        customer_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """发起商品退货"""
        
        item = OrderItemService.get_order_item_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="订单项不存在"
            )
        
        # 检查权限
        if customer_id and item.order.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限退货此商品"
            )
        
        # 检查是否可以退货
        if not item.can_return:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="此商品不允许退货"
            )
        
        if item.status not in [OrderItemStatus.DELIVERED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只有已送达的商品才能申请退货"
            )
        
        # 检查退货数量
        max_returnable = item.delivered_quantity - item.returned_quantity
        if return_quantity > max_returnable:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"最多可退货 {max_returnable} 件"
            )
        
        # 这里应该创建退货记录，简化处理
        # 实际项目中需要创建 OrderReturn 记录
        
        return {
            "message": "退货申请已提交",
            "item_id": item_id,
            "return_quantity": return_quantity,
            "return_reason": return_reason
        }
    
    @staticmethod
    def _recalculate_order_total(db: Session, order: Order):
        """重新计算订单总金额"""
        
        # 获取所有未取消的订单项
        active_items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id,
            OrderItem.status != OrderItemStatus.CANCELLED
        ).all()
        
        subtotal = sum(item.subtotal for item in active_items)
        discount_amount = sum(item.discount_amount for item in active_items)
        tax_amount = sum(item.tax_amount for item in active_items)
        
        order.subtotal = subtotal
        order.discount_amount = discount_amount
        order.tax_amount = tax_amount
        order.total_amount = subtotal - discount_amount + tax_amount + order.shipping_amount
        order.updated_at = datetime.utcnow()
        
        # 如果没有有效商品了，取消订单
        if not active_items:
            order.status = OrderStatus.CANCELLED
            order.cancelled_at = datetime.utcnow()
    
    @staticmethod
    def get_order_items_summary(db: Session, order_id: UUID) -> Dict[str, Any]:
        """获取订单商品汇总信息"""
        
        items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        
        summary = {
            "total_items": len(items),
            "total_quantity": sum(item.quantity for item in items),
            "pending_items": len([item for item in items if item.status == OrderItemStatus.PENDING]),
            "shipped_items": len([item for item in items if item.status == OrderItemStatus.SHIPPED]),
            "delivered_items": len([item for item in items if item.status == OrderItemStatus.DELIVERED]),
            "cancelled_items": len([item for item in items if item.status == OrderItemStatus.CANCELLED]),
            "returned_items": len([item for item in items if item.status == OrderItemStatus.RETURNED]),
            "can_modify": any(item.status in [OrderItemStatus.PENDING, OrderItemStatus.CONFIRMED] for item in items),
            "can_cancel": any(item.can_cancel and item.status not in [OrderItemStatus.SHIPPED, OrderItemStatus.DELIVERED] for item in items)
        }
        
        return summary
