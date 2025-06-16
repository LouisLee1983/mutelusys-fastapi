# -*- coding: utf-8 -*-
"""
商品图片API接口
提供商品图片上传、管理的REST API接口
"""
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.product.image.service import ProductImageService
from app.product.image.schema import (
    ImageUploadResponse,
    ProductImageCreate,
    ProductImageUpdate,
    ProductImageResponse,
    ProductImageListResponse,
    ImageDeleteResponse,
    ImageBatchUpdateRequest
)
from app.product.models import ImageType

router = APIRouter()


@router.post("/upload/{product_id}", response_model=ImageUploadResponse)
def upload_product_image(
    product_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传商品图片或视频文件
    
    - **product_id**: 商品ID
    - **file**: 图片文件（支持jpg, jpeg, png, webp, gif格式，最大10MB）或视频文件（支持mp4, webm, mov格式，最大500MB）
    
    返回上传结果，包含文件URL、尺寸等信息，视频会包含时长和缩略图
    """
    return ProductImageService.upload_image(db, product_id, file)


@router.post("/{product_id}", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
def create_product_image(
    product_id: UUID,
    image_data: ProductImageCreate,
    db: Session = Depends(get_db)
):
    """
    创建商品图片或视频记录
    
    - **product_id**: 商品ID
    - **image_data**: 图片或视频信息
    
    将已上传的文件关联到商品
    """
    return ProductImageService.create_product_image(db, product_id, image_data)


@router.post("/upload-and-create/{product_id}", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
def upload_and_create_product_image(
    product_id: UUID,
    file: UploadFile = File(...),
    image_type: str = Form(default="gallery"),  # 改为字符串类型接收
    alt_text: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    sort_order: int = Form(default=0),
    is_active: bool = Form(default=True),
    db: Session = Depends(get_db)
):
    """
    一步完成图片或视频上传和创建记录
    
    - **product_id**: 商品ID
    - **file**: 图片文件（jpg, jpeg, png, webp, gif，最大10MB）或视频文件（mp4, webm, mov，最大500MB）
    - **image_type**: 媒体类型（main/gallery/detail/banner/thumbnail/video）
    - **alt_text**: 替代文本
    - **title**: 图片/视频标题
    - **description**: 图片/视频描述
    - **sort_order**: 排序顺序
    - **is_active**: 是否激活
    
    组合上传和创建操作，简化前端调用。自动识别文件类型并提取相应元数据。
    """
    # 先上传文件
    upload_result = ProductImageService.upload_image(db, product_id, file)
    
    # 验证并转换image_type
    try:
        # 确保image_type是小写的
        image_type_lower = image_type.lower()
        
        # 根据字符串值获取对应的枚举
        image_type_enum = None
        for enum_item in ImageType:
            if enum_item.value == image_type_lower:
                image_type_enum = enum_item
                break
        
        if image_type_enum is None:
            # 如果没找到匹配的枚举，使用默认值
            image_type_enum = ImageType.GALLERY
            
        # 不再特殊处理视频类型，视频也可以是main/gallery/detail等类型
        # 通过is_video字段来区分是否为视频
            
    except Exception as e:
        # 如果转换失败，使用默认值
        image_type_enum = ImageType.GALLERY
    
    # 再创建记录
    image_data = ProductImageCreate(
        image_url=upload_result.file_url,
        image_type=image_type_enum,
        alt_text=alt_text,
        title=title,
        description=description,
        width=upload_result.width,
        height=upload_result.height,
        file_size=upload_result.file_size // 1024 if upload_result.file_size else None,  # 转换为KB
        duration=upload_result.duration,
        thumbnail_url=None,  # 缩略图URL在视频处理时已生成
        is_video=upload_result.is_video,
        video_format=upload_result.video_format,
        sort_order=sort_order,
        is_active=is_active
    )
    
    return ProductImageService.create_product_image(db, product_id, image_data)


@router.get("/{product_id}", response_model=ProductImageListResponse)
def get_product_images(
    product_id: UUID,
    is_active: Optional[bool] = Query(None, description="筛选激活状态"),
    db: Session = Depends(get_db)
):
    """
    获取商品图片列表
    
    - **product_id**: 商品ID
    - **is_active**: 可选，筛选激活状态
    
    返回该商品的所有图片，按主图优先、排序顺序、创建时间排序
    """
    return ProductImageService.get_product_images(db, product_id, is_active)


@router.get("/detail/{image_id}", response_model=ProductImageResponse)
def get_image_by_id(
    image_id: UUID,
    db: Session = Depends(get_db)
):
    """
    根据ID获取图片详情
    
    - **image_id**: 图片ID
    """
    return ProductImageService.get_image_by_id(db, image_id)


@router.put("/detail/{image_id}", response_model=ProductImageResponse)
def update_product_image(
    image_id: UUID,
    image_data: ProductImageUpdate,
    db: Session = Depends(get_db)
):
    """
    更新商品图片信息
    
    - **image_id**: 图片ID
    - **image_data**: 更新的图片信息
    
    可以更新图片的类型、标题、描述、排序等属性
    """
    return ProductImageService.update_product_image(db, image_id, image_data)


@router.delete("/detail/{image_id}", response_model=ImageDeleteResponse)
def delete_product_image(
    image_id: UUID,
    delete_file: bool = Query(default=True, description="是否同时删除物理文件"),
    db: Session = Depends(get_db)
):
    """
    删除商品图片
    
    - **image_id**: 图片ID
    - **delete_file**: 是否同时删除物理文件（默认true）
    
    删除图片记录，可选择是否同时删除服务器上的物理文件
    """
    return ProductImageService.delete_product_image(db, image_id, delete_file)


@router.put("/{product_id}/batch-order")
def batch_update_image_orders(
    product_id: UUID,
    batch_data: ImageBatchUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    批量更新图片排序
    
    - **product_id**: 商品ID
    - **batch_data**: 包含图片ID和排序的批量数据
    
    用于拖拽排序功能，一次性更新多个图片的排序顺序
    """
    return ProductImageService.batch_update_image_orders(db, product_id, batch_data)


@router.patch("/detail/{image_id}/set-main", response_model=ProductImageResponse)
def set_as_main_image(
    image_id: UUID,
    db: Session = Depends(get_db)
):
    """
    设置为主图
    
    - **image_id**: 图片ID
    
    将指定图片设置为主图，其他主图会自动设置为普通图片
    """
    update_data = ProductImageUpdate(image_type=ImageType.MAIN)
    return ProductImageService.update_product_image(db, image_id, update_data)


@router.patch("/detail/{image_id}/toggle-active", response_model=ProductImageResponse)
def toggle_image_active(
    image_id: UUID,
    db: Session = Depends(get_db)
):
    """
    切换图片激活状态
    
    - **image_id**: 图片ID
    
    在激活和非激活状态之间切换
    """
    # 先获取当前状态
    current_image = ProductImageService.get_image_by_id(db, image_id)
    update_data = ProductImageUpdate(is_active=not current_image.is_active)
    return ProductImageService.update_product_image(db, image_id, update_data)
