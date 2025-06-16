# -*- coding: utf-8 -*-
"""
商品翻译管理服务
提供商品多语言翻译的业务逻辑处理
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status

from app.product.models import ProductTranslation, Product
from app.product.translation.schema import (
    ProductTranslationCreate,
    ProductTranslationUpdate,
    ProductTranslationResponse,
    ProductTranslationListResponse,
    ProductTranslationSummary,
    LanguageTranslationInfo,
    TranslationContentUpdate,
    TranslationSEOUpdate
)


class ProductTranslationService:
    """商品翻译服务类"""

    @staticmethod
    def get_product_translations(
        db: Session,
        product_id: UUID,
        skip: int = 0,
        limit: int = 100,
        language_code: Optional[str] = None,
        has_seo: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> ProductTranslationListResponse:
        """
        获取商品翻译列表
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 构建查询条件
            query = db.query(ProductTranslation).filter(ProductTranslation.product_id == product_id)
            
            if language_code:
                query = query.filter(ProductTranslation.language_code == language_code)
            
            if has_seo is not None:
                if has_seo:
                    query = query.filter(
                        or_(
                            ProductTranslation.seo_title.isnot(None),
                            ProductTranslation.seo_description.isnot(None),
                            ProductTranslation.seo_keywords.isnot(None)
                        )
                    )
                else:
                    query = query.filter(
                        and_(
                            ProductTranslation.seo_title.is_(None),
                            ProductTranslation.seo_description.is_(None),
                            ProductTranslation.seo_keywords.is_(None)
                        )
                    )

            # 总数统计
            total = query.count()

            # 排序
            if hasattr(ProductTranslation, sort_by):
                order_column = getattr(ProductTranslation, sort_by)
                if sort_desc:
                    query = query.order_by(order_column.desc())
                else:
                    query = query.order_by(order_column.asc())

            # 分页
            translations = query.offset(skip).limit(limit).all()

            # 计算分页信息
            pages = (total + limit - 1) // limit if limit > 0 else 0
            page = (skip // limit) + 1 if limit > 0 else 1

            return ProductTranslationListResponse(
                items=[ProductTranslationResponse.from_orm(trans) for trans in translations],
                total=total,
                page=page,
                size=len(translations),
                pages=pages
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取翻译列表失败: {str(e)}")

    @staticmethod
    def get_translation_by_id(db: Session, translation_id: UUID) -> ProductTranslationResponse:
        """
        根据ID获取翻译详情
        """
        try:
            translation = db.query(ProductTranslation).filter(ProductTranslation.id == translation_id).first()
            if not translation:
                raise HTTPException(status_code=404, detail="翻译记录不存在")
            
            return ProductTranslationResponse.from_orm(translation)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取翻译详情失败: {str(e)}")

    @staticmethod
    def get_translation_by_language(
        db: Session, 
        product_id: UUID, 
        language_code: str
    ) -> ProductTranslationResponse:
        """
        根据语言代码获取翻译
        """
        try:
            translation = db.query(ProductTranslation).filter(
                and_(
                    ProductTranslation.product_id == product_id,
                    ProductTranslation.language_code == language_code
                )
            ).first()
            
            if not translation:
                raise HTTPException(status_code=404, detail=f"未找到 {language_code} 语言的翻译")
            
            return ProductTranslationResponse.from_orm(translation)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取翻译失败: {str(e)}")

    @staticmethod
    def create_product_translation(
        db: Session,
        product_id: UUID,
        translation_data: ProductTranslationCreate
    ) -> ProductTranslationResponse:
        """
        创建商品翻译
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 检查同语言翻译是否已存在
            existing_translation = db.query(ProductTranslation).filter(
                and_(
                    ProductTranslation.product_id == product_id,
                    ProductTranslation.language_code == translation_data.language_code
                )
            ).first()
            
            if existing_translation:
                raise HTTPException(
                    status_code=400, 
                    detail=f"商品已存在 {translation_data.language_code} 语言的翻译"
                )

            # 创建翻译记录
            db_translation = ProductTranslation(
                product_id=product_id,
                **translation_data.dict()
            )
            
            db.add(db_translation)
            db.commit()
            db.refresh(db_translation)

            return ProductTranslationResponse.from_orm(db_translation)

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"创建翻译失败: {str(e)}")

    @staticmethod
    def update_product_translation(
        db: Session,
        translation_id: UUID,
        translation_data: ProductTranslationUpdate
    ) -> ProductTranslationResponse:
        """
        更新商品翻译
        """
        try:
            # 查找翻译记录
            db_translation = db.query(ProductTranslation).filter(ProductTranslation.id == translation_id).first()
            if not db_translation:
                raise HTTPException(status_code=404, detail="翻译记录不存在")

            # 如果要更新语言代码，检查是否会产生冲突
            if translation_data.language_code and translation_data.language_code != db_translation.language_code:
                existing_translation = db.query(ProductTranslation).filter(
                    and_(
                        ProductTranslation.product_id == db_translation.product_id,
                        ProductTranslation.language_code == translation_data.language_code,
                        ProductTranslation.id != translation_id
                    )
                ).first()
                
                if existing_translation:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"已存在 {translation_data.language_code} 语言的翻译"
                    )

            # 更新字段
            update_data = translation_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_translation, field, value)
            
            db_translation.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_translation)

            return ProductTranslationResponse.from_orm(db_translation)

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"更新翻译失败: {str(e)}")

    @staticmethod
    def update_translation_content(
        db: Session,
        product_id: UUID,
        language_code: str,
        content_data: TranslationContentUpdate
    ) -> ProductTranslationResponse:
        """
        更新翻译内容
        """
        try:
            translation = db.query(ProductTranslation).filter(
                and_(
                    ProductTranslation.product_id == product_id,
                    ProductTranslation.language_code == language_code
                )
            ).first()
            
            if not translation:
                raise HTTPException(status_code=404, detail=f"未找到 {language_code} 语言的翻译")

            # 更新内容字段
            update_data = content_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(translation, field, value)
            
            translation.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(translation)

            return ProductTranslationResponse.from_orm(translation)

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"更新翻译内容失败: {str(e)}")

    @staticmethod
    def update_translation_seo(
        db: Session,
        product_id: UUID,
        language_code: str,
        seo_data: TranslationSEOUpdate
    ) -> ProductTranslationResponse:
        """
        更新翻译SEO信息
        """
        try:
            translation = db.query(ProductTranslation).filter(
                and_(
                    ProductTranslation.product_id == product_id,
                    ProductTranslation.language_code == language_code
                )
            ).first()
            
            if not translation:
                raise HTTPException(status_code=404, detail=f"未找到 {language_code} 语言的翻译")

            # 更新SEO字段
            update_data = seo_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(translation, field, value)
            
            translation.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(translation)

            return ProductTranslationResponse.from_orm(translation)

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"更新翻译SEO失败: {str(e)}")

    @staticmethod
    def delete_product_translation(db: Session, translation_id: UUID) -> dict:
        """
        删除商品翻译
        """
        try:
            db_translation = db.query(ProductTranslation).filter(ProductTranslation.id == translation_id).first()
            if not db_translation:
                raise HTTPException(status_code=404, detail="翻译记录不存在")

            db.delete(db_translation)
            db.commit()

            return {"message": "翻译删除成功"}

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"删除翻译失败: {str(e)}")

    @staticmethod
    def get_product_translation_summary(db: Session, product_id: UUID) -> ProductTranslationSummary:
        """
        获取商品翻译汇总信息
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 获取所有翻译记录
            translations = db.query(ProductTranslation).filter(ProductTranslation.product_id == product_id).all()
            
            if not translations:
                raise HTTPException(status_code=404, detail="商品暂无翻译设置")

            # 确定默认语言（通常取第一个或者是zh-cn）
            default_translation = next((t for t in translations if t.language_code in ['zh-cn', 'zh']), translations[0])
            
            # 构建语言信息列表
            languages = []
            for trans in translations:
                # 检查是否有SEO信息
                has_seo = bool(trans.seo_title or trans.seo_description or trans.seo_keywords)
                
                # 计算完整性（基础字段完整性）
                required_fields = [trans.name, trans.short_description, trans.description]
                completed_fields = sum(1 for field in required_fields if field and field.strip())
                is_complete = completed_fields >= 2  # 至少有名称和一个描述

                languages.append(LanguageTranslationInfo(
                    language_code=trans.language_code,
                    name=trans.name,
                    short_description=trans.short_description,
                    description=trans.description,
                    has_seo=has_seo,
                    is_complete=is_complete
                ))

            # 计算完成率
            complete_count = sum(1 for lang in languages if lang.is_complete)
            completion_rate = (complete_count / len(languages)) * 100 if languages else 0

            return ProductTranslationSummary(
                product_id=product_id,
                default_language=default_translation.language_code,
                languages=languages,
                total_languages=len(languages),
                completion_rate=round(completion_rate, 2)
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取翻译汇总失败: {str(e)}")

    @staticmethod
    def batch_create_translations(
        db: Session,
        product_id: UUID,
        translations_data: List[ProductTranslationCreate]
    ) -> List[ProductTranslationResponse]:
        """
        批量创建商品翻译
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 检查语言代码重复
            language_codes = [trans.language_code for trans in translations_data]
            if len(language_codes) != len(set(language_codes)):
                raise HTTPException(status_code=400, detail="批量创建中存在重复的语言代码")

            # 检查是否已存在相同语言的翻译
            existing_languages = db.query(ProductTranslation.language_code).filter(
                ProductTranslation.product_id == product_id,
                ProductTranslation.language_code.in_(language_codes)
            ).all()
            
            if existing_languages:
                existing_codes = [lang[0] for lang in existing_languages]
                raise HTTPException(
                    status_code=400, 
                    detail=f"以下语言已存在翻译: {', '.join(existing_codes)}"
                )

            # 批量创建
            created_translations = []
            for trans_data in translations_data:
                db_translation = ProductTranslation(
                    product_id=product_id,
                    **trans_data.dict()
                )
                db.add(db_translation)
                created_translations.append(db_translation)

            db.commit()
            
            # 刷新所有记录
            for trans in created_translations:
                db.refresh(trans)

            return [ProductTranslationResponse.from_orm(trans) for trans in created_translations]

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"批量创建翻译失败: {str(e)}")

    @staticmethod
    def copy_translation(
        db: Session,
        product_id: UUID,
        source_language: str,
        target_language: str
    ) -> ProductTranslationResponse:
        """
        复制翻译到新语言
        """
        try:
            # 查找源翻译
            source_translation = db.query(ProductTranslation).filter(
                and_(
                    ProductTranslation.product_id == product_id,
                    ProductTranslation.language_code == source_language
                )
            ).first()
            
            if not source_translation:
                raise HTTPException(status_code=404, detail=f"未找到 {source_language} 语言的翻译")

            # 检查目标语言是否已存在
            existing_translation = db.query(ProductTranslation).filter(
                and_(
                    ProductTranslation.product_id == product_id,
                    ProductTranslation.language_code == target_language
                )
            ).first()
            
            if existing_translation:
                raise HTTPException(status_code=400, detail=f"{target_language} 语言翻译已存在")

            # 创建新翻译
            new_translation = ProductTranslation(
                product_id=product_id,
                language_code=target_language,
                name=source_translation.name,
                short_description=source_translation.short_description,
                description=source_translation.description,
                specifications=source_translation.specifications,
                benefits=source_translation.benefits,
                instructions=source_translation.instructions,
                seo_title=source_translation.seo_title,
                seo_description=source_translation.seo_description,
                seo_keywords=source_translation.seo_keywords
            )
            
            db.add(new_translation)
            db.commit()
            db.refresh(new_translation)

            return ProductTranslationResponse.from_orm(new_translation)

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"复制翻译失败: {str(e)}") 