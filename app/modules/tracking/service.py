from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from fastapi import HTTPException, status
import uuid

from app.modules.tracking import models, schema
from app.product.models import Product
from app.customer.models import Customer
from app.order.models import Order


class TrackingService:
    
    @staticmethod
    def create_campaign(
        db: Session, 
        campaign_data: schema.CampaignCreate
    ) -> models.TrackingCampaign:
        """创建推广活动"""
        # 检查campaign_code是否已存在
        existing = db.query(models.TrackingCampaign).filter(
            models.TrackingCampaign.campaign_code == campaign_data.campaign_code
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Campaign code {campaign_data.campaign_code} already exists"
            )
        
        campaign = models.TrackingCampaign(**campaign_data.dict())
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign
    
    @staticmethod
    def record_visit(
        db: Session,
        visit_data: schema.TrackingVisitCreate,
        user_id: Optional[int] = None
    ) -> models.TrackingVisit:
        """记录访问"""
        visit = models.TrackingVisit(**visit_data.dict())
        visit.user_id = user_id
        
        # 根据utm_campaign查找对应的campaign
        if visit_data.utm_campaign:
            campaign = db.query(models.TrackingCampaign).filter(
                models.TrackingCampaign.campaign_code == visit_data.utm_campaign
            ).first()
            if campaign:
                visit.campaign_id = campaign.id
        
        db.add(visit)
        db.commit()
        db.refresh(visit)
        return visit
    
    @staticmethod
    def track_behavior(
        db: Session,
        behavior_data: schema.TrackingBehaviorCreate,
        user_id: Optional[int] = None
    ) -> models.TrackingBehavior:
        """记录用户行为"""
        behavior = models.TrackingBehavior(
            event_type=behavior_data.event_type,
            page_url=behavior_data.page_url,
            duration=behavior_data.duration,
            event_data=behavior_data.event_data,
            product_id=behavior_data.product_id,
            user_id=user_id
        )
        
        # 如果提供了session_id而没有visit_id，尝试查找最近的visit
        if behavior_data.session_id and not behavior_data.visit_id:
            recent_visit = db.query(models.TrackingVisit).filter(
                models.TrackingVisit.session_id == behavior_data.session_id
            ).order_by(models.TrackingVisit.visit_time.desc()).first()
            
            if recent_visit:
                behavior.visit_id = recent_visit.id
        else:
            behavior.visit_id = behavior_data.visit_id
        
        db.add(behavior)
        db.commit()
        db.refresh(behavior)
        
        # 如果是查看商品，更新浏览历史
        if behavior_data.event_type == "view_product" and behavior_data.product_id:
            TrackingService.update_view_history(
                db, 
                product_id=behavior_data.product_id,
                session_id=behavior_data.session_id,
                user_id=user_id
            )
        
        return behavior
    
    @staticmethod
    def update_view_history(
        db: Session,
        product_id: int,
        session_id: str,
        user_id: Optional[int] = None
    ):
        """更新商品浏览历史"""
        # 查找现有记录
        query = db.query(models.ProductViewHistory).filter(
            models.ProductViewHistory.product_id == product_id,
            models.ProductViewHistory.session_id == session_id
        )
        
        if user_id:
            query = query.filter(models.ProductViewHistory.user_id == user_id)
        
        view_history = query.first()
        
        if view_history:
            # 更新浏览次数和时间
            view_history.view_count += 1
            view_history.last_viewed_at = datetime.utcnow()
        else:
            # 创建新记录
            view_history = models.ProductViewHistory(
                product_id=product_id,
                session_id=session_id,
                user_id=user_id
            )
            db.add(view_history)
        
        db.commit()
    
    @staticmethod
    def get_recently_viewed(
        db: Session,
        session_id: str,
        user_id: Optional[int] = None,
        limit: int = 10
    ) -> List[schema.RecentlyViewedProduct]:
        """获取最近浏览的商品"""
        query = db.query(
            models.ProductViewHistory,
            Product
        ).join(
            Product, models.ProductViewHistory.product_id == Product.id
        ).filter(
            models.ProductViewHistory.session_id == session_id
        )
        
        if user_id:
            query = query.filter(models.ProductViewHistory.user_id == user_id)
        
        results = query.order_by(
            models.ProductViewHistory.last_viewed_at.desc()
        ).limit(limit).all()
        
        recently_viewed = []
        for history, product in results:
            recently_viewed.append(schema.RecentlyViewedProduct(
                product_id=product.id,
                product_name=product.product_name,
                product_image=product.main_image,
                price=product.price,
                view_count=history.view_count,
                last_viewed_at=history.last_viewed_at
            ))
        
        return recently_viewed
    
    @staticmethod
    def get_campaign_stats(
        db: Session,
        campaign_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> schema.CampaignStats:
        """获取推广活动统计数据"""
        campaign = db.query(models.TrackingCampaign).filter(
            models.TrackingCampaign.id == campaign_id
        ).first()
        
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
        
        # 构建查询条件
        visit_query = db.query(models.TrackingVisit).filter(
            models.TrackingVisit.campaign_id == campaign_id
        )
        
        if start_date:
            visit_query = visit_query.filter(
                models.TrackingVisit.visit_time >= start_date
            )
        if end_date:
            visit_query = visit_query.filter(
                models.TrackingVisit.visit_time <= end_date
            )
        
        # 统计数据
        total_visits = visit_query.count()
        unique_visitors = visit_query.distinct(models.TrackingVisit.visitor_id).count()
        registered_users = visit_query.filter(
            models.TrackingVisit.user_id.isnot(None)
        ).distinct(models.TrackingVisit.user_id).count()
        
        # 获取购买数据
        visit_ids = [v.id for v in visit_query.all()]
        purchases = db.query(models.TrackingBehavior).filter(
            models.TrackingBehavior.visit_id.in_(visit_ids),
            models.TrackingBehavior.event_type == "purchase"
        ).all()
        
        total_purchases = len(purchases)
        total_revenue = sum(
            p.event_data.get("order_amount", 0) for p in purchases 
            if p.event_data
        )
        
        # 计算转化率
        conversion_rate = (total_purchases / total_visits * 100) if total_visits > 0 else 0
        
        # 计算ROI
        roi = None
        if campaign.budget and campaign.budget > 0:
            roi = ((total_revenue - campaign.budget) / campaign.budget * 100)
        
        return schema.CampaignStats(
            campaign_id=campaign.id,
            campaign_code=campaign.campaign_code,
            campaign_name=campaign.campaign_name,
            platform=campaign.platform,
            total_visits=total_visits,
            unique_visitors=unique_visitors,
            registered_users=registered_users,
            total_purchases=total_purchases,
            conversion_rate=conversion_rate,
            total_revenue=total_revenue,
            roi=roi
        )
    
    @staticmethod
    def generate_tracking_url(
        base_url: str,
        campaign_code: str,
        platform: str,
        content: Optional[str] = None,
        term: Optional[str] = None
    ) -> str:
        """生成带追踪参数的URL"""
        params = [
            f"utm_source={platform}",
            f"utm_medium=social",
            f"utm_campaign={campaign_code}"
        ]
        
        if content:
            params.append(f"utm_content={content}")
        if term:
            params.append(f"utm_term={term}")
        
        # 检查base_url是否已有参数
        separator = "&" if "?" in base_url else "?"
        
        return f"{base_url}{separator}{'&'.join(params)}"