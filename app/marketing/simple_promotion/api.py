from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from .models import SimplePromotion
from .schema import (
    SimplePromotionCreate, 
    SimplePromotionUpdate, 
    SimplePromotionResponse,
    ApplyPromotionRequest,
    PromotionResult,
    PROMOTION_TEMPLATES
)
from .service import PromotionService, PromotionTemplateService


router = APIRouter()


@router.post("/promotions", response_model=SimplePromotionResponse)
async def create_promotion(
    promotion: SimplePromotionCreate,
    db: Session = Depends(get_db)
):
    """创建促销"""
    # 检查代码是否已存在
    existing = db.query(SimplePromotion).filter(SimplePromotion.code == promotion.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="促销代码已存在"
        )
    
    db_promotion = SimplePromotion(**promotion.dict())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    
    return db_promotion


@router.get("/promotions", response_model=List[SimplePromotionResponse])
async def list_promotions(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取促销列表"""
    query = db.query(SimplePromotion)
    
    if is_active is not None:
        query = query.filter(SimplePromotion.is_active == is_active)
    
    promotions = query.offset(skip).limit(limit).all()
    return promotions


@router.get("/promotions/{promotion_id}", response_model=SimplePromotionResponse)
async def get_promotion(
    promotion_id: UUID,
    db: Session = Depends(get_db)
):
    """获取单个促销"""
    promotion = db.query(SimplePromotion).filter(SimplePromotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="促销不存在"
        )
    return promotion


@router.put("/promotions/{promotion_id}", response_model=SimplePromotionResponse)
async def update_promotion(
    promotion_id: UUID,
    promotion_update: SimplePromotionUpdate,
    db: Session = Depends(get_db)
):
    """更新促销"""
    promotion = db.query(SimplePromotion).filter(SimplePromotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="促销不存在"
        )
    
    update_data = promotion_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(promotion, field, value)
    
    db.commit()
    db.refresh(promotion)
    return promotion


@router.delete("/promotions/{promotion_id}")
async def delete_promotion(
    promotion_id: UUID,
    db: Session = Depends(get_db)
):
    """删除促销"""
    promotion = db.query(SimplePromotion).filter(SimplePromotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="促销不存在"
        )
    
    db.delete(promotion)
    db.commit()
    return {"message": "促销已删除"}


@router.post("/promotions/apply", response_model=PromotionResult)
async def apply_promotion(
    request: ApplyPromotionRequest,
    db: Session = Depends(get_db)
):
    """应用促销"""
    service = PromotionService(db)
    result = service.apply_promotion(request)
    return result


@router.get("/promotions/code/{code}", response_model=SimplePromotionResponse)
async def get_promotion_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """根据代码获取促销"""
    service = PromotionService(db)
    promotion = service.get_promotion_by_code(code)
    
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="促销代码不存在"
        )
    
    return promotion


@router.post("/promotions/validate/{code}")
async def validate_promotion(
    code: str,
    customer_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """验证促销代码"""
    service = PromotionService(db)
    promotion = service.get_promotion_by_code(code)
    
    if not promotion:
        return {"valid": False, "message": "促销代码不存在"}
    
    if not service.is_promotion_valid(promotion):
        return {"valid": False, "message": "促销已过期或无效"}
    
    if customer_id:
        customer_usage = service.check_customer_usage(promotion.id, customer_id)
        if customer_usage >= promotion.per_customer_limit:
            return {"valid": False, "message": "您已达到此促销的使用次数限制"}
    
    return {
        "valid": True, 
        "message": "促销代码有效",
        "promotion": {
            "name": promotion.name,
            "description": promotion.description,
            "discount_type": promotion.discount_type,
            "discount_value": promotion.discount_value
        }
    }


# 模板相关接口
@router.get("/promotion-templates")
async def get_promotion_templates():
    """获取促销模板"""
    return PROMOTION_TEMPLATES


@router.post("/promotions/from-template")
async def create_promotion_from_template(
    template_name: str,
    code: str,
    start_date: str,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """从模板创建促销"""
    try:
        from datetime import datetime
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date) if end_date else None
        
        promotion_data = PromotionTemplateService.create_from_template(
            template_name, code, start_dt, end_dt
        )
        
        # 检查代码是否已存在
        existing = db.query(SimplePromotion).filter(SimplePromotion.code == code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="促销代码已存在"
            )
        
        db_promotion = SimplePromotion(**promotion_data)
        db.add(db_promotion)
        db.commit()
        db.refresh(db_promotion)
        
        return db_promotion
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 促销统计接口
@router.get("/promotions/{promotion_id}/stats")
async def get_promotion_stats(
    promotion_id: UUID,
    db: Session = Depends(get_db)
):
    """获取促销统计信息"""
    promotion = db.query(SimplePromotion).filter(SimplePromotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="促销不存在"
        )
    
    from .models import CustomerPromotionUsage
    
    # 统计使用情况
    total_usage = promotion.usage_count
    unique_customers = db.query(CustomerPromotionUsage).filter(
        CustomerPromotionUsage.promotion_id == promotion_id
    ).count()
    
    # 计算使用率
    usage_rate = 0
    if promotion.usage_limit:
        usage_rate = (total_usage / promotion.usage_limit) * 100
    
    return {
        "promotion_id": promotion_id,
        "promotion_name": promotion.name,
        "total_usage": total_usage,
        "usage_limit": promotion.usage_limit,
        "usage_rate": usage_rate,
        "unique_customers": unique_customers,
        "is_active": promotion.is_active,
        "start_date": promotion.start_date,
        "end_date": promotion.end_date
    }