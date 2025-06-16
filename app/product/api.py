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

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
def get_products(
    skip: int = Query(default=0, ge=0, description="跳过记录数"),
    limit: int = Query(default=20, ge=1, le=100, description="返回记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
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
