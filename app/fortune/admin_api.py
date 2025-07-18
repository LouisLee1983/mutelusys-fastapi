from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.db.session import get_db
from app.core.dependencies import get_current_admin_user
from app.security.user.models import User
from app.customer.models import Customer
from app.fortune.models import FortuneProfile, FortuneReading, ReadingType
from app.fortune.service import FortuneService
from app.fortune.schema import (
    BaziAnalysisRequest,
    TarotAnalysisRequest, 
    AnalysisResultResponse,
    FortuneReadingResponse,
    FortuneProfileResponse,
    FortuneProfileCreateRequest,
    FortuneProfileUpdateRequest,
    FortuneAnalyticsResponse,
    PaginatedResponse
)

router = APIRouter()

# ==================== 用户档案管理 ====================

@router.get("/profiles", response_model=PaginatedResponse[FortuneProfileResponse])
async def get_fortune_profiles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    customer_email: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    birth_year: Optional[int] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取算命用户档案列表"""
    query = db.query(FortuneProfile).join(Customer, FortuneProfile.customer_id == Customer.id)
    
    # 筛选条件
    if customer_email:
        query = query.filter(Customer.email.ilike(f"%{customer_email}%"))
    if gender:
        query = query.filter(FortuneProfile.gender == gender)
    if birth_year:
        query = query.filter(FortuneProfile.birth_year == birth_year)
    
    # 分页
    total = query.count()
    profiles = query.order_by(desc(FortuneProfile.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    # 加载关联的客户数据
    for profile in profiles:
        profile.customer = db.query(Customer).filter(Customer.id == profile.customer_id).first()
    
    return PaginatedResponse(
        items=[FortuneProfileResponse.from_orm(profile) for profile in profiles],
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/profiles/{profile_id}", response_model=FortuneProfileResponse)
async def get_fortune_profile(
    profile_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取算命用户档案详情"""
    profile = db.query(FortuneProfile).filter(FortuneProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户档案不存在"
        )
    
    # 加载关联的客户数据
    profile.customer = db.query(Customer).filter(Customer.id == profile.customer_id).first()
    
    return FortuneProfileResponse.from_orm(profile)


@router.post("/profiles", response_model=FortuneProfileResponse)
async def create_fortune_profile(
    request: FortuneProfileCreateRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """创建算命用户档案"""
    # 检查客户是否存在
    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="客户不存在"
        )
    
    # 检查是否已有档案
    existing_profile = db.query(FortuneProfile).filter(
        FortuneProfile.customer_id == request.customer_id
    ).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该客户已有算命档案"
        )
    
    # 创建档案
    service = FortuneService(db)
    profile = service.create_or_update_profile(
        customer_id=request.customer_id,
        birth_year=request.birth_year,
        birth_month=request.birth_month,
        birth_day=request.birth_day,
        birth_hour=request.birth_hour,
        gender=request.gender,
        birth_location=request.birth_location,
        timezone=request.timezone
    )
    
    # 加载关联的客户数据
    profile.customer = customer
    
    return FortuneProfileResponse.from_orm(profile)


@router.put("/profiles/{profile_id}", response_model=FortuneProfileResponse)
async def update_fortune_profile(
    profile_id: str,
    request: FortuneProfileUpdateRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """更新算命用户档案"""
    profile = db.query(FortuneProfile).filter(FortuneProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户档案不存在"
        )
    
    # 更新档案
    for field, value in request.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    # 加载关联的客户数据
    profile.customer = db.query(Customer).filter(Customer.id == profile.customer_id).first()
    
    return FortuneProfileResponse.from_orm(profile)


@router.delete("/profiles/{profile_id}")
async def delete_fortune_profile(
    profile_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """删除算命用户档案"""
    profile = db.query(FortuneProfile).filter(FortuneProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户档案不存在"
        )
    
    # 删除相关的算命记录
    db.query(FortuneReading).filter(FortuneReading.profile_id == profile_id).delete()
    
    # 删除档案
    db.delete(profile)
    db.commit()
    
    return {"message": "删除成功"}


# ==================== 算命记录管理 ====================

@router.get("/readings", response_model=PaginatedResponse[FortuneReadingResponse])
async def get_fortune_readings(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    customer_email: Optional[str] = Query(None),
    reading_type: Optional[ReadingType] = Query(None),
    question_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取算命记录列表"""
    query = db.query(FortuneReading).join(Customer, FortuneReading.customer_id == Customer.id)
    
    # 筛选条件
    if customer_email:
        query = query.filter(Customer.email.ilike(f"%{customer_email}%"))
    if reading_type:
        query = query.filter(FortuneReading.reading_type == reading_type)
    if question_type:
        query = query.filter(FortuneReading.question_type == question_type)
    if start_date:
        query = query.filter(FortuneReading.created_at >= start_date)
    if end_date:
        query = query.filter(FortuneReading.created_at <= end_date)
    
    # 分页
    total = query.count()
    readings = query.order_by(desc(FortuneReading.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    # 加载关联数据
    for reading in readings:
        reading.customer = db.query(Customer).filter(Customer.id == reading.customer_id).first()
        if reading.profile_id:
            reading.profile = db.query(FortuneProfile).filter(FortuneProfile.id == reading.profile_id).first()
    
    return PaginatedResponse(
        items=[FortuneReadingResponse.from_orm(reading) for reading in readings],
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/readings/{reading_id}", response_model=FortuneReadingResponse)
async def get_fortune_reading(
    reading_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取算命记录详情"""
    reading = db.query(FortuneReading).filter(FortuneReading.id == reading_id).first()
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="算命记录不存在"
        )
    
    # 加载关联数据
    reading.customer = db.query(Customer).filter(Customer.id == reading.customer_id).first()
    if reading.profile_id:
        reading.profile = db.query(FortuneProfile).filter(FortuneProfile.id == reading.profile_id).first()
    
    return FortuneReadingResponse.from_orm(reading)


@router.delete("/readings/{reading_id}")
async def delete_fortune_reading(
    reading_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """删除算命记录"""
    reading = db.query(FortuneReading).filter(FortuneReading.id == reading_id).first()
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="算命记录不存在"
        )
    
    db.delete(reading)
    db.commit()
    
    return {"message": "删除成功"}


@router.post("/readings/batch-delete")
async def batch_delete_fortune_readings(
    reading_ids: List[str],
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """批量删除算命记录"""
    deleted_count = db.query(FortuneReading).filter(
        FortuneReading.id.in_(reading_ids)
    ).delete(synchronize_session=False)
    
    db.commit()
    
    return {"message": f"成功删除 {deleted_count} 条记录"}


# ==================== 管理员执行算命分析 ====================

@router.post("/bazi/analyze", response_model=AnalysisResultResponse)
async def admin_analyze_bazi(
    request: BaziAnalysisRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """管理员执行八字分析"""
    try:
        service = FortuneService(db)
        result = await service.create_bazi_reading(request.customer_id, request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"八字分析失败: {str(e)}"
        )


@router.post("/tarot/analyze", response_model=AnalysisResultResponse)
async def admin_analyze_tarot(
    request: TarotAnalysisRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """管理员执行塔罗分析"""
    try:
        service = FortuneService(db)
        result = await service.create_tarot_reading(request.customer_id, request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"塔罗分析失败: {str(e)}"
        )


# ==================== 数据统计分析 ====================

@router.get("/analytics", response_model=FortuneAnalyticsResponse)
async def get_fortune_analytics(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    reading_type: Optional[ReadingType] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取算命统计数据"""
    # 基础查询
    profile_query = db.query(FortuneProfile)
    reading_query = db.query(FortuneReading)
    
    # 时间筛选
    if start_date:
        reading_query = reading_query.filter(FortuneReading.created_at >= start_date)
    if end_date:
        reading_query = reading_query.filter(FortuneReading.created_at <= end_date)
    if reading_type:
        reading_query = reading_query.filter(FortuneReading.reading_type == reading_type)
    
    # 统计数据
    total_profiles = profile_query.count()
    total_readings = reading_query.count()
    bazi_readings = reading_query.filter(FortuneReading.reading_type == ReadingType.BAZI).count()
    tarot_readings = reading_query.filter(FortuneReading.reading_type == ReadingType.TAROT).count()
    
    # 问题类型统计
    question_stats = db.query(
        FortuneReading.question_type,
        func.count(FortuneReading.id).label('count')
    ).filter(
        FortuneReading.question_type.isnot(None)
    ).group_by(FortuneReading.question_type).all()
    
    # 用户参与度统计
    active_users = db.query(func.count(func.distinct(FortuneReading.customer_id))).scalar()
    
    return FortuneAnalyticsResponse(
        total_profiles=total_profiles,
        total_readings=total_readings,
        bazi_readings=bazi_readings,
        tarot_readings=tarot_readings,
        popular_questions=[
            {"question_type": stat[0], "count": stat[1], "percentage": (stat[1] / total_readings * 100) if total_readings > 0 else 0}
            for stat in question_stats
        ],
        user_engagement={
            "active_users": active_users,
            "returning_users": 0,  # 需要更复杂的查询
            "average_readings_per_user": total_readings / active_users if active_users > 0 else 0
        }
    )


@router.get("/analytics/engagement")
async def get_user_engagement_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取用户参与度统计"""
    # 简化的参与度统计
    active_users = db.query(func.count(func.distinct(FortuneReading.customer_id))).scalar()
    total_readings = db.query(func.count(FortuneReading.id)).scalar()
    
    return {
        "active_users": active_users,
        "returning_users": 0,  # 需要更复杂的查询逻辑
        "average_readings_per_user": total_readings / active_users if active_users > 0 else 0
    }


@router.get("/analytics/question-types")
async def get_question_type_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取问题类型统计"""
    total_readings = db.query(func.count(FortuneReading.id)).scalar()
    
    question_stats = db.query(
        FortuneReading.question_type,
        func.count(FortuneReading.id).label('count')
    ).filter(
        FortuneReading.question_type.isnot(None)
    ).group_by(FortuneReading.question_type).all()
    
    return [
        {
            "question_type": stat[0],
            "count": stat[1],
            "percentage": (stat[1] / total_readings * 100) if total_readings > 0 else 0
        }
        for stat in question_stats
    ]


@router.get("/analytics/trends")
async def get_fortune_trends(
    period: str = Query('daily', regex='^(daily|weekly|monthly)$'),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取算命趋势数据"""
    # 简化的趋势数据，返回每日统计
    query = db.query(
        func.date(FortuneReading.created_at).label('date'),
        func.count(FortuneReading.id).label('total_readings'),
        func.sum(func.case((FortuneReading.reading_type == ReadingType.BAZI, 1), else_=0)).label('bazi_count'),
        func.sum(func.case((FortuneReading.reading_type == ReadingType.TAROT, 1), else_=0)).label('tarot_count')
    ).group_by(func.date(FortuneReading.created_at))
    
    if start_date:
        query = query.filter(FortuneReading.created_at >= start_date)
    if end_date:
        query = query.filter(FortuneReading.created_at <= end_date)
    
    trends = query.order_by(func.date(FortuneReading.created_at)).all()
    
    return [
        {
            "date": str(trend.date),
            "total_readings": trend.total_readings,
            "bazi_count": trend.bazi_count,
            "tarot_count": trend.tarot_count
        }
        for trend in trends
    ]