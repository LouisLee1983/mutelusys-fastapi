from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator, root_validator
from decimal import Decimal

from app.payment.method.models import PaymentMethodStatus
from app.payment.gateway.models import GatewayStatus
from app.payment.transaction.models import TransactionType, TransactionStatus


# 基础响应模型
class ResponseBase(BaseModel):
    code: int = 200
    message: str = "Success"
    data: Any = None


# =================== 支付方式 ===================

# 支付方式基础模型
class PaymentMethodBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    status: PaymentMethodStatus = PaymentMethodStatus.INACTIVE
    
    # 手续费设�?
    fee_type: Optional[str] = "fixed"  # fixed, percentage, mixed
    fee_fixed: float = 0.0
    fee_percentage: float = 0.0
    min_fee: Optional[float] = None
    max_fee: Optional[float] = None
    
    # 显示设置
    icon_url: Optional[str] = None
    logo_url: Optional[str] = None
    sort_order: int = 0
    
    # 支付限制
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    allowed_countries: Optional[List[str]] = None
    allowed_currencies: Optional[List[str]] = None
    
    # 支付网关关联
    gateway_id: Optional[UUID] = None
    gateway_config: Optional[Dict[str, Any]] = None
    
    # 系统设置
    is_default: bool = False
    is_cod: bool = False
    is_online: bool = True
    is_installment: bool = False
    is_public: bool = True
    
    # 额外设置
    meta_data: Optional[Dict[str, Any]] = None


# 创建支付方式
class PaymentMethodCreate(PaymentMethodBase):
    pass


# 更新支付方式
class PaymentMethodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    status: Optional[PaymentMethodStatus] = None
    fee_type: Optional[str] = None
    fee_fixed: Optional[float] = None
    fee_percentage: Optional[float] = None
    min_fee: Optional[float] = None
    max_fee: Optional[float] = None
    icon_url: Optional[str] = None
    logo_url: Optional[str] = None
    sort_order: Optional[int] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    allowed_countries: Optional[List[str]] = None
    allowed_currencies: Optional[List[str]] = None
    gateway_id: Optional[UUID] = None
    gateway_config: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None
    is_cod: Optional[bool] = None
    is_online: Optional[bool] = None
    is_installment: Optional[bool] = None
    is_public: Optional[bool] = None
    meta_data: Optional[Dict[str, Any]] = None


# 支付方式响应
class PaymentMethodResponse(PaymentMethodBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 支付方式详情响应
class PaymentMethodDetailResponse(ResponseBase):
    data: Optional[PaymentMethodResponse] = None


# 支付方式列表响应
class PaymentMethodListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }


# =================== 支付网关 ===================

# 支付网关基础模型
class PaymentGatewayBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    status: GatewayStatus = GatewayStatus.INACTIVE
    
    # 网关配置
    api_url: Optional[str] = None
    sandbox_api_url: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    merchant_id: Optional[str] = None
    webhook_url: Optional[str] = None
    callback_url: Optional[str] = None
    
    # 环境设置
    is_sandbox: bool = True
    
    # 安全设置
    encryption_key: Optional[str] = None
    encryption_method: Optional[str] = None
    signature_key: Optional[str] = None
    
    # 支持功能
    supports_refund: bool = False
    supports_partial_refund: bool = False
    supports_installment: bool = False
    supports_recurring: bool = False
    supports_multi_currency: bool = False
    
    # 支持的货币和国家
    supported_currencies: Optional[List[str]] = None
    supported_countries: Optional[List[str]] = None
    
    # 结算信息
    settlement_currency: Optional[str] = None
    settlement_period_days: Optional[int] = None
    
    # 显示设置
    logo_url: Optional[str] = None
    icon_url: Optional[str] = None
    
    # 扩展设置
    config: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None


# 创建支付网关
class PaymentGatewayCreate(PaymentGatewayBase):
    pass


# 更新支付网关
class PaymentGatewayUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[GatewayStatus] = None
    api_url: Optional[str] = None
    sandbox_api_url: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    merchant_id: Optional[str] = None
    webhook_url: Optional[str] = None
    callback_url: Optional[str] = None
    is_sandbox: Optional[bool] = None
    encryption_key: Optional[str] = None
    encryption_method: Optional[str] = None
    signature_key: Optional[str] = None
    supports_refund: Optional[bool] = None
    supports_partial_refund: Optional[bool] = None
    supports_installment: Optional[bool] = None
    supports_recurring: Optional[bool] = None
    supports_multi_currency: Optional[bool] = None
    supported_currencies: Optional[List[str]] = None
    supported_countries: Optional[List[str]] = None
    settlement_currency: Optional[str] = None
    settlement_period_days: Optional[int] = None
    logo_url: Optional[str] = None
    icon_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None


# 支付网关响应
class PaymentGatewayResponse(PaymentGatewayBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 支付网关详情响应
class PaymentGatewayDetailResponse(ResponseBase):
    data: Optional[PaymentGatewayResponse] = None


# 支付网关列表响应
class PaymentGatewayListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }


# =================== 支付交易 ===================

# 支付交易基础模型
class PaymentTransactionBase(BaseModel):
    order_id: Optional[UUID] = None
    payment_method_id: UUID
    transaction_type: TransactionType
    amount: float
    currency_code: str
    fee_amount: float = 0.0
    transaction_id: Optional[str] = None
    parent_transaction_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
    customer_ip: Optional[str] = None
    customer_user_agent: Optional[str] = None
    payment_details: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    note: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


# 创建支付交易
class PaymentTransactionCreate(PaymentTransactionBase):
    pass


# 更新支付交易
class PaymentTransactionUpdate(BaseModel):
    status: Optional[TransactionStatus] = None
    transaction_id: Optional[str] = None
    response_code: Optional[str] = None
    response_message: Optional[str] = None
    gateway_response: Optional[Dict[str, Any]] = None
    is_settled: Optional[bool] = None
    settlement_date: Optional[datetime] = None
    refunded_amount: Optional[float] = None
    is_refundable: Optional[bool] = None
    note: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


# 支付交易响应
class PaymentTransactionResponse(PaymentTransactionBase):
    id: UUID
    status: TransactionStatus
    response_code: Optional[str] = None
    response_message: Optional[str] = None
    gateway_response: Optional[Dict[str, Any]] = None
    is_settled: bool
    settlement_date: Optional[datetime] = None
    refunded_amount: float
    is_refundable: bool
    created_at: datetime
    updated_at: datetime
    expired_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# 支付交易详情响应
class PaymentTransactionDetailResponse(ResponseBase):
    data: Optional[PaymentTransactionResponse] = None


# 支付交易列表响应
class PaymentTransactionListResponse(ResponseBase):
    data: Dict[str, Any] = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "pages": 1
    }


# =================== 支付处理 ===================

# 支付初始化请�?
class PaymentInitRequest(BaseModel):
    order_id: UUID
    payment_method_id: UUID
    amount: float
    currency_code: str
    customer_id: Optional[UUID] = None
    return_url: Optional[str] = None
    cancel_url: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None


# 支付初始化响�?
class PaymentInitResponse(ResponseBase):
    data: Dict[str, Any] = {
        "transaction_id": "",
        "payment_url": None,
        "payment_method": "",
        "amount": 0.0,
        "currency_code": "",
        "status": "",
        "expired_at": None,
        "payment_instructions": None,
        "payment_details": None
    }


# 支付确认请求
class PaymentConfirmRequest(BaseModel):
    transaction_id: UUID
    gateway_response: Optional[Dict[str, Any]] = None
    payment_details: Optional[Dict[str, Any]] = None


# 支付确认响应
class PaymentConfirmResponse(ResponseBase):
    data: Dict[str, Any] = {
        "transaction_id": "",
        "order_id": "",
        "status": "",
        "success": False,
        "message": ""
    }


# 退款请�?
class RefundRequest(BaseModel):
    transaction_id: UUID
    amount: float
    reason: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


# 退款响�?
class RefundResponse(ResponseBase):
    data: Dict[str, Any] = {
        "refund_transaction_id": "",
        "original_transaction_id": "",
        "order_id": "",
        "amount": 0.0,
        "status": "",
        "success": False,
        "message": ""
    }


# 支付回调验证
class PaymentWebhookRequest(BaseModel):
    gateway_code: str
    payload: Dict[str, Any]


# 支付状态查询请�?
class PaymentStatusRequest(BaseModel):
    transaction_id: Optional[UUID] = None
    order_id: Optional[UUID] = None
    external_transaction_id: Optional[str] = None


# 支付状态查询响�?
class PaymentStatusResponse(ResponseBase):
    data: Dict[str, Any] = {
        "transaction_id": "",
        "order_id": "",
        "payment_method": "",
        "amount": 0.0,
        "currency_code": "",
        "status": "",
        "created_at": "",
        "updated_at": "",
        "payment_details": None
    }
