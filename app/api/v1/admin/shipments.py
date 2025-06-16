from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
import math

from app.core.database import get_db
from app.order.shipment.service import ShipmentService, CarrierService
from app.order.shipment.schema import (
    ShipmentCreate, ShipmentUpdate, ShipmentStatusUpdate, ShipmentResponse,
    ShipmentListResponse, ShipmentDetailResponse, 
    TrackingRecordCreate, TrackingResponse,
    CarrierCreate, CarrierResponse, CarrierListResponse,
    ShipmentFilter
)

router = APIRouter()


@router.get("/api/v1/admin/shipments", response_model=ShipmentListResponse)
async def get_shipments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_desc: bool = Query(True, description="是否降序"),
    
    # 过滤参数
    order_id: Optional[str] = Query(None, description="订单ID"),
    shipment_code: Optional[str] = Query(None, description="发货单号"),
    status: Optional[str] = Query(None, description="发货状态"),
    carrier_id: Optional[str] = Query(None, description="承运商ID"),
    tracking_number: Optional[str] = Query(None, description="快递单号"),
    recipient_name: Optional[str] = Query(None, description="收件人姓名"),
    recipient_phone: Optional[str] = Query(None, description="收件人电话"),
    
    db: Session = Depends(get_db)
):
    """获取发货记录列表"""
    try:
        # 构建过滤条件
        filters = {}
        if order_id:
            filters['order_id'] = UUID(order_id)
        if shipment_code:
            filters['shipment_code'] = shipment_code
        if status:
            filters['status'] = status
        if carrier_id:
            filters['carrier_id'] = UUID(carrier_id)
        if tracking_number:
            filters['tracking_number'] = tracking_number
        if recipient_name:
            filters['recipient_name'] = recipient_name
        if recipient_phone:
            filters['recipient_phone'] = recipient_phone
        
        # 构建查询参数
        from app.order.shipment.schema import ShipmentListParams
        params = ShipmentListParams(
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_desc=sort_desc,
            filters=ShipmentFilter(**filters) if filters else None
        )
        
        # 获取数据
        shipments, total = ShipmentService.get_shipments(db, params)
        
        # 转换为响应格式
        items = [ShipmentResponse.from_orm(shipment) for shipment in shipments]
        pages = math.ceil(total / page_size) if total > 0 else 1
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取发货记录失败: {str(e)}")


@router.post("/api/v1/admin/shipments", response_model=ShipmentDetailResponse)
async def create_shipment(
    shipment_data: ShipmentCreate,
    db: Session = Depends(get_db)
):
    """创建发货记录"""
    try:
        shipment = ShipmentService.create_shipment(db, shipment_data)
        return {
            "code": 200,
            "message": "创建成功",
            "data": ShipmentResponse.from_orm(shipment)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建发货记录失败: {str(e)}")


@router.get("/api/v1/admin/shipments/{shipment_id}", response_model=ShipmentDetailResponse)
async def get_shipment_detail(
    shipment_id: UUID,
    db: Session = Depends(get_db)
):
    """获取发货记录详情"""
    try:
        shipment = ShipmentService.get_shipment_by_id(db, shipment_id)
        if not shipment:
            raise HTTPException(status_code=404, detail="发货记录不存在")
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": ShipmentResponse.from_orm(shipment)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取发货记录详情失败: {str(e)}")


@router.put("/api/v1/admin/shipments/{shipment_id}", response_model=ShipmentDetailResponse)
async def update_shipment(
    shipment_id: UUID,
    update_data: ShipmentUpdate,
    db: Session = Depends(get_db)
):
    """更新发货记录"""
    try:
        shipment = ShipmentService.update_shipment(db, shipment_id, update_data)
        if not shipment:
            raise HTTPException(status_code=404, detail="发货记录不存在")
        
        return {
            "code": 200,
            "message": "更新成功",
            "data": ShipmentResponse.from_orm(shipment)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新发货记录失败: {str(e)}")


@router.patch("/api/v1/admin/shipments/{shipment_id}/status", response_model=ShipmentDetailResponse)
async def update_shipment_status(
    shipment_id: UUID,
    status_data: ShipmentStatusUpdate,
    db: Session = Depends(get_db)
):
    """更新发货状态"""
    try:
        shipment = ShipmentService.update_shipment_status(db, shipment_id, status_data)
        if not shipment:
            raise HTTPException(status_code=404, detail="发货记录不存在")
        
        return {
            "code": 200,
            "message": "状态更新成功",
            "data": ShipmentResponse.from_orm(shipment)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新发货状态失败: {str(e)}")


@router.delete("/api/v1/admin/shipments/{shipment_id}")
async def delete_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db)
):
    """删除发货记录"""
    try:
        result = ShipmentService.delete_shipment(db, shipment_id)
        if not result:
            raise HTTPException(status_code=404, detail="发货记录不存在")
        
        return {
            "code": 200,
            "message": "删除成功",
            "data": None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除发货记录失败: {str(e)}")


@router.get("/api/v1/admin/orders/{order_id}/shipments", response_model=List[ShipmentResponse])
async def get_order_shipments(
    order_id: UUID,
    db: Session = Depends(get_db)
):
    """获取订单的所有发货记录"""
    try:
        shipments = ShipmentService.get_order_shipments(db, order_id)
        return [ShipmentResponse.from_orm(shipment) for shipment in shipments]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取订单发货记录失败: {str(e)}")


@router.post("/api/v1/admin/shipments/{shipment_id}/tracking", response_model=TrackingResponse)
async def add_tracking_record(
    shipment_id: UUID,
    tracking_data: TrackingRecordCreate,
    db: Session = Depends(get_db)
):
    """添加物流跟踪记录"""
    try:
        tracking_record = ShipmentService.add_tracking_record(db, shipment_id, tracking_data)
        if not tracking_record:
            raise HTTPException(status_code=404, detail="发货记录不存在")
        
        return {
            "code": 200,
            "message": "跟踪记录添加成功",
            "data": [tracking_record]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加跟踪记录失败: {str(e)}")


@router.get("/api/v1/admin/shipments/{shipment_id}/tracking", response_model=TrackingResponse)
async def get_tracking_records(
    shipment_id: UUID,
    db: Session = Depends(get_db)
):
    """获取物流跟踪记录"""
    try:
        tracking_records = ShipmentService.get_tracking_records(db, shipment_id)
        return {
            "code": 200,
            "message": "获取成功",
            "data": tracking_records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取跟踪记录失败: {str(e)}")


@router.get("/api/v1/admin/shipments/statistics")
async def get_shipment_statistics(
    db: Session = Depends(get_db)
):
    """获取发货统计信息"""
    try:
        stats = ShipmentService.count_shipments_by_status(db)
        return {
            "code": 200,
            "message": "获取成功",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


# 承运商管理API
@router.get("/api/v1/admin/carriers", response_model=CarrierListResponse)
async def get_carriers(
    active_only: bool = Query(True, description="仅显示活跃的承运商"),
    db: Session = Depends(get_db)
):
    """获取承运商列表"""
    try:
        carriers = CarrierService.get_carriers(db, active_only)
        return {
            "code": 200,
            "message": "获取成功",
            "data": [CarrierResponse.from_orm(carrier) for carrier in carriers]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取承运商列表失败: {str(e)}")


@router.post("/api/v1/admin/carriers", response_model=CarrierResponse)
async def create_carrier(
    carrier_data: CarrierCreate,
    db: Session = Depends(get_db)
):
    """创建承运商"""
    try:
        carrier = CarrierService.create_carrier(db, carrier_data)
        return CarrierResponse.from_orm(carrier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建承运商失败: {str(e)}")


@router.get("/api/v1/admin/carriers/{carrier_id}", response_model=CarrierResponse)
async def get_carrier_detail(
    carrier_id: UUID,
    db: Session = Depends(get_db)
):
    """获取承运商详情"""
    try:
        carrier = CarrierService.get_carrier_by_id(db, carrier_id)
        if not carrier:
            raise HTTPException(status_code=404, detail="承运商不存在")
        
        return CarrierResponse.from_orm(carrier)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取承运商详情失败: {str(e)}")


@router.put("/api/v1/admin/carriers/{carrier_id}", response_model=CarrierResponse)
async def update_carrier(
    carrier_id: UUID,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """更新承运商"""
    try:
        carrier = CarrierService.update_carrier(db, carrier_id, update_data)
        if not carrier:
            raise HTTPException(status_code=404, detail="承运商不存在")
        
        return CarrierResponse.from_orm(carrier)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新承运商失败: {str(e)}")


@router.delete("/api/v1/admin/carriers/{carrier_id}")
async def delete_carrier(
    carrier_id: UUID,
    db: Session = Depends(get_db)
):
    """删除承运商"""
    try:
        result = CarrierService.delete_carrier(db, carrier_id)
        if not result:
            raise HTTPException(status_code=404, detail="承运商不存在")
        
        return {
            "code": 200,
            "message": "删除成功",
            "data": None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除承运商失败: {str(e)}") 