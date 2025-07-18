from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from uuid import UUID

from app.content.banner.models import Banner, BannerTranslation, BannerType
from app.content.banner.schema import (
    BannerCreate, BannerUpdate, BannerListQuery, BannerBatchUpdate,
    BannerTranslationCreate, BannerTranslationUpdate
)
from app.content.models import ContentStatus


class BannerService:
    """*E��"""

    @staticmethod
    def create_banner(db: Session, banner_data: BannerCreate, created_by: Optional[UUID] = None) -> Banner:
        """�*E"""
        # �*E;�U
        banner = Banner(
            title=banner_data.title,
            type=banner_data.type,
            image_url=banner_data.image_url,
            mobile_image_url=banner_data.mobile_image_url,
            link_url=banner_data.link_url,
            position=banner_data.position,
            start_date=banner_data.start_date,
            end_date=banner_data.end_date,
            sort_order=banner_data.sort_order,
            alt_text=banner_data.alt_text,
            open_in_new_tab=banner_data.open_in_new_tab,
            additional_css=banner_data.additional_css,
            additional_info=banner_data.additional_info,
            status=ContentStatus.DRAFT,
            created_by=created_by,
            updated_by=created_by
        )
        
        db.add(banner)
        db.flush()  # ��IDFФ

        # �� ��
        for translation_data in banner_data.translations:
            translation = BannerTranslation(
                banner_id=banner.id,
                language_code=translation_data.language_code,
                title=translation_data.title,
                subtitle=translation_data.subtitle,
                description=translation_data.description,
                button_text=translation_data.button_text,
                alt_text=translation_data.alt_text
            )
            db.add(translation)

        db.commit()
        db.refresh(banner)
        return banner

    @staticmethod
    def get_banner_by_id(db: Session, banner_id: UUID) -> Optional[Banner]:
        """9nID��*E"""
        return db.query(Banner).filter(Banner.id == banner_id).first()

    @staticmethod
    def get_banners_list(db: Session, query: BannerListQuery) -> tuple[List[Banner], int]:
        """��*Eh"""
        base_query = db.query(Banner)

        # [	a�
        if query.type:
            base_query = base_query.filter(Banner.type == query.type)
        
        if query.status:
            base_query = base_query.filter(Banner.status == query.status)
        
        if query.position:
            base_query = base_query.filter(Banner.position == query.position)
        
        if query.search:
            search_term = f"%{query.search}%"
            base_query = base_query.filter(
                or_(
                    Banner.title.ilike(search_term),
                    Banner.alt_text.ilike(search_term)
                )
            )

        # ;p
        total = base_query.count()

        # ���u
        banners = (
            base_query
            .order_by(desc(Banner.sort_order), desc(Banner.created_at))
            .offset((query.page - 1) * query.page_size)
            .limit(query.page_size)
            .all()
        )

        return banners, total

    @staticmethod
    def update_banner(db: Session, banner_id: UUID, banner_data: BannerUpdate, updated_by: Optional[UUID] = None) -> Optional[Banner]:
        """��*E"""
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if not banner:
            return None

        # ��W�
        update_data = banner_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(banner, field, value)
        
        banner.updated_by = updated_by
        banner.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(banner)
        return banner

    @staticmethod
    def delete_banner(db: Session, banner_id: UUID) -> bool:
        """ d*E"""
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if not banner:
            return False

        db.delete(banner)
        db.commit()
        return True

    @staticmethod
    def get_banners_by_position(db: Session, position: str, language_code: Optional[str] = None) -> List[Banner]:
        """9nMn���;�*E"""
        query = db.query(Banner).filter(
            and_(
                Banner.position == position,
                Banner.status == ContentStatus.PUBLISHED,
                or_(
                    Banner.start_date.is_(None),
                    Banner.start_date <= datetime.utcnow()
                ),
                or_(
                    Banner.end_date.is_(None),
                    Banner.end_date >= datetime.utcnow()
                )
            )
        ).order_by(desc(Banner.sort_order), desc(Banner.created_at))

        return query.all()

    @staticmethod
    def get_banners_by_type(db: Session, banner_type: BannerType, language_code: Optional[str] = None) -> List[Banner]:
        """9n{����;�*E"""
        query = db.query(Banner).filter(
            and_(
                Banner.type == banner_type,
                Banner.status == ContentStatus.PUBLISHED,
                or_(
                    Banner.start_date.is_(None),
                    Banner.start_date <= datetime.utcnow()
                ),
                or_(
                    Banner.end_date.is_(None),
                    Banner.end_date >= datetime.utcnow()
                )
            )
        ).order_by(desc(Banner.sort_order), desc(Banner.created_at))

        return query.all()

    @staticmethod
    def batch_update_status(db: Session, batch_data: BannerBatchUpdate, updated_by: Optional[UUID] = None) -> List[Banner]:
        """y���*E�"""
        banners = db.query(Banner).filter(Banner.id.in_(batch_data.banner_ids)).all()
        
        for banner in banners:
            if batch_data.status:
                banner.status = batch_data.status
            
            if batch_data.sort_orders and str(banner.id) in batch_data.sort_orders:
                banner.sort_order = batch_data.sort_orders[str(banner.id)]
            
            banner.updated_by = updated_by
            banner.updated_at = datetime.utcnow()

        db.commit()
        return banners

    @staticmethod
    def create_translation(db: Session, banner_id: UUID, translation_data: BannerTranslationCreate) -> Optional[BannerTranslation]:
        """�*E��"""
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if not banner:
            return None

        # ��/&�X(�� ���
        existing = db.query(BannerTranslation).filter(
            and_(
                BannerTranslation.banner_id == banner_id,
                BannerTranslation.language_code == translation_data.language_code
            )
        ).first()

        if existing:
            # ���	��
            for field, value in translation_data.dict(exclude_unset=True).items():
                setattr(existing, field, value)
            existing.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # ����
            translation = BannerTranslation(
                banner_id=banner_id,
                **translation_data.dict()
            )
            db.add(translation)
            db.commit()
            db.refresh(translation)
            return translation

    @staticmethod
    def update_translation(db: Session, translation_id: UUID, translation_data: BannerTranslationUpdate) -> Optional[BannerTranslation]:
        """��*E��"""
        translation = db.query(BannerTranslation).filter(BannerTranslation.id == translation_id).first()
        if not translation:
            return None

        update_data = translation_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(translation, field, value)
        
        translation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(translation)
        return translation

    @staticmethod
    def delete_translation(db: Session, translation_id: UUID) -> bool:
        """ d*E��"""
        translation = db.query(BannerTranslation).filter(BannerTranslation.id == translation_id).first()
        if not translation:
            return False

        db.delete(translation)
        db.commit()
        return True

    @staticmethod
    def get_active_home_banners(db: Session, language_code: Optional[str] = None) -> List[Banner]:
        """�֖u�;�n��"""
        return BannerService.get_banners_by_type(db, BannerType.HOME_SLIDER, language_code)

    @staticmethod
    def reorder_banners(db: Session, banner_orders: Dict[str, int], updated_by: Optional[UUID] = None) -> List[Banner]:
        """Ͱ��*E"""
        banners = []
        for banner_id, sort_order in banner_orders.items():
            banner = db.query(Banner).filter(Banner.id == UUID(banner_id)).first()
            if banner:
                banner.sort_order = sort_order
                banner.updated_by = updated_by
                banner.updated_at = datetime.utcnow()
                banners.append(banner)

        db.commit()
        return banners