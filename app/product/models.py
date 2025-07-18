# -*- coding: utf-8 -*-
"""
商品核心模型定义
包含产品、分类、翻译等核心模型
"""
import uuid
import enum
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, Enum, JSON, Table, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProductStatus(str, enum.Enum):
    """商品状态枚举"""
    DRAFT = "draft"        # 草稿
    ACTIVE = "active"      # 上架
    INACTIVE = "inactive"  # 下架
    DELETED = "deleted"    # 已删除


class CategoryLevel(str, enum.Enum):
    """分类层级枚举"""
    LEVEL_1 = "level_1"    # 一级分类
    LEVEL_2 = "level_2"    # 二级分类
    LEVEL_3 = "level_3"    # 三级分类


# 多对多关系表定义，商品与标签
product_tag = Table(
    'product_tag',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('product_tags.id', ondelete="CASCADE"), primary_key=True)
)

# 多对多关系表定义，商品与场景
product_scene = Table(
    'product_scene',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('scene_id', UUID(as_uuid=True), ForeignKey('product_scenes.id', ondelete="CASCADE"), primary_key=True)
)

# 多对多关系表定义，商品与意图
product_intent = Table(
    'product_intent',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('intent_id', UUID(as_uuid=True), ForeignKey('product_intents.id', ondelete="CASCADE"), primary_key=True)
)

# 多对多关系表定义，商品与符号
product_symbol = Table(
    'product_symbol',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('symbol_id', UUID(as_uuid=True), ForeignKey('product_symbols.id', ondelete="CASCADE"), primary_key=True)
)

# 多对多关系表定义，商品与材质
product_material = Table(
    'product_material',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('material_id', UUID(as_uuid=True), ForeignKey('product_materials.id', ondelete="CASCADE"), primary_key=True)
)

# 多对多关系表定义，商品与主题
product_theme = Table(
    'product_theme',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('theme_id', UUID(as_uuid=True), ForeignKey('product_themes.id', ondelete="CASCADE"), primary_key=True)
)

# 多对多关系表定义，商品与目标群体
product_target_group = Table(
    'product_target_group',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('target_group_id', UUID(as_uuid=True), ForeignKey('product_target_groups.id', ondelete="CASCADE"), primary_key=True)
)

# 多对多关系表定义，商品与分类
product_category = Table(
    'product_category',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('product_categories.id', ondelete="CASCADE"), primary_key=True)
)

# SKU与属性值的多对多关联表
sku_attribute_value = Table(
    "sku_attribute_value",
    Base.metadata,
    Column("sku_id", UUID(as_uuid=True), ForeignKey("product_skus.id", ondelete="CASCADE"), primary_key=True),
    Column("attribute_value_id", UUID(as_uuid=True), ForeignKey("product_attribute_values.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)

# 套装与意图的多对多关联表
bundle_intent = Table(
    "bundle_intent",
    Base.metadata,
    Column("bundle_id", UUID(as_uuid=True), ForeignKey("product_bundles.id", ondelete="CASCADE"), primary_key=True),
    Column("intent_id", UUID(as_uuid=True), ForeignKey("product_intents.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)

# 套装与主题的多对多关联表
bundle_theme = Table(
    "bundle_theme",
    Base.metadata,
    Column("bundle_id", UUID(as_uuid=True), ForeignKey("product_bundles.id", ondelete="CASCADE"), primary_key=True),
    Column("theme_id", UUID(as_uuid=True), ForeignKey("product_themes.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
)


class Product(Base):
    """商品信息表，包括基本信息、状态、分类、多语言描述、SEO信息等"""
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku_code = Column(String(50), nullable=False, unique=True, index=True, comment="商品编码，唯一")
    sku_name = Column(String(255), nullable=True, comment="商品SKU外显名称，给消费者看的名称")
    name = Column(String(255), nullable=True, comment="商品名称")
    description = Column(Text, nullable=True, comment="商品描述")
    status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.DRAFT, comment="商品状态：草稿、上架、下架、已删除")
    weight = Column(Float, nullable=True, comment="商品重量(克)")
    width = Column(Float, nullable=True, comment="商品宽度(厘米)")
    height = Column(Float, nullable=True, comment="商品高度(厘米)")
    length = Column(Float, nullable=True, comment="商品长度(厘米)")
    is_featured = Column(Boolean, default=False, comment="是否推荐商品")
    is_new = Column(Boolean, default=True, comment="是否新品")
    is_bestseller = Column(Boolean, default=False, comment="是否畅销品")
    is_customizable = Column(Boolean, default=False, comment="是否支持定制")
    tax_class = Column(String(50), nullable=True, comment="税务类别")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    # 主图URL字段，用于快速展示，避免JOIN查询
    main_image_url = Column(String(512), nullable=True, comment="商品主图URL，用于列表展示和快速访问")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    meta_data = Column(JSON, nullable=True, comment="元数据，存储其他扩展信息")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    translations = relationship("ProductTranslation", back_populates="product", cascade="all, delete-orphan")
    
    # 一对多关系
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    prices = relationship("ProductPrice", back_populates="product", cascade="all, delete-orphan")
    skus = relationship("ProductSku", back_populates="product", cascade="all, delete-orphan")
    inventories = relationship("ProductInventory", back_populates="product", cascade="all, delete-orphan")
    
    # 多对多关系
    categories = relationship("ProductCategory", secondary=product_category, back_populates="products")
    tags = relationship("ProductTag", secondary=product_tag, back_populates="products")
    scenes = relationship("ProductScene", secondary=product_scene, back_populates="products")
    intents = relationship("ProductIntent", secondary=product_intent, back_populates="products")
    symbols = relationship("ProductSymbol", secondary=product_symbol, back_populates="products")
    materials = relationship("ProductMaterial", secondary=product_material, back_populates="products")
    themes = relationship("ProductTheme", secondary=product_theme, back_populates="products")
    target_groups = relationship("ProductTargetGroup", secondary=product_target_group, back_populates="products")
    # 文章关联关系 - 延迟导入避免循环依赖
    # articles = relationship("ProductArticle", secondary="product_article_associations", back_populates="products")


class ProductCategory(Base):
    """商品分类表，支持多级分类和多语言"""
    __tablename__ = "product_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="分类别名，用于URL")
    description = Column(Text, nullable=True, comment="分类描述")
    parent_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=True, comment="父分类ID")
    level = Column(Enum(CategoryLevel), nullable=False, default=CategoryLevel.LEVEL_1, comment="分类层级")
    image_url = Column(String(255), nullable=True, default="/static/uploads/category-hero-images/category-default-hero-image.jpg", comment="分类图片URL")
    icon_url = Column(String(255), nullable=True, default="/static/uploads/category-hero-images/category-default-icon.jpg", comment="分类图标URL")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐分类")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    parent = relationship("ProductCategory", remote_side=[id], backref="children")
    products = relationship("Product", secondary=product_category, back_populates="categories")
    translations = relationship("ProductCategoryTranslation", back_populates="category", cascade="all, delete-orphan")


class ProductTranslation(Base):
    """商品多语言翻译表，包括名称、描述、规格等"""
    __tablename__ = "product_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    name = Column(String(255), nullable=False, comment="商品名称")
    sku_name = Column(String(255), nullable=True, comment="商品SKU外显名称翻译")
    short_description = Column(Text, nullable=True, comment="商品简短描述")
    description = Column(Text, nullable=True, comment="商品详细描述")
    specifications = Column(Text, nullable=True, comment="商品规格")
    benefits = Column(Text, nullable=True, comment="商品好处/特点")
    instructions = Column(Text, nullable=True, comment="使用说明")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    product = relationship("Product", back_populates="translations")
    
    async def translate_to(self, target_language: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        将当前产品翻译记录翻译到目标语言
        
        Args:
            target_language: 目标语言代码 (如 en-US, th-TH)
            context: 翻译上下文
        
        Returns:
            翻译结果字典，包含所有翻译后的字段
        """
        from app.analytics.ai_copilot.alibaba_service import AlibabaBailianService
        
        service = AlibabaBailianService()
        
        # 准备需要翻译的文本
        texts_to_translate = {
            "name": self.name,
            "sku_name": self.sku_name or "",
            "short_description": self.short_description or "",
            "description": self.description or "",
            "specifications": self.specifications or "",
            "benefits": self.benefits or "",
            "instructions": self.instructions or "",
            "seo_title": self.seo_title or "",
            "seo_description": self.seo_description or "",
            "seo_keywords": self.seo_keywords or ""
        }
        
        # 构建翻译上下文
        translation_context = f"这是商品相关的内容翻译。商品名称是：{self.name}"
        if self.sku_name:
            translation_context += f"，SKU名称是：{self.sku_name}"
        if context:
            translation_context += f"。{context}"
        
        translated_results = {}
        
        # 逐个翻译字段
        for field_name, text in texts_to_translate.items():
            if text and text.strip():  # 只翻译非空字段
                try:
                    result = await service.translate_text(
                        source_text=text,
                        target_language=target_language,
                        source_language=self.language_code,
                        context=translation_context
                    )
                    
                    if result["success"]:
                        translated_results[field_name] = result["translated_text"]
                    else:
                        print(f"翻译字段 {field_name} 失败: {result.get('error')}")
                        translated_results[field_name] = text  # 保留原文
                        
                except Exception as e:
                    print(f"翻译字段 {field_name} 异常: {str(e)}")
                    translated_results[field_name] = text  # 保留原文
            else:
                translated_results[field_name] = text  # 空字段保持空
        
        return {
            "product_id": self.product_id,
            "language_code": target_language,
            "name": translated_results.get("name", ""),
            "sku_name": translated_results.get("sku_name", ""),
            "short_description": translated_results.get("short_description", ""),
            "description": translated_results.get("description", ""),
            "specifications": translated_results.get("specifications", ""),
            "benefits": translated_results.get("benefits", ""),
            "instructions": translated_results.get("instructions", ""),
            "seo_title": translated_results.get("seo_title", ""),
            "seo_description": translated_results.get("seo_description", ""),
            "seo_keywords": translated_results.get("seo_keywords", ""),
            "source_language": self.language_code,
            "translation_timestamp": datetime.utcnow().isoformat()
        }


class ProductCategoryTranslation(Base):
    """商品分类多语言翻译表"""
    __tablename__ = "product_category_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    name = Column(String(100), nullable=False, comment="分类名称")
    description = Column(Text, nullable=True, comment="分类描述")
    seo_title = Column(String(2048), nullable=True, comment="SEO标题")
    seo_description = Column(String(2048), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(2048), nullable=True, comment="SEO关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    category = relationship("ProductCategory", back_populates="translations")
    
    async def translate_to(self, target_language: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        将当前分类翻译记录翻译到目标语言
        
        Args:
            target_language: 目标语言代码 (如 en-US, th-TH)
            context: 翻译上下文
        
        Returns:
            翻译结果字典，包含所有翻译后的字段
        """
        from app.analytics.ai_copilot.alibaba_service import AlibabaBailianService
        
        service = AlibabaBailianService()
        
        # 准备需要翻译的文本
        texts_to_translate = {
            "name": self.name,
            "description": self.description or "",
            "seo_title": self.seo_title or "",
            "seo_description": self.seo_description or "",
            "seo_keywords": self.seo_keywords or ""
        }
        
        # 构建翻译上下文
        translation_context = f"这是商品分类相关的内容翻译。分类名称是：{self.name}"
        if context:
            translation_context += f"。{context}"
        
        translated_results = {}
        
        # 逐个翻译字段
        for field_name, text in texts_to_translate.items():
            if text and text.strip():  # 只翻译非空字段
                try:
                    result = await service.translate_text(
                        source_text=text,
                        target_language=target_language,
                        source_language=self.language_code,
                        context=translation_context
                    )
                    
                    if result["success"]:
                        translated_results[field_name] = result["translated_text"]
                    else:
                        print(f"翻译字段 {field_name} 失败: {result.get('error')}")
                        translated_results[field_name] = text  # 保留原文
                        
                except Exception as e:
                    print(f"翻译字段 {field_name} 异常: {str(e)}")
                    translated_results[field_name] = text  # 保留原文
            else:
                translated_results[field_name] = text  # 空字段保持空
        
        return {
            "category_id": self.category_id,
            "language_code": target_language,
            "name": translated_results.get("name", ""),
            "description": translated_results.get("description", ""),
            "seo_title": translated_results.get("seo_title", ""),
            "seo_description": translated_results.get("seo_description", ""),
            "seo_keywords": translated_results.get("seo_keywords", ""),
            "source_language": self.language_code,
            "translation_timestamp": datetime.utcnow().isoformat()
        }


# ==================== 枚举类型定义 ====================

class MaterialType(str, enum.Enum):
    GEMSTONE = "gemstone"        # 宝石类
    CRYSTAL = "crystal"          # 水晶类
    WOOD = "wood"                # 木材类
    METAL = "metal"              # 金属类
    FABRIC = "fabric"            # 布料类
    CERAMIC = "ceramic"          # 陶瓷类
    STONE = "stone"              # 石材类
    BAMBOO = "bamboo"            # 竹材类
    OTHER = "other"              # 其他材质


class GenderType(str, enum.Enum):
    MALE = "male"              # 男性
    FEMALE = "female"          # 女性
    UNISEX = "unisex"          # 中性/通用


class AgeGroup(str, enum.Enum):
    CHILD = "child"            # 儿童
    TEEN = "teen"              # 青少年
    ADULT = "adult"            # 成人
    SENIOR = "senior"          # 老年人
    ALL = "all"                # 所有年龄段


class InventoryOperation(str, enum.Enum):
    PURCHASE = "purchase"        # 采购入库
    SALE = "sale"                # 销售出库
    RETURN = "return"            # 退货入库
    ADJUSTMENT = "adjustment"    # 库存调整
    DAMAGE = "damage"            # 损坏报废
    TRANSFER = "transfer"        # 仓库调拨


class AttributeType(str, enum.Enum):
    TEXT = "text"                # 文本类型
    SELECT = "select"            # 单选类型
    MULTISELECT = "multiselect"  # 多选类型
    BOOLEAN = "boolean"          # 布尔类型
    DATE = "date"                # 日期类型
    NUMBER = "number"            # 数字类型
    COLOR = "color"              # 颜色类型


# ==================== 商品相关模型 ====================

class ProductPrice(Base):
    """商品多币种价格设置，包括原价、销售价、特价"""
    __tablename__ = "product_prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)
    currency_code = Column(String(3), nullable=False,
                           comment="货币代码，如USD, SGD, MYR")
    regular_price = Column(Float, nullable=False, comment="原始价格")
    sale_price = Column(Float, nullable=True, comment="销售价格")
    discount_percentage = Column(Float, nullable=True, comment="折扣百分比")
    special_price = Column(Float, nullable=True, comment="特价")
    special_price_start_date = Column(Date, nullable=True, comment="特价开始日期")
    special_price_end_date = Column(Date, nullable=True, comment="特价结束日期")
    min_quantity = Column(Integer, default=1, comment="最小购买数量")
    is_default = Column(Boolean, default=False, comment="是否为默认币种价格")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    product = relationship("Product", back_populates="prices")


class ImageType(str, enum.Enum):
    MAIN = "main"               # 主图
    GALLERY = "gallery"         # 轮播展示图
    DETAIL = "detail"           # 详情图
    BANNER = "banner"           # 海报大图
    THUMBNAIL = "thumbnail"     # 缩略图
    VIDEO = "video"             # 产品视频


class ProductImage(Base):
    """商品图片表，支持多图排序和图片属性（现已扩展支持视频）"""
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False, comment="图片/视频URL")
    image_type = Column(Enum(ImageType), nullable=False,
                        default=ImageType.GALLERY, comment="媒体类型")
    alt_text = Column(String(255), nullable=True, comment="替代文本，用于SEO和无障碍访问")
    title = Column(String(255), nullable=True, comment="图片/视频标题")
    description = Column(Text, nullable=True, comment="图片/视频描述")
    width = Column(Integer, nullable=True, comment="图片宽度/视频宽度(像素)")
    height = Column(Integer, nullable=True, comment="图片高度/视频高度(像素)")
    file_size = Column(Integer, nullable=True, comment="文件大小(KB)")
    # 视频特有字段
    duration = Column(Integer, nullable=True, comment="视频时长(秒)")
    thumbnail_url = Column(String(255), nullable=True, comment="视频缩略图URL")
    is_video = Column(Boolean, default=False, comment="是否为视频文件")
    video_format = Column(String(10), nullable=True, comment="视频格式(mp4, webm等)")
    # 原有字段
    sort_order = Column(Integer, default=0, comment="排序顺序")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    product = relationship("Product", back_populates="images")


class ProductAttribute(Base):
    """商品属性表，定义属性类型和配置"""
    __tablename__ = "product_attributes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="属性名称")
    code = Column(String(50), nullable=False, unique=True,
                  index=True, comment="属性代码，如color, size")
    description = Column(Text, nullable=True, comment="属性描述")
    type = Column(Enum(AttributeType), nullable=False,
                  default=AttributeType.SELECT, comment="属性类型")
    display_order = Column(Integer, default=0, comment="显示顺序")
    is_required = Column(Boolean, default=False, comment="是否必填")
    is_configurable = Column(Boolean, default=True, comment="是否用于配置SKU的属性")
    is_searchable = Column(Boolean, default=False, comment="是否可搜索")
    is_comparable = Column(Boolean, default=False, comment="是否可比较")
    is_filterable = Column(Boolean, default=True, comment="是否可筛选")
    is_visible_on_frontend = Column(Boolean, default=True, comment="是否在前端可见")
    configuration = Column(JSON, nullable=True, comment="属性配置信息，如验证规则")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    values = relationship("ProductAttributeValue",
                          back_populates="attribute", cascade="all, delete-orphan")


class ProductAttributeValue(Base):
    """商品属性值表，存储预定义的属性值"""
    __tablename__ = "product_attribute_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attribute_id = Column(UUID(as_uuid=True), ForeignKey(
        "product_attributes.id", ondelete="CASCADE"), nullable=False)
    value = Column(String(255), nullable=False, comment="属性值")
    label = Column(String(255), nullable=True, comment="显示标签")
    color_code = Column(String(30), nullable=True, comment="颜色代码，当类型为颜色时使用")
    image_url = Column(String(255), nullable=True, comment="图片URL，如颜色样式图")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    attribute = relationship("ProductAttribute", back_populates="values")
    skus = relationship(
        "ProductSku", secondary="sku_attribute_value", back_populates="attribute_values")


# ==================== SKU 相关模型 ====================

class ProductSku(Base):
    """商品SKU表，关联属性组合和库存"""
    __tablename__ = "product_skus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sku_code = Column(String(50), nullable=False, unique=True, index=True, comment="SKU编码，唯一，内部使用")
    sku_name = Column(String(255), nullable=True, comment="SKU外显名称，给消费者看的名称")
    barcode = Column(String(50), nullable=True, comment="条形码")
    image_url = Column(String(255), nullable=True, comment="SKU特定图片URL")
    price_adjustment = Column(Float, default=0, comment="相对于基础价格的调整，可正可负")
    weight_adjustment = Column(Float, default=0, comment="相对于基础重量的调整，可正可负")
    width_adjustment = Column(Float, default=0, comment="相对于基础宽度的调整，可正可负")
    height_adjustment = Column(Float, default=0, comment="相对于基础高度的调整，可正可负")
    length_adjustment = Column(Float, default=0, comment="相对于基础长度的调整，可正可负")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_default = Column(Boolean, default=False, comment="是否为默认SKU")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    # 简化的库存管理字段
    stock_quantity = Column(Integer, default=0, nullable=False, comment="当前库存数量")
    low_stock_threshold = Column(Integer, default=10, nullable=False, comment="低库存预警值")
    meta_data = Column(JSON, nullable=True, comment="元数据，存储其他扩展信息")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    product = relationship("Product", back_populates="skus")
    attribute_values = relationship("ProductAttributeValue", secondary=sku_attribute_value, back_populates="skus")
    inventories = relationship("ProductInventory", back_populates="sku", cascade="all, delete-orphan")
    translations = relationship("ProductSkuTranslation", back_populates="sku", cascade="all, delete-orphan")
    
    # 计算属性
    @property
    def is_low_stock(self):
        """是否低库存"""
        return self.stock_quantity <= self.low_stock_threshold
    
    @property
    def is_out_of_stock(self):
        """是否缺货"""
        return self.stock_quantity <= 0


class ProductSkuTranslation(Base):
    """商品SKU多语言翻译表"""
    __tablename__ = "product_sku_translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku_id = Column(UUID(as_uuid=True), ForeignKey("product_skus.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String(10), nullable=False, comment="语言代码，如en-US, zh-CN")
    sku_name = Column(String(255), nullable=False, comment="SKU外显名称翻译")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    sku = relationship("ProductSku", back_populates="translations")
    
    async def translate_to(self, target_language: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        将当前SKU翻译记录翻译到目标语言
        
        Args:
            target_language: 目标语言代码 (如 en-US, th-TH)
            context: 翻译上下文
        
        Returns:
            翻译结果字典，包含翻译后的字段
        """
        from app.analytics.ai_copilot.alibaba_service import AlibabaBailianService
        
        service = AlibabaBailianService()
        
        # 构建翻译上下文
        translation_context = f"这是商品SKU名称翻译。SKU名称是：{self.sku_name}"
        if context:
            translation_context += f"。{context}"
        
        try:
            result = await service.translate_text(
                source_text=self.sku_name,
                target_language=target_language,
                source_language=self.language_code,
                context=translation_context
            )
            
            if result["success"]:
                translated_sku_name = result["translated_text"]
            else:
                print(f"翻译SKU名称失败: {result.get('error')}")
                translated_sku_name = self.sku_name  # 保留原文
                
        except Exception as e:
            print(f"翻译SKU名称异常: {str(e)}")
            translated_sku_name = self.sku_name  # 保留原文
        
        return {
            "sku_id": self.sku_id,
            "language_code": target_language,
            "sku_name": translated_sku_name,
            "source_language": self.language_code,
            "translation_timestamp": datetime.utcnow().isoformat()
        }


# ==================== 库存相关模型 ====================

class ProductInventory(Base):
    """商品库存表，包括可用库存、预警值、库存变更记录等"""
    __tablename__ = "product_inventories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sku_id = Column(UUID(as_uuid=True), ForeignKey("product_skus.id", ondelete="CASCADE"), nullable=True)
    quantity = Column(Integer, default=0, nullable=False, comment="可用库存数量")
    reserved_quantity = Column(Integer, default=0, nullable=False, comment="已预留数量（已下单未发货）")
    alert_threshold = Column(Integer, nullable=True, comment="库存预警阈值")
    ideal_quantity = Column(Integer, nullable=True, comment="理想库存量")
    reorder_point = Column(Integer, nullable=True, comment="重新订货点")
    reorder_quantity = Column(Integer, nullable=True, comment="重新订货数量")
    is_in_stock = Column(Boolean, default=True, comment="是否有库存")
    is_managed = Column(Boolean, default=True, comment="是否进行库存管理")
    location = Column(String(50), nullable=True, comment="库存位置编码")
    notes = Column(Text, nullable=True, comment="备注信息")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    product = relationship("Product", back_populates="inventories")
    sku = relationship("ProductSku", back_populates="inventories")
    history = relationship("InventoryHistory", back_populates="inventory", cascade="all, delete-orphan")


class InventoryHistory(Base):
    """库存变更历史记录表"""
    __tablename__ = "inventory_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("product_inventories.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)
    operation = Column(Enum(InventoryOperation), nullable=False, comment="操作类型")
    quantity = Column(Integer, nullable=False, comment="变更数量，正为增加，负为减少")
    previous_quantity = Column(Integer, nullable=False, comment="变更前数量")
    current_quantity = Column(Integer, nullable=False, comment="变更后数量")
    operator_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reference_number = Column(String(50), nullable=True, comment="参考单号，如采购单、销售单")
    notes = Column(Text, nullable=True, comment="备注信息")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    inventory = relationship("ProductInventory", back_populates="history")


# ==================== 标签相关模型 ====================

class ProductTag(Base):
    """商品标签表，用于筛选和推荐"""
    __tablename__ = "product_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="标签名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="标签别名，用于URL")
    description = Column(Text, nullable=True, comment="标签描述")
    icon_url = Column(String(255), nullable=True, comment="标签图标URL")
    color = Column(String(30), nullable=True, comment="标签颜色代码，如#FF5733")
    is_active = Column(Boolean, default=True, comment="是否激活")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 多对多关系
    products = relationship("Product", secondary=product_tag, back_populates="tags")


# ==================== 场景相关模型 ====================

class ProductScene(Base):
    """商品场景关联表，定义产品适用的生活场景（冥想、瑜伽、家居装饰等）"""
    __tablename__ = "product_scenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="场景名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="场景别名，用于URL")
    description = Column(Text, nullable=True, comment="场景描述")
    icon_url = Column(String(255), nullable=True, comment="场景图标URL")
    banner_url = Column(String(255), nullable=True, comment="场景横幅图片URL")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐场景")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 多对多关系
    products = relationship("Product", secondary=product_scene, back_populates="scenes")
    # interested_customers = relationship("Customer", secondary="customer_scene_preference", back_populates="scene_preferences")  # 暂时注释，等Customer模型定义后再启用


# ==================== 意图相关模型 ====================

class ProductIntent(Base):
    """商品意图分类，如保护、财富、爱情、平衡等精神和生活意图"""
    __tablename__ = "product_intents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="意图名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="意图别名，用于URL")
    description = Column(Text, nullable=True, comment="意图描述")
    icon_url = Column(String(255), nullable=True, comment="意图图标URL")
    banner_url = Column(String(255), nullable=True, comment="意图横幅图片URL")
    color_code = Column(String(30), nullable=True, comment="意图颜色代码")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐意图")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    cultural_significance = Column(Text, nullable=True, comment="文化意义")
    spiritual_meaning = Column(Text, nullable=True, comment="精神含义")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 多对多关系
    products = relationship("Product", secondary=product_intent, back_populates="intents")
    bundles = relationship("ProductBundle", secondary=bundle_intent, back_populates="intents")
    # customers = relationship("Customer", secondary="customer_intent", back_populates="intents")  # 暂时注释，等Customer模型定义后再启用


# ==================== 符号相关模型 ====================

class ProductSymbol(Base):
    """商品符号关联，如莲花、佛像、龙等文化符号及其意义"""
    __tablename__ = "product_symbols"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="符号名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="符号别名，用于URL")
    description = Column(Text, nullable=True, comment="符号描述")
    icon_url = Column(String(255), nullable=True, comment="符号图标URL")
    image_url = Column(String(255), nullable=True, comment="符号图片URL")
    cultural_meaning = Column(Text, nullable=True, comment="文化含义")
    spiritual_significance = Column(Text, nullable=True, comment="精神意义")
    origin = Column(Text, nullable=True, comment="起源和历史")
    usage_guide = Column(Text, nullable=True, comment="使用指南")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐符号")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 多对多关系
    products = relationship("Product", secondary=product_symbol, back_populates="symbols")
    # interested_customers = relationship("Customer", secondary="customer_cultural_preference", back_populates="cultural_preferences")  # 暂时注释，等Customer模型定义后再启用


# ==================== 材质相关模型 ====================

class ProductMaterial(Base):
    """材质详细分类，特别是宝石（翡翠、黑曜石、虎眼石等）和珍贵木材类型"""
    __tablename__ = "product_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="材质名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="材质别名，用于URL")
    material_type = Column(Enum(MaterialType), nullable=False, default=MaterialType.OTHER, comment="材质类型")
    description = Column(Text, nullable=True, comment="材质描述")
    icon_url = Column(String(255), nullable=True, comment="材质图标URL")
    image_url = Column(String(255), nullable=True, comment="材质图片URL")
    parent_id = Column(UUID(as_uuid=True), ForeignKey("product_materials.id"), nullable=True, comment="父材质ID")
    properties = Column(Text, nullable=True, comment="材质特性")
    origin_locations = Column(Text, nullable=True, comment="原产地")
    care_instructions = Column(Text, nullable=True, comment="保养说明")
    cultural_significance = Column(Text, nullable=True, comment="文化意义")
    energy_properties = Column(Text, nullable=True, comment="能量属性（针对宝石、水晶等）")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐材质")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 多对多关系
    products = relationship("Product", secondary=product_material, back_populates="materials")
    
    # 关联关系
    parent = relationship("ProductMaterial", remote_side=[id], backref="children")


# ==================== 主题相关模型 ====================

class ProductTheme(Base):
    """主题系列，如年度主题（生肖年）、节日主题、文化主题系列"""
    __tablename__ = "product_themes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="主题名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="主题别名，用于URL")
    description = Column(Text, nullable=True, comment="主题描述")
    icon_url = Column(String(255), nullable=True, comment="主题图标URL")
    banner_url = Column(String(255), nullable=True, comment="主题横幅图片URL")
    background_color = Column(String(30), nullable=True, comment="主题背景颜色代码")
    text_color = Column(String(30), nullable=True, comment="主题文本颜色代码")
    start_date = Column(Date, nullable=True, comment="主题开始日期")
    end_date = Column(Date, nullable=True, comment="主题结束日期")
    is_seasonal = Column(Boolean, default=False, comment="是否季节性主题")
    is_cultural = Column(Boolean, default=False, comment="是否文化相关主题")
    is_yearly = Column(Boolean, default=False, comment="是否年度主题")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐主题")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    cultural_significance = Column(Text, nullable=True, comment="文化意义")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 多对多关系
    products = relationship("Product", secondary=product_theme, back_populates="themes")
    bundles = relationship("ProductBundle", secondary=bundle_theme, back_populates="themes")


# ==================== 目标群体相关模型 ====================

class ProductTargetGroup(Base):
    """目标人群分类，如男性、女性、情侣、儿童等特定人群"""
    __tablename__ = "product_target_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="目标人群名称")
    slug = Column(String(100), nullable=False, unique=True, index=True, comment="目标人群别名，用于URL")
    description = Column(Text, nullable=True, comment="目标人群描述")
    icon_url = Column(String(255), nullable=True, comment="目标人群图标URL")
    gender = Column(Enum(GenderType), nullable=True, comment="性别类型")
    age_group = Column(Enum(AgeGroup), nullable=True, comment="年龄段")
    is_couple = Column(Boolean, default=False, comment="是否情侣/伴侣群体")
    is_family = Column(Boolean, default=False, comment="是否家庭群体")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐目标人群")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    buying_preferences = Column(Text, nullable=True, comment="购买偏好")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 多对多关系
    products = relationship("Product", secondary=product_target_group, back_populates="target_groups")


# ==================== 套装相关模型 ====================

class ProductBundle(Base):
    """产品套装/组合，支持多个相关产品打包销售"""
    __tablename__ = "product_bundles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, comment="套装名称")
    slug = Column(String(255), nullable=False, unique=True, index=True, comment="套装别名，用于URL")
    description = Column(Text, nullable=True, comment="套装描述")
    short_description = Column(Text, nullable=True, comment="简短描述")
    image_url = Column(String(255), nullable=True, comment="套装主图URL")
    sku_code = Column(String(50), nullable=False, unique=True, index=True, comment="套装SKU编码")
    discount_type = Column(String(20), nullable=True, comment="折扣类型：percentage, fixed_amount")
    discount_value = Column(Float, nullable=True, comment="折扣值")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_featured = Column(Boolean, default=False, comment="是否推荐套装")
    start_date = Column(DateTime, nullable=True, comment="套装开始日期")
    end_date = Column(DateTime, nullable=True, comment="套装结束日期")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    seo_title = Column(String(255), nullable=True, comment="SEO标题")
    seo_description = Column(String(500), nullable=True, comment="SEO描述")
    seo_keywords = Column(String(255), nullable=True, comment="SEO关键词")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    items = relationship("BundleItem", back_populates="bundle", cascade="all, delete-orphan")
    
    # 多对多关系
    intents = relationship("ProductIntent", secondary=bundle_intent, back_populates="bundles")
    themes = relationship("ProductTheme", secondary=bundle_theme, back_populates="bundles")


class BundleItem(Base):
    """套装项目表，关联套装与商品"""
    __tablename__ = "bundle_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bundle_id = Column(UUID(as_uuid=True), ForeignKey("product_bundles.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sku_id = Column(UUID(as_uuid=True), ForeignKey("product_skus.id", ondelete="SET NULL"), nullable=True)
    quantity = Column(Integer, default=1, nullable=False, comment="数量")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    discount_type = Column(String(20), nullable=True, comment="单品折扣类型：percentage, fixed_amount")
    discount_value = Column(Float, nullable=True, comment="单品折扣值")
    is_mandatory = Column(Boolean, default=True, comment="是否必选项")
    description = Column(Text, nullable=True, comment="说明")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联关系
    bundle = relationship("ProductBundle", back_populates="items")
    product = relationship("Product")
    sku = relationship("ProductSku")


# ==================== 简化的库存日志模型 ====================

class StockLog(Base):
    """库存变动日志表，记录所有库存变动历史"""
    __tablename__ = "stock_logs"
    
    id = Column(Integer, primary_key=True)
    sku_id = Column(UUID(as_uuid=True), ForeignKey('product_skus.id', ondelete="CASCADE"), nullable=False)
    
    # 核心信息
    change_type = Column(String(20), nullable=False, comment="变动类型：in(入库), out(出库), order(订单), cancel(取消), adjust(调整), return(退货)")
    quantity = Column(Integer, nullable=False, comment="变动数量(正数增加,负数减少)")
    balance = Column(Integer, nullable=False, comment="变动后余额")
    
    # 关联信息
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id', ondelete="SET NULL"), nullable=True, comment="关联的订单ID")
    remark = Column(String(200), nullable=True, comment="备注")
    
    # 记录信息
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String(50), nullable=True, comment="操作人名称")
    
    # 关联关系
    sku = relationship("ProductSku")
