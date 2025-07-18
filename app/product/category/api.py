from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status, UploadFile, File, Form
from fastapi.params import Body
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.product.category.schema import (
    ProductCategory,
    ProductCategoryCreate,
    ProductCategoryUpdate,
    ProductCategoryList,
    ProductCategoryTreeList,
    ProductCategoryTranslation,
    ProductCategoryTranslationCreate,
    ProductCategoryTranslationUpdate
)
from app.product.category.service import ProductCategoryService
from app.security.models import User

router = APIRouter()

# 统一响应格式
def success_response(data: Any = None, message: str = "操作成功", code: int = 200):
    return {"code": code, "message": message, "data": data}

def error_response(message: str = "操作失败", code: int = 400, data: Any = None):
    return {"code": code, "message": message, "data": data}


@router.get("")
def get_categories(
    skip: int = Query(0, ge=0, description="分页起始位置"),
    limit: int = Query(100, ge=1, le=1000, description="每页数量"),
    parent_id: Optional[UUID] = Query(None, description="父分类ID"),
    level: Optional[str] = Query(None, description="分类层级"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    is_featured: Optional[bool] = Query(None, description="是否推荐分类"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    include_children: bool = Query(False, description="是否包含子分类"),
    db: Session = Depends(get_db)
):
    """
    获取产品分类列表，支持分页、过滤和搜索
    """
    result = ProductCategoryService.get_categories(
        db, skip, limit, parent_id, level, is_active, is_featured, search, include_children
    )
    return success_response(data=result)


@router.get("/tree")
def get_category_tree(
    parent_id: Optional[UUID] = Query(None, description="父分类ID，为空则返回一级分类树"),
    db: Session = Depends(get_db)
):
    """
    获取产品分类树形结构，支持指定父分类ID获取子树
    """
    result = ProductCategoryService.get_category_tree(db, parent_id)
    return success_response(data=result)


@router.get("/{category_id}")
def get_category(
    category_id: UUID = Path(..., description="分类ID"),
    db: Session = Depends(get_db)
):
    """
    根据ID获取产品分类详情
    """
    result = ProductCategoryService.get_category_by_id(db, category_id)
    return success_response(data=result)


@router.get("/slug/{slug}", response_model=ProductCategory)
def get_category_by_slug(
    slug: str = Path(..., description="分类别名"),
    db: Session = Depends(get_db)
):
    """
    根据别名获取产品分类详情
    """
    return ProductCategoryService.get_category_by_slug(db, slug)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    category: ProductCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的产品分类
    """
    result = ProductCategoryService.create_category(db, category)
    return success_response(data=result, message="创建分类成功", code=201)


@router.put("/{category_id}")
def update_category(
    category_id: UUID = Path(..., description="分类ID"),
    category: ProductCategoryUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新产品分类信息
    """
    result = ProductCategoryService.update_category(db, category_id, category)
    return success_response(data=result, message="更新分类成功")


@router.delete("/{category_id}")
def delete_category(
    category_id: UUID = Path(..., description="分类ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除产品分类
    """
    ProductCategoryService.delete_category(db, category_id)
    return success_response(message="删除分类成功")


# 分类翻译相关API
@router.get("/{category_id}/translations/{language_code}", response_model=ProductCategoryTranslation)
def get_category_translation(
    category_id: UUID = Path(..., description="分类ID"),
    language_code: str = Path(..., description="语言代码"),
    db: Session = Depends(get_db)
):
    """
    获取产品分类的指定语言翻译
    """
    return ProductCategoryService.get_category_translation(db, category_id, language_code)


@router.post("/{category_id}/translations", response_model=ProductCategoryTranslation, status_code=status.HTTP_201_CREATED)
def create_category_translation(
    category_id: UUID = Path(..., description="分类ID"),
    translation: ProductCategoryTranslationCreate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为产品分类添加新的语言翻译
    """
    return ProductCategoryService.create_category_translation(db, category_id, translation)


@router.put("/{category_id}/translations/{language_code}", response_model=ProductCategoryTranslation)
def update_category_translation(
    category_id: UUID = Path(..., description="分类ID"),
    language_code: str = Path(..., description="语言代码"),
    translation: ProductCategoryTranslationUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新产品分类的语言翻译
    """
    return ProductCategoryService.update_category_translation(db, category_id, language_code, translation)


@router.delete("/{category_id}/translations/{language_code}", response_model=Dict[str, Any])
def delete_category_translation(
    category_id: UUID = Path(..., description="分类ID"),
    language_code: str = Path(..., description="语言代码"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除产品分类的语言翻译
    """
    return ProductCategoryService.delete_category_translation(db, category_id, language_code)


@router.post("/import", status_code=status.HTTP_201_CREATED)
def import_categories(
    root_category_guid: UUID = Query(..., description="根分类GUID"),
    categories: List[ProductCategoryCreate] = Body(..., description="产品分类列表"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    通过json格式的数据批量导入多级分类
    通过json格式的数据批量导入多级分类，场景是前端admin-web在一个富文本中输入json数据，然后点击导入按钮，将json数据导入到数据库中
    json数据格式并没有记录父类guid，它是根据层级关系来确定的，所以需要根据层级关系来确定父类guid
    json数据格式如下：
    [
        {
            "name": "分类名称",
            "level": "分类层级",
            "slug": "分类别名",
            "description": "分类描述",
            "image_url": "分类图片URL",
            "icon_url": "分类图标URL",
            "is_active": true,
            "is_featured": true,
            "sort_order": 0,
            "seo_title": "SEO标题",
            "seo_description": "SEO描述",
            "seo_keywords": "SEO关键词",
            "children": [
                {
                    "name": "子分类名称",
                    "level": "子分类层级",
                    "slug": "子分类别名",
                    "description": "子分类描述",
                    "image_url": "子分类图片URL",
                    "icon_url": "子分类图标URL",
                    "is_active": true,
                    "is_featured": true,
                    "sort_order": 0,
                    "seo_title": "子分类SEO标题",
                    "seo_description": "子分类SEO描述",
                    "seo_keywords": "子分类SEO关键词",
                    "children": [
                        {
                            "name": "孙子分类名称",
                            "level": "孙子分类层级",
                            "slug": "孙子分类别名",
                            "description": "孙子分类描述",
                            "image_url": "孙子分类图片URL",
                            "icon_url": "孙子分类图标URL",
                            "is_active": true,
                            "is_featured": true,
                            "sort_order": 0,
                            "seo_title": "孙子分类SEO标题",
                            "seo_description": "孙子分类SEO描述",
                            "seo_keywords": "孙子分类SEO关键词",
                        }
                    ]
                }
            ]
        }
    ]
    """
    ProductCategoryService.import_categories(db, root_category_guid, categories)
    return success_response(message="导入分类成功")


@router.post("/{category_id}/upload-hero-image")
async def upload_category_hero_image(
    category_id: UUID = Path(..., description="分类ID"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    上传分类大图（hero image）
    """
    result = await ProductCategoryService.upload_category_image(
        db, category_id, file, image_type="hero"
    )
    return success_response(data=result, message="分类大图上传成功")


@router.post("/{category_id}/upload-icon-image")
async def upload_category_icon_image(
    category_id: UUID = Path(..., description="分类ID"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    上传分类小图（icon image）
    """
    result = await ProductCategoryService.upload_category_image(
        db, category_id, file, image_type="icon"
    )
    return success_response(data=result, message="分类图标上传成功")


@router.delete("/{category_id}/delete-hero-image")
async def delete_category_hero_image(
    category_id: UUID = Path(..., description="分类ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除分类大图（hero image）
    """
    result = await ProductCategoryService.delete_category_image(
        db, category_id, image_type="hero"
    )
    return success_response(data=result, message="分类大图删除成功")


@router.delete("/{category_id}/delete-icon-image")
async def delete_category_icon_image(
    category_id: UUID = Path(..., description="分类ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除分类小图（icon image）
    """
    result = await ProductCategoryService.delete_category_image(
        db, category_id, image_type="icon"
    )
    return success_response(data=result, message="分类图标删除成功")

