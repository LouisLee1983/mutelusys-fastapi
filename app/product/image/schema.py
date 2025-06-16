# -*- coding: utf-8 -*-
"""
商品图片数据结构定义
包含图片上传、管理相关的Schema定义
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.product.models import ImageType


class ImageUploadResponse(BaseModel):
    """图片/视频上传响应Schema"""
    file_name: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件相对路径")
    file_url: str = Field(..., description="文件访问URL")
    file_size: int = Field(..., description="文件大小(字节)")
    width: Optional[int] = Field(None, description="图片宽度/视频宽度(像素)")
    height: Optional[int] = Field(None, description="图片高度/视频高度(像素)")
    is_video: bool = Field(default=False, description="是否为视频文件")
    duration: Optional[int] = Field(None, description="视频时长(秒)")
    video_format: Optional[str] = Field(None, description="视频格式")


class ProductImageBase(BaseModel):
    """商品图片/视频基础Schema"""
    image_type: ImageType = Field(default=ImageType.GALLERY, description="媒体类型")
    alt_text: Optional[str] = Field(None, description="替代文本，用于SEO和无障碍访问")
    title: Optional[str] = Field(None, description="图片/视频标题")
    description: Optional[str] = Field(None, description="图片/视频描述")
    sort_order: int = Field(default=0, description="排序顺序")
    is_active: bool = Field(default=True, description="是否激活")


class ProductImageCreate(ProductImageBase):
    """创建商品图片/视频请求Schema"""
    image_url: str = Field(..., description="图片/视频URL")
    width: Optional[int] = Field(None, description="图片宽度/视频宽度(像素)")
    height: Optional[int] = Field(None, description="图片高度/视频高度(像素)")
    file_size: Optional[int] = Field(None, description="文件大小(KB)")
    # 视频特有字段
    duration: Optional[int] = Field(None, description="视频时长(秒)")
    thumbnail_url: Optional[str] = Field(None, description="视频缩略图URL")
    is_video: bool = Field(default=False, description="是否为视频文件")
    video_format: Optional[str] = Field(None, description="视频格式(mp4, webm等)")
    
    @validator('image_url')
    def validate_image_url(cls, v):
        if not v or not v.strip():
            raise ValueError('文件URL不能为空')
        return v.strip()


class ProductImageUpdate(BaseModel):
    """更新商品图片/视频请求Schema"""
    image_type: Optional[ImageType] = Field(None, description="媒体类型")
    alt_text: Optional[str] = Field(None, description="替代文本")
    title: Optional[str] = Field(None, description="图片/视频标题")
    description: Optional[str] = Field(None, description="图片/视频描述")
    sort_order: Optional[int] = Field(None, description="排序顺序")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ProductImageResponse(ProductImageBase):
    """商品图片/视频响应Schema"""
    id: UUID = Field(..., description="媒体ID")
    product_id: UUID = Field(..., description="商品ID")
    image_url: str = Field(..., description="图片/视频URL")
    width: Optional[int] = Field(None, description="图片宽度/视频宽度(像素)")
    height: Optional[int] = Field(None, description="图片高度/视频高度(像素)")
    file_size: Optional[int] = Field(None, description="文件大小(KB)")
    # 视频特有字段
    duration: Optional[int] = Field(None, description="视频时长(秒)")
    thumbnail_url: Optional[str] = Field(None, description="视频缩略图URL")
    is_video: bool = Field(default=False, description="是否为视频文件")
    video_format: Optional[str] = Field(None, description="视频格式(mp4, webm等)")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class ProductImageListResponse(BaseModel):
    """商品图片列表响应Schema"""
    images: List[ProductImageResponse] = Field(..., description="图片列表")
    total: int = Field(..., description="总数量")


class ImageBatchUpdateRequest(BaseModel):
    """批量更新图片排序请求Schema"""
    image_orders: List[dict] = Field(..., description="图片排序列表")
    
    @validator('image_orders')
    def validate_image_orders(cls, v):
        for item in v:
            if 'id' not in item or 'sort_order' not in item:
                raise ValueError('每个图片排序项必须包含id和sort_order字段')
        return v


class ImageDeleteResponse(BaseModel):
    """图片删除响应Schema"""
    success: bool = Field(..., description="删除是否成功")
    message: str = Field(..., description="删除结果消息")
    deleted_file_path: Optional[str] = Field(None, description="已删除的文件路径")
