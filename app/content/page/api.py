from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.content.page.service import PageService
from app.content.page.schema import (
    PageCreate, PageUpdate, PageResponse, PageListQuery, PageListResponse,
    PageBatchUpdate, PublicPageResponse, PageTranslationCreate,
    PageTranslationUpdate, PageTranslationResponse, StaticPageType,
    PageStatistics
)
from app.content.models import ContentStatus

# 管理端路由
router = APIRouter()

# 公开API路由（供前端使用）
public_router = APIRouter()


@router.post("/", response_model=PageResponse, summary="创建页面")
def create_page(
    page_data: PageCreate,
    db: Session = Depends(get_db)
):
    """创建新的页面"""
    try:
        # 检查slug是否已存在
        existing_page = PageService.get_page_by_slug(db, page_data.slug)
        if existing_page:
            raise HTTPException(status_code=400, detail="页面别名已存在")
        
        page = PageService.create_page(db, page_data)
        return page
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建页面失败: {str(e)}")


@router.get("/", response_model=PageListResponse, summary="获取页面列表")
def get_pages(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: ContentStatus = Query(None, description="状态筛选"),
    template: str = Query(None, description="模板筛选"),
    is_homepage: bool = Query(None, description="是否首页筛选"),
    search: str = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取页面列表，支持筛选和分页"""
    query = PageListQuery(
        page=page,
        page_size=page_size,
        status=status,
        template=template,
        is_homepage=is_homepage,
        search=search
    )
    
    pages, total = PageService.get_pages_list(db, query)
    total_pages = (total + page_size - 1) // page_size
    
    return PageListResponse(
        items=pages,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/statistics", response_model=PageStatistics, summary="获取页面统计")
def get_page_statistics(db: Session = Depends(get_db)):
    """获取页面统计数据"""
    return PageService.get_statistics(db)


@router.get("/static", response_model=List[PageResponse], summary="获取静态页面")
def get_static_pages(db: Session = Depends(get_db)):
    """获取所有静态页面"""
    pages = PageService.get_static_pages(db)
    return pages


@router.post("/init-static", response_model=List[PageResponse], summary="初始化默认静态页面")
def init_static_pages(db: Session = Depends(get_db)):
    """初始化默认静态页面"""
    pages = PageService.init_default_static_pages(db)
    return pages


@router.get("/{page_id}", response_model=PageResponse, summary="获取页面详情")
def get_page(
    page_id: UUID = Path(..., description="页面ID"),
    db: Session = Depends(get_db)
):
    """根据ID获取页面详情"""
    page = PageService.get_page_by_id(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="页面不存在")
    return page


@router.get("/slug/{slug}", response_model=PageResponse, summary="根据slug获取页面")
def get_page_by_slug(
    slug: str = Path(..., description="页面别名"),
    db: Session = Depends(get_db)
):
    """根据slug获取页面详情"""
    page = PageService.get_page_by_slug(db, slug)
    if not page:
        raise HTTPException(status_code=404, detail="页面不存在")
    return page


@router.put("/{page_id}", response_model=PageResponse, summary="更新页面")
def update_page(
    page_id: UUID = Path(..., description="页面ID"),
    page_data: PageUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新页面信息"""
    # 如果更新slug，检查是否已存在
    if page_data.slug:
        existing_page = PageService.get_page_by_slug(db, page_data.slug)
        if existing_page and existing_page.id != page_id:
            raise HTTPException(status_code=400, detail="页面别名已存在")
    
    page = PageService.update_page(db, page_id, page_data)
    if not page:
        raise HTTPException(status_code=404, detail="页面不存在")
    return page


@router.delete("/{page_id}", summary="删除页面")
def delete_page(
    page_id: UUID = Path(..., description="页面ID"),
    db: Session = Depends(get_db)
):
    """删除指定页面"""
    success = PageService.delete_page(db, page_id)
    if not success:
        raise HTTPException(status_code=404, detail="页面不存在")
    return {"message": "页面删除成功"}


@router.post("/{page_id}/publish", response_model=PageResponse, summary="发布页面")
def publish_page(
    page_id: UUID = Path(..., description="页面ID"),
    db: Session = Depends(get_db)
):
    """发布页面"""
    page = PageService.publish_page(db, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="页面不存在")
    return page


@router.patch("/batch", response_model=List[PageResponse], summary="批量更新页面")
def batch_update_pages(
    batch_data: PageBatchUpdate,
    db: Session = Depends(get_db)
):
    """批量更新页面状态或属性"""
    try:
        pages = PageService.batch_update_status(db, batch_data)
        return pages
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"批量更新失败: {str(e)}")


@router.get("/template/{template}", response_model=List[PageResponse], summary="根据模板获取页面")
def get_pages_by_template(
    template: str = Path(..., description="模板名称"),
    db: Session = Depends(get_db)
):
    """根据模板获取页面列表"""
    pages = PageService.get_pages_by_template(db, template)
    return pages


# 页面翻译管理
@router.post("/{page_id}/translations", response_model=PageTranslationResponse, summary="创建页面翻译")
def create_page_translation(
    page_id: UUID = Path(..., description="页面ID"),
    translation_data: PageTranslationCreate = ...,
    db: Session = Depends(get_db)
):
    """为页面创建或更新翻译"""
    translation = PageService.create_translation(db, page_id, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail="页面不存在")
    return translation


@router.put("/translations/{translation_id}", response_model=PageTranslationResponse, summary="更新页面翻译")
def update_page_translation(
    translation_id: UUID = Path(..., description="翻译ID"),
    translation_data: PageTranslationUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新页面翻译"""
    translation = PageService.update_translation(db, translation_id, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail="翻译不存在")
    return translation


@router.delete("/translations/{translation_id}", summary="删除页面翻译")
def delete_page_translation(
    translation_id: UUID = Path(..., description="翻译ID"),
    db: Session = Depends(get_db)
):
    """删除页面翻译"""
    success = PageService.delete_translation(db, translation_id)
    if not success:
        raise HTTPException(status_code=404, detail="翻译不存在")
    return {"message": "翻译删除成功"}


# === 公开API（供C端使用） ===

@public_router.get("/", response_model=List[PublicPageResponse], summary="获取已发布页面列表")
def get_published_pages(
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取已发布的页面列表（公开API）"""
    pages = PageService.get_published_pages(db, language_code)
    return pages


@public_router.get("/homepage", response_model=PublicPageResponse, summary="获取首页")
def get_homepage(
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取首页（公开API）"""
    page = PageService.get_homepage(db, language_code)
    if not page:
        raise HTTPException(status_code=404, detail="首页不存在")
    return page


@public_router.get("/{slug}", response_model=PublicPageResponse, summary="根据slug获取页面详情")
def public_get_page_by_slug(
    slug: str = Path(..., description="页面别名"),
    db: Session = Depends(get_db)
):
    """根据slug获取页面详情（公开API）"""
    page = PageService.get_page_by_slug(db, slug)
    if not page or page.status != ContentStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="页面不存在")
    
    return page


@public_router.post("/static/{page_type}", response_model=PublicPageResponse, summary="创建静态页面")
def create_static_page(
    page_type: StaticPageType = Path(..., description="静态页面类型"),
    title: str = Query(..., description="页面标题"),
    content: str = Query(..., description="页面内容"),
    db: Session = Depends(get_db)
):
    """创建或更新静态页面（公开API）"""
    page = PageService.create_static_page(db, page_type, title, content)
    return page
