# -*- coding: utf-8 -*-
"""
订单运费记录API路由
包含订单收费项目和运费记录的管理接口
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from .service import OrderRecordService
from .schema import (
    OrderChargeItemCreate, OrderChargeItemUpdate, OrderChargeItemResponse,
    OrderShippingInfoCreate, OrderShippingInfoUpdate, OrderShippingInfoResponse,
    CreateOrderShippingRequest, OrderShippingStatsResponse
)

router = APIRouter(prefix="/order-records")


# ==================== 订单收费项目接口 ====================

@router.post("/charge-items", response_model=OrderChargeItemResponse)
async def create_charge_item(
    item_data: OrderChargeItemCreate,
    db: Session = Depends(get_db)
):
    """创建订单收费项目"""
    try:
        service = OrderRecordService(db)
        charge_item = service.create_charge_item(item_data)
        return OrderChargeItemResponse.from_orm(charge_item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/charge-items/order/{order_id}", response_model=List[OrderChargeItemResponse])
async def get_charge_items_by_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """获取订单的所有收费项目"""
    service = OrderRecordService(db)
    charge_items = service.get_charge_items_by_order(order_id)
    return [OrderChargeItemResponse.from_orm(item) for item in charge_items]


@router.put("/charge-items/{item_id}", response_model=OrderChargeItemResponse)
async def update_charge_item(
    item_id: UUID,
    item_data: OrderChargeItemUpdate,
    db: Session = Depends(get_db)
):
    """更新订单收费项目"""
    service = OrderRecordService(db)
    charge_item = service.update_charge_item(item_id, item_data)
    if not charge_item:
        raise HTTPException(status_code=404, detail="收费项目不存在")
    return OrderChargeItemResponse.from_orm(charge_item)


@router.delete("/charge-items/{item_id}")
async def delete_charge_item(
    item_id: UUID,
    db: Session = Depends(get_db)
):
    """删除订单收费项目"""
    service = OrderRecordService(db)
    success = service.delete_charge_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="收费项目不存在")
    return {"message": "收费项目删除成功"}


# ==================== 订单运费记录接口 ====================

@router.post("/shipping-info", response_model=OrderShippingInfoResponse)
async def create_shipping_info(
    shipping_data: OrderShippingInfoCreate,
    db: Session = Depends(get_db)
):
    """创建订单运费记录"""
    try:
        service = OrderRecordService(db)
        shipping_info = service.create_shipping_info(shipping_data)
        return OrderShippingInfoResponse.from_orm(shipping_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/shipping-info/from-calculation", response_model=OrderShippingInfoResponse)
async def create_shipping_from_calculation(
    request: CreateOrderShippingRequest,
    db: Session = Depends(get_db)
):
    """根据运费计算结果创建订单运费记录"""
    try:
        service = OrderRecordService(db)
        shipping_info = service.create_order_shipping_from_calculation(request)
        return OrderShippingInfoResponse.from_orm(shipping_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"系统错误: {str(e)}")


@router.get("/shipping-info/order/{order_id}", response_model=OrderShippingInfoResponse)
async def get_shipping_info_by_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """获取订单运费记录"""
    service = OrderRecordService(db)
    shipping_info = service.get_shipping_info_by_order(order_id)
    if not shipping_info:
        raise HTTPException(status_code=404, detail="订单运费记录不存在")
    return OrderShippingInfoResponse.from_orm(shipping_info)


@router.put("/shipping-info/order/{order_id}", response_model=OrderShippingInfoResponse)
async def update_shipping_info(
    order_id: str,
    shipping_data: OrderShippingInfoUpdate,
    db: Session = Depends(get_db)
):
    """更新订单运费记录"""
    service = OrderRecordService(db)
    shipping_info = service.update_shipping_info(order_id, shipping_data)
    if not shipping_info:
        raise HTTPException(status_code=404, detail="订单运费记录不存在")
    return OrderShippingInfoResponse.from_orm(shipping_info)


# ==================== 物流跟踪接口 ====================

@router.put("/shipping-info/order/{order_id}/tracking")
async def update_tracking_info(
    order_id: str,
    tracking_number: str,
    tracking_url: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """更新物流跟踪信息"""
    service = OrderRecordService(db)
    shipping_info = service.update_tracking_info(order_id, tracking_number, tracking_url)
    if not shipping_info:
        raise HTTPException(status_code=404, detail="订单运费记录不存在")
    return {"message": "跟踪信息更新成功", "tracking_number": tracking_number}


@router.put("/shipping-info/order/{order_id}/delivered")
async def mark_as_delivered(
    order_id: str,
    delivered_at: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """标记订单为已送达"""
    service = OrderRecordService(db)
    shipping_info = service.mark_as_delivered(order_id, delivered_at)
    if not shipping_info:
        raise HTTPException(status_code=404, detail="订单运费记录不存在")
    return {"message": "订单已标记为送达", "delivered_at": shipping_info.delivered_at}


@router.put("/shipping-info/order/{order_id}/status")
async def update_shipping_status(
    order_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """更新发货状态"""
    service = OrderRecordService(db)
    shipping_info = service.update_shipping_status(order_id, status)
    if not shipping_info:
        raise HTTPException(status_code=404, detail="订单运费记录不存在")
    return {"message": "发货状态更新成功", "status": status}


# ==================== 统计分析接口 ====================

@router.get("/stats", response_model=OrderShippingStatsResponse)
async def get_shipping_stats(
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    db: Session = Depends(get_db)
):
    """获取运费统计数据"""
    service = OrderRecordService(db)
    stats = service.get_shipping_stats(start_date, end_date)
    return stats


@router.get("/orders/by-method/{method_code}", response_model=List[OrderShippingInfoResponse])
async def get_orders_by_shipping_method(
    method_code: str,
    limit: int = Query(50, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """根据快递方式获取订单列表"""
    service = OrderRecordService(db)
    orders = service.get_orders_by_shipping_method(method_code, limit)
    return [OrderShippingInfoResponse.from_orm(order) for order in orders]


@router.get("/orders/by-zone/{zone_name}", response_model=List[OrderShippingInfoResponse])
async def get_orders_by_zone(
    zone_name: str,
    limit: int = Query(50, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """根据运费地区获取订单列表"""
    service = OrderRecordService(db)
    orders = service.get_orders_by_zone(zone_name, limit)
    return [OrderShippingInfoResponse.from_orm(order) for order in orders]


@router.get("/orders/free-shipping", response_model=List[OrderShippingInfoResponse])
async def get_free_shipping_orders(
    limit: int = Query(50, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """获取免运费订单列表"""
    service = OrderRecordService(db)
    orders = service.get_free_shipping_orders(limit)
    return [OrderShippingInfoResponse.from_orm(order) for order in orders] 