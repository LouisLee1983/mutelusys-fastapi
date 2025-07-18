from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_customer
from app.customer.models import Customer
from app.fortune.service import FortuneService
from app.fortune.schema import (
    BaziAnalysisRequest,
    TarotAnalysisRequest, 
    AnalysisResultResponse,
    FortuneReadingResponse,
    FortuneHistoryResponse,
    FortuneProfileResponse
)

router = APIRouter()


@router.post("/bazi/analyze", response_model=AnalysisResultResponse)
async def analyze_bazi(
    request: BaziAnalysisRequest,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """八字命理分析"""
    try:
        service = FortuneService(db)
        result = await service.create_bazi_reading(str(current_customer.id), request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"八字分析失败: {str(e)}"
        )


@router.post("/tarot/analyze", response_model=AnalysisResultResponse)
async def analyze_tarot(
    request: TarotAnalysisRequest,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """塔罗牌分析"""
    try:
        service = FortuneService(db)
        result = await service.create_tarot_reading(str(current_customer.id), request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"塔罗分析失败: {str(e)}"
        )


@router.get("/history", response_model=FortuneHistoryResponse)
async def get_fortune_history(
    limit: int = 20,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """获取算命历史记录"""
    service = FortuneService(db)
    readings = service.get_reading_history(str(current_customer.id), limit)
    
    # 获取用户档案
    profile = db.query(service.db.query(FortuneProfile).filter(
        FortuneProfile.customer_id == current_customer.id
    ).first())
    
    return FortuneHistoryResponse(
        readings=[FortuneReadingResponse.from_orm(reading) for reading in readings],
        total_count=len(readings),
        has_profile=profile is not None,
        profile=FortuneProfileResponse.from_orm(profile) if profile else None
    )


@router.get("/reading/{reading_id}", response_model=FortuneReadingResponse)
async def get_reading_detail(
    reading_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """获取算命记录详情"""
    service = FortuneService(db)
    reading = service.get_reading_by_id(reading_id, str(current_customer.id))
    
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="算命记录不存在"
        )
    
    return FortuneReadingResponse.from_orm(reading)