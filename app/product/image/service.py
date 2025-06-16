# -*- coding: utf-8 -*-
"""
商品图片服务类
提供图片上传、管理的业务逻辑实现
"""
import os
import uuid
import shutil
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from datetime import datetime
from pathlib import Path
from PIL import Image
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status, UploadFile

try:
    from moviepy.editor import VideoFileClip
    VIDEO_PROCESSING_AVAILABLE = True
except ImportError:
    VIDEO_PROCESSING_AVAILABLE = False

from app.product.models import Product, ProductImage
from app.product.image.schema import (
    ImageUploadResponse,
    ProductImageCreate,
    ProductImageUpdate,
    ProductImageResponse,
    ProductImageListResponse,
    ImageDeleteResponse,
    ImageBatchUpdateRequest
)


class ProductImageService:
    """商品图片和视频服务类"""
    
    # 配置常量
    UPLOAD_DIR = "static/uploads/product-images"
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov"}
    ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS
    MAX_IMAGE_FILE_SIZE = 10 * 1024 * 1024  # 10MB for images
    MAX_VIDEO_FILE_SIZE = 500 * 1024 * 1024  # 500MB for videos
    
    @classmethod
    def _ensure_upload_dir(cls, product_id: UUID) -> Path:
        """确保上传目录存在"""
        upload_path = Path(cls.UPLOAD_DIR) / str(product_id)
        upload_path.mkdir(parents=True, exist_ok=True)
        return upload_path
    
    @classmethod
    def _is_video_file(cls, filename: str) -> bool:
        """判断是否为视频文件"""
        file_extension = Path(filename).suffix.lower()
        return file_extension in cls.ALLOWED_VIDEO_EXTENSIONS
    
    @classmethod
    def _validate_file(cls, file: UploadFile) -> None:
        """验证文件"""
        # 检查文件扩展名
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件格式。支持的格式: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )
        
        # 检查文件大小
        is_video = file_extension in cls.ALLOWED_VIDEO_EXTENSIONS
        max_size = cls.MAX_VIDEO_FILE_SIZE if is_video else cls.MAX_IMAGE_FILE_SIZE
        max_size_mb = max_size // 1024 // 1024
        
        if file.size and file.size > max_size:
            file_type = "视频" if is_video else "图片"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{file_type}文件大小超过限制，最大允许 {max_size_mb}MB"
            )
    
    @classmethod
    def _get_image_dimensions(cls, file_path: Path) -> Tuple[Optional[int], Optional[int]]:
        """获取图片尺寸"""
        try:
            with Image.open(file_path) as img:
                return img.size  # (width, height)
        except Exception:
            return None, None
    
    @classmethod
    def _get_video_info(cls, file_path: Path) -> Dict[str, Any]:
        """获取视频信息"""
        if not VIDEO_PROCESSING_AVAILABLE:
            return {
                "width": None,
                "height": None,
                "duration": None,
                "thumbnail_url": None
            }
        
        try:
            with VideoFileClip(str(file_path)) as clip:
                # 获取视频尺寸和时长
                width, height = clip.size if clip.size else (None, None)
                duration = int(clip.duration) if clip.duration else None
                
                # 生成缩略图
                thumbnail_url = None
                if clip.duration and clip.duration > 1:
                    thumbnail_filename = f"{file_path.stem}_thumb.jpg"
                    thumbnail_path = file_path.parent / thumbnail_filename
                    
                    # 在视频第1秒处截取缩略图
                    clip.save_frame(str(thumbnail_path), t=1)
                    
                    # 构造缩略图URL
                    relative_thumbnail_path = thumbnail_path.relative_to(Path("static"))
                    thumbnail_url = f"/static/{relative_thumbnail_path.as_posix()}"
                
                return {
                    "width": width,
                    "height": height,
                    "duration": duration,
                    "thumbnail_url": thumbnail_url
                }
        except Exception as e:
            print(f"视频信息提取失败: {e}")
            return {
                "width": None,
                "height": None,
                "duration": None,
                "thumbnail_url": None
            }
    
    @classmethod
    def upload_image(cls, db: Session, product_id: UUID, file: UploadFile) -> ImageUploadResponse:
        """
        上传商品图片文件
        """
        # 验证商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        # 验证文件
        cls._validate_file(file)
        
        # 确保上传目录存在
        upload_dir = cls._ensure_upload_dir(product_id)
        
        # 生成唯一文件名
        file_extension = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4().hex}_{int(datetime.now().timestamp())}{file_extension}"
        file_path = upload_dir / unique_filename
        
        try:
            # 保存文件
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 判断文件类型
            is_video = cls._is_video_file(file.filename)
            
            # 获取文件信息
            width, height = None, None
            duration, thumbnail_url, video_format = None, None, None
            
            if is_video:
                # 获取视频信息
                video_info = cls._get_video_info(file_path)
                width = video_info.get("width")
                height = video_info.get("height")
                duration = video_info.get("duration")
                thumbnail_url = video_info.get("thumbnail_url")
                video_format = Path(file.filename).suffix.lower()[1:]  # 去掉点号
            else:
                # 获取图片尺寸
                width, height = cls._get_image_dimensions(file_path)
            
            # 构造响应
            relative_path = f"uploads/product-images/{product_id}/{unique_filename}"
            file_url = f"/static/{relative_path}"
            
            return ImageUploadResponse(
                file_name=unique_filename,
                file_path=relative_path,
                file_url=file_url,
                file_size=file_path.stat().st_size,
                width=width,
                height=height,
                is_video=is_video,
                duration=duration,
                video_format=video_format
            )
            
        except Exception as e:
            # 如果出错，删除已上传的文件
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"文件上传失败: {str(e)}"
            )
    
    @staticmethod
    def create_product_image(
        db: Session, 
        product_id: UUID, 
        image_data: ProductImageCreate
    ) -> ProductImageResponse:
        """
        创建商品图片记录
        """
        # 验证商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        # 如果是主图类型，先将其他主图设为非主图
        if image_data.image_type.value == "main":
            db.query(ProductImage).filter(
                ProductImage.product_id == product_id,
                ProductImage.image_type == "main"
            ).update({"image_type": "gallery"})
        
        # 创建图片记录
        create_data = image_data.dict()
        create_data["product_id"] = product_id
        
        new_image = ProductImage(**create_data)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        
        return ProductImageResponse.from_orm(new_image)
    
    @staticmethod
    def get_product_images(
        db: Session, 
        product_id: UUID,
        is_active: Optional[bool] = None
    ) -> ProductImageListResponse:
        """
        获取商品图片列表
        """
        # 验证商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        # 构建查询
        query = db.query(ProductImage).filter(ProductImage.product_id == product_id)
        
        if is_active is not None:
            query = query.filter(ProductImage.is_active == is_active)
        
        # 排序：主图优先，然后按sort_order，最后按创建时间
        images = query.order_by(
            desc(ProductImage.image_type == "main"),
            ProductImage.sort_order,
            ProductImage.created_at
        ).all()
        
        return ProductImageListResponse(
            images=[ProductImageResponse.from_orm(image) for image in images],
            total=len(images)
        )
    
    @staticmethod
    def get_image_by_id(db: Session, image_id: UUID) -> ProductImageResponse:
        """
        根据ID获取图片详情
        """
        image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"图片ID {image_id} 不存在"
            )
        
        return ProductImageResponse.from_orm(image)
    
    @staticmethod
    def update_product_image(
        db: Session, 
        image_id: UUID, 
        image_data: ProductImageUpdate
    ) -> ProductImageResponse:
        """
        更新商品图片信息
        """
        image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"图片ID {image_id} 不存在"
            )
        
        # 如果更新为主图类型，先将其他主图设为非主图
        if image_data.image_type and image_data.image_type.value == "main":
            db.query(ProductImage).filter(
                ProductImage.product_id == image.product_id,
                ProductImage.image_type == "main",
                ProductImage.id != image_id
            ).update({"image_type": "gallery"})
        
        # 更新图片信息
        update_data = image_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(image, key, value)
        
        image.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(image)
        
        return ProductImageResponse.from_orm(image)
    
    @classmethod
    def delete_product_image(
        cls, 
        db: Session, 
        image_id: UUID,
        delete_file: bool = True
    ) -> ImageDeleteResponse:
        """
        删除商品图片
        """
        image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"图片ID {image_id} 不存在"
            )
        
        # 保存文件路径信息
        file_path = None
        if delete_file and image.image_url:
            # 从URL提取文件路径
            if image.image_url.startswith('/static/'):
                relative_path = image.image_url[8:]  # 去掉 '/static/' 前缀
                file_path = Path("static") / relative_path
        
        # 删除数据库记录
        db.delete(image)
        db.commit()
        
        # 删除物理文件
        deleted_file_path = None
        if delete_file and file_path and file_path.exists():
            try:
                file_path.unlink()
                deleted_file_path = str(file_path)
            except Exception as e:
                # 文件删除失败不影响数据库操作
                pass
        
        return ImageDeleteResponse(
            success=True,
            message="图片删除成功",
            deleted_file_path=deleted_file_path
        )
    
    @staticmethod
    def batch_update_image_orders(
        db: Session, 
        product_id: UUID, 
        batch_data: ImageBatchUpdateRequest
    ) -> Dict[str, Any]:
        """
        批量更新图片排序
        """
        # 验证商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        # 验证所有图片ID是否属于该商品
        image_ids = [item['id'] for item in batch_data.image_orders]
        existing_images = db.query(ProductImage).filter(
            ProductImage.id.in_(image_ids),
            ProductImage.product_id == product_id
        ).all()
        
        if len(existing_images) != len(image_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="部分图片ID不存在或不属于该商品"
            )
        
        # 批量更新排序
        try:
            for item in batch_data.image_orders:
                db.query(ProductImage).filter(
                    ProductImage.id == item['id']
                ).update({"sort_order": item['sort_order']})
            
            db.commit()
            
            return {
                "success": True,
                "message": "图片排序更新成功",
                "updated_count": len(image_ids)
            }
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"批量更新失败: {str(e)}"
            )
