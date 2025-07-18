from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from uuid import UUID

from app.content.promotion.models import (
    PromotionContent, PromotionContentTranslation, PromotionContentType,
    PromotionTextTemplate
)
from app.content.promotion.schema import (
    PromotionContentCreate, PromotionContentUpdate, PromotionContentListQuery,
    PromotionContentBatchUpdate, PromotionContentTranslationCreate,
    PromotionContentTranslationUpdate, PromotionTextTemplateCreate,
    PromotionTextTemplateUpdate
)
from app.content.models import ContentStatus


class PromotionContentService:
    """促销内容管理服务"""

    @staticmethod
    def create_content(db: Session, content_data: PromotionContentCreate, created_by: Optional[UUID] = None) -> PromotionContent:
        """创建促销内容"""
        # 创建主记录
        content = PromotionContent(
            title=content_data.title,
            content_type=content_data.content_type,
            promotion_id=UUID(content_data.promotion_id) if content_data.promotion_id else None,
            short_text=content_data.short_text,
            content=content_data.content,
            button_text=content_data.button_text,
            link_url=content_data.link_url,
            background_color=content_data.background_color,
            text_color=content_data.text_color,
            font_size=content_data.font_size,
            position=content_data.position,
            start_date=content_data.start_date,
            end_date=content_data.end_date,
            sort_order=content_data.sort_order,
            target_pages=content_data.target_pages,
            target_countries=content_data.target_countries,
            target_languages=content_data.target_languages,
            additional_settings=content_data.additional_settings,
            status=ContentStatus.DRAFT,
            created_by=created_by,
            updated_by=created_by
        )
        
        db.add(content)
        db.flush()  # 获取ID但不提交

        # 创建多语言翻译
        for translation_data in content_data.translations:
            translation = PromotionContentTranslation(
                content_id=content.id,
                language_code=translation_data.language_code,
                title=translation_data.title,
                short_text=translation_data.short_text,
                content=translation_data.content,
                button_text=translation_data.button_text
            )
            db.add(translation)

        db.commit()
        db.refresh(content)
        return content

    @staticmethod
    def get_content_by_id(db: Session, content_id: UUID) -> Optional[PromotionContent]:
        """根据ID获取促销内容"""
        return db.query(PromotionContent).filter(PromotionContent.id == content_id).first()

    @staticmethod
    def get_contents_list(db: Session, query: PromotionContentListQuery) -> tuple[List[PromotionContent], int]:
        """获取促销内容列表"""
        base_query = db.query(PromotionContent)

        # 筛选条件
        if query.content_type:
            base_query = base_query.filter(PromotionContent.content_type == query.content_type)
        
        if query.status:
            base_query = base_query.filter(PromotionContent.status == query.status)
        
        if query.position:
            base_query = base_query.filter(PromotionContent.position == query.position)
            
        if query.promotion_id:
            base_query = base_query.filter(PromotionContent.promotion_id == UUID(query.promotion_id))
        
        if query.search:
            search_term = f"%{query.search}%"
            base_query = base_query.filter(
                or_(
                    PromotionContent.title.ilike(search_term),
                    PromotionContent.short_text.ilike(search_term),
                    PromotionContent.content.ilike(search_term)
                )
            )

        # 总数
        total = base_query.count()

        # 排序和分页
        contents = (
            base_query
            .order_by(desc(PromotionContent.sort_order), desc(PromotionContent.created_at))
            .offset((query.page - 1) * query.page_size)
            .limit(query.page_size)
            .all()
        )

        return contents, total

    @staticmethod
    def update_content(db: Session, content_id: UUID, content_data: PromotionContentUpdate, updated_by: Optional[UUID] = None) -> Optional[PromotionContent]:
        """更新促销内容"""
        content = db.query(PromotionContent).filter(PromotionContent.id == content_id).first()
        if not content:
            return None

        # 更新字段
        update_data = content_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'promotion_id' and value:
                value = UUID(value)
            setattr(content, field, value)
        
        content.updated_by = updated_by
        content.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(content)
        return content

    @staticmethod
    def delete_content(db: Session, content_id: UUID) -> bool:
        """删除促销内容"""
        content = db.query(PromotionContent).filter(PromotionContent.id == content_id).first()
        if not content:
            return False

        db.delete(content)
        db.commit()
        return True

    @staticmethod
    def get_active_contents_by_type(db: Session, content_type: PromotionContentType, language_code: Optional[str] = None) -> List[PromotionContent]:
        """根据类型获取激活的促销内容"""
        now = datetime.utcnow()
        query = db.query(PromotionContent).filter(
            and_(
                PromotionContent.content_type == content_type,
                PromotionContent.status == ContentStatus.PUBLISHED,
                or_(
                    PromotionContent.start_date.is_(None),
                    PromotionContent.start_date <= now
                ),
                or_(
                    PromotionContent.end_date.is_(None),
                    PromotionContent.end_date >= now
                )
            )
        ).order_by(desc(PromotionContent.sort_order), desc(PromotionContent.created_at))

        return query.all()

    @staticmethod
    def get_active_contents_by_position(db: Session, position: str, language_code: Optional[str] = None) -> List[PromotionContent]:
        """根据位置获取激活的促销内容"""
        now = datetime.utcnow()
        query = db.query(PromotionContent).filter(
            and_(
                PromotionContent.position == position,
                PromotionContent.status == ContentStatus.PUBLISHED,
                or_(
                    PromotionContent.start_date.is_(None),
                    PromotionContent.start_date <= now
                ),
                or_(
                    PromotionContent.end_date.is_(None),
                    PromotionContent.end_date >= now
                )
            )
        ).order_by(desc(PromotionContent.sort_order), desc(PromotionContent.created_at))

        return query.all()

    @staticmethod
    def batch_update_status(db: Session, batch_data: PromotionContentBatchUpdate, updated_by: Optional[UUID] = None) -> List[PromotionContent]:
        """批量更新促销内容状态"""
        contents = db.query(PromotionContent).filter(PromotionContent.id.in_([UUID(id) for id in batch_data.content_ids])).all()
        
        for content in contents:
            if batch_data.status:
                content.status = batch_data.status
            
            if batch_data.sort_orders and str(content.id) in batch_data.sort_orders:
                content.sort_order = batch_data.sort_orders[str(content.id)]
            
            content.updated_by = updated_by
            content.updated_at = datetime.utcnow()

        db.commit()
        return contents

    @staticmethod
    def create_translation(db: Session, content_id: UUID, translation_data: PromotionContentTranslationCreate) -> Optional[PromotionContentTranslation]:
        """创建促销内容翻译"""
        content = db.query(PromotionContent).filter(PromotionContent.id == content_id).first()
        if not content:
            return None

        # 检查是否已存在该语言的翻译
        existing = db.query(PromotionContentTranslation).filter(
            and_(
                PromotionContentTranslation.content_id == content_id,
                PromotionContentTranslation.language_code == translation_data.language_code
            )
        ).first()

        if existing:
            # 更新现有翻译
            for field, value in translation_data.dict(exclude_unset=True).items():
                setattr(existing, field, value)
            existing.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # 创建新翻译
            translation = PromotionContentTranslation(
                content_id=content_id,
                **translation_data.dict()
            )
            db.add(translation)
            db.commit()
            db.refresh(translation)
            return translation

    @staticmethod
    def update_translation(db: Session, translation_id: UUID, translation_data: PromotionContentTranslationUpdate) -> Optional[PromotionContentTranslation]:
        """更新促销内容翻译"""
        translation = db.query(PromotionContentTranslation).filter(PromotionContentTranslation.id == translation_id).first()
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
        """删除促销内容翻译"""
        translation = db.query(PromotionContentTranslation).filter(PromotionContentTranslation.id == translation_id).first()
        if not translation:
            return False

        db.delete(translation)
        db.commit()
        return True

    @staticmethod
    def get_banner_texts(db: Session, language_code: Optional[str] = None) -> List[PromotionContent]:
        """获取横幅文本"""
        return PromotionContentService.get_active_contents_by_type(db, PromotionContentType.BANNER_TEXT, language_code)

    @staticmethod
    def get_notifications(db: Session, language_code: Optional[str] = None) -> List[PromotionContent]:
        """获取通知文本"""
        return PromotionContentService.get_active_contents_by_type(db, PromotionContentType.NOTIFICATION, language_code)

    @staticmethod
    def reorder_contents(db: Session, content_orders: Dict[str, int], updated_by: Optional[UUID] = None) -> List[PromotionContent]:
        """重新排序促销内容"""
        contents = []
        for content_id, sort_order in content_orders.items():
            content = db.query(PromotionContent).filter(PromotionContent.id == UUID(content_id)).first()
            if content:
                content.sort_order = sort_order
                content.updated_by = updated_by
                content.updated_at = datetime.utcnow()
                contents.append(content)

        db.commit()
        return contents


class PromotionTextTemplateService:
    """促销文本模板服务"""

    @staticmethod
    def create_template(db: Session, template_data: PromotionTextTemplateCreate) -> PromotionTextTemplate:
        """创建促销文本模板"""
        template = PromotionTextTemplate(
            name=template_data.name,
            content_type=template_data.content_type,
            template_title=template_data.template_title,
            template_content=template_data.template_content,
            template_variables=template_data.template_variables,
            default_styles=template_data.default_styles
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

    @staticmethod
    def get_template_by_id(db: Session, template_id: UUID) -> Optional[PromotionTextTemplate]:
        """根据ID获取模板"""
        return db.query(PromotionTextTemplate).filter(PromotionTextTemplate.id == template_id).first()

    @staticmethod
    def get_templates_by_type(db: Session, content_type: PromotionContentType) -> List[PromotionTextTemplate]:
        """根据类型获取模板列表"""
        return db.query(PromotionTextTemplate).filter(
            PromotionTextTemplate.content_type == content_type
        ).order_by(desc(PromotionTextTemplate.usage_count)).all()

    @staticmethod
    def update_template(db: Session, template_id: UUID, template_data: PromotionTextTemplateUpdate) -> Optional[PromotionTextTemplate]:
        """更新促销文本模板"""
        template = db.query(PromotionTextTemplate).filter(PromotionTextTemplate.id == template_id).first()
        if not template:
            return None

        update_data = template_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(template, field, value)
        
        template.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(template)
        return template

    @staticmethod
    def delete_template(db: Session, template_id: UUID) -> bool:
        """删除促销文本模板"""
        template = db.query(PromotionTextTemplate).filter(PromotionTextTemplate.id == template_id).first()
        if not template:
            return False

        db.delete(template)
        db.commit()
        return True

    @staticmethod
    def increment_usage(db: Session, template_id: UUID) -> Optional[PromotionTextTemplate]:
        """增加模板使用次数"""
        template = db.query(PromotionTextTemplate).filter(PromotionTextTemplate.id == template_id).first()
        if not template:
            return None

        template.usage_count += 1
        db.commit()
        db.refresh(template)
        return template