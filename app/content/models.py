import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


# 内容状态枚举
class ContentStatus(str, enum.Enum):
    DRAFT = "draft"        # 草稿
    PUBLISHED = "published"  # 已发布
    ARCHIVED = "archived"  # 已归档
    DELETED = "deleted"    # 已删除


# 内容类型枚举
class ContentType(str, enum.Enum):
    PAGE = "page"              # 页面
    BLOG = "blog"              # 博客
    BANNER = "banner"          # 横幅
    FAQ = "faq"                # 常见问题
    CULTURAL_STORY = "cultural_story"  # 文化故事
    SYMBOL_DICTIONARY = "symbol_dictionary"  # 符号词典
    MATERIAL_GUIDE = "material_guide"  # 材质指南
    MEDITATION_GUIDE = "meditation_guide"  # 冥想指南
    INTENTION_GUIDE = "intention_guide"  # 意图使用指南
    CULTURAL_CALENDAR = "cultural_calendar"  # 文化日历
    SCENE_BASED = "scene_based"  # 基于场景的内容
