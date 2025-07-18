import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, BigInteger, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class MediaType(str, enum.Enum):
    """媒体类型枚举"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    OTHER = "other"


class MediaCategory(str, enum.Enum):
    """媒体分类枚举"""
    PRODUCT = "product"           # 产品图片
    BANNER = "banner"             # 横幅图片
    BLOG = "blog"                 # 博客图片
    CONTENT = "content"           # 内容图片
    AVATAR = "avatar"             # 头像
    LOGO = "logo"                 # 标志
    ICON = "icon"                 # 图标
    PROMOTION = "promotion"       # 促销相关
    GENERAL = "general"           # 通用媒体


class MediaStatus(str, enum.Enum):
    """媒体状态枚举"""
    ACTIVE = "active"             # 活跃
    ARCHIVED = "archived"         # 已归档
    DELETED = "deleted"           # 已删除


class MediaFile(Base):
    """媒体文件表"""
    __tablename__ = "media_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 文件基本信息
    filename = Column(String(255), nullable=False, comment="原始文件名")
    stored_filename = Column(String(255), nullable=False, comment="存储文件名")
    file_path = Column(String(500), nullable=False, comment="文件存储路径")
    file_url = Column(String(500), nullable=False, comment="文件访问URL")
    
    # 文件属性
    file_size = Column(BigInteger, nullable=False, comment="文件大小（字节）")
    mime_type = Column(String(100), nullable=False, comment="MIME类型")
    media_type = Column(Enum(MediaType), nullable=False, comment="媒体类型")
    category = Column(Enum(MediaCategory), nullable=False, default=MediaCategory.GENERAL, comment="媒体分类")
    
    # 图片特定属性
    width = Column(Integer, nullable=True, comment="图片宽度")
    height = Column(Integer, nullable=True, comment="图片高度")
    
    # 视频特定属性
    duration = Column(Integer, nullable=True, comment="视频时长（秒）")
    
    # 元数据
    title = Column(String(255), nullable=True, comment="媒体标题")
    description = Column(Text, nullable=True, comment="媒体描述")
    alt_text = Column(String(255), nullable=True, comment="替代文本")
    tags = Column(ARRAY(String), nullable=True, comment="标签列表")
    
    # 状态和权限
    status = Column(Enum(MediaStatus), nullable=False, default=MediaStatus.ACTIVE, comment="媒体状态")
    is_public = Column(Boolean, default=True, comment="是否公开访问")
    
    # 使用统计
    download_count = Column(Integer, default=0, comment="下载次数")
    reference_count = Column(Integer, default=0, comment="引用次数")
    
    # 额外信息
    metadata = Column(JSON, nullable=True, comment="额外元数据")
    
    # 审计字段
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="上传者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    folders = relationship("MediaFolder", secondary="media_file_folder", back_populates="files")


class MediaFolder(Base):
    """媒体文件夹表"""
    __tablename__ = "media_folders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="文件夹名称")
    description = Column(Text, nullable=True, comment="文件夹描述")
    parent_id = Column(UUID(as_uuid=True), ForeignKey("media_folders.id"), nullable=True, comment="父文件夹ID")
    
    # 权限设置
    is_public = Column(Boolean, default=True, comment="是否公开")
    
    # 统计信息
    file_count = Column(Integer, default=0, comment="文件数量")
    total_size = Column(BigInteger, default=0, comment="总大小")
    
    # 审计字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    parent = relationship("MediaFolder", remote_side=[id], back_populates="children")
    children = relationship("MediaFolder", back_populates="parent")
    files = relationship("MediaFile", secondary="media_file_folder", back_populates="folders")


# 媒体文件和文件夹的多对多关联表
from sqlalchemy import Table
media_file_folder = Table(
    "media_file_folder",
    Base.metadata,
    Column("file_id", UUID(as_uuid=True), ForeignKey("media_files.id", ondelete="CASCADE"), primary_key=True),
    Column("folder_id", UUID(as_uuid=True), ForeignKey("media_folders.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class MediaUsage(Base):
    """媒体使用记录表"""
    __tablename__ = "media_usage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    media_file_id = Column(UUID(as_uuid=True), ForeignKey("media_files.id", ondelete="CASCADE"), nullable=False)
    
    # 引用信息
    reference_type = Column(String(50), nullable=False, comment="引用类型：blog, banner, product等")
    reference_id = Column(UUID(as_uuid=True), nullable=False, comment="引用对象ID")
    field_name = Column(String(100), nullable=True, comment="字段名称")
    
    # 使用上下文
    context = Column(JSON, nullable=True, comment="使用上下文信息")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    media_file = relationship("MediaFile")


class MediaProcessingJob(Base):
    """媒体处理任务表"""
    __tablename__ = "media_processing_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    media_file_id = Column(UUID(as_uuid=True), ForeignKey("media_files.id", ondelete="CASCADE"), nullable=False)
    
    # 任务信息
    job_type = Column(String(50), nullable=False, comment="任务类型：resize, compress, format_convert等")
    parameters = Column(JSON, nullable=False, comment="处理参数")
    status = Column(String(20), nullable=False, default="pending", comment="任务状态：pending, processing, completed, failed")
    
    # 结果信息
    output_path = Column(String(500), nullable=True, comment="输出文件路径")
    error_message = Column(Text, nullable=True, comment="错误信息")
    
    # 时间信息
    started_at = Column(DateTime, nullable=True, comment="开始时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    media_file = relationship("MediaFile")