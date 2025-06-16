import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


# 菜单项类型枚举
class MenuItemType(str, enum.Enum):
    LINK = "link"        # 链接
    PAGE = "page"        # 内部页面
    CATEGORY = "category"  # 商品分类
    CUSTOM = "custom"    # 自定义


class NavigationMenu(Base):
    """导航菜单表"""
    __tablename__ = "navigation_menus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="菜单名称")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="菜单代码，如'main_menu', 'footer_menu'")
    description = Column(String(255), nullable=True, comment="菜单描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    items = relationship("NavigationMenuItem", back_populates="menu", cascade="all, delete-orphan")


class NavigationMenuItem(Base):
    """导航菜单项表，支持多级和多语言"""
    __tablename__ = "navigation_menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("navigation_menus.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("navigation_menu_items.id"), nullable=True, comment="父菜单项ID")
    title = Column(String(100), nullable=False, comment="菜单项标题")
    type = Column(Enum(MenuItemType), nullable=False, default=MenuItemType.LINK, comment="菜单项类型")
    url = Column(String(255), nullable=True, comment="链接URL")
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id"), nullable=True, comment="关联页面ID")
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=True, comment="关联分类ID")
    icon = Column(String(100), nullable=True, comment="图标")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    is_active = Column(Boolean, default=True, comment="是否激活")
    open_in_new_tab = Column(Boolean, default=False, comment="是否在新标签页打开")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    menu = relationship("NavigationMenu", back_populates="items")
    parent = relationship("NavigationMenuItem", remote_side=[id], backref="children")
    translations = relationship("NavigationMenuItemTranslation", back_populates="menu_item", cascade="all, delete-orphan")
    

class NavigationMenuItemTranslation(Base):
    """导航菜单项多语言翻译表"""
    __tablename__ = "navigation_menu_item_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("navigation_menu_items.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    title = Column(String(100), nullable=False, comment="菜单项标题")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    menu_item = relationship("NavigationMenuItem", back_populates="translations")

    # 联合索引确保每个菜单项对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
