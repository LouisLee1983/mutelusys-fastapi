# -*- coding: utf-8 -*-
"""
商品API接口
提供简单的商品管理接口
"""
import os
import uuid as uuid_lib
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.product.service import ProductService
from app.product.schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    ProductQueryParams
)
from app.product.models import ProductCategory, ProductStatus, Product
from app.product.sku.translation_service import ProductSkuTranslationService
from app.product.sku.schema import (
    ProductSkuTranslationCreate,
    ProductSkuTranslationUpdate,
    ProductSkuTranslationResponse,
    ProductSkuWithTranslations
)

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
def get_products(
    skip: int = Query(default=0, ge=0, description="跳过记录数"),
    limit: int = Query(default=20, ge=1, le=100, description="返回记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    category_id: Optional[UUID] = Query(None, description="分类ID筛选"),
    status: Optional[ProductStatus] = Query(None, description="商品状态筛选"),
    is_featured: Optional[bool] = Query(None, description="是否推荐商品筛选"),
    is_new: Optional[bool] = Query(None, description="是否新品筛选"),
    is_bestseller: Optional[bool] = Query(None, description="是否畅销品筛选"),
    sort_by: str = Query(default="updated_at", description="排序字段"),
    sort_desc: bool = Query(default=True, description="是否降序排序"),
    db: Session = Depends(get_db)
):
    """
    获取商品列表
    
    支持分页、搜索和基本筛选功能
    """
    return ProductService.get_products(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        category_id=category_id,
        status=status,
        is_featured=is_featured,
        is_new=is_new,
        is_bestseller=is_bestseller,
        sort_by=sort_by,
        sort_desc=sort_desc
    )


@router.get("/statistics")
def get_product_statistics(db: Session = Depends(get_db)):
    """
    获取商品统计信息
    """
    return ProductService.get_product_statistics(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    根据ID获取商品详情
    """
    return ProductService.get_product_by_id(db, product_id)


@router.get("/sku/{sku_code}", response_model=ProductResponse)
def get_product_by_sku(
    sku_code: str,
    db: Session = Depends(get_db)
):
    """
    根据SKU编码获取商品详情
    """
    return ProductService.get_product_by_sku(db, sku_code)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    创建新商品
    """
    return ProductService.create_product(db, product_data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    更新商品信息
    """
    return ProductService.update_product(db, product_id, product_data)


@router.patch("/{product_id}/status", response_model=ProductResponse)
def update_product_status(
    product_id: UUID,
    new_status: ProductStatus,
    db: Session = Depends(get_db)
):
    """
    更新商品状态
    """
    return ProductService.update_product_status(db, product_id, new_status)


@router.delete("/{product_id}")
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    删除商品（软删除）
    """
    return ProductService.delete_product(db, product_id)


# 商品分类关系管理API
@router.get("/{product_id}/categories")
def get_product_categories(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    获取商品的分类列表
    """
    try:
        print(f"product_id: {product_id}")
        
        # 直接查询中间表（最高效的方案）
        result = db.execute(
            text("SELECT category_id FROM product_category WHERE product_id = :product_id"),
            {"product_id": str(product_id)}
        )
        category_ids = [str(row[0]) for row in result.fetchall()]
        
        return {"code": 200, "message": "获取成功", "data": category_ids}
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取商品分类失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取商品分类失败: {str(e)}")


@router.put("/{product_id}/categories")
def update_product_categories(
    product_id: UUID,
    category_ids: List[UUID] = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    更新商品的分类关系
    """
    try:
        from app.product.models import Product, ProductCategory
        from sqlalchemy.exc import IntegrityError
        
        # 检查商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")
        
        # 验证分类ID是否存在
        existing_categories = db.query(ProductCategory).filter(
            ProductCategory.id.in_(category_ids)
        ).all()
        
        if len(existing_categories) != len(category_ids):
            existing_ids = {cat.id for cat in existing_categories}
            missing_ids = set(category_ids) - existing_ids
            raise HTTPException(
                status_code=400, 
                detail=f"分类不存在: {missing_ids}"
            )
        
        # 更新商品分类关系
        product.categories = existing_categories
        db.commit()
        
        return {"code": 200, "message": "分类更新成功", "data": None}
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="数据库操作失败")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新商品分类失败: {str(e)}")


# 商品主图管理API
@router.post("/{product_id}/main-image")
async def upload_product_main_image(
    product_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传商品主图
    """
    try:
        from app.product.models import Product
        
        # 检查商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")
        
        # 验证文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        
        # 获取文件扩展名
        file_extension = os.path.splitext(file.filename)[1] if file.filename else '.jpg'
        if not file_extension:
            file_extension = '.jpg'
        
        # 创建商品图片目录
        upload_dir = f"static/uploads/product-images/{product_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = f"{upload_dir}/main-image{file_extension}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 更新商品的主图URL
        main_image_url = f"/static/uploads/product-images/{product_id}/main-image{file_extension}"
        product.main_image_url = main_image_url
        db.commit()
        
        return {
            "code": 200,
            "message": "主图上传成功",
            "data": {
                "main_image_url": main_image_url
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"上传主图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"上传主图失败: {str(e)}")


@router.delete("/{product_id}/main-image")
def delete_product_main_image(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    删除商品主图
    """
    try:
        from app.product.models import Product
        
        # 检查商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")
        
        # 删除文件
        if product.main_image_url:
            try:
                # 移除URL前缀，获取实际文件路径
                file_path = product.main_image_url.lstrip('/')
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"删除文件失败: {str(e)}")
        
        # 清空商品的主图URL
        product.main_image_url = None
        db.commit()
        
        return {
            "code": 200,
            "message": "主图删除成功",
            "data": None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"删除主图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除主图失败: {str(e)}")


# ==================== SKU翻译相关端点 ====================

@router.post("/skus/{sku_id}/translations", response_model=ProductSkuTranslationResponse, summary="创建SKU翻译")
async def create_sku_translation(
    sku_id: UUID,
    translation_data: ProductSkuTranslationCreate,
    db: Session = Depends(get_db)
):
    """创建SKU翻译"""
    try:
        return ProductSkuTranslationService.create_translation(db, sku_id, translation_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/skus/{sku_id}/translations", response_model=List[ProductSkuTranslationResponse], summary="获取SKU所有翻译")
async def get_sku_translations(
    sku_id: UUID,
    db: Session = Depends(get_db)
):
    """获取SKU的所有翻译"""
    return ProductSkuTranslationService.get_sku_translations(db, sku_id)


@router.get("/skus/{sku_id}/translations/{language_code}", response_model=ProductSkuTranslationResponse, summary="获取SKU指定语言翻译")
async def get_sku_translation(
    sku_id: UUID,
    language_code: str,
    db: Session = Depends(get_db)
):
    """获取SKU指定语言的翻译"""
    translation = ProductSkuTranslationService.get_translation(db, sku_id, language_code)
    if not translation:
        raise HTTPException(status_code=404, detail=f"SKU {sku_id} 的 {language_code} 翻译不存在")
    return translation


@router.put("/skus/{sku_id}/translations/{language_code}", response_model=ProductSkuTranslationResponse, summary="更新SKU翻译")
async def update_sku_translation(
    sku_id: UUID,
    language_code: str,
    translation_data: ProductSkuTranslationUpdate,
    db: Session = Depends(get_db)
):
    """更新SKU翻译"""
    translation = ProductSkuTranslationService.update_translation(db, sku_id, language_code, translation_data)
    if not translation:
        raise HTTPException(status_code=404, detail=f"SKU {sku_id} 的 {language_code} 翻译不存在")
    return translation


@router.delete("/skus/{sku_id}/translations/{language_code}", summary="删除SKU翻译")
async def delete_sku_translation(
    sku_id: UUID,
    language_code: str,
    db: Session = Depends(get_db)
):
    """删除SKU翻译"""
    success = ProductSkuTranslationService.delete_translation(db, sku_id, language_code)
    if not success:
        raise HTTPException(status_code=404, detail=f"SKU {sku_id} 的 {language_code} 翻译不存在")
    return {"message": f"SKU {sku_id} 的 {language_code} 翻译已删除"}


@router.post("/skus/{sku_id}/translations/auto-translate", summary="自动翻译SKU")
async def auto_translate_sku(
    sku_id: UUID,
    target_languages: List[str] = Query(..., description="目标语言列表"),
    source_language: str = Query("zh-CN", description="源语言"),
    context: Optional[str] = Query(None, description="翻译上下文"),
    db: Session = Depends(get_db)
):
    """自动翻译SKU到指定语言"""
    result = await ProductSkuTranslationService.auto_translate_sku(
        db=db,
        sku_id=sku_id,
        target_languages=target_languages,
        source_language=source_language,
        context=context
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "翻译失败"))
    
    return result


@router.get("/skus/{sku_id}/sku-name/{language_code}", summary="获取指定语言的SKU名称")
async def get_sku_name_by_language(
    sku_id: UUID,
    language_code: str,
    fallback_to_default: bool = Query(True, description="是否回退到默认名称"),
    db: Session = Depends(get_db)
):
    """获取指定语言的SKU名称"""
    sku_name = ProductSkuTranslationService.get_sku_name_by_language(
        db=db,
        sku_id=sku_id,
        language_code=language_code,
        fallback_to_default=fallback_to_default
    )
    
    if not sku_name:
        raise HTTPException(status_code=404, detail=f"SKU {sku_id} 的 {language_code} 名称不存在")
    
    return {"sku_id": sku_id, "language_code": language_code, "sku_name": sku_name}


@router.post("/skus/translations/batch-create-default", summary="批量创建默认翻译")
async def batch_create_default_sku_translations(
    language_code: str = Query("zh-CN", description="语言代码"),
    db: Session = Depends(get_db)
):
    """批量为现有SKU创建默认语言翻译记录"""
    result = ProductSkuTranslationService.batch_create_default_translations(db, language_code)
    return result
