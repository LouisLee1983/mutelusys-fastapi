import uuid
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


# 报表类型枚举
class ReportType(str, enum.Enum):
    DAILY = "daily"              # 日报
    WEEKLY = "weekly"            # 周报
    MONTHLY = "monthly"          # 月报
    QUARTERLY = "quarterly"      # 季报
    ANNUAL = "annual"            # 年报
    CUSTOM = "custom"            # 自定义时间范围


# 报表状态枚举
class ReportStatus(str, enum.Enum):
    PENDING = "pending"          # 待生成
    GENERATING = "generating"    # 生成中
    COMPLETED = "completed"      # 已完成
    FAILED = "failed"            # 生成失败
    EXPIRED = "expired"          # 已过期


# 分析维度类型枚举
class DimensionType(str, enum.Enum):
    TIME = "time"                # 时间维度
    PRODUCT = "product"          # 商品维度
    CATEGORY = "category"        # 分类维度
    CUSTOMER = "customer"        # 客户维度
    REGION = "region"            # 地区维度
    CHANNEL = "channel"          # 渠道维度
    INTENT = "intent"            # 意图维度
    SYMBOL = "symbol"            # 符号维度
    SCENE = "scene"              # 场景维度
    MATERIAL = "material"        # 材质维度
    THEME = "theme"              # 主题维度
    CUSTOM = "custom"            # 自定义维度


# 报表基类，包含所有报表共有的属性
class ReportBase(Base):
    """报表基类，用于继承"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, comment="报表标题")
    description = Column(String(500), nullable=True, comment="报表描述")
    report_type = Column(Enum(ReportType), nullable=False, default=ReportType.DAILY, comment="报表类型")
    status = Column(Enum(ReportStatus), nullable=False, default=ReportStatus.PENDING, comment="报表状态")
    start_date = Column(Date, nullable=False, comment="开始日期")
    end_date = Column(Date, nullable=False, comment="结束日期")
    dimensions = Column(ARRAY(String), nullable=True, comment="分析维度")
    filters = Column(JSONB, nullable=True, comment="筛选条件")
    data = Column(JSONB, nullable=True, comment="报表数据")
    file_url = Column(String(255), nullable=True, comment="报表文件URL")
    scheduled = Column(Boolean, default=False, comment="是否定期生成")
    schedule_config = Column(JSONB, nullable=True, comment="定时配置")
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# 用户行为类型枚举
class UserBehaviorType(str, enum.Enum):
    VIEW = "view"                # 浏览
    SEARCH = "search"            # 搜索
    CLICK = "click"              # 点击
    ADD_TO_CART = "add_to_cart"  # 加入购物车
    ADD_TO_WISHLIST = "add_to_wishlist"  # 加入收藏
    PURCHASE = "purchase"        # 购买
    SHARE = "share"              # 分享
    REVIEW = "review"            # 评论
    FILTER = "filter"            # 筛选
    SORT = "sort"                # 排序
    OTHER = "other"              # 其他行为


# 设备类型枚举
class DeviceType(str, enum.Enum):
    DESKTOP = "desktop"          # 桌面端
    MOBILE = "mobile"            # 手机端
    TABLET = "tablet"            # 平板
    APP = "app"                  # 应用程序
    OTHER = "other"              # 其他设备
