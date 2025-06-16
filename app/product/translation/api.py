# -*- coding: utf-8 -*-
"""
商品翻译管理API接口
提供商品多语言翻译的REST API
"""
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import get_db
from app.product.translation.service import ProductTranslationService
from app.product.translation.chatgpt_service import deepseek_translation_service
from app.product.translation.schema import (
    ProductTranslationCreate,
    ProductTranslationUpdate,
    ProductTranslationResponse,
    ProductTranslationListResponse,
    ProductTranslationBatchCreate,
    ProductTranslationSummary,
    TranslationContentUpdate,
    TranslationSEOUpdate
)

router = APIRouter()


@router.get("/products/{product_id}/translations", response_model=ProductTranslationListResponse)
def get_product_translations(
    product_id: UUID,
    skip: int = Query(default=0, ge=0, description="跳过记录数"),
    limit: int = Query(default=100, ge=1, le=100, description="返回记录数"),
    language_code: Optional[str] = Query(None, description="语言代码筛选"),
    has_seo: Optional[bool] = Query(None, description="是否有SEO信息筛选"),
    sort_by: str = Query(default="created_at", description="排序字段"),
    sort_desc: bool = Query(default=True, description="是否降序排序"),
    db: Session = Depends(get_db)
):
    """
    获取商品翻译列表
    
    支持分页、筛选和排序功能
    """
    return ProductTranslationService.get_product_translations(
        db=db,
        product_id=product_id,
        skip=skip,
        limit=limit,
        language_code=language_code,
        has_seo=has_seo,
        sort_by=sort_by,
        sort_desc=sort_desc
    )


@router.get("/products/{product_id}/translations/summary", response_model=ProductTranslationSummary)
def get_product_translation_summary(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    获取商品翻译汇总信息
    
    包含所有语言的翻译信息和完成度统计
    """
    return ProductTranslationService.get_product_translation_summary(db, product_id)


@router.get("/products/{product_id}/translations/{language_code}", response_model=ProductTranslationResponse)
def get_translation_by_language(
    product_id: UUID,
    language_code: str,
    db: Session = Depends(get_db)
):
    """
    根据语言代码获取翻译详情
    """
    return ProductTranslationService.get_translation_by_language(db, product_id, language_code)


@router.get("/translations/{translation_id}", response_model=ProductTranslationResponse)
def get_translation_by_id(
    translation_id: UUID,
    db: Session = Depends(get_db)
):
    """
    根据ID获取翻译详情
    """
    return ProductTranslationService.get_translation_by_id(db, translation_id)


@router.post("/products/{product_id}/translations", response_model=ProductTranslationResponse, status_code=status.HTTP_201_CREATED)
def create_product_translation(
    product_id: UUID,
    translation_data: ProductTranslationCreate,
    db: Session = Depends(get_db)
):
    """
    创建商品翻译
    
    为指定商品添加新的语言翻译
    """
    return ProductTranslationService.create_product_translation(db, product_id, translation_data)


@router.post("/products/{product_id}/translations/batch", response_model=List[ProductTranslationResponse], status_code=status.HTTP_201_CREATED)
def batch_create_product_translations(
    product_id: UUID,
    batch_data: ProductTranslationBatchCreate,
    db: Session = Depends(get_db)
):
    """
    批量创建商品翻译
    
    一次性为商品添加多个语言的翻译
    """
    return ProductTranslationService.batch_create_translations(db, product_id, batch_data.translations)


@router.put("/translations/{translation_id}", response_model=ProductTranslationResponse)
def update_product_translation(
    translation_id: UUID,
    translation_data: ProductTranslationUpdate,
    db: Session = Depends(get_db)
):
    """
    更新商品翻译
    
    修改指定翻译记录的信息
    """
    return ProductTranslationService.update_product_translation(db, translation_id, translation_data)


@router.patch("/products/{product_id}/translations/{language_code}/content")
def update_translation_content(
    product_id: UUID,
    language_code: str,
    content_data: TranslationContentUpdate,
    db: Session = Depends(get_db)
):
    """
    更新翻译内容
    
    只更新商品的基础内容字段
    """
    return ProductTranslationService.update_translation_content(db, product_id, language_code, content_data)


@router.patch("/products/{product_id}/translations/{language_code}/seo")
def update_translation_seo(
    product_id: UUID,
    language_code: str,
    seo_data: TranslationSEOUpdate,
    db: Session = Depends(get_db)
):
    """
    更新翻译SEO信息
    
    只更新SEO相关字段
    """
    return ProductTranslationService.update_translation_seo(db, product_id, language_code, seo_data)


@router.post("/products/{product_id}/translations/copy", response_model=ProductTranslationResponse, status_code=status.HTTP_201_CREATED)
def copy_translation(
    product_id: UUID,
    source_language: str = Query(..., description="源语言代码"),
    target_language: str = Query(..., description="目标语言代码"),
    db: Session = Depends(get_db)
):
    """
    复制翻译到新语言
    
    将现有语言的翻译复制为新语言的翻译
    """
    return ProductTranslationService.copy_translation(db, product_id, source_language, target_language)


@router.delete("/translations/{translation_id}")
def delete_product_translation(
    translation_id: UUID,
    db: Session = Depends(get_db)
):
    """
    删除商品翻译
    
    删除指定的翻译记录
    """
    return ProductTranslationService.delete_product_translation(db, translation_id)


# 统计接口
@router.get("/products/{product_id}/translations/statistics")
def get_translation_statistics(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    获取商品翻译统计信息
    
    包含翻译数量、语言数量、完成度等统计数据
    """
    try:
        from app.product.models import ProductTranslation
        
        # 基本统计
        total_translations = db.query(ProductTranslation).filter(ProductTranslation.product_id == product_id).count()
        
        # 语言统计
        language_stats = db.query(ProductTranslation.language_code).filter(
            ProductTranslation.product_id == product_id
        ).distinct().all()
        
        language_count = len(language_stats)
        language_list = [lang[0] for lang in language_stats]
        
        # SEO统计
        seo_count = db.query(ProductTranslation).filter(
            ProductTranslation.product_id == product_id,
            or_(
                ProductTranslation.seo_title.isnot(None),
                ProductTranslation.seo_description.isnot(None),
                ProductTranslation.seo_keywords.isnot(None)
            )
        ).count()
        
        # 完整性统计
        translations = db.query(ProductTranslation).filter(ProductTranslation.product_id == product_id).all()
        complete_count = 0
        for trans in translations:
            required_fields = [trans.name, trans.short_description, trans.description]
            completed_fields = sum(1 for field in required_fields if field and field.strip())
            if completed_fields >= 2:
                complete_count += 1
        
        completion_rate = (complete_count / total_translations * 100) if total_translations > 0 else 0
        
        return {
            "product_id": product_id,
            "total_translations": total_translations,
            "language_count": language_count,
            "languages": language_list,
            "seo_count": seo_count,
            "complete_count": complete_count,
            "completion_rate": round(completion_rate, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取翻译统计失败: {str(e)}")


# 翻译验证接口
@router.post("/products/{product_id}/translations/validate")
def validate_translation_data(
    product_id: UUID,
    translation_data: ProductTranslationCreate,
    db: Session = Depends(get_db)
):
    """
    验证翻译数据
    
    在实际创建前验证翻译数据的有效性
    """
    try:
        from app.product.models import Product, ProductTranslation
        from sqlalchemy import and_
        
        # 验证商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"valid": False, "message": "商品不存在"}
        
        # 检查语言是否已存在
        existing_translation = db.query(ProductTranslation).filter(
            and_(
                ProductTranslation.product_id == product_id,
                ProductTranslation.language_code == translation_data.language_code
            )
        ).first()
        
        if existing_translation:
            return {"valid": False, "message": f"语言 {translation_data.language_code} 已存在翻译"}
        
        # 验证必填字段
        if not translation_data.name or len(translation_data.name.strip()) == 0:
            return {"valid": False, "message": "商品名称不能为空"}
        
        # 验证语言代码格式
        if len(translation_data.language_code) < 2:
            return {"valid": False, "message": "语言代码格式不正确"}
        
        return {"valid": True, "message": "翻译数据验证通过"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"翻译验证失败: {str(e)}")


# 获取支持的语言列表
@router.get("/translations/supported-languages")
def get_supported_languages():
    """
    获取支持的语言列表
    """
    supported_languages = [
        {"code": "zh-cn", "name": "简体中文", "native_name": "简体中文"},
        {"code": "zh-tw", "name": "繁体中文", "native_name": "繁體中文"},
        {"code": "en-us", "name": "English (US)", "native_name": "English"},
        {"code": "en-gb", "name": "English (UK)", "native_name": "English"},
        {"code": "ja-jp", "name": "Japanese", "native_name": "日本語"},
        {"code": "ko-kr", "name": "Korean", "native_name": "한국어"},
        {"code": "ms-my", "name": "Malay", "native_name": "Bahasa Malaysia"},
        {"code": "th-th", "name": "Thai", "native_name": "ภาษาไทย"},
        {"code": "vi-vn", "name": "Vietnamese", "native_name": "Tiếng Việt"},
        {"code": "id-id", "name": "Indonesian", "native_name": "Bahasa Indonesia"},
        {"code": "tl-ph", "name": "Filipino", "native_name": "Filipino"},
        {"code": "es-es", "name": "Spanish", "native_name": "Español"},
        {"code": "fr-fr", "name": "French", "native_name": "Français"},
        {"code": "de-de", "name": "German", "native_name": "Deutsch"},
        {"code": "it-it", "name": "Italian", "native_name": "Italiano"},
        {"code": "pt-pt", "name": "Portuguese", "native_name": "Português"},
        {"code": "ru-ru", "name": "Russian", "native_name": "Русский"},
        {"code": "ar-sa", "name": "Arabic", "native_name": "العربية"},
        {"code": "hi-in", "name": "Hindi", "native_name": "हिन्दी"},
        {"code": "ta-in", "name": "Tamil", "native_name": "தமிழ்"}
    ]
    
    return {
        "languages": supported_languages,
        "total": len(supported_languages)
    }


# DeepSeek翻译接口
@router.post("/products/{product_id}/translations/deepseek-translate", response_model=ProductTranslationResponse, status_code=status.HTTP_201_CREATED)
async def deepseek_translate_product(
    product_id: UUID,
    target_language: str = Body(..., description="目标语言代码"),
    source_language: str = Body(default="zh-cn", description="源语言代码，默认为中文"),
    auto_save: bool = Body(default=True, description="是否自动保存翻译结果"),
    db: Session = Depends(get_db)
):
    """
    使用DeepSeek自动翻译商品信息
    
    根据源语言的商品信息，使用DeepSeek API自动翻译到目标语言
    """
    try:
        # 获取源语言的翻译信息作为翻译基础
        source_translation = ProductTranslationService.get_translation_by_language(
            db, product_id, source_language
        )
        
        # 准备翻译源数据
        source_data = {
            "name": source_translation.name,
            "short_description": source_translation.short_description or "",
            "description": source_translation.description or "",
            "specifications": source_translation.specifications or "",
            "benefits": source_translation.benefits or "",
            "instructions": source_translation.instructions or "",
            "seo_title": source_translation.seo_title or "",
            "seo_description": source_translation.seo_description or "",
            "seo_keywords": source_translation.seo_keywords or ""
        }
        
        # 调用DeepSeek翻译服务
        translated_data = await deepseek_translation_service.translate_product_info(
            source_data, target_language
        )
        
        # 添加语言代码
        translated_data["language_code"] = target_language
        
        if auto_save:
            # 检查目标语言是否已存在翻译
            try:
                existing_translation = ProductTranslationService.get_translation_by_language(
                    db, product_id, target_language
                )
                # 如果存在，更新现有翻译
                return ProductTranslationService.update_product_translation(
                    db, existing_translation.id, ProductTranslationUpdate(**translated_data)
                )
            except HTTPException:
                # 如果不存在，创建新翻译
                return ProductTranslationService.create_product_translation(
                    db, product_id, ProductTranslationCreate(**translated_data)
                )
        else:
            # 不自动保存，仅返回翻译结果
            return {
                "id": None,
                "product_id": product_id,
                "created_at": None,
                "updated_at": None,
                **translated_data
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DeepSeek翻译失败: {str(e)}")


@router.post("/products/{product_id}/translations/deepseek-batch-translate", status_code=status.HTTP_201_CREATED)
async def deepseek_batch_translate_product(
    product_id: UUID,
    target_languages: List[str] = Body(..., description="目标语言代码列表"),
    source_language: str = Body(default="zh-cn", description="源语言代码，默认为中文"),
    auto_save: bool = Body(default=True, description="是否自动保存翻译结果"),
    db: Session = Depends(get_db)
):
    """
    使用DeepSeek批量翻译商品信息到多种语言
    """
    try:
        # 获取源语言的翻译信息
        source_translation = ProductTranslationService.get_translation_by_language(
            db, product_id, source_language
        )
        
        # 准备翻译源数据
        source_data = {
            "name": source_translation.name,
            "short_description": source_translation.short_description or "",
            "description": source_translation.description or "",
            "specifications": source_translation.specifications or "",
            "benefits": source_translation.benefits or "",
            "instructions": source_translation.instructions or "",
            "seo_title": source_translation.seo_title or "",
            "seo_description": source_translation.seo_description or "",
            "seo_keywords": source_translation.seo_keywords or ""
        }
        
        # 批量翻译
        translation_results = await deepseek_translation_service.batch_translate_product_info(
            source_data, target_languages
        )
        
        saved_translations = []
        failed_translations = []
        
        if auto_save:
            # 保存翻译结果
            for language_code, translated_data in translation_results.items():
                try:
                    translated_data["language_code"] = language_code
                    
                    # 检查是否已存在该语言的翻译
                    try:
                        existing_translation = ProductTranslationService.get_translation_by_language(
                            db, product_id, language_code
                        )
                        # 更新现有翻译
                        updated_translation = ProductTranslationService.update_product_translation(
                            db, existing_translation.id, ProductTranslationUpdate(**translated_data)
                        )
                        saved_translations.append(updated_translation)
                    except HTTPException:
                        # 创建新翻译
                        new_translation = ProductTranslationService.create_product_translation(
                            db, product_id, ProductTranslationCreate(**translated_data)
                        )
                        saved_translations.append(new_translation)
                        
                except Exception as e:
                    failed_translations.append({
                        "language_code": language_code,
                        "error": str(e)
                    })
        
        return {
            "success_count": len(saved_translations) if auto_save else len(translation_results),
            "total_count": len(target_languages),
            "saved_translations": saved_translations if auto_save else [],
            "translation_results": translation_results if not auto_save else {},
            "failed_translations": failed_translations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量DeepSeek翻译失败: {str(e)}")


# 保留原有的ChatGPT接口以保持兼容性，但内部使用DeepSeek服务
@router.post("/products/{product_id}/translations/chatgpt-translate", response_model=ProductTranslationResponse, status_code=status.HTTP_201_CREATED)
async def chatgpt_translate_product(
    product_id: UUID,
    target_language: str = Body(..., description="目标语言代码"),
    source_language: str = Body(default="zh-cn", description="源语言代码，默认为中文"),
    auto_save: bool = Body(default=True, description="是否自动保存翻译结果"),
    db: Session = Depends(get_db)
):
    """
    使用AI自动翻译商品信息（现由DeepSeek提供服务）
    
    根据源语言的商品信息，使用AI API自动翻译到目标语言
    """
    # 直接调用DeepSeek翻译接口
    return await deepseek_translate_product(product_id, target_language, source_language, auto_save, db)


@router.post("/products/{product_id}/translations/chatgpt-batch-translate", status_code=status.HTTP_201_CREATED)
async def chatgpt_batch_translate_product(
    product_id: UUID,
    target_languages: List[str] = Body(..., description="目标语言代码列表"),
    source_language: str = Body(default="zh-cn", description="源语言代码，默认为中文"),
    auto_save: bool = Body(default=True, description="是否自动保存翻译结果"),
    db: Session = Depends(get_db)
):
    """
    使用AI批量翻译商品信息到多种语言（现由DeepSeek提供服务）
    """
    # 直接调用DeepSeek批量翻译接口
    return await deepseek_batch_translate_product(product_id, target_languages, source_language, auto_save, db) 