from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.content.promotion.service import PromotionContentService, PromotionTextTemplateService
from app.content.promotion.schema import (
    PromotionContentCreate, PromotionContentUpdate, PromotionContentResponse,
    PromotionContentListQuery, PromotionContentListResponse, PromotionContentBatchUpdate,
    PublicPromotionContentResponse, PromotionContentTranslationCreate,
    PromotionContentTranslationUpdate, PromotionContentTranslationResponse,
    PromotionTextTemplateCreate, PromotionTextTemplateUpdate, PromotionTextTemplateResponse
)
from app.content.promotion.models import PromotionContentType
from app.content.models import ContentStatus

# 管理端路由
router = APIRouter()

# 公开API路由（供前端使用）
public_router = APIRouter()


@router.post("/", response_model=PromotionContentResponse, summary="创建促销内容")
def create_promotion_content(
    content_data: PromotionContentCreate,
    db: Session = Depends(get_db)
):
    """创建新的促销内容"""
    try:
        content = PromotionContentService.create_content(db, content_data)
        return content
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建促销内容失败: {str(e)}")


@router.get("/", response_model=PromotionContentListResponse, summary="获取促销内容列表")
def get_promotion_contents(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    content_type: PromotionContentType = Query(None, description="内容类型筛选"),
    status: ContentStatus = Query(None, description="状态筛选"),
    position: str = Query(None, description="位置筛选"),
    promotion_id: str = Query(None, description="促销活动ID筛选"),
    search: str = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取促销内容列表，支持筛选和分页"""
    query = PromotionContentListQuery(
        page=page,
        page_size=page_size,
        content_type=content_type,
        status=status,
        position=position,
        promotion_id=promotion_id,
        search=search
    )
    
    contents, total = PromotionContentService.get_contents_list(db, query)
    total_pages = (total + page_size - 1) // page_size
    
    return PromotionContentListResponse(
        items=contents,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{content_id}", response_model=PromotionContentResponse, summary="获取促销内容详情")
def get_promotion_content(
    content_id: UUID = Path(..., description="促销内容ID"),
    db: Session = Depends(get_db)
):
    """根据ID获取促销内容详情"""
    content = PromotionContentService.get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="促销内容不存在")
    return content


@router.put("/{content_id}", response_model=PromotionContentResponse, summary="更新促销内容")
def update_promotion_content(
    content_id: UUID = Path(..., description="促销内容ID"),
    content_data: PromotionContentUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新促销内容信息"""
    content = PromotionContentService.update_content(db, content_id, content_data)
    if not content:
        raise HTTPException(status_code=404, detail="促销内容不存在")
    return content


@router.delete("/{content_id}", summary="删除促销内容")
def delete_promotion_content(
    content_id: UUID = Path(..., description="促销内容ID"),
    db: Session = Depends(get_db)
):
    """删除指定促销内容"""
    success = PromotionContentService.delete_content(db, content_id)
    if not success:
        raise HTTPException(status_code=404, detail="促销内容不存在")
    return {"message": "促销内容删除成功"}


@router.patch("/batch", response_model=List[PromotionContentResponse], summary="批量更新促销内容")
def batch_update_promotion_contents(
    batch_data: PromotionContentBatchUpdate,
    db: Session = Depends(get_db)
):
    """批量更新促销内容状态或排序"""
    try:
        contents = PromotionContentService.batch_update_status(db, batch_data)
        return contents
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"批量更新失败: {str(e)}")


@router.put("/reorder", response_model=List[PromotionContentResponse], summary="重新排序促销内容")
def reorder_promotion_contents(
    content_orders: Dict[str, int],
    db: Session = Depends(get_db)
):
    """重新排序促销内容"""
    try:
        contents = PromotionContentService.reorder_contents(db, content_orders)
        return contents
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"排序更新失败: {str(e)}")


@router.get("/type/{content_type}", response_model=List[PromotionContentResponse], summary="根据类型获取促销内容")
def get_promotion_contents_by_type(
    content_type: PromotionContentType = Path(..., description="内容类型"),
    language_code: str = Query(None, description="语言代码"),
    db: Session = Depends(get_db)
):
    """根据类型获取激活的促销内容"""
    contents = PromotionContentService.get_active_contents_by_type(db, content_type, language_code)
    return contents


@router.get("/position/{position}", response_model=List[PromotionContentResponse], summary="根据位置获取促销内容")
def get_promotion_contents_by_position(
    position: str = Path(..., description="位置标识"),
    language_code: str = Query(None, description="语言代码"),
    db: Session = Depends(get_db)
):
    """根据位置获取激活的促销内容"""
    contents = PromotionContentService.get_active_contents_by_position(db, position, language_code)
    return contents


# 促销内容翻译管理
@router.post("/{content_id}/translations", response_model=PromotionContentTranslationResponse, summary="创建促销内容翻译")
def create_promotion_content_translation(
    content_id: UUID = Path(..., description="促销内容ID"),
    translation_data: PromotionContentTranslationCreate = ...,
    db: Session = Depends(get_db)
):
    """为促销内容创建或更新翻译"""
    translation = PromotionContentService.create_translation(db, content_id, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail="促销内容不存在")
    return translation


@router.put("/translations/{translation_id}", response_model=PromotionContentTranslationResponse, summary="更新促销内容翻译")
def update_promotion_content_translation(
    translation_id: UUID = Path(..., description="翻译ID"),
    translation_data: PromotionContentTranslationUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新促销内容翻译"""
    translation = PromotionContentService.update_translation(db, translation_id, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail="翻译不存在")
    return translation


@router.delete("/translations/{translation_id}", summary="删除促销内容翻译")
def delete_promotion_content_translation(
    translation_id: UUID = Path(..., description="翻译ID"),
    db: Session = Depends(get_db)
):
    """删除促销内容翻译"""
    success = PromotionContentService.delete_translation(db, translation_id)
    if not success:
        raise HTTPException(status_code=404, detail="翻译不存在")
    return {"message": "翻译删除成功"}


# === 促销文本模板管理 ===

template_router = APIRouter()

@template_router.post("/", response_model=PromotionTextTemplateResponse, summary="创建促销文本模板")
def create_promotion_text_template(
    template_data: PromotionTextTemplateCreate,
    db: Session = Depends(get_db)
):
    """创建新的促销文本模板"""
    try:
        template = PromotionTextTemplateService.create_template(db, template_data)
        return template
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建模板失败: {str(e)}")


@template_router.get("/", response_model=List[PromotionTextTemplateResponse], summary="获取促销文本模板列表")
def get_promotion_text_templates(
    content_type: PromotionContentType = Query(..., description="内容类型"),
    db: Session = Depends(get_db)
):
    """根据内容类型获取促销文本模板列表"""
    templates = PromotionTextTemplateService.get_templates_by_type(db, content_type)
    return templates


@template_router.get("/{template_id}", response_model=PromotionTextTemplateResponse, summary="获取促销文本模板详情")
def get_promotion_text_template(
    template_id: UUID = Path(..., description="模板ID"),
    db: Session = Depends(get_db)
):
    """根据ID获取促销文本模板详情"""
    template = PromotionTextTemplateService.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    return template


@template_router.put("/{template_id}", response_model=PromotionTextTemplateResponse, summary="更新促销文本模板")
def update_promotion_text_template(
    template_id: UUID = Path(..., description="模板ID"),
    template_data: PromotionTextTemplateUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新促销文本模板"""
    template = PromotionTextTemplateService.update_template(db, template_id, template_data)
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    return template


@template_router.delete("/{template_id}", summary="删除促销文本模板")
def delete_promotion_text_template(
    template_id: UUID = Path(..., description="模板ID"),
    db: Session = Depends(get_db)
):
    """删除指定促销文本模板"""
    success = PromotionTextTemplateService.delete_template(db, template_id)
    if not success:
        raise HTTPException(status_code=404, detail="模板不存在")
    return {"message": "模板删除成功"}


# === 公开API（供C端使用） ===

@public_router.get("/banner-texts", response_model=List[PublicPromotionContentResponse], summary="获取横幅文本")
def get_banner_texts(
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取横幅文本（公开API）"""
    contents = PromotionContentService.get_banner_texts(db, language_code)
    return contents


@public_router.get("/notifications", response_model=List[PublicPromotionContentResponse], summary="获取通知文本")
def get_notifications(
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取通知文本（公开API）"""
    contents = PromotionContentService.get_notifications(db, language_code)
    return contents


@public_router.get("/type/{content_type}", response_model=List[PublicPromotionContentResponse], summary="根据类型获取促销内容")
def public_get_promotion_contents_by_type(
    content_type: PromotionContentType = Path(..., description="内容类型"),
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """根据类型获取激活的促销内容（公开API）"""
    contents = PromotionContentService.get_active_contents_by_type(db, content_type, language_code)
    return contents


@public_router.get("/position/{position}", response_model=List[PublicPromotionContentResponse], summary="根据位置获取促销内容")
def public_get_promotion_contents_by_position(
    position: str = Path(..., description="位置标识"),
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """根据位置获取激活的促销内容（公开API）"""
    contents = PromotionContentService.get_active_contents_by_position(db, position, language_code)
    return contents