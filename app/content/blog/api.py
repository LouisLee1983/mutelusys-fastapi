from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.content.blog.service import BlogService, BlogTagService, BlogCategoryService
from app.content.blog.schema import (
    BlogCreate, BlogUpdate, BlogResponse, BlogListQuery, BlogListResponse,
    BlogBatchUpdate, PublicBlogResponse, BlogTranslationCreate,
    BlogTranslationUpdate, BlogTranslationResponse, BlogTagCreate,
    BlogTagUpdate, BlogTagResponse, BlogCategoryCreate, BlogCategoryUpdate,
    BlogCategoryResponse, BlogStatistics
)
from app.content.models import ContentStatus

# 管理端路由
router = APIRouter()

# 公开API路由（供前端使用）
public_router = APIRouter()


@router.post("/", response_model=BlogResponse, summary="创建博客文章")
def create_blog(
    blog_data: BlogCreate,
    db: Session = Depends(get_db)
):
    """创建新的博客文章"""
    try:
        # 检查slug是否已存在
        existing_blog = BlogService.get_blog_by_slug(db, blog_data.slug)
        if existing_blog:
            raise HTTPException(status_code=400, detail="文章别名已存在")
        
        blog = BlogService.create_blog(db, blog_data)
        return blog
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建博客文章失败: {str(e)}")


@router.get("/", response_model=BlogListResponse, summary="获取博客文章列表")
def get_blogs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: ContentStatus = Query(None, description="状态筛选"),
    category_id: str = Query(None, description="分类筛选"),
    tag_id: str = Query(None, description="标签筛选"),
    is_featured: bool = Query(None, description="是否推荐筛选"),
    search: str = Query(None, description="搜索关键词"),
    author_id: str = Query(None, description="作者筛选"),
    db: Session = Depends(get_db)
):
    """获取博客文章列表，支持筛选和分页"""
    query = BlogListQuery(
        page=page,
        page_size=page_size,
        status=status,
        category_id=category_id,
        tag_id=tag_id,
        is_featured=is_featured,
        search=search,
        author_id=author_id
    )
    
    blogs, total = BlogService.get_blogs_list(db, query)
    total_pages = (total + page_size - 1) // page_size
    
    return BlogListResponse(
        items=blogs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/statistics", response_model=BlogStatistics, summary="获取博客统计")
def get_blog_statistics(db: Session = Depends(get_db)):
    """获取博客统计数据"""
    return BlogService.get_statistics(db)


@router.get("/{blog_id}", response_model=BlogResponse, summary="获取博客文章详情")
def get_blog(
    blog_id: UUID = Path(..., description="博客文章ID"),
    db: Session = Depends(get_db)
):
    """根据ID获取博客文章详情"""
    blog = BlogService.get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="博客文章不存在")
    return blog


@router.get("/slug/{slug}", response_model=BlogResponse, summary="根据slug获取博客文章")
def get_blog_by_slug(
    slug: str = Path(..., description="文章别名"),
    db: Session = Depends(get_db)
):
    """根据slug获取博客文章详情"""
    blog = BlogService.get_blog_by_slug(db, slug)
    if not blog:
        raise HTTPException(status_code=404, detail="博客文章不存在")
    return blog


@router.put("/{blog_id}", response_model=BlogResponse, summary="更新博客文章")
def update_blog(
    blog_id: UUID = Path(..., description="博客文章ID"),
    blog_data: BlogUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新博客文章信息"""
    # 如果更新slug，检查是否已存在
    if blog_data.slug:
        existing_blog = BlogService.get_blog_by_slug(db, blog_data.slug)
        if existing_blog and existing_blog.id != blog_id:
            raise HTTPException(status_code=400, detail="文章别名已存在")
    
    blog = BlogService.update_blog(db, blog_id, blog_data)
    if not blog:
        raise HTTPException(status_code=404, detail="博客文章不存在")
    return blog


@router.delete("/{blog_id}", summary="删除博客文章")
def delete_blog(
    blog_id: UUID = Path(..., description="博客文章ID"),
    db: Session = Depends(get_db)
):
    """删除指定博客文章"""
    success = BlogService.delete_blog(db, blog_id)
    if not success:
        raise HTTPException(status_code=404, detail="博客文章不存在")
    return {"message": "博客文章删除成功"}


@router.post("/{blog_id}/publish", response_model=BlogResponse, summary="发布博客文章")
def publish_blog(
    blog_id: UUID = Path(..., description="博客文章ID"),
    db: Session = Depends(get_db)
):
    """发布博客文章"""
    blog = BlogService.publish_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="博客文章不存在")
    return blog


@router.patch("/batch", response_model=List[BlogResponse], summary="批量更新博客文章")
def batch_update_blogs(
    batch_data: BlogBatchUpdate,
    db: Session = Depends(get_db)
):
    """批量更新博客文章状态或属性"""
    try:
        blogs = BlogService.batch_update_status(db, batch_data)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"批量更新失败: {str(e)}")


# 博客翻译管理
@router.post("/{blog_id}/translations", response_model=BlogTranslationResponse, summary="创建博客翻译")
def create_blog_translation(
    blog_id: UUID = Path(..., description="博客文章ID"),
    translation_data: BlogTranslationCreate = ...,
    db: Session = Depends(get_db)
):
    """为博客文章创建或更新翻译"""
    translation = BlogService.create_translation(db, blog_id, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail="博客文章不存在")
    return translation


@router.put("/translations/{translation_id}", response_model=BlogTranslationResponse, summary="更新博客翻译")
def update_blog_translation(
    translation_id: UUID = Path(..., description="翻译ID"),
    translation_data: BlogTranslationUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新博客翻译"""
    translation = BlogService.update_translation(db, translation_id, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail="翻译不存在")
    return translation


# === 博客标签管理 ===

tag_router = APIRouter()

@tag_router.post("/", response_model=BlogTagResponse, summary="创建博客标签")
def create_blog_tag(
    tag_data: BlogTagCreate,
    db: Session = Depends(get_db)
):
    """创建新的博客标签"""
    try:
        tag = BlogTagService.create_tag(db, tag_data)
        return tag
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建标签失败: {str(e)}")


@tag_router.get("/", response_model=List[BlogTagResponse], summary="获取所有博客标签")
def get_blog_tags(db: Session = Depends(get_db)):
    """获取所有博客标签"""
    tags = BlogTagService.get_all_tags(db)
    return tags


@tag_router.get("/{tag_id}", response_model=BlogTagResponse, summary="获取博客标签详情")
def get_blog_tag(
    tag_id: UUID = Path(..., description="标签ID"),
    db: Session = Depends(get_db)
):
    """根据ID获取博客标签详情"""
    tag = BlogTagService.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@tag_router.put("/{tag_id}", response_model=BlogTagResponse, summary="更新博客标签")
def update_blog_tag(
    tag_id: UUID = Path(..., description="标签ID"),
    tag_data: BlogTagUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新博客标签"""
    tag = BlogTagService.update_tag(db, tag_id, tag_data)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@tag_router.delete("/{tag_id}", summary="删除博客标签")
def delete_blog_tag(
    tag_id: UUID = Path(..., description="标签ID"),
    db: Session = Depends(get_db)
):
    """删除指定博客标签"""
    success = BlogTagService.delete_tag(db, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="标签不存在")
    return {"message": "标签删除成功"}


# === 博客分类管理 ===

category_router = APIRouter()

@category_router.post("/", response_model=BlogCategoryResponse, summary="创建博客分类")
def create_blog_category(
    category_data: BlogCategoryCreate,
    db: Session = Depends(get_db)
):
    """创建新的博客分类"""
    try:
        category = BlogCategoryService.create_category(db, category_data)
        return category
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建分类失败: {str(e)}")


@category_router.get("/", response_model=List[BlogCategoryResponse], summary="获取所有博客分类")
def get_blog_categories(db: Session = Depends(get_db)):
    """获取所有博客分类"""
    categories = BlogCategoryService.get_all_categories(db)
    return categories


@category_router.get("/{category_id}", response_model=BlogCategoryResponse, summary="获取博客分类详情")
def get_blog_category(
    category_id: UUID = Path(..., description="分类ID"),
    db: Session = Depends(get_db)
):
    """根据ID获取博客分类详情"""
    category = BlogCategoryService.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category


@category_router.put("/{category_id}", response_model=BlogCategoryResponse, summary="更新博客分类")
def update_blog_category(
    category_id: UUID = Path(..., description="分类ID"),
    category_data: BlogCategoryUpdate = ...,
    db: Session = Depends(get_db)
):
    """更新博客分类"""
    category = BlogCategoryService.update_category(db, category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category


@category_router.delete("/{category_id}", summary="删除博客分类")
def delete_blog_category(
    category_id: UUID = Path(..., description="分类ID"),
    db: Session = Depends(get_db)
):
    """删除指定博客分类"""
    success = BlogCategoryService.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="分类不存在")
    return {"message": "分类删除成功"}


# === 公开API（供C端使用） ===

@public_router.get("/", response_model=List[PublicBlogResponse], summary="获取已发布博客列表")
def get_published_blogs(
    limit: int = Query(10, ge=1, le=50, description="限制数量"),
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取已发布的博客列表（公开API）"""
    blogs = BlogService.get_published_blogs(db, limit, language_code)
    return blogs


@public_router.get("/featured", response_model=List[PublicBlogResponse], summary="获取推荐博客")
def get_featured_blogs(
    limit: int = Query(5, ge=1, le=20, description="限制数量"),
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取推荐博客（公开API）"""
    blogs = BlogService.get_featured_blogs(db, limit, language_code)
    return blogs


@public_router.get("/{slug}", response_model=PublicBlogResponse, summary="根据slug获取博客详情")
def public_get_blog_by_slug(
    slug: str = Path(..., description="文章别名"),
    db: Session = Depends(get_db)
):
    """根据slug获取博客详情并增加浏览次数（公开API）"""
    blog = BlogService.get_blog_by_slug(db, slug)
    if not blog or blog.status != ContentStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="博客文章不存在")
    
    # 增加浏览次数
    BlogService.increment_view_count(db, blog.id)
    
    return blog
