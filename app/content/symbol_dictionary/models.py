import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, Float, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base
from app.content.models import ContentStatus


# 符号类型枚举
class SymbolType(str, enum.Enum):
    RELIGIOUS = "religious"    # 宗教符号
    SPIRITUAL = "spiritual"    # 精神符号
    CULTURAL = "cultural"      # 文化符号
    ZODIAC = "zodiac"          # 生肖符号
    MYTHOLOGICAL = "mythological"  # 神话符号
    NATURAL = "natural"        # 自然符号
    GEOMETRIC = "geometric"    # 几何符号
    ANIMAL = "animal"          # 动物符号
    PLANT = "plant"            # 植物符号
    OTHER = "other"            # 其他符号


class SymbolDictionary(Base):
    """符号词典表，解释各类符号和图案的文化意义"""
    __tablename__ = "symbol_dictionaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="符号名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="符号别名，用于URL")
    description = Column(Text, nullable=False, comment="符号描述和意义")
    symbol_type = Column(Enum(SymbolType), nullable=False, comment="符号类型")
    origin = Column(String(100), nullable=True, comment="符号起源")
    cultural_significance = Column(Text, nullable=True, comment="文化意义")
    spiritual_meaning = Column(Text, nullable=True, comment="精神含义")
    image_url = Column(String(255), nullable=True, comment="符号图片URL")
    additional_images = Column(ARRAY(String), nullable=True, comment="额外图片URL数组")
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.PUBLISHED, comment="状态")
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    view_count = Column(Integer, default=0, comment="浏览次数")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    related_product_symbol_id = Column(UUID(as_uuid=True), ForeignKey("product_symbols.id"), nullable=True, comment="关联的产品符号ID")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="创建者ID")
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("SymbolDictionaryTranslation", back_populates="symbol", cascade="all, delete-orphan")
    related_product_symbol = relationship("ProductSymbol", backref="dictionary_entries")


class SymbolDictionaryTranslation(Base):
    """符号词典多语言翻译表"""
    __tablename__ = "symbol_dictionary_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol_id = Column(UUID(as_uuid=True), ForeignKey("symbol_dictionaries.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    name = Column(String(100), nullable=False, comment="符号名称")
    description = Column(Text, nullable=False, comment="符号描述和意义")
    origin = Column(String(100), nullable=True, comment="符号起源")
    cultural_significance = Column(Text, nullable=True, comment="文化意义")
    spiritual_meaning = Column(Text, nullable=True, comment="精神含义")
    meta_title = Column(String(255), nullable=True, comment="Meta标题")
    meta_description = Column(String(500), nullable=True, comment="Meta描述")
    meta_keywords = Column(String(255), nullable=True, comment="Meta关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    symbol = relationship("SymbolDictionary", back_populates="translations")

    # 联合索引确保每个符号对每种语言只有一个翻译
    __table_args__ = (
        {},
    )
