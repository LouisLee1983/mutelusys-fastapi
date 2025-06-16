from typing import Optional, List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_admin_user
from app.marketing.coupon.models import CouponStatus, CouponFormat
from app.marketing.coupon.schema import (
    CouponCreate, CouponUpdate, CouponValidate, CouponBatchCreate,
    CouponIssue, CouponResponse, CouponDetailResponse, CouponListResponse,
    CouponValidationResponse, CouponBatchResponse, CustomerCouponResponse,
    CustomerCouponListResponse, CouponListRequest, ResponseBase
)
from app.marketing.coupon.service import CouponService
from app.security.user.models import User


# 创建路由
router = APIRouter()


# ------------ 公共接口 ------------

@router.post("/validate", response_model=CouponValidationResponse)
async def validate_coupon(
    validate_data: CouponValidate,
    db: Session = Depends(get_db)
):
    """验证优惠券
    
    验证优惠券是否有效，并计算折扣金额
    """
    result = CouponService.validate_coupon(db, validate_data)
    return CouponValidationResponse(
        data=result,
        message="验证成功" if result["is_valid"] else result["message"]
    )


@router.get("/public", response_model=CouponListResponse)
async def get_public_coupons(
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db)
):
    """获取公开优惠券列表
    
    获取可公开使用的优惠券列表
    """
    from app.marketing.coupon.schema import PaginationParams, CouponFilter
    
    filters = CouponFilter(
        is_public=True,
        status=CouponStatus.ACTIVE
    )
    pagination = PaginationParams(
        page=page,
        page_size=page_size,
        sort_by="created_at",
        sort_desc=True
    )
    
    coupons, total = CouponService.get_coupons(db, filters, pagination)
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    return CouponListResponse(
        data={
            "items": coupons,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    )


# ------------ 用户接口 ------------

@router.get("/my-coupons", response_model=CustomerCouponListResponse)
async def get_my_coupons(
    include_used: bool = Query(False),
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取我的优惠券
    
    获取当前登录用户的优惠券列表
    """
    # 验证用户是否有关联的客户账号
    if not current_user.customer_id:
        return CustomerCouponListResponse(
            data={
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size,
                "pages": 0
            }
        )
    
    # 获取客户的优惠券
    coupons = CouponService.get_customer_coupons(db, current_user.customer_id, include_used)
    
    # 计算分页
    total = len(coupons)
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    start = (page - 1) * page_size
    end = start + page_size
    paged_coupons = coupons[start:end]
    
    return CustomerCouponListResponse(
        data={
            "items": paged_coupons,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    )


# ------------ 管理员接口 ------------

@router.post("/admin/coupons", response_model=CouponDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_coupon(
    coupon_data: CouponCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建优惠券
    
    管理员创建新的优惠券
    """
    try:
        coupon = CouponService.create_coupon(db, coupon_data)
        return CouponDetailResponse(
            data=coupon,
            message="优惠券创建成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"优惠券创建失败: {str(e)}"
        )


@router.post("/admin/coupon-batches", response_model=ResponseBase, status_code=status.HTTP_201_CREATED)
async def create_coupon_batch(
    batch_data: CouponBatchCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批量创建优惠券
    
    管理员批量创建新的优惠券
    """
    try:
        batch, count = CouponService.create_coupon_batch(db, batch_data)
        return ResponseBase(
            message=f"批量创建成功，共创建 {count} 个优惠券",
            data={
                "batch_id": str(batch.id),
                "batch_name": batch.name,
                "quantity": batch.quantity,
                "generated_count": count
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量创建优惠券失败: {str(e)}"
        )


@router.get("/admin/coupons", response_model=CouponListResponse)
async def get_coupons_admin(
    code: Optional[str] = Query(None),
    status: Optional[CouponStatus] = Query(None),
    batch_id: Optional[UUID] = Query(None),
    is_public: Optional[bool] = Query(None),
    is_featured: Optional[bool] = Query(None),
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取优惠券列表
    
    管理员获取优惠券列表，支持过滤和分页
    """
    from app.marketing.coupon.schema import PaginationParams, CouponFilter
    
    filters = CouponFilter(
        code=code,
        status=status,
        batch_id=batch_id,
        is_public=is_public,
        is_featured=is_featured
    )
    pagination = PaginationParams(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_desc=sort_desc
    )
    
    coupons, total = CouponService.get_coupons(db, filters, pagination)
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    return CouponListResponse(
        data={
            "items": coupons,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    )


@router.get("/admin/coupons/{coupon_id}", response_model=CouponDetailResponse)
async def get_coupon_admin(
    coupon_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取优惠券详情
    
    管理员获取指定优惠券的详细信息
    """
    coupon = CouponService.get_coupon_by_id(db, coupon_id)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="优惠券不存在"
        )
    
    return CouponDetailResponse(data=coupon)


@router.get("/admin/coupons/code/{code}", response_model=CouponDetailResponse)
async def get_coupon_by_code_admin(
    code: str = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """通过优惠券码获取优惠券详情
    
    管理员通过优惠券码获取优惠券详情
    """
    coupon = CouponService.get_coupon_by_code(db, code)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="优惠券不存在"
        )
    
    return CouponDetailResponse(data=coupon)


@router.put("/admin/coupons/{coupon_id}", response_model=CouponDetailResponse)
async def update_coupon_admin(
    coupon_id: UUID = Path(...),
    update_data: CouponUpdate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新优惠券
    
    管理员更新优惠券信息
    """
    updated_coupon = CouponService.update_coupon(db, coupon_id, update_data)
    if not updated_coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="优惠券不存在"
        )
    
    return CouponDetailResponse(
        data=updated_coupon,
        message="优惠券更新成功"
    )


@router.post("/admin/coupons/{coupon_id}/cancel", response_model=CouponDetailResponse)
async def cancel_coupon_admin(
    coupon_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """取消优惠券
    
    管理员取消优惠券
    """
    try:
        cancelled_coupon = CouponService.cancel_coupon(db, coupon_id)
        if not cancelled_coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="优惠券不存在"
            )
        
        return CouponDetailResponse(
            data=cancelled_coupon,
            message="优惠券已取消"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/admin/coupons/issue", response_model=ResponseBase)
async def issue_coupons_admin(
    issue_data: CouponIssue,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """发放优惠券
    
    管理员向客户发放优惠券
    """
    try:
        issued_coupons = CouponService.issue_coupon_to_customers(db, issue_data, current_admin.id)
        return ResponseBase(
            message=f"优惠券发放成功，共发放给 {len(issued_coupons)} 位客户",
            data={
                "issued_count": len(issued_coupons),
                "coupon_id": str(issue_data.coupon_id)
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"优惠券发放失败: {str(e)}"
        )


@router.get("/admin/coupon-batches", response_model=ResponseBase)
async def get_coupon_batches_admin(
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取优惠券批次列表
    
    管理员获取优惠券批次列表
    """
    batches, total = CouponService.get_coupon_batches(db, page, page_size)
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    return ResponseBase(
        data={
            "items": batches,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    )


@router.get("/admin/coupon-batches/{batch_id}", response_model=ResponseBase)
async def get_coupon_batch_admin(
    batch_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取优惠券批次详情
    
    管理员获取指定优惠券批次的详细信息
    """
    batch = CouponService.get_batch_by_id(db, batch_id)
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="优惠券批次不存在"
        )
    
    return ResponseBase(data=batch)


@router.get("/admin/coupon-batches/{batch_id}/coupons", response_model=CouponListResponse)
async def get_batch_coupons_admin(
    batch_id: UUID = Path(...),
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取批次中的优惠券列表
    
    管理员获取指定批次中的优惠券列表
    """
    from app.marketing.coupon.schema import PaginationParams, CouponFilter
    
    filters = CouponFilter(batch_id=batch_id)
    pagination = PaginationParams(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_desc=sort_desc
    )
    
    coupons, total = CouponService.get_coupons(db, filters, pagination)
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    return CouponListResponse(
        data={
            "items": coupons,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    )
