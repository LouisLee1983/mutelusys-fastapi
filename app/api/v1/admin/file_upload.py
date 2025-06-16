#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件上传API路由
"""

from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse

from app.core.file_upload import file_upload_service

router = APIRouter()

@router.post("/upload-image", summary="上传单个商品图片", tags=["文件上传"])
async def upload_image(
    file: UploadFile = File(..., description="要上传的图片文件")
):
    """上传单个商品图片"""
    try:
        result = await file_upload_service.upload_product_image(file)
        return {
            "code": 200,
            "message": "图片上传成功",
            "data": result
        }
    except HTTPException as e:
        return {
            "code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"图片上传失败: {str(e)}",
            "data": None
        }

@router.post("/upload-images", summary="批量上传商品图片", tags=["文件上传"])
async def upload_images(
    files: List[UploadFile] = File(..., description="要上传的图片文件列表")
):
    """批量上传商品图片"""
    try:
        if len(files) > 10:
            return {
                "code": 400,
                "message": "最多只能同时上传10张图片",
                "data": None
            }
        
        result = await file_upload_service.upload_multiple_images(files)
        return {
            "code": 200,
            "message": f"成功上传 {result['uploaded_count']} 张图片",
            "data": result
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"批量上传失败: {str(e)}",
            "data": None
        }

@router.get("/test-images", summary="获取测试用商品图片", tags=["文件上传"])
async def get_test_images(
    limit: int = Query(5, ge=1, le=20, description="返回图片数量限制")
):
    """获取测试用的商品图片"""
    try:
        images = file_upload_service.get_test_images(limit)
        return {
            "code": 200,
            "message": "获取测试图片成功",
            "data": {
                "total": len(images),
                "images": images
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取测试图片失败: {str(e)}",
            "data": None
        }

@router.delete("/delete-file", summary="删除上传的文件", tags=["文件上传"])
async def delete_file(
    file_path: str = Query(..., description="要删除的文件路径")
):
    """删除上传的文件"""
    try:
        success = file_upload_service.delete_file(file_path)
        if success:
            return {
                "code": 200,
                "message": "文件删除成功",
                "data": {"success": True}
            }
        else:
            return {
                "code": 404,
                "message": "文件不存在或删除失败",
                "data": {"success": False}
            }
    except Exception as e:
        return {
            "code": 500,
            "message": f"删除文件失败: {str(e)}",
            "data": None
        } 