#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件上传服务
"""

import os
import uuid
import shutil
from typing import List, Optional
from pathlib import Path
from datetime import datetime
from fastapi import UploadFile, HTTPException
import aiofiles
from PIL import Image
import io

class FileUploadService:
    """文件上传服务"""
    
    def __init__(self):
        # 配置上传目录 - 修正为FastAPI项目内的static目录
        self.upload_base_dir = Path("static/uploads")
        self.product_images_dir = self.upload_base_dir / "product-images"
        self.ai_analysis_dir = self.upload_base_dir / "ai-analysis"
        
        # 创建上传目录
        self._ensure_directories()
        
        # 支持的图片格式
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        
    def _ensure_directories(self):
        """确保上传目录存在"""
        for directory in [self.upload_base_dir, self.product_images_dir, self.ai_analysis_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _validate_image(self, file: UploadFile) -> None:
        """验证图片文件"""
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名不能为空")
        
        # 检查文件扩展名
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件格式。支持的格式: {', '.join(self.allowed_extensions)}"
            )
        
        # 检查文件大小
        if hasattr(file, 'size') and file.size and file.size > self.max_file_size:
            raise HTTPException(
                status_code=400, 
                detail=f"文件大小超过限制。最大允许: {self.max_file_size // (1024*1024)}MB"
            )
    
    async def upload_product_image(self, file: UploadFile) -> dict:
        """上传商品图片"""
        self._validate_image(file)
        
        # 生成唯一文件名
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
        file_path = self.product_images_dir / unique_filename
        
        try:
            # 保存文件
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # 验证图片完整性
            try:
                with Image.open(file_path) as img:
                    img.verify()
            except Exception:
                # 如果图片损坏，删除文件
                if file_path.exists():
                    file_path.unlink()
                raise HTTPException(status_code=400, detail="图片文件损坏")
            
            # 生成访问URL
            relative_path = f"/static/uploads/product-images/{unique_filename}"
            
            return {
                "success": True,
                "filename": unique_filename,
                "original_name": file.filename,
                "file_path": str(file_path),
                "url": relative_path,  # 前端期望的字段名
                "relative_path": relative_path,
                "file_size": len(content),
                "upload_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            # 清理已上传的文件
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")
    
    async def upload_multiple_images(self, files: List[UploadFile]) -> dict:
        """批量上传图片"""
        results = []
        errors = []
        
        for file in files:
            try:
                result = await self.upload_product_image(file)
                results.append(result)
            except HTTPException as e:
                errors.append({
                    "filename": getattr(file, 'filename', 'unknown'),
                    "error": e.detail
                })
            except Exception as e:
                errors.append({
                    "filename": getattr(file, 'filename', 'unknown'),
                    "error": str(e)
                })
        
        return {
            "success": len(errors) == 0,
            "uploaded_count": len(results),
            "error_count": len(errors),
            "results": results,
            "errors": errors
        }
    
    def get_test_images(self, limit: int = 5) -> List[dict]:
        """获取测试用的商品图片"""
        test_images_dir = Path("../design-media/images/product-images")
        
        if not test_images_dir.exists():
            return []
        
        test_images = []
        for file_path in test_images_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.allowed_extensions:
                # 生成访问URL
                relative_path = f"test-images/product-images/{file_path.name}"
                access_url = f"http://localhost:8000/static/{relative_path}"
                
                test_images.append({
                    "filename": file_path.name,
                    "file_path": str(file_path),
                    "access_url": access_url,
                    "relative_path": relative_path,
                    "file_size": file_path.stat().st_size if file_path.exists() else 0
                })
                
                if len(test_images) >= limit:
                    break
        
        return test_images
    
    def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                return True
            return False
        except Exception:
            return False
    
    async def create_thumbnail(self, image_path: str, max_size: tuple = (300, 300)) -> Optional[str]:
        """创建缩略图"""
        try:
            source_path = Path(image_path)
            if not source_path.exists():
                return None
            
            # 生成缩略图文件名
            thumb_filename = f"thumb_{source_path.stem}{source_path.suffix}"
            thumb_path = source_path.parent / thumb_filename
            
            # 创建缩略图
            with Image.open(source_path) as img:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(thumb_path, optimize=True, quality=85)
            
            return str(thumb_path)
            
        except Exception:
            return None

# 创建全局实例
file_upload_service = FileUploadService() 