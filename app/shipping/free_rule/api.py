# -*- coding: utf-8 -*-
"""
免运费规则API路由
包含管理端和公开端接口
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from .service import FreeShippingRuleService
from .schema import (
    FreeShippingRuleCreate, FreeShippingRuleUpdate, FreeShippingRuleResponse,
    FreeShippingRuleTranslationCreate, FreeShippingRuleTranslationUpdate,
    FreeShippingRuleQueryParams, ApplyFreeShippingRequest, FreeShippingCheckResult,
    FreeShippingRuleTypeEnum
)

router = APIRouter(prefix="/free-rules")

# ==================== 管理端接口 ====================

@router.post("/admin/free-rules", response_model=FreeShippingRuleResponse)
async def create_free_shipping_rule(
    rule_data: FreeShippingRuleCreate,
    db: Session = Depends(get_db)
):
    """创建免运费规则"""
    try:
        service = FreeShippingRuleService(db)
        rule = service.create_rule(rule_data)
        return rule
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建免运费规则失败: {str(e)}")


@router.get("/admin/free-rules")
async def list_free_shipping_rules(
    rule_type: FreeShippingRuleTypeEnum = Query(None, description="规则类型筛选"),
    is_active: bool = Query(None, description="是否启用筛选"),
    language_code: str = Query("zh-CN", description="语言代码"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    db: Session = Depends(get_db)
):
    """获取免运费规则列表"""
    try:
        service = FreeShippingRuleService(db)
        rules, total = service.list_rules(
            rule_type=rule_type,
            is_active=is_active,
            language_code=language_code,
            page=page,
            page_size=page_size
        )
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "items": rules,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取免运费规则列表失败: {str(e)}")


@router.get("/admin/free-rules/{rule_id}", response_model=FreeShippingRuleResponse)
async def get_free_shipping_rule(
    rule_id: UUID,
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """根据ID获取免运费规则详情"""
    try:
        service = FreeShippingRuleService(db)
        rule = service.get_rule_by_id(rule_id, language_code)
        if not rule:
            raise HTTPException(status_code=404, detail="免运费规则不存在")
        return rule
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取免运费规则失败: {str(e)}")


@router.get("/admin/free-rules/code/{code}", response_model=FreeShippingRuleResponse)
async def get_free_shipping_rule_by_code(
    code: str,
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """根据代码获取免运费规则详情"""
    try:
        service = FreeShippingRuleService(db)
        rule = service.get_rule_by_code(code, language_code)
        if not rule:
            raise HTTPException(status_code=404, detail="免运费规则不存在")
        return rule
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取免运费规则失败: {str(e)}")


@router.put("/admin/free-rules/{rule_id}", response_model=FreeShippingRuleResponse)
async def update_free_shipping_rule(
    rule_id: UUID,
    rule_data: FreeShippingRuleUpdate,
    db: Session = Depends(get_db)
):
    """更新免运费规则"""
    try:
        service = FreeShippingRuleService(db)
        rule = service.update_rule(rule_id, rule_data)
        if not rule:
            raise HTTPException(status_code=404, detail="免运费规则不存在")
        return rule
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新免运费规则失败: {str(e)}")


@router.delete("/admin/free-rules/{rule_id}")
async def delete_free_shipping_rule(
    rule_id: UUID,
    db: Session = Depends(get_db)
):
    """删除免运费规则"""
    try:
        service = FreeShippingRuleService(db)
        success = service.delete_rule(rule_id)
        if not success:
            raise HTTPException(status_code=404, detail="免运费规则不存在")
        return {"code": 200, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除免运费规则失败: {str(e)}")


# ==================== 翻译管理接口 ====================

@router.post("/admin/free-rules/{rule_id}/translations")
async def create_free_shipping_rule_translation(
    rule_id: UUID,
    translation_data: FreeShippingRuleTranslationCreate,
    db: Session = Depends(get_db)
):
    """创建免运费规则翻译"""
    try:
        service = FreeShippingRuleService(db)
        translation = service.create_translation(rule_id, translation_data)
        if not translation:
            raise HTTPException(status_code=404, detail="免运费规则不存在")
        return {
            "code": 200,
            "message": "创建翻译成功",
            "data": translation
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建翻译失败: {str(e)}")


@router.put("/admin/free-rules/{rule_id}/translations/{language_code}")
async def update_free_shipping_rule_translation(
    rule_id: UUID,
    language_code: str,
    translation_data: FreeShippingRuleTranslationUpdate,
    db: Session = Depends(get_db)
):
    """更新免运费规则翻译"""
    try:
        service = FreeShippingRuleService(db)
        translation = service.update_translation(rule_id, language_code, translation_data)
        if not translation:
            raise HTTPException(status_code=404, detail="翻译不存在")
        return {
            "code": 200,
            "message": "更新翻译成功",
            "data": translation
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新翻译失败: {str(e)}")


@router.delete("/admin/free-rules/{rule_id}/translations/{language_code}")
async def delete_free_shipping_rule_translation(
    rule_id: UUID,
    language_code: str,
    db: Session = Depends(get_db)
):
    """删除免运费规则翻译"""
    try:
        service = FreeShippingRuleService(db)
        success = service.delete_translation(rule_id, language_code)
        if not success:
            raise HTTPException(status_code=404, detail="翻译不存在")
        return {"code": 200, "message": "删除翻译成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除翻译失败: {str(e)}")


# ==================== 公开端接口 ====================

@router.post("/public/free-shipping/check", response_model=FreeShippingCheckResult)
async def check_free_shipping(
    request: ApplyFreeShippingRequest,
    db: Session = Depends(get_db)
):
    """检查是否符合免运费条件"""
    try:
        service = FreeShippingRuleService(db)
        result = service.check_free_shipping(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"免运费检查失败: {str(e)}")


@router.get("/public/free-shipping/rules")
async def get_active_free_shipping_rules(
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取当前有效的免运费规则（公开展示）"""
    try:
        service = FreeShippingRuleService(db)
        rules, total = service.list_rules(
            is_active=True,
            language_code=language_code,
            page=1,
            page_size=100
        )
        
        # 只返回必要的公开信息
        public_rules = []
        for rule in rules:
            public_rule = {
                "id": rule.id,
                "name": rule.name,
                "description": rule.description,
                "rule_type": rule.rule_type,
                "min_amount": rule.min_amount,
                "min_quantity": rule.min_quantity,
                "start_date": rule.start_date,
                "end_date": rule.end_date
            }
            public_rules.append(public_rule)
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": public_rules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取免运费规则失败: {str(e)}")


# ==================== 批量操作接口 ====================

@router.patch("/admin/free-rules/batch/status")
async def batch_update_free_shipping_rule_status(
    rule_ids: List[UUID],
    is_active: bool,
    db: Session = Depends(get_db)
):
    """批量更新免运费规则状态"""
    try:
        service = FreeShippingRuleService(db)
        updated_count = 0
        
        for rule_id in rule_ids:
            rule_data = FreeShippingRuleUpdate(is_active=is_active)
            result = service.update_rule(rule_id, rule_data)
            if result:
                updated_count += 1
        
        return {
            "code": 200,
            "message": f"批量更新成功，共更新 {updated_count} 条记录",
            "data": {
                "updated_count": updated_count,
                "total_count": len(rule_ids)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量更新失败: {str(e)}")


@router.delete("/admin/free-rules/batch")
async def batch_delete_free_shipping_rules(
    rule_ids: List[UUID],
    db: Session = Depends(get_db)
):
    """批量删除免运费规则"""
    try:
        service = FreeShippingRuleService(db)
        deleted_count = 0
        
        for rule_id in rule_ids:
            success = service.delete_rule(rule_id)
            if success:
                deleted_count += 1
        
        return {
            "code": 200,
            "message": f"批量删除成功，共删除 {deleted_count} 条记录",
            "data": {
                "deleted_count": deleted_count,
                "total_count": len(rule_ids)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除失败: {str(e)}") 