from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_admin_user
from app.payment.method.models import PaymentMethodStatus
from app.payment.gateway.models import GatewayStatus
from app.payment.transaction.models import TransactionType, TransactionStatus
from app.payment.schema import (
    PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse, PaymentMethodDetailResponse, PaymentMethodListResponse,
    PaymentGatewayCreate, PaymentGatewayUpdate, PaymentGatewayResponse, PaymentGatewayDetailResponse, PaymentGatewayListResponse,
    PaymentTransactionResponse, PaymentTransactionDetailResponse, PaymentTransactionListResponse,
    PaymentInitRequest, PaymentInitResponse, PaymentConfirmRequest, PaymentConfirmResponse,
    RefundRequest, RefundResponse, PaymentStatusRequest, PaymentStatusResponse, PaymentWebhookRequest,
    ResponseBase
)
from app.payment.service import (
    PaymentMethodService, PaymentGatewayService, PaymentTransactionService, PaymentProcessingService
)
from app.security.user.models import User


# 创建路由
router = APIRouter()


# ==================== 客户端接口 ====================

@router.post("/initialize", response_model=PaymentInitResponse)
async def initialize_payment(
    payment_data: PaymentInitRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """初始化支付
    
    为订单创建支付交易并返回支付信息
    """
    try:
        # 添加客户信息
        if current_user.customer_id:
            payment_data.customer_id = current_user.customer_id
        
        # 添加客户IP
        client_ip = request.client.host if request.client else None
        
        result = PaymentProcessingService.initialize_payment(db, payment_data)
        
        return PaymentInitResponse(
            data=result,
            message="支付初始化成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付初始化失败: {str(e)}"
        )


@router.post("/confirm", response_model=PaymentConfirmResponse)
async def confirm_payment(
    confirm_data: PaymentConfirmRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """确认支付
    
    确认支付完成并更新交易状态
    """
    try:
        result = PaymentProcessingService.confirm_payment(
            db, 
            confirm_data,
            current_user.id,
            request.client.host if request.client else None
        )
        
        return PaymentConfirmResponse(
            data=result,
            message="支付确认成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付确认失败: {str(e)}"
        )


@router.post("/status", response_model=PaymentStatusResponse)
async def check_payment_status(
    status_request: PaymentStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询支付状态
    
    查询交易的支付状态
    """
    try:
        result = PaymentProcessingService.check_payment_status(db, status_request)
        
        return PaymentStatusResponse(
            data=result,
            message="查询支付状态成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询支付状态失败: {str(e)}"
        )


@router.get("/methods", response_model=PaymentMethodListResponse)
async def get_available_payment_methods(
    currency_code: Optional[str] = Query(None),
    country_code: Optional[str] = Query(None),
    amount: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    """获取可用的支付方式
    
    获取所有激活且公开的支付方式
    """
    # 获取所有公开可用的支付方式
    payment_methods = PaymentMethodService.get_payment_methods(
        db, 
        status=PaymentMethodStatus.ACTIVE,
        is_public=True
    )
    
    # 如果提供了过滤条件，进行过滤
    filtered_methods = []
    for method in payment_methods:
        # 过滤币种
        if currency_code and method.allowed_currencies and currency_code not in method.allowed_currencies:
            continue
        
        # 过滤国家
        if country_code:
            if method.excluded_countries and country_code in method.excluded_countries:
                continue
            if method.allowed_countries and country_code not in method.allowed_countries:
                continue
        
        # 过滤金额
        if amount:
            if method.min_amount and amount < method.min_amount:
                continue
            if method.max_amount and amount > method.max_amount:
                continue
        
        filtered_methods.append(method)
    
    return PaymentMethodListResponse(
        data={
            "items": filtered_methods,
            "total": len(filtered_methods),
            "page": 1,
            "page_size": len(filtered_methods),
            "pages": 1
        }
    )


@router.get("/transactions/my", response_model=PaymentTransactionListResponse)
async def get_my_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取我的交易记录
    
    获取当前用户的所有交易记录
    """
    if not current_user.customer_id:
        return PaymentTransactionListResponse(
            data={
                "items": [],
                "total": 0,
                "page": 1,
                "page_size": limit,
                "pages": 0
            }
        )
    
    transactions = PaymentTransactionService.get_transactions_by_customer_id(
        db, current_user.customer_id, skip, limit
    )
    
    count_transactions = len(PaymentTransactionService.get_transactions_by_customer_id(
        db, current_user.customer_id, 0, 1000
    ))
    
    pages = (count_transactions + limit - 1) // limit if limit > 0 else 0
    
    return PaymentTransactionListResponse(
        data={
            "items": transactions,
            "total": count_transactions,
            "page": skip // limit + 1 if limit > 0 else 1,
            "page_size": limit,
            "pages": pages
        }
    )


# ==================== 支付网关回调 ====================

@router.post("/webhook", response_model=ResponseBase)
async def payment_webhook(
    webhook_data: PaymentWebhookRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """支付网关回调
    
    处理支付网关的异步回调通知
    """
    try:
        result = PaymentProcessingService.handle_payment_webhook(
            db, 
            webhook_data,
            request.client.host if request.client else None
        )
        
        return ResponseBase(
            data=result,
            message="支付回调处理成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付回调处理失败: {str(e)}"
        )


# ==================== 管理员接口 ====================

# 支付方式管理

@router.post("/admin/methods", response_model=PaymentMethodDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_payment_method(
    method_data: PaymentMethodCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建支付方式
    
    管理员创建新的支付方式
    """
    try:
        payment_method = PaymentMethodService.create_payment_method(db, method_data)
        return PaymentMethodDetailResponse(
            data=payment_method,
            message="支付方式创建成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付方式创建失败: {str(e)}"
        )


@router.get("/admin/methods", response_model=PaymentMethodListResponse)
async def get_payment_methods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[PaymentMethodStatus] = Query(None),
    is_public: Optional[bool] = Query(None),
    gateway_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取支付方式列表
    
    管理员获取支付方式列表，支持过滤
    """
    payment_methods = PaymentMethodService.get_payment_methods(
        db, skip, limit, status, is_public, gateway_id
    )
    
    count_methods = len(PaymentMethodService.get_payment_methods(
        db, 0, 1000, status, is_public, gateway_id
    ))
    
    pages = (count_methods + limit - 1) // limit if limit > 0 else 0
    
    return PaymentMethodListResponse(
        data={
            "items": payment_methods,
            "total": count_methods,
            "page": skip // limit + 1 if limit > 0 else 1,
            "page_size": limit,
            "pages": pages
        }
    )


@router.get("/admin/methods/{method_id}", response_model=PaymentMethodDetailResponse)
async def get_payment_method(
    method_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取支付方式详情
    
    管理员获取指定支付方式的详细信息
    """
    payment_method = PaymentMethodService.get_payment_method_by_id(db, method_id)
    if not payment_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="支付方式不存在"
        )
    
    return PaymentMethodDetailResponse(data=payment_method)


@router.put("/admin/methods/{method_id}", response_model=PaymentMethodDetailResponse)
async def update_payment_method(
    method_id: UUID = Path(...),
    update_data: PaymentMethodUpdate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新支付方式
    
    管理员更新支付方式信息
    """
    try:
        updated_method = PaymentMethodService.update_payment_method(db, method_id, update_data)
        if not updated_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="支付方式不存在"
            )
        
        return PaymentMethodDetailResponse(
            data=updated_method,
            message="支付方式更新成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付方式更新失败: {str(e)}"
        )


@router.delete("/admin/methods/{method_id}", response_model=ResponseBase)
async def delete_payment_method(
    method_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除支付方式
    
    管理员删除支付方式
    """
    success = PaymentMethodService.delete_payment_method(db, method_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="支付方式不存在"
        )
    
    return ResponseBase(message="支付方式删除成功")


# 支付网关管理

@router.post("/admin/gateways", response_model=PaymentGatewayDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_payment_gateway(
    gateway_data: PaymentGatewayCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建支付网关
    
    管理员创建新的支付网关
    """
    try:
        gateway = PaymentGatewayService.create_payment_gateway(db, gateway_data)
        return PaymentGatewayDetailResponse(
            data=gateway,
            message="支付网关创建成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付网关创建失败: {str(e)}"
        )


@router.get("/admin/gateways", response_model=PaymentGatewayListResponse)
async def get_payment_gateways(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[GatewayStatus] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取支付网关列表
    
    管理员获取支付网关列表，支持过滤
    """
    gateways = PaymentGatewayService.get_payment_gateways(db, skip, limit, status)
    
    count_gateways = len(PaymentGatewayService.get_payment_gateways(db, 0, 1000, status))
    
    pages = (count_gateways + limit - 1) // limit if limit > 0 else 0
    
    return PaymentGatewayListResponse(
        data={
            "items": gateways,
            "total": count_gateways,
            "page": skip // limit + 1 if limit > 0 else 1,
            "page_size": limit,
            "pages": pages
        }
    )


@router.get("/admin/gateways/{gateway_id}", response_model=PaymentGatewayDetailResponse)
async def get_payment_gateway(
    gateway_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取支付网关详情
    
    管理员获取指定支付网关的详细信息
    """
    gateway = PaymentGatewayService.get_payment_gateway_by_id(db, gateway_id)
    if not gateway:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="支付网关不存在"
        )
    
    return PaymentGatewayDetailResponse(data=gateway)


@router.put("/admin/gateways/{gateway_id}", response_model=PaymentGatewayDetailResponse)
async def update_payment_gateway(
    gateway_id: UUID = Path(...),
    update_data: PaymentGatewayUpdate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新支付网关
    
    管理员更新支付网关信息
    """
    try:
        updated_gateway = PaymentGatewayService.update_payment_gateway(db, gateway_id, update_data)
        if not updated_gateway:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="支付网关不存在"
            )
        
        return PaymentGatewayDetailResponse(
            data=updated_gateway,
            message="支付网关更新成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付网关更新失败: {str(e)}"
        )


@router.delete("/admin/gateways/{gateway_id}", response_model=ResponseBase)
async def delete_payment_gateway(
    gateway_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除支付网关
    
    管理员删除支付网关
    """
    success = PaymentGatewayService.delete_payment_gateway(db, gateway_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="支付网关不存在"
        )
    
    return ResponseBase(message="支付网关删除成功")


# 交易管理

@router.get("/admin/transactions", response_model=PaymentTransactionListResponse)
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[TransactionStatus] = Query(None),
    transaction_type: Optional[TransactionType] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取交易记录列表
    
    管理员获取交易记录列表，支持过滤
    """
    transactions = PaymentTransactionService.get_transactions(
        db, skip, limit, status, transaction_type, from_date, to_date
    )
    
    # 简化获取总数
    total_count = len(PaymentTransactionService.get_transactions(
        db, 0, 1000, status, transaction_type, from_date, to_date
    ))
    
    pages = (total_count + limit - 1) // limit if limit > 0 else 0
    
    return PaymentTransactionListResponse(
        data={
            "items": transactions,
            "total": total_count,
            "page": skip // limit + 1 if limit > 0 else 1,
            "page_size": limit,
            "pages": pages
        }
    )


@router.get("/admin/transactions/{transaction_id}", response_model=PaymentTransactionDetailResponse)
async def get_transaction(
    transaction_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取交易记录详情
    
    管理员获取指定交易记录的详细信息
    """
    transaction = PaymentTransactionService.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交易记录不存在"
        )
    
    return PaymentTransactionDetailResponse(data=transaction)


@router.get("/admin/orders/{order_id}/transactions", response_model=PaymentTransactionListResponse)
async def get_order_transactions(
    order_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单的交易记录
    
    管理员获取指定订单的所有交易记录
    """
    transactions = PaymentTransactionService.get_transactions_by_order_id(db, order_id)
    
    return PaymentTransactionListResponse(
        data={
            "items": transactions,
            "total": len(transactions),
            "page": 1,
            "page_size": len(transactions),
            "pages": 1
        }
    )


@router.post("/admin/transactions/refund", response_model=RefundResponse)
async def refund_transaction(
    refund_data: RefundRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """退款处理
    
    管理员处理交易退款
    """
    try:
        result = PaymentProcessingService.process_refund(
            db, 
            refund_data, 
            current_admin.id,
            request.client.host if request.client else None
        )
        
        return RefundResponse(
            data=result,
            message="退款处理成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退款处理失败: {str(e)}"
        )
