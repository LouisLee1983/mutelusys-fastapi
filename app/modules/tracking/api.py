from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin_user, get_current_user_optional
from app.core.security import get_password_hash
from app.modules.tracking import schema, service
from app.security.models import User
from app.security.user.models import User as AdminUser

router = APIRouter()


@router.post("/campaigns", response_model=schema.CampaignInDB)
def create_campaign(
    campaign_data: schema.CampaignCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建推广活动"""
    # 设置广告投手为当前管理员
    campaign_data_dict = campaign_data.dict()
    campaign_data_dict["advertiser_id"] = current_admin.id
    
    return service.TrackingService.create_campaign(
        db, 
        schema.CampaignCreate(**campaign_data_dict)
    )


@router.get("/campaigns", response_model=List[schema.CampaignInDB])
def get_campaigns(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取推广活动列表"""
    from app.modules.tracking.models import TrackingCampaign
    
    query = db.query(TrackingCampaign)
    
    # 如果不是超级管理员，只能看到自己的推广活动
    if not current_admin.is_superuser:
        query = query.filter(TrackingCampaign.advertiser_id == current_admin.id)
    
    if status:
        query = query.filter(TrackingCampaign.status == status)
    if platform:
        query = query.filter(TrackingCampaign.platform == platform)
    
    campaigns = query.offset(skip).limit(limit).all()
    return campaigns


@router.get("/campaigns/{campaign_id}/stats", response_model=schema.CampaignStats)
def get_campaign_stats(
    campaign_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取推广活动统计数据"""
    return service.TrackingService.get_campaign_stats(
        db, campaign_id, start_date, end_date
    )


@router.post("/generate-url")
def generate_tracking_url(
    base_url: str,
    campaign_code: str,
    platform: str,
    content: Optional[str] = None,
    term: Optional[str] = None,
    current_admin = Depends(get_current_admin_user)
):
    """生成带追踪参数的URL"""
    tracking_url = service.TrackingService.generate_tracking_url(
        base_url, campaign_code, platform, content, term
    )
    return {"tracking_url": tracking_url}


# 公开API（不需要登录）

@router.post("/track/visit", response_model=schema.TrackingVisitInDB)
def track_visit(
    visit_data: schema.TrackingVisitCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    """记录用户访问"""
    # 从请求头获取IP和User-Agent
    visit_data_dict = visit_data.dict()
    visit_data_dict["ip_address"] = request.client.host
    visit_data_dict["user_agent"] = request.headers.get("user-agent", "")
    
    user_id = current_user.id if current_user else None
    
    return service.TrackingService.record_visit(
        db, 
        schema.TrackingVisitCreate(**visit_data_dict),
        user_id
    )


@router.post("/track/behavior", response_model=schema.TrackingBehaviorInDB)
def track_behavior(
    behavior_data: schema.TrackingBehaviorCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    """记录用户行为"""
    user_id = current_user.id if current_user else None
    
    return service.TrackingService.track_behavior(
        db, behavior_data, user_id
    )


@router.get("/recently-viewed", response_model=List[schema.RecentlyViewedProduct])
def get_recently_viewed(
    session_id: str,
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    """获取最近浏览的商品"""
    user_id = current_user.id if current_user else None
    
    return service.TrackingService.get_recently_viewed(
        db, session_id, user_id, limit
    )


@router.post("/track/batch-behaviors")
def track_batch_behaviors(
    behaviors: List[schema.TrackingBehaviorCreate],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    """批量记录用户行为"""
    user_id = current_user.id if current_user else None
    
    results = []
    for behavior_data in behaviors:
        try:
            result = service.TrackingService.track_behavior(
                db, behavior_data, user_id
            )
            results.append({"success": True, "id": result.id})
        except Exception as e:
            results.append({"success": False, "error": str(e)})
    
    return {"results": results}