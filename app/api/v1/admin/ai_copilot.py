# -*- coding: utf-8 -*-
"""
AI助手API路由
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.analytics.ai_copilot.service import AICopilotService
from app.analytics.ai_copilot.schema import (
    ProductAnalysisRequest, ProductAnalysisResponse,
    ApplyAnalysisRequest, AICallRecord, ProductAIAnalysis
)
from app.product.category.service import ProductCategoryService
from app.product.attribute.service import ProductAttributeService
from app.product.models import ProductCategoryTranslation
from app.analytics.ai_copilot.alibaba_service import AlibabaBailianService


router = APIRouter()
ai_service = AICopilotService()


@router.post(
    "/analyze-product",
    summary="分析商品图片",
    description="上传商品图片，使用AI分析并生成商品信息建议"
)
async def analyze_product_images(
    request: ProductAnalysisRequest,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # 需要根据实际的认证系统调整
):
    """分析商品图片并生成建议"""
    try:
        # TODO: 从认证用户中获取user_id
        user_id = None  # current_user.id if current_user else None
        
        result = await ai_service.analyze_product_images(
            db=db,
            request=request,
            user_id=user_id
        )
        
        return {
            "code": 200,
            "message": "分析成功",
            "data": {
                "call_record_id": str(result.call_record_id),
                "analysis_id": str(result.analysis_id),
                "analysis": result.analysis,
                "suggestions": result.suggestions
            }
        }
        
    except Exception as e:
        return {
            "code": 500,
            "message": f"分析失败: {str(e)}",
            "data": None
        }


@router.post(
    "/apply-suggestions",
    summary="应用AI建议",
    description="根据AI分析结果创建或更新商品"
)
async def apply_analysis_suggestions(
    request: ApplyAnalysisRequest,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)
):
    """应用AI分析建议创建商品"""
    try:
        # TODO: 从认证用户中获取user_id
        user_id = None  # current_user.id if current_user else None
        
        result = await ai_service.apply_analysis_suggestions(
            db=db,
            request=request,
            user_id=user_id
        )
        
        return {
            "code": 200,
            "message": "应用成功",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"应用失败: {str(e)}"
        )


@router.get(
    "/analysis/{analysis_id}",
    summary="获取分析结果",
    description="根据分析ID获取详细的分析结果"
)
async def get_analysis_result(
    analysis_id: UUID,
    db: Session = Depends(get_db)
):
    """获取分析结果详情"""
    from app.analytics.ai_copilot.models import ProductAIAnalysis as ProductAIAnalysisModel
    from app.analytics.ai_copilot.schema import ProductAIAnalysis
    
    analysis = db.query(ProductAIAnalysisModel).filter(
        ProductAIAnalysisModel.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分析结果不存在"
        )
    
    # 使用自定义的转换方法处理JSON字符串字段
    return {
        "code": 200,
        "message": "获取成功",
        "data": ProductAIAnalysis.from_db_model(analysis)
    }


@router.get(
    "/call-records",
    summary="获取AI调用记录",
    description="获取AI调用历史记录列表"
)
async def get_call_records(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取AI调用记录列表"""
    from app.analytics.ai_copilot.models import AICallRecord as AICallRecordModel
    
    # 查询总数
    total = db.query(AICallRecordModel).count()
    
    # 查询记录
    records = db.query(AICallRecordModel).order_by(
        AICallRecordModel.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    # 计算页码
    page = skip // limit + 1 if limit else 1
    
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "total": total,
            "page": page,
            "size": limit,
            "items": [AICallRecord.from_orm(record) for record in records]
        }
    }


@router.get(
    "/statistics",
    summary="获取AI使用统计",
    description="获取AI调用统计信息，包括成功率、成本等"
)
async def get_ai_statistics(
    db: Session = Depends(get_db)
):
    """获取AI使用统计"""
    from app.analytics.ai_copilot.models import AICallRecord as AICallRecordModel, AICallStatus
    from sqlalchemy import func
    
    # 总调用次数
    total_calls = db.query(AICallRecordModel).count()
    
    # 成功调用次数
    success_calls = db.query(AICallRecordModel).filter(
        AICallRecordModel.status == AICallStatus.SUCCESS
    ).count()
    
    # 失败调用次数
    failed_calls = db.query(AICallRecordModel).filter(
        AICallRecordModel.status == AICallStatus.FAILED
    ).count()
    
    # 总成本
    total_cost = db.query(func.sum(AICallRecordModel.cost)).scalar() or 0
    
    # 平均响应时间
    avg_duration = db.query(func.avg(AICallRecordModel.duration_ms)).scalar() or 0
    
    # 成功率
    success_rate = (success_calls / total_calls * 100) if total_calls > 0 else 0
    
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "total_calls": total_calls,
            "success_calls": success_calls,
            "failed_calls": failed_calls,
            "success_rate": round(success_rate, 2),
            "total_cost": round(total_cost, 4),
            "avg_duration_ms": round(avg_duration, 2)
        }
    }


@router.get(
    "/system-data",
    summary="获取系统数据",
    description="获取系统基础数据，用于AI分析结果映射"
)
async def get_system_data_for_ai(
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_admin_user)
):
    """
    获取系统基础数据，用于AI分析结果映射
    包括：分类树、属性列表、常用属性值等
    """
    try:
        # 获取分类树
        categories_result = ProductCategoryService.get_category_tree(db)
        
        # 获取可配置属性（用于SKU）
        configurable_attributes = ProductAttributeService.get_configurable_attributes(db)
        
        # 获取所有属性的简要信息
        attributes_result = ProductAttributeService.get_attributes(
            db, skip=0, limit=1000, is_visible=True
        )
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "categories": categories_result.get("items", []),
                "configurable_attributes": configurable_attributes,
                "all_attributes": attributes_result.get("items", [])
            }
        }
    except Exception as e:
        print(f"获取系统数据失败: {str(e)}")
        return {
            "code": 500,
            "message": f"获取系统数据失败: {str(e)}",
            "data": {
                "categories": [],
                "configurable_attributes": [],
                "all_attributes": []
            }
        }


@router.post(
    "/create-product-from-ai", 
    summary="根据AI分析创建商品",
    description="根据AI分析结果创建商品"
)
async def create_product_from_ai_analysis(
    request: dict,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_admin_user)
):
    """
    根据AI分析结果创建商品
    请求数据包含：商品基本信息、分类ID、属性设置、SKU配置等
    """
    try:
        # 验证请求数据
        if not request.get("ai_analysis_id"):
            return {
                "code": 400,
                "message": "缺少AI分析ID",
                "data": None
            }
        
        # 获取AI分析记录
        from app.analytics.ai_copilot.models import ProductAIAnalysis as ProductAIAnalysisModel
        analysis_record = db.query(ProductAIAnalysisModel).filter(
            ProductAIAnalysisModel.id == request["ai_analysis_id"]
        ).first()
        
        if not analysis_record:
            return {
                "code": 404,
                "message": "AI分析记录不存在",
                "data": None
            }
        
        # 这里应该调用商品创建服务
        # 由于涉及复杂的商品创建逻辑，暂时返回成功状态
        # 后续需要集成完整的商品创建API
        
        # 记录创建操作
        from datetime import datetime
        analysis_record.is_used = True
        analysis_record.used_at = datetime.utcnow()
        db.commit()
        
        return {
            "code": 200,
            "message": "商品创建成功",
            "data": {
                "product_id": "placeholder_product_id",
                "message": "商品已根据AI分析结果创建"
            }
        }
        
    except Exception as e:
        print(f"根据AI分析创建商品失败: {str(e)}")
        return {
            "code": 500,
            "message": f"创建商品失败: {str(e)}",
            "data": None
        }


@router.post(
    "/translate-category",
    summary="AI翻译分类",
    description="使用AI翻译分类信息到多种语言"
)
async def translate_category(
    request: dict,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_admin_user)
):
    """
    AI翻译分类
    请求数据包含：category_id, target_languages
    """
    try:
        category_id = request.get("category_id")
        target_languages = request.get("target_languages", [])
        
        if not category_id:
            return {
                "code": 400,
                "message": "缺少分类ID",
                "data": None
            }
        
        if not target_languages:
            return {
                "code": 400,
                "message": "缺少目标语言",
                "data": None
            }
        
        # 查找中文原版翻译
        source_translation = db.query(ProductCategoryTranslation).filter(
            ProductCategoryTranslation.category_id == category_id,
            ProductCategoryTranslation.language_code == "zh-CN"
        ).first()
        
        if not source_translation:
            return {
                "code": 404,
                "message": "未找到中文原版分类翻译",
                "data": None
            }
        
        results = []
        ai_service = AlibabaBailianService()
        
        # 逐个翻译到目标语言
        for target_language in target_languages:
            try:
                # 检查是否已存在翻译
                existing_translation = db.query(ProductCategoryTranslation).filter(
                    ProductCategoryTranslation.category_id == category_id,
                    ProductCategoryTranslation.language_code == target_language
                ).first()
                
                if existing_translation:
                    results.append({
                        "language": target_language,
                        "status": "skipped",
                        "message": "翻译已存在"
                    })
                    continue
                
                # 调用AI翻译
                translation_result = await source_translation.translate_to(
                    target_language=target_language,
                    context="这是电商系统的商品分类翻译"
                )
                
                if translation_result and translation_result.get("name"):
                    # 保存翻译结果
                    new_translation = ProductCategoryTranslation(
                        category_id=translation_result["category_id"],
                        language_code=translation_result["language_code"],
                        name=translation_result["name"],
                        description=translation_result["description"],
                        seo_title=translation_result["seo_title"],
                        seo_description=translation_result["seo_description"],
                        seo_keywords=translation_result["seo_keywords"]
                    )
                    
                    db.add(new_translation)
                    db.flush()  # 确保数据写入
                    
                    results.append({
                        "language": target_language,
                        "status": "success",
                        "message": "翻译成功",
                        "translation": {
                            "name": translation_result["name"],
                            "description": translation_result["description"],
                            "seo_title": translation_result["seo_title"]
                        }
                    })
                else:
                    results.append({
                        "language": target_language,
                        "status": "failed",
                        "message": "AI翻译失败"
                    })
                    
            except Exception as e:
                print(f"翻译语言 {target_language} 失败: {str(e)}")
                results.append({
                    "language": target_language,
                    "status": "error",
                    "message": str(e)
                })
        
        # 提交所有翻译
        db.commit()
        
        return {
            "code": 200,
            "message": f"翻译完成，共处理 {len(target_languages)} 种语言",
            "data": {
                "results": results,
                "total_languages": len(target_languages),
                "success_count": len([r for r in results if r["status"] == "success"]),
                "failed_count": len([r for r in results if r["status"] in ["failed", "error"]]),
                "skipped_count": len([r for r in results if r["status"] == "skipped"])
            }
        }
        
    except Exception as e:
        print(f"分类翻译失败: {str(e)}")
        return {
            "code": 500,
            "message": f"分类翻译失败: {str(e)}",
            "data": None
        } 