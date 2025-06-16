import uuid
import random
import string
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_, and_

from app.order.return_.models import OrderReturn, ReturnStatus, ReturnReason, ReturnAction, return_item
from app.order.return_.schema import (
    ReturnCreate, ReturnStatusUpdate, ReturnApprove, ReturnReject,
    ReturnReceive, ReturnRefund, ReturnFilter, ReturnListParams,
    UpdateReturnTracking
)
from app.order.models import Order


class ReturnService:
    @staticmethod
    def generate_return_number() -> str:
        """生成退货单号，格式为：RT + 年月日 + 6位随机数字"""
        date_prefix = datetime.now().strftime("%Y%m%d")
        random_suffix = ''.join(random.choices(string.digits, k=6))
        return f"RT{date_prefix}{random_suffix}"

    @staticmethod
    def create_return(db: Session, return_data: ReturnCreate, customer_id: Optional[uuid.UUID] = None) -> OrderReturn:
        """创建退货申请"""
        # 检查订单是否存在
        order = db.query(Order).filter(Order.id == return_data.order_id).first()
        if not order:
            raise ValueError(f"订单 {return_data.order_id} 不存在")
        
        # 验证订单所有权（如果提供了客户ID）
        if customer_id and order.customer_id != customer_id:
            raise ValueError("无权为此订单创建退货申请")
        
        # 创建退货记录
        return_record = OrderReturn(
            id=uuid.uuid4(),
            order_id=return_data.order_id,
            return_number=ReturnService.generate_return_number(),
            status=ReturnStatus.PENDING,
            reason=return_data.reason,
            reason_detail=return_data.reason_detail,
            requested_action=return_data.requested_action,
            customer_comment=return_data.customer_comment,
            images=return_data.images,
            attachments=return_data.attachments,
            customer_needs_to_ship=(return_data.requested_action != ReturnAction.REFUND)  # 如果只是退款，不需要退货
        )
        
        db.add(return_record)
        db.flush()  # 获取退货ID
        
        # 关联订单项
        for item_data in return_data.items:
            # 检查订单项是否存在
            from app.order.models import OrderItem
            item = db.query(OrderItem).filter(
                OrderItem.id == item_data.order_item_id,
                OrderItem.order_id == return_data.order_id
            ).first()
            
            if not item:
                raise ValueError(f"订单项 {item_data.order_item_id} 不存在")
            
            # 添加到退货项关联表
            stmt = return_item.insert().values(
                return_id=return_record.id,
                order_item_id=item_data.order_item_id,
                quantity=item_data.quantity,
                reason=item_data.reason,
                reason_detail=item_data.reason_detail
            )
            db.execute(stmt)
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def get_return_by_id(db: Session, return_id: uuid.UUID) -> Optional[OrderReturn]:
        """通过ID获取退货记录"""
        return db.query(OrderReturn).filter(OrderReturn.id == return_id).first()

    @staticmethod
    def get_return_by_number(db: Session, return_number: str) -> Optional[OrderReturn]:
        """通过退货单号获取退货记录"""
        return db.query(OrderReturn).filter(OrderReturn.return_number == return_number).first()

    @staticmethod
    def get_returns_by_order_id(db: Session, order_id: uuid.UUID) -> List[OrderReturn]:
        """获取订单的所有退货记录"""
        return db.query(OrderReturn).filter(OrderReturn.order_id == order_id).all()

    @staticmethod
    def get_returns_by_customer_id(db: Session, customer_id: uuid.UUID, page: int = 1, page_size: int = 20) -> Tuple[List[OrderReturn], int]:
        """获取客户的所有退货记录"""
        query = db.query(OrderReturn).join(Order).filter(Order.customer_id == customer_id)
        total = query.count()
        
        offset = (page - 1) * page_size
        returns = query.order_by(desc(OrderReturn.created_at)).offset(offset).limit(page_size).all()
        
        return returns, total

    @staticmethod
    def get_returns(db: Session, params: ReturnListParams) -> Tuple[List[OrderReturn], int]:
        """获取退货记录列表，支持分页、排序和过滤"""
        query = db.query(OrderReturn)
        
        # 应用过滤条件
        if params.filters:
            filters = params.filters
            if filters.order_id:
                query = query.filter(OrderReturn.order_id == filters.order_id)
            if filters.return_number:
                query = query.filter(OrderReturn.return_number.ilike(f"%{filters.return_number}%"))
            if filters.status:
                query = query.filter(OrderReturn.status == filters.status)
            if filters.reason:
                query = query.filter(OrderReturn.reason == filters.reason)
            if filters.requested_action:
                query = query.filter(OrderReturn.requested_action == filters.requested_action)
            if filters.approved_action:
                query = query.filter(OrderReturn.approved_action == filters.approved_action)
            if filters.date_from:
                query = query.filter(OrderReturn.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(OrderReturn.created_at <= filters.date_to)
            if filters.customer_id:
                query = query.join(Order).filter(Order.customer_id == filters.customer_id)
        
        # 获取总数
        total = query.count()
        
        # 应用排序
        if params.sort_desc:
            query = query.order_by(desc(getattr(OrderReturn, params.sort_by)))
        else:
            query = query.order_by(asc(getattr(OrderReturn, params.sort_by)))
        
        # 应用分页
        offset = (params.page - 1) * params.page_size
        query = query.offset(offset).limit(params.page_size)
        
        return query.all(), total

    @staticmethod
    def update_return_status(db: Session, return_id: uuid.UUID, status_data: ReturnStatusUpdate, handler_id: Optional[uuid.UUID] = None, handler_name: Optional[str] = None) -> Optional[OrderReturn]:
        """更新退货状态"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 更新状态
        old_status = return_record.status
        return_record.status = status_data.status
        
        # 更新处理信息
        if handler_id:
            return_record.handler_id = handler_id
        if handler_name:
            return_record.handler_name = handler_name
        
        if status_data.admin_comment:
            return_record.admin_comment = status_data.admin_comment
            
        if status_data.resolution_comment:
            return_record.resolution_comment = status_data.resolution_comment
        
        # 更新相关时间戳
        now = datetime.utcnow()
        if status_data.status == ReturnStatus.APPROVED and not return_record.approved_at:
            return_record.approved_at = now
        elif status_data.status == ReturnStatus.RECEIVED and not return_record.received_at:
            return_record.received_at = now
        elif status_data.status == ReturnStatus.REFUNDED and not return_record.refunded_at:
            return_record.refunded_at = now
        elif status_data.status == ReturnStatus.COMPLETED and not return_record.completed_at:
            return_record.completed_at = now
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def approve_return(db: Session, return_id: uuid.UUID, approve_data: ReturnApprove, handler_id: Optional[uuid.UUID] = None, handler_name: Optional[str] = None) -> Optional[OrderReturn]:
        """批准退货申请"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 检查状态
        if return_record.status != ReturnStatus.PENDING:
            raise ValueError(f"只有处于待处理状态的退货申请才能被批准，当前状态: {return_record.status}")
        
        # 更新批准信息
        return_record.status = ReturnStatus.APPROVED
        return_record.approved_action = approve_data.approved_action
        return_record.approved_at = datetime.utcnow()
        return_record.handler_id = handler_id or return_record.handler_id
        return_record.handler_name = handler_name or return_record.handler_name
        
        # 更新退款信息
        if approve_data.refund_amount:
            return_record.refund_amount = approve_data.refund_amount
            return_record.refund_tax = approve_data.refund_tax or 0
            return_record.refund_shipping = approve_data.refund_shipping or 0
            return_record.refund_total = (
                approve_data.refund_amount +
                (approve_data.refund_tax or 0) +
                (approve_data.refund_shipping or 0)
            )
        
        # 更新物流信息
        return_record.return_shipping_method = approve_data.return_shipping_method
        return_record.return_label_url = approve_data.return_label_url
        return_record.customer_needs_to_ship = approve_data.customer_needs_to_ship
        
        # 更新备注
        if approve_data.admin_comment:
            return_record.admin_comment = approve_data.admin_comment
        if approve_data.resolution_comment:
            return_record.resolution_comment = approve_data.resolution_comment
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def reject_return(db: Session, return_id: uuid.UUID, reject_data: ReturnReject, handler_id: Optional[uuid.UUID] = None, handler_name: Optional[str] = None) -> Optional[OrderReturn]:
        """拒绝退货申请"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 检查状态
        if return_record.status != ReturnStatus.PENDING:
            raise ValueError(f"只有处于待处理状态的退货申请才能被拒绝，当前状态: {return_record.status}")
        
        # 更新拒绝信息
        return_record.status = ReturnStatus.REJECTED
        return_record.handler_id = handler_id or return_record.handler_id
        return_record.handler_name = handler_name or return_record.handler_name
        return_record.resolution_comment = reject_data.resolution_comment
        
        if reject_data.admin_comment:
            return_record.admin_comment = reject_data.admin_comment
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def receive_return(db: Session, return_id: uuid.UUID, receive_data: ReturnReceive, handler_id: Optional[uuid.UUID] = None, handler_name: Optional[str] = None) -> Optional[OrderReturn]:
        """确认收到退货"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 检查状态
        if return_record.status != ReturnStatus.APPROVED:
            raise ValueError(f"只有处于已批准状态的退货申请才能被确认收到，当前状态: {return_record.status}")
        
        # 更新接收信息
        return_record.status = ReturnStatus.RECEIVED
        return_record.received_at = datetime.utcnow()
        return_record.handler_id = handler_id or return_record.handler_id
        return_record.handler_name = handler_name or return_record.handler_name
        
        if receive_data.admin_comment:
            return_record.admin_comment = receive_data.admin_comment
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def process_refund(db: Session, return_id: uuid.UUID, refund_data: ReturnRefund, handler_id: Optional[uuid.UUID] = None, handler_name: Optional[str] = None) -> Optional[OrderReturn]:
        """处理退款"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 检查状态
        valid_statuses = [ReturnStatus.APPROVED, ReturnStatus.RECEIVED]
        if return_record.status not in valid_statuses:
            raise ValueError(f"只有处于已批准或已收到退货状态的申请才能处理退款，当前状态: {return_record.status}")
        
        # 更新退款信息
        refund_tax = refund_data.refund_tax or 0
        refund_shipping = refund_data.refund_shipping or 0
        refund_total = refund_data.refund_amount + refund_tax + refund_shipping
        
        return_record.refund_amount = refund_data.refund_amount
        return_record.refund_tax = refund_tax
        return_record.refund_shipping = refund_shipping
        return_record.refund_total = refund_total
        return_record.refund_method = refund_data.refund_method
        return_record.refund_transaction_id = refund_data.refund_transaction_id
        
        # 更新状态
        return_record.status = ReturnStatus.REFUNDED
        return_record.refunded_at = datetime.utcnow()
        return_record.handler_id = handler_id or return_record.handler_id
        return_record.handler_name = handler_name or return_record.handler_name
        
        if refund_data.admin_comment:
            return_record.admin_comment = refund_data.admin_comment
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def complete_return(db: Session, return_id: uuid.UUID, admin_comment: Optional[str] = None, handler_id: Optional[uuid.UUID] = None, handler_name: Optional[str] = None) -> Optional[OrderReturn]:
        """完成退货流程"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 检查状态
        valid_statuses = [ReturnStatus.REFUNDED, ReturnStatus.RECEIVED]
        if return_record.status not in valid_statuses:
            raise ValueError(f"只有处于已退款或已收到退货状态的申请才能被标记为完成，当前状态: {return_record.status}")
        
        # 更新状态
        return_record.status = ReturnStatus.COMPLETED
        return_record.completed_at = datetime.utcnow()
        return_record.handler_id = handler_id or return_record.handler_id
        return_record.handler_name = handler_name or return_record.handler_name
        
        if admin_comment:
            return_record.admin_comment = admin_comment
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def cancel_return(db: Session, return_id: uuid.UUID, admin_comment: Optional[str] = None, handler_id: Optional[uuid.UUID] = None, handler_name: Optional[str] = None) -> Optional[OrderReturn]:
        """取消退货申请"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 检查状态
        if return_record.status not in [ReturnStatus.PENDING, ReturnStatus.APPROVED]:
            raise ValueError(f"只有处于待处理或已批准状态的退货申请才能被取消，当前状态: {return_record.status}")
        
        # 更新状态
        return_record.status = ReturnStatus.CANCELLED
        return_record.handler_id = handler_id or return_record.handler_id
        return_record.handler_name = handler_name or return_record.handler_name
        
        if admin_comment:
            return_record.admin_comment = admin_comment
        
        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def update_return_tracking(db: Session, return_id: uuid.UUID, tracking_data: UpdateReturnTracking) -> Optional[OrderReturn]:
        """更新退货追踪信息"""
        return_record = ReturnService.get_return_by_id(db, return_id)
        if not return_record:
            return None
        
        # 检查状态
        if return_record.status not in [ReturnStatus.APPROVED]:
            raise ValueError(f"只有处于已批准状态的退货申请才能更新追踪信息，当前状态: {return_record.status}")
        
        # 更新追踪信息
        return_record.return_tracking_number = tracking_data.return_tracking_number
        
        if tracking_data.admin_comment:
            return_record.admin_comment = tracking_data.admin_comment
        
        db.commit()
        db.refresh(return_record)
        return return_record
