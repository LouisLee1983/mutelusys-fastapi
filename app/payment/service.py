import uuid
import random
import string
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_, and_, func
from uuid import UUID

from app.payment.method.models import PaymentMethod, PaymentMethodStatus
from app.payment.gateway.models import PaymentGateway, GatewayStatus
from app.payment.transaction.models import PaymentTransaction, TransactionType, TransactionStatus
from app.payment.models import PaymentLog
from app.payment.schema import (
    PaymentMethodCreate, PaymentMethodUpdate,
    PaymentGatewayCreate, PaymentGatewayUpdate,
    PaymentTransactionCreate, PaymentTransactionUpdate,
    PaymentInitRequest, PaymentConfirmRequest, RefundRequest, PaymentStatusRequest, PaymentWebhookRequest
)


class PaymentMethodService:
    @staticmethod
    def create_payment_method(db: Session, payment_method_data: PaymentMethodCreate) -> PaymentMethod:
        """创建支付方式"""
        # 检查支付方式代码是否已存在
        existing = db.query(PaymentMethod).filter(PaymentMethod.code == payment_method_data.code).first()
        if existing:
            raise ValueError(f"支付方式代码 {payment_method_data.code} 已存在")
        
        # 如果设置为默认，先取消其他默认支付方式
        if payment_method_data.is_default:
            db.query(PaymentMethod).filter(PaymentMethod.is_default == True).update({"is_default": False})
        
        # 验证网关ID
        if payment_method_data.gateway_id:
            gateway = db.query(PaymentGateway).filter(PaymentGateway.id == payment_method_data.gateway_id).first()
            if not gateway:
                raise ValueError(f"支付网关 {payment_method_data.gateway_id} 不存在")
        
        # 创建新支付方式
        payment_method = PaymentMethod(
            id=uuid.uuid4(),
            code=payment_method_data.code,
            name=payment_method_data.name,
            description=payment_method_data.description,
            instructions=payment_method_data.instructions,
            status=payment_method_data.status,
            fee_type=payment_method_data.fee_type,
            fee_fixed=payment_method_data.fee_fixed,
            fee_percentage=payment_method_data.fee_percentage,
            min_fee=payment_method_data.min_fee,
            max_fee=payment_method_data.max_fee,
            icon_url=payment_method_data.icon_url,
            logo_url=payment_method_data.logo_url,
            sort_order=payment_method_data.sort_order,
            min_amount=payment_method_data.min_amount,
            max_amount=payment_method_data.max_amount,
            allowed_countries=payment_method_data.allowed_countries,
            allowed_currencies=payment_method_data.allowed_currencies,
            gateway_id=payment_method_data.gateway_id,
            gateway_config=payment_method_data.gateway_config,
            is_default=payment_method_data.is_default,
            is_cod=payment_method_data.is_cod,
            is_online=payment_method_data.is_online,
            is_installment=payment_method_data.is_installment,
            is_public=payment_method_data.is_public,
            meta_data=payment_method_data.meta_data
        )
        
        db.add(payment_method)
        db.commit()
        db.refresh(payment_method)
        return payment_method

    @staticmethod
    def update_payment_method(db: Session, payment_method_id: UUID, update_data: PaymentMethodUpdate) -> Optional[PaymentMethod]:
        """更新支付方式"""
        payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()
        if not payment_method:
            return None
        
        # 获取需要更新的字段
        update_dict = update_data.dict(exclude_unset=True)
        
        # 检查默认支付方式
        if update_dict.get("is_default"):
            db.query(PaymentMethod).filter(PaymentMethod.is_default == True).update({"is_default": False})
        
        # 验证网关ID
        if update_dict.get("gateway_id"):
            gateway = db.query(PaymentGateway).filter(PaymentGateway.id == update_dict["gateway_id"]).first()
            if not gateway:
                raise ValueError(f"支付网关 {update_dict['gateway_id']} 不存在")
        
        # 更新字段
        for key, value in update_dict.items():
            setattr(payment_method, key, value)
        
        db.commit()
        db.refresh(payment_method)
        return payment_method

    @staticmethod
    def get_payment_method_by_id(db: Session, payment_method_id: UUID) -> Optional[PaymentMethod]:
        """通过ID获取支付方式"""
        return db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()

    @staticmethod
    def get_payment_method_by_code(db: Session, code: str) -> Optional[PaymentMethod]:
        """通过代码获取支付方式"""
        return db.query(PaymentMethod).filter(PaymentMethod.code == code).first()

    @staticmethod
    def get_payment_methods(db: Session, skip: int = 0, limit: int = 100, 
                          status: Optional[PaymentMethodStatus] = None,
                          is_public: Optional[bool] = None,
                          gateway_id: Optional[UUID] = None) -> List[PaymentMethod]:
        """获取支付方式列表，支持过滤"""
        query = db.query(PaymentMethod)
        
        # 应用过滤条件
        if status:
            query = query.filter(PaymentMethod.status == status)
        if is_public is not None:
            query = query.filter(PaymentMethod.is_public == is_public)
        if gateway_id:
            query = query.filter(PaymentMethod.gateway_id == gateway_id)
        
        # 应用排序
        query = query.order_by(asc(PaymentMethod.sort_order), asc(PaymentMethod.name))
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def delete_payment_method(db: Session, payment_method_id: UUID) -> bool:
        """删除支付方式"""
        payment_method = db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()
        if not payment_method:
            return False
        
        # 检查是否有关联的交易
        transactions = db.query(PaymentTransaction).filter(
            PaymentTransaction.payment_method_id == payment_method_id
        ).first()
        
        if transactions:
            # 存在关联交易，将状态设为不可用
            payment_method.status = PaymentMethodStatus.INACTIVE
            payment_method.is_public = False
        else:
            # 不存在关联交易，可以安全删除
            db.delete(payment_method)
        
        db.commit()
        return True


class PaymentGatewayService:
    @staticmethod
    def create_payment_gateway(db: Session, gateway_data: PaymentGatewayCreate) -> PaymentGateway:
        """创建支付网关"""
        # 检查支付网关代码是否已存在
        existing = db.query(PaymentGateway).filter(PaymentGateway.code == gateway_data.code).first()
        if existing:
            raise ValueError(f"支付网关代码 {gateway_data.code} 已存在")
        
        # 创建新支付网关
        gateway = PaymentGateway(
            id=uuid.uuid4(),
            code=gateway_data.code,
            name=gateway_data.name,
            description=gateway_data.description,
            status=gateway_data.status,
            api_url=gateway_data.api_url,
            sandbox_api_url=gateway_data.sandbox_api_url,
            api_key=gateway_data.api_key,
            api_secret=gateway_data.api_secret,
            merchant_id=gateway_data.merchant_id,
            webhook_url=gateway_data.webhook_url,
            callback_url=gateway_data.callback_url,
            is_sandbox=gateway_data.is_sandbox,
            encryption_key=gateway_data.encryption_key,
            encryption_method=gateway_data.encryption_method,
            signature_key=gateway_data.signature_key,
            supports_refund=gateway_data.supports_refund,
            supports_partial_refund=gateway_data.supports_partial_refund,
            supports_installment=gateway_data.supports_installment,
            supports_recurring=gateway_data.supports_recurring,
            supports_multi_currency=gateway_data.supports_multi_currency,
            supported_currencies=gateway_data.supported_currencies,
            supported_countries=gateway_data.supported_countries,
            settlement_currency=gateway_data.settlement_currency,
            settlement_period_days=gateway_data.settlement_period_days,
            logo_url=gateway_data.logo_url,
            icon_url=gateway_data.icon_url,
            config=gateway_data.config,
            meta_data=gateway_data.meta_data
        )
        
        db.add(gateway)
        db.commit()
        db.refresh(gateway)
        return gateway

    @staticmethod
    def update_payment_gateway(db: Session, gateway_id: UUID, update_data: PaymentGatewayUpdate) -> Optional[PaymentGateway]:
        """更新支付网关"""
        gateway = db.query(PaymentGateway).filter(PaymentGateway.id == gateway_id).first()
        if not gateway:
            return None
        
        # 获取需要更新的字段
        update_dict = update_data.dict(exclude_unset=True)
        
        # 更新字段
        for key, value in update_dict.items():
            setattr(gateway, key, value)
        
        db.commit()
        db.refresh(gateway)
        return gateway

    @staticmethod
    def get_payment_gateway_by_id(db: Session, gateway_id: UUID) -> Optional[PaymentGateway]:
        """通过ID获取支付网关"""
        return db.query(PaymentGateway).filter(PaymentGateway.id == gateway_id).first()

    @staticmethod
    def get_payment_gateway_by_code(db: Session, code: str) -> Optional[PaymentGateway]:
        """通过代码获取支付网关"""
        return db.query(PaymentGateway).filter(PaymentGateway.code == code).first()

    @staticmethod
    def get_payment_gateways(db: Session, skip: int = 0, limit: int = 100, 
                           status: Optional[GatewayStatus] = None) -> List[PaymentGateway]:
        """获取支付网关列表，支持过滤"""
        query = db.query(PaymentGateway)
        
        # 应用过滤条件
        if status:
            query = query.filter(PaymentGateway.status == status)
        
        # 应用排序
        query = query.order_by(asc(PaymentGateway.name))
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def delete_payment_gateway(db: Session, gateway_id: UUID) -> bool:
        """删除支付网关"""
        gateway = db.query(PaymentGateway).filter(PaymentGateway.id == gateway_id).first()
        if not gateway:
            return False
        
        # 检查是否有关联的支付方式
        payment_methods = db.query(PaymentMethod).filter(
            PaymentMethod.gateway_id == gateway_id
        ).first()
        
        if payment_methods:
            # 存在关联支付方式，将状态设为不可用
            gateway.status = GatewayStatus.INACTIVE
        else:
            # 不存在关联支付方式，可以安全删除
            db.delete(gateway)
        
        db.commit()
        return True


class PaymentTransactionService:
    @staticmethod
    def create_transaction(db: Session, transaction_data: PaymentTransactionCreate) -> PaymentTransaction:
        """创建支付交易记录"""
        # 验证支付方式
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == transaction_data.payment_method_id
        ).first()
        if not payment_method:
            raise ValueError(f"支付方式 {transaction_data.payment_method_id} 不存在")
        
        # 验证父交易（如果有）
        if transaction_data.parent_transaction_id:
            parent_transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.id == transaction_data.parent_transaction_id
            ).first()
            if not parent_transaction:
                raise ValueError(f"父交易 {transaction_data.parent_transaction_id} 不存在")
        
        # 设置有效期（默认24小时）
        expired_at = datetime.utcnow() + timedelta(hours=24)
        
        # 创建交易记录
        transaction = PaymentTransaction(
            id=uuid.uuid4(),
            order_id=transaction_data.order_id,
            payment_method_id=transaction_data.payment_method_id,
            transaction_type=transaction_data.transaction_type,
            status=TransactionStatus.PENDING,  # 初始状态为处理中
            amount=transaction_data.amount,
            currency_code=transaction_data.currency_code,
            fee_amount=transaction_data.fee_amount,
            transaction_id=transaction_data.transaction_id,
            parent_transaction_id=transaction_data.parent_transaction_id,
            customer_id=transaction_data.customer_id,
            customer_ip=transaction_data.customer_ip,
            customer_user_agent=transaction_data.customer_user_agent,
            payment_details=transaction_data.payment_details,
            description=transaction_data.description,
            note=transaction_data.note,
            meta_data=transaction_data.meta_data,
            is_settled=False,
            refunded_amount=0.0,
            is_refundable=False,
            expired_at=expired_at
        )
        
        db.add(transaction)
        
        # 记录操作日志
        log = PaymentLog(
            id=uuid.uuid4(),
            transaction_id=transaction.id,
            order_id=transaction_data.order_id,
            action="create_transaction",
            status="success",
            message=f"创建{transaction_data.transaction_type}交易",
            details={
                "amount": transaction_data.amount,
                "currency": transaction_data.currency_code,
                "payment_method": str(transaction_data.payment_method_id)
            },
            ip_address=transaction_data.customer_ip
        )
        db.add(log)
        
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def update_transaction(db: Session, transaction_id: UUID, 
                         update_data: PaymentTransactionUpdate,
                         user_id: Optional[UUID] = None,
                         ip_address: Optional[str] = None) -> Optional[PaymentTransaction]:
        """更新交易记录"""
        transaction = db.query(PaymentTransaction).filter(PaymentTransaction.id == transaction_id).first()
        if not transaction:
            return None
        
        # 获取需要更新的字段
        update_dict = update_data.dict(exclude_unset=True)
        
        # 记录原状态
        old_status = transaction.status
        
        # 更新字段
        for key, value in update_dict.items():
            setattr(transaction, key, value)
        
        # 记录操作日志
        log = PaymentLog(
            id=uuid.uuid4(),
            transaction_id=transaction.id,
            order_id=transaction.order_id,
            user_id=user_id,
            action="update_transaction",
            status="success",
            message=f"更新交易状态：{old_status} -> {transaction.status}",
            details=update_dict,
            ip_address=ip_address
        )
        db.add(log)
        
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: UUID) -> Optional[PaymentTransaction]:
        """通过ID获取交易记录"""
        return db.query(PaymentTransaction).filter(PaymentTransaction.id == transaction_id).first()

    @staticmethod
    def get_transactions_by_order_id(db: Session, order_id: UUID) -> List[PaymentTransaction]:
        """获取订单的所有交易记录"""
        return db.query(PaymentTransaction).filter(PaymentTransaction.order_id == order_id).all()

    @staticmethod
    def get_transactions_by_customer_id(db: Session, customer_id: UUID, 
                                      skip: int = 0, limit: int = 100) -> List[PaymentTransaction]:
        """获取客户的所有交易记录"""
        return db.query(PaymentTransaction).filter(
            PaymentTransaction.customer_id == customer_id
        ).order_by(desc(PaymentTransaction.created_at)).offset(skip).limit(limit).all()

    @staticmethod
    def get_transactions(db: Session, skip: int = 0, limit: int = 100, 
                       status: Optional[TransactionStatus] = None,
                       transaction_type: Optional[TransactionType] = None,
                       from_date: Optional[datetime] = None,
                       to_date: Optional[datetime] = None) -> List[PaymentTransaction]:
        """获取交易记录列表，支持过滤"""
        query = db.query(PaymentTransaction)
        
        # 应用过滤条件
        if status:
            query = query.filter(PaymentTransaction.status == status)
        if transaction_type:
            query = query.filter(PaymentTransaction.transaction_type == transaction_type)
        if from_date:
            query = query.filter(PaymentTransaction.created_at >= from_date)
        if to_date:
            query = query.filter(PaymentTransaction.created_at <= to_date)
        
        # 应用排序
        query = query.order_by(desc(PaymentTransaction.created_at))
        
        return query.offset(skip).limit(limit).all()


class PaymentProcessingService:
    @staticmethod
    def initialize_payment(db: Session, payment_data: PaymentInitRequest) -> Dict[str, Any]:
        """初始化支付流程"""
        # 验证支付方式
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_data.payment_method_id,
            PaymentMethod.status == PaymentMethodStatus.ACTIVE
        ).first()
        
        if not payment_method:
            raise ValueError(f"支付方式不存在或不可用")
        
        # 验证支付金额
        if payment_method.min_amount and payment_data.amount < payment_method.min_amount:
            raise ValueError(f"支付金额不能低于 {payment_method.min_amount}")
        
        if payment_method.max_amount and payment_data.amount > payment_method.max_amount:
            raise ValueError(f"支付金额不能高于 {payment_method.max_amount}")
        
        # 验证币种
        if payment_method.allowed_currencies and payment_data.currency_code not in payment_method.allowed_currencies:
            raise ValueError(f"不支持的币种: {payment_data.currency_code}")
        
        # 计算手续费
        fee_amount = 0.0
        if payment_method.fee_type == "fixed":
            fee_amount = payment_method.fee_fixed
        elif payment_method.fee_type == "percentage":
            fee_amount = payment_data.amount * (payment_method.fee_percentage / 100)
        elif payment_method.fee_type == "mixed":
            fee_amount = payment_method.fee_fixed + (payment_data.amount * (payment_method.fee_percentage / 100))
        
        # 应用最小/最大手续费限制
        if payment_method.min_fee and fee_amount < payment_method.min_fee:
            fee_amount = payment_method.min_fee
        if payment_method.max_fee and fee_amount > payment_method.max_fee:
            fee_amount = payment_method.max_fee
        
        # 创建交易记录
        transaction_data = PaymentTransactionCreate(
            order_id=payment_data.order_id,
            payment_method_id=payment_data.payment_method_id,
            transaction_type=TransactionType.PAYMENT,
            amount=payment_data.amount,
            currency_code=payment_data.currency_code,
            fee_amount=fee_amount,
            customer_id=payment_data.customer_id,
            meta_data=payment_data.meta_data,
            payment_details={
                "return_url": payment_data.return_url,
                "cancel_url": payment_data.cancel_url,
                "custom_fields": payment_data.custom_fields
            }
        )
        
        transaction = PaymentTransactionService.create_transaction(db, transaction_data)
        
        # 根据支付方式类型准备响应
        payment_url = None
        payment_instructions = None
        payment_details = None
        
        # 判断是否为在线支付，需要跳转或显示支付指引
        if payment_method.is_online:
            if payment_method.gateway_id:
                # 获取网关信息
                gateway = db.query(PaymentGateway).filter(
                    PaymentGateway.id == payment_method.gateway_id,
                    PaymentGateway.status == GatewayStatus.ACTIVE
                ).first()
                
                if gateway:
                    # 这里应该调用实际的支付网关接口，获取支付URL
                    # 简化版本，仅返回模拟数据
                    payment_url = f"{gateway.api_url}/pay?transaction_id={transaction.id}"
            else:
                # 无需网关的支付方式，如银行转账
                payment_instructions = payment_method.instructions
                payment_details = {
                    "method_name": payment_method.name,
                    "method_code": payment_method.code
                }
        else:
            # 货到付款等线下支付方式
            payment_instructions = payment_method.instructions
        
        return {
            "transaction_id": str(transaction.id),
            "payment_url": payment_url,
            "payment_method": payment_method.name,
            "amount": payment_data.amount,
            "currency_code": payment_data.currency_code,
            "status": transaction.status,
            "expired_at": transaction.expired_at,
            "payment_instructions": payment_instructions,
            "payment_details": payment_details
        }

    @staticmethod
    def confirm_payment(db: Session, confirm_data: PaymentConfirmRequest,
                      user_id: Optional[UUID] = None, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """确认支付完成"""
        # 获取交易记录
        transaction = db.query(PaymentTransaction).filter(
            PaymentTransaction.id == confirm_data.transaction_id
        ).first()
        
        if not transaction:
            raise ValueError("交易记录不存在")
        
        if transaction.status != TransactionStatus.PENDING:
            raise ValueError(f"交易状态不正确：{transaction.status}")
        
        # 获取支付方式
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == transaction.payment_method_id
        ).first()
        
        if not payment_method:
            raise ValueError("支付方式不存在")
        
        # 更新交易状态为成功
        update_data = PaymentTransactionUpdate(
            status=TransactionStatus.SUCCESS,
            gateway_response=confirm_data.gateway_response,
            payment_details=confirm_data.payment_details,
            is_refundable=True,  # 成功支付后可以退款
            response_code="SUCCESS",
            response_message="支付成功"
        )
        
        updated_transaction = PaymentTransactionService.update_transaction(
            db, transaction.id, update_data, user_id, ip_address
        )
        
        return {
            "transaction_id": str(updated_transaction.id),
            "order_id": str(updated_transaction.order_id) if updated_transaction.order_id else None,
            "status": updated_transaction.status,
            "success": True,
            "message": "支付成功"
        }

    @staticmethod
    def process_refund(db: Session, refund_data: RefundRequest,
                     user_id: Optional[UUID] = None, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """处理退款"""
        # 获取原交易
        original_transaction = db.query(PaymentTransaction).filter(
            PaymentTransaction.id == refund_data.transaction_id
        ).first()
        
        if not original_transaction:
            raise ValueError("原交易记录不存在")
        
        if original_transaction.status != TransactionStatus.SUCCESS:
            raise ValueError(f"原交易状态不允许退款：{original_transaction.status}")
        
        if not original_transaction.is_refundable:
            raise ValueError("该交易不允许退款")
        
        # 验证退款金额
        if refund_data.amount <= 0:
            raise ValueError("退款金额必须大于0")
        
        if refund_data.amount > (original_transaction.amount - original_transaction.refunded_amount):
            raise ValueError("退款金额超过可退款金额")
        
        # 获取支付方式
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == original_transaction.payment_method_id
        ).first()
        
        if not payment_method:
            raise ValueError("支付方式不存在")
        
        # 验证支付方式是否支持退款
        if payment_method.gateway_id:
            gateway = db.query(PaymentGateway).filter(
                PaymentGateway.id == payment_method.gateway_id
            ).first()
            
            if not gateway or not gateway.supports_refund:
                raise ValueError("该支付方式不支持在线退款")
        
        # 创建退款交易
        refund_transaction_data = PaymentTransactionCreate(
            order_id=original_transaction.order_id,
            payment_method_id=original_transaction.payment_method_id,
            transaction_type=TransactionType.REFUND,
            amount=refund_data.amount,
            currency_code=original_transaction.currency_code,
            fee_amount=0.0,  # 退款通常不收手续费
            parent_transaction_id=original_transaction.id,
            customer_id=original_transaction.customer_id,
            description=f"退款：{refund_data.reason}" if refund_data.reason else "退款",
            meta_data=refund_data.meta_data
        )
        
        refund_transaction = PaymentTransactionService.create_transaction(db, refund_transaction_data)
        
        # 更新原交易的退款金额
        original_transaction.refunded_amount += refund_data.amount
        
        # 如果已全额退款，更新状态和不可退款标志
        if original_transaction.refunded_amount >= original_transaction.amount:
            original_transaction.status = TransactionStatus.REFUNDED
            original_transaction.is_refundable = False
        else:
            original_transaction.status = TransactionStatus.PARTIALLY_REFUNDED
        
        # 更新退款交易状态为成功（简化流程，实际可能需要异步处理）
        update_data = PaymentTransactionUpdate(
            status=TransactionStatus.SUCCESS,
            response_code="SUCCESS",
            response_message="退款成功"
        )
        
        updated_refund = PaymentTransactionService.update_transaction(
            db, refund_transaction.id, update_data, user_id, ip_address
        )
        
        db.commit()
        
        return {
            "refund_transaction_id": str(updated_refund.id),
            "original_transaction_id": str(original_transaction.id),
            "order_id": str(original_transaction.order_id) if original_transaction.order_id else None,
            "amount": refund_data.amount,
            "status": updated_refund.status,
            "success": True,
            "message": "退款处理成功"
        }

    @staticmethod
    def check_payment_status(db: Session, status_request: PaymentStatusRequest) -> Dict[str, Any]:
        """检查支付状态"""
        transaction = None
        
        # 根据提供的参数查询交易
        if status_request.transaction_id:
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.id == status_request.transaction_id
            ).first()
        elif status_request.order_id:
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.order_id == status_request.order_id,
                PaymentTransaction.transaction_type == TransactionType.PAYMENT
            ).order_by(desc(PaymentTransaction.created_at)).first()
        elif status_request.external_transaction_id:
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.transaction_id == status_request.external_transaction_id
            ).first()
        
        if not transaction:
            raise ValueError("未找到交易记录")
        
        # 获取支付方式
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == transaction.payment_method_id
        ).first()
        
        payment_method_name = payment_method.name if payment_method else "未知支付方式"
        
        return {
            "transaction_id": str(transaction.id),
            "order_id": str(transaction.order_id) if transaction.order_id else None,
            "payment_method": payment_method_name,
            "amount": transaction.amount,
            "currency_code": transaction.currency_code,
            "status": transaction.status,
            "created_at": transaction.created_at.isoformat(),
            "updated_at": transaction.updated_at.isoformat(),
            "payment_details": transaction.payment_details
        }

    @staticmethod
    def handle_payment_webhook(db: Session, webhook_data: PaymentWebhookRequest, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """处理支付网关回调"""
        # 获取支付网关
        gateway = db.query(PaymentGateway).filter(
            PaymentGateway.code == webhook_data.gateway_code
        ).first()
        
        if not gateway:
            raise ValueError(f"支付网关不存在: {webhook_data.gateway_code}")
        
        # 从回调数据中提取交易ID（不同网关可能有不同格式）
        # 此处简化，假设回调数据中包含transaction_id字段
        external_transaction_id = webhook_data.payload.get("transaction_id")
        order_id = webhook_data.payload.get("order_id")
        transaction = None
        
        if external_transaction_id:
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.transaction_id == external_transaction_id
            ).first()
        elif order_id:
            # 尝试通过订单ID查找
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.order_id == order_id,
                PaymentTransaction.transaction_type == TransactionType.PAYMENT
            ).order_by(desc(PaymentTransaction.created_at)).first()
        
        if not transaction:
            # 记录未知交易的回调
            log = PaymentLog(
                id=uuid.uuid4(),
                action="webhook_unknown_transaction",
                status="failure",
                message=f"收到未知交易的支付回调",
                details=webhook_data.payload,
                ip_address=ip_address
            )
            db.add(log)
            db.commit()
            raise ValueError("交易记录不存在")
        
        # 提取支付状态（不同网关可能有不同格式）
        payment_status = webhook_data.payload.get("status")
        new_status = None
        
        if payment_status == "success" or payment_status == "paid" or payment_status == "completed":
            new_status = TransactionStatus.SUCCESS
        elif payment_status == "failed" or payment_status == "declined":
            new_status = TransactionStatus.FAILED
        elif payment_status == "cancelled":
            new_status = TransactionStatus.CANCELLED
        elif payment_status == "pending":
            new_status = TransactionStatus.PENDING
        else:
            # 未知状态
            log = PaymentLog(
                id=uuid.uuid4(),
                transaction_id=transaction.id,
                order_id=transaction.order_id,
                action="webhook_unknown_status",
                status="failure",
                message=f"收到未知状态的支付回调: {payment_status}",
                details=webhook_data.payload,
                ip_address=ip_address
            )
            db.add(log)
            db.commit()
            raise ValueError(f"未知的支付状态: {payment_status}")
        
        # 更新交易状态
        update_data = PaymentTransactionUpdate(
            status=new_status,
            transaction_id=external_transaction_id or transaction.transaction_id,
            gateway_response=webhook_data.payload,
            response_code=webhook_data.payload.get("response_code"),
            response_message=webhook_data.payload.get("response_message"),
            is_refundable=new_status == TransactionStatus.SUCCESS  # 成功支付后可以退款
        )
        
        updated_transaction = PaymentTransactionService.update_transaction(
            db, transaction.id, update_data, None, ip_address
        )
        
        # 记录webhook处理日志
        log = PaymentLog(
            id=uuid.uuid4(),
            transaction_id=transaction.id,
            order_id=transaction.order_id,
            action="webhook_processed",
            status="success",
            message=f"处理支付回调: {payment_status} -> {new_status}",
            details=webhook_data.payload,
            ip_address=ip_address
        )
        db.add(log)
        db.commit()
        
        return {
            "transaction_id": str(updated_transaction.id),
            "order_id": str(updated_transaction.order_id) if updated_transaction.order_id else None,
            "status": updated_transaction.status,
            "success": True,
            "message": "支付回调处理成功"
        }
