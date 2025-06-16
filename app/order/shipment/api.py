from typing import Optional, List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_admin_user
from app.order.shipment.schema import (
    ShipmentCreate, ShipmentStatusUpdate, TrackingUpdateCreate,
    ShipmentResponse, ShipmentDetailResponse, ShipmentListResponse,
    ShipmentListParams, ShipmentBriefResponse, TrackingUpdateResponse,
    ResponseBase
)
from app.order.shipment.service import ShipmentService
from app.security.user.models import User


# 创建路由
router = APIRouter()


# 用户接口 - 允许客户查看自己的物流信息
@router.get("/my-orders/{order_id}/shipments", response_model=ShipmentListResponse)
async def get_my_order_shipments(
    order_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户指定订单的物流信息
    
    用户可以查看自己订单的物流发货记录
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
    
    # 获取订单的所有物流记录
    shipments = ShipmentService.get_shipments_by_order_id(db, order_id)
    
    return ShipmentListResponse(
        data={
            "items": shipments,
            "total": len(shipments),
            "page": 1,
            "page_size": len(shipments),
            "pages": 1
        }
    )


@router.get("/my-shipments/{shipment_id}", response_model=ShipmentDetailResponse)
async def get_my_shipment_detail(
    shipment_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户指定物流记录的详细信息
    
    用户可以查看自己订单的物流详情和追踪信息
    """
    # 获取物流记录
    shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流记录不存在"
        )
    
    # 验证订单所有权
    from app.order.service import OrderService
    order = OrderService.get_order_by_id(db, shipment.order_id)
    if not order or not current_user.customer_id or order.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此物流记录"
        )
    
    # 加载物流追踪记录
    tracking_updates = ShipmentService.get_tracking_updates(db, shipment_id)
    shipment.tracking_updates = tracking_updates
    
    return ShipmentDetailResponse(data=shipment)


@router.get("/track/{tracking_number}", response_model=ShipmentDetailResponse)
async def track_shipment(
    tracking_number: str = Path(..., min_length=3),
    db: Session = Depends(get_db)
):
    """公开接口：通过物流单号查询物流信息
    
    无需登录，可通过物流单号追踪物流状态
    """
    # 搜索物流记录
    shipment = ShipmentService.search_shipment_by_tracking(db, tracking_number)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到相关物流记录"
        )
    
    # 加载物流追踪记录
    tracking_updates = ShipmentService.get_tracking_updates(db, shipment.id)
    shipment.tracking_updates = tracking_updates
    
    return ShipmentDetailResponse(data=shipment)


# 管理员接口
@router.post("/admin/shipments", response_model=ShipmentDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment_admin(
    shipment_data: ShipmentCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建物流记录（管理员）
    
    管理员可以为订单创建物流发货记录
    """
    try:
        shipment = ShipmentService.create_shipment(db, shipment_data)
        return ShipmentDetailResponse(
            message="物流记录创建成功",
            data=shipment
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"物流记录创建失败: {str(e)}"
        )


@router.get("/admin/shipments", response_model=ShipmentListResponse)
async def get_shipments_admin(
    params: ShipmentListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取物流记录列表（管理员）
    
    管理员可以获取所有物流记录，支持分页、排序和过滤
    """
    shipments, total = ShipmentService.get_shipments(db, params)
    pages = (total + params.page_size - 1) // params.page_size if params.page_size > 0 else 0
    
    return ShipmentListResponse(
        data={
            "items": shipments,
            "total": total,
            "page": params.page,
            "page_size": params.page_size,
            "pages": pages
        }
    )


@router.get("/admin/orders/{order_id}/shipments", response_model=ShipmentListResponse)
async def get_order_shipments_admin(
    order_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单的物流记录列表（管理员）
    
    管理员可以获取指定订单的所有物流记录
    """
    # 验证订单是否存在
    from app.order.service import OrderService
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 获取订单的所有物流记录
    shipments = ShipmentService.get_shipments_by_order_id(db, order_id)
    
    return ShipmentListResponse(
        data={
            "items": shipments,
            "total": len(shipments),
            "page": 1,
            "page_size": len(shipments),
            "pages": 1
        }
    )


@router.get("/admin/shipments/{shipment_id}", response_model=ShipmentDetailResponse)
async def get_shipment_detail_admin(
    shipment_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取物流记录详情（管理员）
    
    管理员可以查看任何物流记录的详细信息
    """
    shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流记录不存在"
        )
    
    # 加载物流追踪记录
    tracking_updates = ShipmentService.get_tracking_updates(db, shipment_id)
    shipment.tracking_updates = tracking_updates
    
    return ShipmentDetailResponse(data=shipment)


@router.put("/admin/shipments/{shipment_id}/status", response_model=ShipmentDetailResponse)
async def update_shipment_status_admin(
    shipment_id: UUID,
    status_data: ShipmentStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新物流状态（管理员）
    
    管理员可以更新物流记录的状态
    """
    shipment = ShipmentService.update_shipment_status(db, shipment_id, status_data)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流记录不存在"
        )
    
    return ShipmentDetailResponse(
        message=f"物流状态已更新为 {status_data.status.value}",
        data=shipment
    )


@router.post("/admin/shipments/{shipment_id}/tracking", response_model=ResponseBase)
async def add_tracking_update_admin(
    shipment_id: UUID,
    tracking_data: TrackingUpdateCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """添加物流追踪更新（管理员）
    
    管理员可以为物流记录添加追踪信息
    """
    tracking = ShipmentService.add_tracking_update(db, shipment_id, tracking_data)
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流记录不存在"
        )
    
    return ResponseBase(
        message="物流追踪信息已添加",
        data=tracking
    )


@router.post("/admin/shipments/{shipment_id}/mark-shipped", response_model=ShipmentDetailResponse)
async def mark_as_shipped_admin(
    shipment_id: UUID,
    tracking_number: Optional[str] = Query(None),
    tracking_url: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """标记为已发货（管理员）
    
    管理员可以将物流记录标记为已发货状态
    """
    shipment = ShipmentService.mark_as_shipped(db, shipment_id, tracking_number, tracking_url)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流记录不存在"
        )
    
    return ShipmentDetailResponse(
        message="物流记录已标记为已发货",
        data=shipment
    )


@router.get("/admin/shipments/{shipment_id}/tracking", response_model=ResponseBase)
async def get_tracking_updates_admin(
    shipment_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取物流追踪记录列表（管理员）
    
    管理员可以获取物流记录的所有追踪历史
    """
    # 验证物流记录是否存在
    shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流记录不存在"
        )
    
    # 获取物流追踪记录
    tracking_updates = ShipmentService.get_tracking_updates(db, shipment_id)
    
    return ResponseBase(
        data=tracking_updates
    )
