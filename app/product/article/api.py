"""
产品文章管理API路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_admin_user
from app.security.user.models import User
from app.product.article.service import ProductArticleService
from app.product.article.schema import (
    ProductArticleCreateRequest,
    ProductArticleUpdateRequest,
    ProductArticleTranslationCreateRequest,
    ProductArticleTranslationUpdateRequest,
    ProductArticleAssignRequest,
    ProductArticleResponse,
    ProductArticleListResponse,
    ProductArticleTranslationResponse,
    PaginatedArticleResponse,
    ArticleStatsResponse,
    ProductWithArticlesResponse
)
from app.product.article.models import ArticleStatus, ArticleType

router = APIRouter()

# ==================== 文章管理 ====================

@router.get("/articles", response_model=PaginatedArticleResponse)
async def get_articles(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    article_type: Optional[ArticleType] = Query(None, description="文章类型"),
    status: Optional[ArticleStatus] = Query(None, description="文章状态"),
    category: Optional[str] = Query(None, description="文章分类"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    service = ProductArticleService(db)
    articles, total = service.get_articles(
        page=page,
        limit=limit,
        article_type=article_type,
        status=status,
        category=category,
        keyword=keyword
    )
    
    # 计算每个文章关联的产品数量
    article_list = []
    for article in articles:
        products = service.get_article_products(str(article.id))
        article_data = ProductArticleListResponse.from_orm(article)
        article_data.product_count = len(products)
        article_list.append(article_data)
    
    return PaginatedArticleResponse(
        items=article_list,
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit
    )


@router.post("/articles", response_model=ProductArticleResponse)
async def create_article(
    request: ProductArticleCreateRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """创建产品文章"""
    service = ProductArticleService(db)
    
    # 检查slug是否已存在
    existing = service.get_article_by_slug(request.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文章别名已存在"
        )
    
    article = service.create_article(request, author_id=str(current_admin.id))
    
    # 获取关联产品数量
    products = service.get_article_products(str(article.id))
    article_response = ProductArticleResponse.from_orm(article)
    article_response.product_count = len(products)
    
    return article_response


@router.get("/articles/{article_id}", response_model=ProductArticleResponse)
async def get_article(
    article_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取文章详情"""
    service = ProductArticleService(db)
    article = service.get_article_by_id(article_id, include_translations=True)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    # 获取关联产品数量
    products = service.get_article_products(article_id)
    article_response = ProductArticleResponse.from_orm(article)
    article_response.product_count = len(products)
    
    return article_response


@router.put("/articles/{article_id}", response_model=ProductArticleResponse)
async def update_article(
    article_id: str,
    request: ProductArticleUpdateRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """更新文章"""
    service = ProductArticleService(db)
    
    # 如果更新slug，检查是否冲突
    if request.slug:
        existing = service.get_article_by_slug(request.slug)
        if existing and str(existing.id) != article_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文章别名已存在"
            )
    
    article = service.update_article(article_id, request)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    # 获取关联产品数量
    products = service.get_article_products(article_id)
    article_response = ProductArticleResponse.from_orm(article)
    article_response.product_count = len(products)
    
    return article_response


@router.delete("/articles/{article_id}")
async def delete_article(
    article_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """删除文章"""
    service = ProductArticleService(db)
    success = service.delete_article(article_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    return {"message": "文章删除成功"}


@router.post("/articles/{article_id}/publish", response_model=ProductArticleResponse)
async def publish_article(
    article_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """发布文章"""
    service = ProductArticleService(db)
    article = service.publish_article(article_id)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    # 获取关联产品数量
    products = service.get_article_products(article_id)
    article_response = ProductArticleResponse.from_orm(article)
    article_response.product_count = len(products)
    
    return article_response


# ==================== 翻译管理 ====================

@router.post("/articles/{article_id}/translations", response_model=ProductArticleTranslationResponse)
async def create_article_translation(
    article_id: str,
    request: ProductArticleTranslationCreateRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """创建文章翻译"""
    service = ProductArticleService(db)
    translation = service.create_translation(
        article_id, 
        request, 
        translator_id=str(current_admin.id)
    )
    
    if not translation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文章不存在或该语言翻译已存在"
        )
    
    return ProductArticleTranslationResponse.from_orm(translation)


@router.get("/articles/{article_id}/translations", response_model=List[ProductArticleTranslationResponse])
async def get_article_translations(
    article_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取文章的所有翻译"""
    service = ProductArticleService(db)
    translations = service.get_article_translations(article_id)
    
    return [ProductArticleTranslationResponse.from_orm(t) for t in translations]


@router.put("/translations/{translation_id}", response_model=ProductArticleTranslationResponse)
async def update_article_translation(
    translation_id: str,
    request: ProductArticleTranslationUpdateRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """更新文章翻译"""
    service = ProductArticleService(db)
    translation = service.update_translation(translation_id, request)
    
    if not translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="翻译记录不存在"
        )
    
    return ProductArticleTranslationResponse.from_orm(translation)


# ==================== 产品关联管理 ====================

@router.post("/articles/{article_id}/assign-products")
async def assign_article_to_products(
    article_id: str,
    request: ProductArticleAssignRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """将文章分配给产品"""
    service = ProductArticleService(db)
    success = service.assign_article_to_products(article_id, request)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    return {"message": "文章分配成功"}


@router.delete("/articles/{article_id}/products/{product_id}")
async def remove_article_from_product(
    article_id: str,
    product_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """将文章从产品移除"""
    service = ProductArticleService(db)
    success = service.remove_article_from_product(article_id, product_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="关联关系不存在"
        )
    
    return {"message": "文章移除成功"}


@router.get("/articles/{article_id}/products", response_model=List[ProductWithArticlesResponse])
async def get_article_products(
    article_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取关联文章的产品列表"""
    service = ProductArticleService(db)
    products = service.get_article_products(article_id)
    
    return [ProductWithArticlesResponse.from_orm(p) for p in products]


# ==================== 公开API - 用于前端展示 ====================

@router.get("/public/products/{product_id}/articles", response_model=List[ProductArticleResponse])
async def get_product_articles_public(
    product_id: str,
    language_code: Optional[str] = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """获取产品关联的文章（公开接口）"""
    service = ProductArticleService(db)
    articles = service.get_product_articles(product_id, language_code)
    
    return [ProductArticleResponse.from_orm(article) for article in articles]


@router.get("/public/articles/{slug}", response_model=ProductArticleResponse)
async def get_article_public(
    slug: str,
    language_code: Optional[str] = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """根据slug获取文章（公开接口）"""
    service = ProductArticleService(db)
    article = service.get_article_by_slug(slug, language_code)
    
    if not article or article.status != ArticleStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在或未发布"
        )
    
    # 增加浏览次数
    article.view_count += 1
    service.db.commit()
    
    return ProductArticleResponse.from_orm(article)


# ==================== 统计信息 ====================

@router.get("/articles/stats", response_model=ArticleStatsResponse)
async def get_article_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取文章统计信息"""
    service = ProductArticleService(db)
    stats = service.get_article_stats()
    
    return ArticleStatsResponse(**stats)