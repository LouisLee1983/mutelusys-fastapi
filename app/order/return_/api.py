from typing import Optional, List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_admin_user
from app.order.return_.schema import (
    ReturnCreate, ReturnStatusUpdate, ReturnApprove, ReturnReject,
    ReturnReceive, ReturnRefund, ReturnResponse, ReturnDetailResponse,
    ReturnListResponse, ReturnListParams, UpdateReturnTracking,
    ResponseBase
)
from app.order.return_.service import ReturnService
from app.security.user.models import User


# 创建路由
router = APIRouter()


# 用户接口 - 允许客户创建和查看自己的退货申请
@router.post("/my-returns", response_model=ReturnDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_return(
    return_data: ReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建退货申请
    
    用户可以为自己的订单创建退货申请
    """
    try:
        # 验证用户是否有关联的客户账号
        if not current_user.customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户没有关联的客户账号"
            )
        
        # 创建退货申请
        return_record = ReturnService.create_return(db, return_data, current_user.customer_id)
        return ReturnDetailResponse(
            message="退货申请已提交",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退货申请创建失败: {str(e)}"
        )


@router.get("/my-returns", response_model=ReturnListResponse)
async def get_my_returns(
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的退货申请列表
    
    用户可以查看自己的所有退货申请
    """
    # 验证用户是否有关联的客户账号
    if not current_user.customer_id:
        return ReturnListResponse(
            data={
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size,
                "pages": 0
            }
        )
    
    returns, total = ReturnService.get_returns_by_customer_id(db, current_user.customer_id, page, page_size)
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    return ReturnListResponse(
        data={
            "items": returns,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    )


@router.get("/my-returns/{return_id}", response_model=ReturnDetailResponse)
async def get_my_return_detail(
    return_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的退货申请详情
    
    用户可以查看自己的退货申请详情
    """
    # 获取退货记录
    return_record = ReturnService.get_return_by_id(db, return_id)
    if not return_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="退货申请不存在"
        )
    
    # 验证退货记录所有权
    from app.order.service import OrderService
    order = OrderService.get_order_by_id(db, return_record.order_id)
    if not order or not current_user.customer_id or order.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此退货申请"
        )
    
    return ReturnDetailResponse(data=return_record)


@router.get("/my-orders/{order_id}/returns", response_model=ReturnListResponse)
async def get_my_order_returns(
    order_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户指定订单的退货申请列表
    
    用户可以查看自己特定订单的所有退货申请
    """
    # 验证订单所有权
    from app.order.service import OrderService
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    if not current_user.customer_id or order.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此订单"
        )
    
    # 获取订单的所有退货记录
    returns = ReturnService.get_returns_by_order_id(db, order_id)
    
    return ReturnListResponse(
        data={
            "items": returns,
            "total": len(returns),
            "page": 1,
            "page_size": len(returns),
            "pages": 1
        }
    )


@router.post("/my-returns/{return_id}/cancel", response_model=ReturnDetailResponse)
async def cancel_my_return(
    return_id: UUID = Path(...),
    comment: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取消自己的退货申请
    
    用户可以取消自己的待处理退货申请
    """
    # 获取退货记录
    return_record = ReturnService.get_return_by_id(db, return_id)
    if not return_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="退货申请不存在"
        )
    
    # 验证退货记录所有权
    from app.order.service import OrderService
    order = OrderService.get_order_by_id(db, return_record.order_id)
    if not order or not current_user.customer_id or order.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此退货申请"
        )
    
    # 检查状态
    if return_record.status not in [ReturnStatus.PENDING, ReturnStatus.APPROVED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"只有处于待处理或已批准状态的退货申请才能被取消，当前状态: {return_record.status}"
        )
    
    try:
        # 取消退货申请
        cancelled_return = ReturnService.cancel_return(db, return_id, comment)
        return ReturnDetailResponse(
            message="退货申请已取消",
            data=cancelled_return
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退货申请取消失败: {str(e)}"
        )


# 管理员接口
@router.get("/admin/returns", response_model=ReturnListResponse)
async def get_returns_admin(
    params: ReturnListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取退货申请列表（管理员）
    
    管理员可以获取所有退货申请，支持分页、排序和过滤
    """
    returns, total = ReturnService.get_returns(db, params)
    pages = (total + params.page_size - 1) // params.page_size if params.page_size > 0 else 0
    
    return ReturnListResponse(
        data={
            "items": returns,
            "total": total,
            "page": params.page,
            "page_size": params.page_size,
            "pages": pages
        }
    )


@router.get("/admin/returns/{return_id}", response_model=ReturnDetailResponse)
async def get_return_detail_admin(
    return_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取退货申请详情（管理员）
    
    管理员可以查看任何退货申请的详细信息
    """
    return_record = ReturnService.get_return_by_id(db, return_id)
    if not return_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="退货申请不存在"
        )
    
    return ReturnDetailResponse(data=return_record)


@router.get("/admin/returns/number/{return_number}", response_model=ReturnDetailResponse)
async def get_return_by_number_admin(
    return_number: str = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """通过退货单号获取退货申请详情（管理员）
    
    管理员可以通过退货单号查询退货申请
    """
    return_record = ReturnService.get_return_by_number(db, return_number)
    if not return_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="退货申请不存在"
        )
    
    return ReturnDetailResponse(data=return_record)


@router.get("/admin/orders/{order_id}/returns", response_model=ReturnListResponse)
async def get_order_returns_admin(
    order_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单的退货申请列表（管理员）
    
    管理员可以获取指定订单的所有退货申请
    """
    # 验证订单是否存在
    from app.order.service import OrderService
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 获取订单的所有退货记录
    returns = ReturnService.get_returns_by_order_id(db, order_id)
    
    return ReturnListResponse(
        data={
            "items": returns,
            "total": len(returns),
            "page": 1,
            "page_size": len(returns),
            "pages": 1
        }
    )


@router.put("/admin/returns/{return_id}/status", response_model=ReturnDetailResponse)
async def update_return_status_admin(
    return_id: UUID,
    status_data: ReturnStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新退货申请状态（管理员）
    
    管理员可以更新退货申请的状态
    """
    try:
        return_record = ReturnService.update_return_status(
            db, return_id, status_data, 
            handler_id=current_admin.id, 
            handler_name=current_admin.username
        )
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message=f"退货申请状态已更新为 {status_data.status.value}",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退货申请状态更新失败: {str(e)}"
        )


@router.post("/admin/returns/{return_id}/approve", response_model=ReturnDetailResponse)
async def approve_return_admin(
    return_id: UUID,
    approve_data: ReturnApprove,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批准退货申请（管理员）
    
    管理员可以批准退货申请并设置退款信息
    """
    try:
        return_record = ReturnService.approve_return(
            db, return_id, approve_data, 
            handler_id=current_admin.id, 
            handler_name=current_admin.username
        )
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message="退货申请已批准",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退货申请批准失败: {str(e)}"
        )


@router.post("/admin/returns/{return_id}/reject", response_model=ReturnDetailResponse)
async def reject_return_admin(
    return_id: UUID,
    reject_data: ReturnReject,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """拒绝退货申请（管理员）
    
    管理员可以拒绝退货申请并提供拒绝原因
    """
    try:
        return_record = ReturnService.reject_return(
            db, return_id, reject_data, 
            handler_id=current_admin.id, 
            handler_name=current_admin.username
        )
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message="退货申请已拒绝",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退货申请拒绝失败: {str(e)}"
        )


@router.post("/admin/returns/{return_id}/receive", response_model=ReturnDetailResponse)
async def receive_return_admin(
    return_id: UUID,
    receive_data: ReturnReceive,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """确认收到退货（管理员）
    
    管理员可以确认收到客户的退货
    """
    try:
        return_record = ReturnService.receive_return(
            db, return_id, receive_data, 
            handler_id=current_admin.id, 
            handler_name=current_admin.username
        )
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message="已确认收到退货",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"确认收到退货失败: {str(e)}"
        )


@router.post("/admin/returns/{return_id}/refund", response_model=ReturnDetailResponse)
async def process_refund_admin(
    return_id: UUID,
    refund_data: ReturnRefund,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """处理退款（管理员）
    
    管理员可以处理退货申请的退款
    """
    try:
        return_record = ReturnService.process_refund(
            db, return_id, refund_data, 
            handler_id=current_admin.id, 
            handler_name=current_admin.username
        )
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message="退款已处理",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理退款失败: {str(e)}"
        )


@router.post("/admin/returns/{return_id}/complete", response_model=ReturnDetailResponse)
async def complete_return_admin(
    return_id: UUID,
    admin_comment: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """完成退货流程（管理员）
    
    管理员可以将退货申请标记为完成
    """
    try:
        return_record = ReturnService.complete_return(
            db, return_id, admin_comment, 
            handler_id=current_admin.id, 
            handler_name=current_admin.username
        )
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message="退货流程已完成",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"完成退货流程失败: {str(e)}"
        )


@router.post("/admin/returns/{return_id}/cancel", response_model=ReturnDetailResponse)
async def cancel_return_admin(
    return_id: UUID,
    admin_comment: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """取消退货申请（管理员）
    
    管理员可以取消退货申请
    """
    try:
        return_record = ReturnService.cancel_return(
            db, return_id, admin_comment, 
            handler_id=current_admin.id, 
            handler_name=current_admin.username
        )
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message="退货申请已取消",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取消退货申请失败: {str(e)}"
        )


@router.put("/admin/returns/{return_id}/tracking", response_model=ReturnDetailResponse)
async def update_return_tracking_admin(
    return_id: UUID,
    tracking_data: UpdateReturnTracking,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新退货追踪信息（管理员）
    
    管理员可以更新退货的物流追踪信息
    """
    try:
        return_record = ReturnService.update_return_tracking(db, return_id, tracking_data)
        if not return_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="退货申请不存在"
            )
        
        return ReturnDetailResponse(
            message="退货追踪信息已更新",
            data=return_record
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新退货追踪信息失败: {str(e)}"
        )
