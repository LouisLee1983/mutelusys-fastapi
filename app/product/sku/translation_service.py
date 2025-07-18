# -*- coding: utf-8 -*-
"""
ProductSku翻译服务模块
提供SKU翻译的增删改查和自动翻译功能
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.product.models import ProductSku, ProductSkuTranslation
from app.product.sku.schema import (
    ProductSkuTranslationCreate,
    ProductSkuTranslationUpdate,
    ProductSkuTranslationResponse
)


class ProductSkuTranslationService:
    """SKU翻译服务类"""

    @staticmethod
    def create_translation(
        db: Session, 
        sku_id: UUID, 
        translation_data: ProductSkuTranslationCreate
    ) -> ProductSkuTranslationResponse:
        """创建SKU翻译"""
        # 检查SKU是否存在
        sku = db.query(ProductSku).filter(ProductSku.id == sku_id).first()
        if not sku:
            raise ValueError(f"SKU {sku_id} 不存在")
        
        # 检查是否已存在该语言的翻译
        existing = db.query(ProductSkuTranslation).filter(
            and_(
                ProductSkuTranslation.sku_id == sku_id,
                ProductSkuTranslation.language_code == translation_data.language_code
            )
        ).first()
        
        if existing:
            raise ValueError(f"SKU {sku_id} 的 {translation_data.language_code} 翻译已存在")
        
        # 创建翻译记录
        translation = ProductSkuTranslation(
            sku_id=sku_id,
            language_code=translation_data.language_code,
            sku_name=translation_data.sku_name
        )
        
        db.add(translation)
        db.commit()
        db.refresh(translation)
        
        return ProductSkuTranslationResponse.from_orm(translation)

    @staticmethod
    def get_translation(
        db: Session, 
        sku_id: UUID, 
        language_code: str
    ) -> Optional[ProductSkuTranslationResponse]:
        """获取指定语言的SKU翻译"""
        translation = db.query(ProductSkuTranslation).filter(
            and_(
                ProductSkuTranslation.sku_id == sku_id,
                ProductSkuTranslation.language_code == language_code
            )
        ).first()
        
        if translation:
            return ProductSkuTranslationResponse.from_orm(translation)
        return None

    @staticmethod
    def get_sku_translations(db: Session, sku_id: UUID) -> List[ProductSkuTranslationResponse]:
        """获取SKU的所有翻译"""
        translations = db.query(ProductSkuTranslation).filter(
            ProductSkuTranslation.sku_id == sku_id
        ).all()
        
        return [ProductSkuTranslationResponse.from_orm(t) for t in translations]

    @staticmethod
    def update_translation(
        db: Session,
        sku_id: UUID,
        language_code: str,
        translation_data: ProductSkuTranslationUpdate
    ) -> Optional[ProductSkuTranslationResponse]:
        """更新SKU翻译"""
        translation = db.query(ProductSkuTranslation).filter(
            and_(
                ProductSkuTranslation.sku_id == sku_id,
                ProductSkuTranslation.language_code == language_code
            )
        ).first()
        
        if not translation:
            return None
        
        # 更新字段
        if translation_data.sku_name is not None:
            translation.sku_name = translation_data.sku_name
        
        db.commit()
        db.refresh(translation)
        
        return ProductSkuTranslationResponse.from_orm(translation)

    @staticmethod
    def delete_translation(db: Session, sku_id: UUID, language_code: str) -> bool:
        """删除SKU翻译"""
        translation = db.query(ProductSkuTranslation).filter(
            and_(
                ProductSkuTranslation.sku_id == sku_id,
                ProductSkuTranslation.language_code == language_code
            )
        ).first()
        
        if not translation:
            return False
        
        db.delete(translation)
        db.commit()
        return True

    @staticmethod
    async def auto_translate_sku(
        db: Session,
        sku_id: UUID,
        target_languages: List[str],
        source_language: str = "zh-CN",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """自动翻译SKU到指定语言"""
        # 获取源语言翻译记录
        source_translation = db.query(ProductSkuTranslation).filter(
            and_(
                ProductSkuTranslation.sku_id == sku_id,
                ProductSkuTranslation.language_code == source_language
            )
        ).first()
        
        if not source_translation:
            # 如果没有源语言翻译，尝试从SKU表获取
            sku = db.query(ProductSku).filter(ProductSku.id == sku_id).first()
            if not sku or not sku.sku_name:
                return {
                    "success": False,
                    "error": f"SKU {sku_id} 没有可用的源语言内容进行翻译"
                }
            
            # 创建源语言翻译记录
            source_translation = ProductSkuTranslation(
                sku_id=sku_id,
                language_code=source_language,
                sku_name=sku.sku_name
            )
            db.add(source_translation)
            db.commit()
            db.refresh(source_translation)
        
        results = []
        
        # 对每种目标语言进行翻译
        for target_lang in target_languages:
            if target_lang == source_language:
                continue
            
            try:
                # 调用翻译方法
                translation_result = await source_translation.translate_to(
                    target_language=target_lang,
                    context=context
                )
                
                # 检查是否已存在该语言的翻译
                existing = db.query(ProductSkuTranslation).filter(
                    and_(
                        ProductSkuTranslation.sku_id == sku_id,
                        ProductSkuTranslation.language_code == target_lang
                    )
                ).first()
                
                if existing:
                    # 更新现有翻译
                    existing.sku_name = translation_result["sku_name"]
                    db.commit()
                    db.refresh(existing)
                    translation_obj = existing
                else:
                    # 创建新翻译
                    translation_obj = ProductSkuTranslation(
                        sku_id=UUID(translation_result["sku_id"]),
                        language_code=translation_result["language_code"],
                        sku_name=translation_result["sku_name"]
                    )
                    db.add(translation_obj)
                    db.commit()
                    db.refresh(translation_obj)
                
                results.append({
                    "language": target_lang,
                    "success": True,
                    "translation": ProductSkuTranslationResponse.from_orm(translation_obj).dict()
                })
                
            except Exception as e:
                results.append({
                    "language": target_lang,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "sku_id": str(sku_id),
            "source_language": source_language,
            "results": results
        }

    @staticmethod
    def get_sku_name_by_language(
        db: Session,
        sku_id: UUID,
        language_code: str,
        fallback_to_default: bool = True
    ) -> Optional[str]:
        """获取指定语言的SKU名称"""
        # 首先尝试从翻译表获取
        translation = db.query(ProductSkuTranslation).filter(
            and_(
                ProductSkuTranslation.sku_id == sku_id,
                ProductSkuTranslation.language_code == language_code
            )
        ).first()
        
        if translation:
            return translation.sku_name
        
        # 如果允许回退，则使用原始SKU名称
        if fallback_to_default:
            sku = db.query(ProductSku).filter(ProductSku.id == sku_id).first()
            if sku:
                return sku.sku_name or sku.sku_code
        
        return None

    @staticmethod
    def batch_create_default_translations(
        db: Session,
        language_code: str = "zh-CN"
    ) -> Dict[str, Any]:
        """批量为现有SKU创建默认语言翻译记录"""
        # 获取所有没有该语言翻译的SKU
        skus_without_translation = db.query(ProductSku).filter(
            ~ProductSku.id.in_(
                db.query(ProductSkuTranslation.sku_id).filter(
                    ProductSkuTranslation.language_code == language_code
                )
            ),
            ProductSku.sku_name.isnot(None)
        ).all()
        
        created_count = 0
        
        for sku in skus_without_translation:
            translation = ProductSkuTranslation(
                sku_id=sku.id,
                language_code=language_code,
                sku_name=sku.sku_name
            )
            db.add(translation)
            created_count += 1
        
        db.commit()
        
        return {
            "success": True,
            "language_code": language_code,
            "created_count": created_count,
            "message": f"为 {created_count} 个SKU创建了 {language_code} 翻译记录"
        } 