from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator

from app.content.media.models import MediaType, MediaCategory, MediaStatus


class MediaFolderCreate(BaseModel):
    """媒体文件夹创建模型"""
    name: str = Field(..., description="文件夹名称", example="产品图片")
    description: Optional[str] = Field(None, description="文件夹描述")
    parent_id: Optional[str] = Field(None, description="父文件夹ID")
    is_public: bool = Field(True, description="是否公开")


class MediaFolderUpdate(BaseModel):
    """媒体文件夹更新模型"""
    name: Optional[str] = Field(None, description="文件夹名称")
    description: Optional[str] = Field(None, description="文件夹描述")
    parent_id: Optional[str] = Field(None, description="父文件夹ID")
    is_public: Optional[bool] = Field(None, description="是否公开")


class MediaFolderResponse(BaseModel):
    """媒体文件夹响应模型"""
    id: str
    name: str
    description: Optional[str] = None
    parent_id: Optional[str] = None
    is_public: bool
    file_count: int
    total_size: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MediaFileCreate(BaseModel):
    """媒体文件创建模型"""
    filename: str = Field(..., description="原始文件名")
    file_path: str = Field(..., description="文件存储路径")
    file_url: str = Field(..., description="文件访问URL")
    file_size: int = Field(..., description="文件大小")
    mime_type: str = Field(..., description="MIME类型")
    media_type: MediaType = Field(..., description="媒体类型")
    category: MediaCategory = Field(MediaCategory.GENERAL, description="媒体分类")
    
    # 可选属性
    width: Optional[int] = Field(None, description="图片宽度")
    height: Optional[int] = Field(None, description="图片高度")
    duration: Optional[int] = Field(None, description="视频时长")
    title: Optional[str] = Field(None, description="媒体标题")
    description: Optional[str] = Field(None, description="媒体描述")
    alt_text: Optional[str] = Field(None, description="替代文本")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    is_public: bool = Field(True, description="是否公开访问")
    metadata: Optional[Dict[str, Any]] = Field(None, description="额外元数据")
    folder_ids: Optional[List[str]] = Field([], description="所属文件夹ID列表")


class MediaFileUpdate(BaseModel):
    """媒体文件更新模型"""
    title: Optional[str] = Field(None, description="媒体标题")
    description: Optional[str] = Field(None, description="媒体描述")
    alt_text: Optional[str] = Field(None, description="替代文本")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    category: Optional[MediaCategory] = Field(None, description="媒体分类")
    status: Optional[MediaStatus] = Field(None, description="媒体状态")
    is_public: Optional[bool] = Field(None, description="是否公开访问")
    metadata: Optional[Dict[str, Any]] = Field(None, description="额外元数据")
    folder_ids: Optional[List[str]] = Field(None, description="所属文件夹ID列表")


class MediaFileResponse(BaseModel):
    """媒体文件响应模型"""
    id: str
    filename: str
    stored_filename: str
    file_path: str
    file_url: str
    file_size: int
    mime_type: str
    media_type: MediaType
    category: MediaCategory
    
    # 媒体属性
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    
    # 元数据
    title: Optional[str] = None
    description: Optional[str] = None
    alt_text: Optional[str] = None
    tags: Optional[List[str]] = None
    
    # 状态
    status: MediaStatus
    is_public: bool
    
    # 统计
    download_count: int
    reference_count: int
    
    # 额外信息
    metadata: Optional[Dict[str, Any]] = None
    
    # 时间戳
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MediaFileListQuery(BaseModel):
    """媒体文件列表查询参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    media_type: Optional[MediaType] = Field(None, description="媒体类型筛选")
    category: Optional[MediaCategory] = Field(None, description="分类筛选")
    status: Optional[MediaStatus] = Field(None, description="状态筛选")
    folder_id: Optional[str] = Field(None, description="文件夹筛选")
    tags: Optional[List[str]] = Field(None, description="标签筛选")
    search: Optional[str] = Field(None, description="搜索关键词")
    is_public: Optional[bool] = Field(None, description="是否公开筛选")


class MediaFileListResponse(BaseModel):
    """媒体文件列表响应模型"""
    items: List[MediaFileResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class MediaFileBatchUpdate(BaseModel):
    """媒体文件批量更新模型"""
    file_ids: List[str] = Field(..., description="文件ID列表")
    category: Optional[MediaCategory] = Field(None, description="分类")
    status: Optional[MediaStatus] = Field(None, description="状态")
    tags: Optional[List[str]] = Field(None, description="标签")
    folder_ids: Optional[List[str]] = Field(None, description="文件夹ID列表")


class MediaUsageCreate(BaseModel):
    """媒体使用记录创建模型"""
    media_file_id: str = Field(..., description="媒体文件ID")
    reference_type: str = Field(..., description="引用类型")
    reference_id: str = Field(..., description="引用对象ID")
    field_name: Optional[str] = Field(None, description="字段名称")
    context: Optional[Dict[str, Any]] = Field(None, description="使用上下文")


class MediaUsageResponse(BaseModel):
    """媒体使用记录响应模型"""
    id: str
    media_file_id: str
    reference_type: str
    reference_id: str
    field_name: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MediaUploadResponse(BaseModel):
    """媒体上传响应模型"""
    file_id: str
    filename: str
    file_url: str
    file_size: int
    media_type: MediaType
    success: bool
    message: str


class MediaBatchUploadResponse(BaseModel):
    """媒体批量上传响应模型"""
    uploaded_files: List[MediaUploadResponse]
    total_uploaded: int
    total_failed: int
    success_rate: float


class MediaStatistics(BaseModel):
    """媒体统计模型"""
    total_files: int
    total_size: int
    files_by_type: Dict[str, int]
    files_by_category: Dict[str, int]
    total_folders: int
    public_files: int
    private_files: int


class MediaSearchQuery(BaseModel):
    """媒体搜索查询模型"""
    keyword: Optional[str] = Field(None, description="关键词")
    media_types: Optional[List[MediaType]] = Field(None, description="媒体类型")
    categories: Optional[List[MediaCategory]] = Field(None, description="分类")
    tags: Optional[List[str]] = Field(None, description="标签")
    size_range: Optional[Dict[str, int]] = Field(None, description="文件大小范围")
    date_range: Optional[Dict[str, datetime]] = Field(None, description="日期范围")
    sort_by: str = Field("created_at", description="排序字段")
    sort_order: str = Field("desc", description="排序方向")


class PublicMediaFileResponse(BaseModel):
    """公开媒体文件响应模型（前端使用）"""
    id: str
    filename: str
    file_url: str
    file_size: int
    media_type: MediaType
    category: MediaCategory
    width: Optional[int] = None
    height: Optional[int] = None
    title: Optional[str] = None
    alt_text: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True