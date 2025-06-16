#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品复制脚本
复制指定商品及其所有关联数据（SKU、图片、翻译、价格、库存等）
并将新商品与所有活跃分类建立关联
"""

import sys
import os
import uuid
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.product.models import (
    Product, ProductSku, ProductImage, ProductTranslation, 
    ProductPrice, ProductInventory, ProductCategory,
    product_category, product_tag, product_scene, 
    product_intent, product_symbol, product_material,
    product_theme, product_target_group, sku_attribute_value
)


def copy_product_data(db, original_product_id: str, copies_count: int = 4):
    """
    复制商品数据并与所有活跃分类建立关联
    
    Args:
        db: 数据库会话
        original_product_id: 原始商品UUID
        copies_count: 复制数量，默认4个
    """
    try:
        # 转换UUID
        original_uuid = uuid.UUID(original_product_id)
        
        # 查找原始商品
        original_product = db.query(Product).filter(Product.id == original_uuid).first()
        if not original_product:
            print(f"❌ 未找到商品 ID: {original_product_id}")
            return False
            
        print(f"📦 找到原始商品: {original_product.name} (SKU: {original_product.sku_code})")
        
        # 获取原始商品的所有关联数据
        original_skus = db.query(ProductSku).filter(ProductSku.product_id == original_uuid).all()
        original_images = db.query(ProductImage).filter(ProductImage.product_id == original_uuid).all()
        original_translations = db.query(ProductTranslation).filter(ProductTranslation.product_id == original_uuid).all()
        original_prices = db.query(ProductPrice).filter(ProductPrice.product_id == original_uuid).all()
        original_inventories = db.query(ProductInventory).filter(ProductInventory.product_id == original_uuid).all()
        
        # 获取多对多关系数据
        original_tags = original_product.tags
        original_scenes = original_product.scenes
        original_intents = original_product.intents
        original_symbols = original_product.symbols
        original_materials = original_product.materials
        original_themes = original_product.themes
        original_target_groups = original_product.target_groups
        
        # 获取所有活跃分类，用于关联新商品
        all_categories = db.query(ProductCategory).filter(ProductCategory.is_active == True).all()
        
        print(f"📊 原始商品数据统计:")
        print(f"   - SKU数量: {len(original_skus)}")
        print(f"   - 图片数量: {len(original_images)}")
        print(f"   - 翻译数量: {len(original_translations)}")
        print(f"   - 价格数量: {len(original_prices)}")
        print(f"   - 库存记录: {len(original_inventories)}")
        print(f"   - 标签数量: {len(original_tags)}")
        print(f"   - 数据库中活跃分类数量: {len(all_categories)}")
        print(f"🔄 每个新商品将与所有 {len(all_categories)} 个分类建立关联")
        
        created_products = []  # 存储新创建的商品ID
        
        # 开始复制
        for i in range(1, copies_count + 1):
            print(f"\n🔄 开始创建副本 {i}/{copies_count}...")
            
            # 1. 复制商品主体
            new_product_id = uuid.uuid4()
            new_sku_code = f"{original_product.sku_code}_COPY_{i}"
            created_products.append(new_product_id)
            
            new_product = Product(
                id=new_product_id,
                sku_code=new_sku_code,
                name=f"{original_product.name} (副本{i})" if original_product.name else None,
                description=original_product.description,
                status=original_product.status,
                weight=original_product.weight,
                width=original_product.width,
                height=original_product.height,
                length=original_product.length,
                is_featured=original_product.is_featured,
                is_new=original_product.is_new,
                is_bestseller=original_product.is_bestseller,
                is_customizable=original_product.is_customizable,
                tax_class=original_product.tax_class,
                sort_order=original_product.sort_order,
                seo_title=original_product.seo_title,
                seo_description=original_product.seo_description,
                seo_keywords=original_product.seo_keywords,
                meta_data=original_product.meta_data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(new_product)
            db.flush()  # 获取新ID
            
            # 2. 复制SKU
            sku_mapping = {}  # 存储原SKU ID到新SKU ID的映射
            for original_sku in original_skus:
                new_sku_id = uuid.uuid4()
                new_sku = ProductSku(
                    id=new_sku_id,
                    product_id=new_product_id,
                    sku_code=f"{original_sku.sku_code}_COPY_{i}",
                    barcode=original_sku.barcode,
                    image_url=original_sku.image_url,
                    price_adjustment=original_sku.price_adjustment,
                    weight_adjustment=original_sku.weight_adjustment,
                    width_adjustment=original_sku.width_adjustment,
                    height_adjustment=original_sku.height_adjustment,
                    length_adjustment=original_sku.length_adjustment,
                    is_active=original_sku.is_active,
                    is_default=original_sku.is_default,
                    sort_order=original_sku.sort_order,
                    meta_data=original_sku.meta_data,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_sku)
                sku_mapping[original_sku.id] = new_sku_id
            
            # 先提交SKU数据，确保外键约束满足
            db.flush()
            
            # 然后复制SKU属性值关联
            for original_sku in original_skus:
                new_sku_id = sku_mapping[original_sku.id]
                for attr_value in original_sku.attribute_values:
                    db.execute(
                        sku_attribute_value.insert().values(
                            sku_id=new_sku_id,
                            attribute_value_id=attr_value.id,
                            created_at=datetime.utcnow()
                        )
                    )
            
            # 3. 复制图片
            for original_image in original_images:
                new_image = ProductImage(
                    id=uuid.uuid4(),
                    product_id=new_product_id,
                    image_url=original_image.image_url,
                    image_type=original_image.image_type,
                    alt_text=original_image.alt_text,
                    title=original_image.title,
                    description=original_image.description,
                    width=original_image.width,
                    height=original_image.height,
                    file_size=original_image.file_size,
                    duration=original_image.duration,
                    thumbnail_url=original_image.thumbnail_url,
                    is_video=original_image.is_video,
                    video_format=original_image.video_format,
                    sort_order=original_image.sort_order,
                    is_active=original_image.is_active,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_image)
            
            # 4. 复制翻译
            for original_translation in original_translations:
                new_translation = ProductTranslation(
                    id=uuid.uuid4(),
                    product_id=new_product_id,
                    language_code=original_translation.language_code,
                    name=f"{original_translation.name} (副本{i})" if original_translation.name else None,
                    short_description=original_translation.short_description,
                    description=original_translation.description,
                    specifications=original_translation.specifications,
                    benefits=original_translation.benefits,
                    instructions=original_translation.instructions,
                    seo_title=original_translation.seo_title,
                    seo_description=original_translation.seo_description,
                    seo_keywords=original_translation.seo_keywords,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_translation)
            
            # 5. 复制价格
            for original_price in original_prices:
                new_price = ProductPrice(
                    id=uuid.uuid4(),
                    product_id=new_product_id,
                    currency_code=original_price.currency_code,
                    regular_price=original_price.regular_price,
                    sale_price=original_price.sale_price,
                    discount_percentage=original_price.discount_percentage,
                    special_price=original_price.special_price,
                    special_price_start_date=original_price.special_price_start_date,
                    special_price_end_date=original_price.special_price_end_date,
                    min_quantity=original_price.min_quantity,
                    is_default=original_price.is_default,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_price)
            
            # 6. 复制库存（按原SKU映射到新SKU）
            for original_inventory in original_inventories:
                new_sku_id = sku_mapping.get(original_inventory.sku_id) if original_inventory.sku_id else None
                
                new_inventory = ProductInventory(
                    id=uuid.uuid4(),
                    product_id=new_product_id,
                    sku_id=new_sku_id,
                    quantity=original_inventory.quantity,
                    reserved_quantity=0,  # 重置预留数量
                    alert_threshold=original_inventory.alert_threshold,
                    ideal_quantity=original_inventory.ideal_quantity,
                    reorder_point=original_inventory.reorder_point,
                    reorder_quantity=original_inventory.reorder_quantity,
                    is_in_stock=original_inventory.is_in_stock,
                    is_managed=original_inventory.is_managed,
                    location=original_inventory.location,
                    notes=original_inventory.notes,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_inventory)
            
            # 7. 复制多对多关系
            # 分类关系 - 与所有活跃分类建立关联
            print(f"   🔗 与 {len(all_categories)} 个分类建立关联...")
            for category in all_categories:
                db.execute(
                    product_category.insert().values(
                        product_id=new_product_id,
                        category_id=category.id
                    )
                )
            
            # 标签关系
            for tag in original_tags:
                db.execute(
                    product_tag.insert().values(
                        product_id=new_product_id,
                        tag_id=tag.id
                    )
                )
            
            # 场景关系
            for scene in original_scenes:
                db.execute(
                    product_scene.insert().values(
                        product_id=new_product_id,
                        scene_id=scene.id
                    )
                )
            
            # 意图关系
            for intent in original_intents:
                db.execute(
                    product_intent.insert().values(
                        product_id=new_product_id,
                        intent_id=intent.id
                    )
                )
            
            # 符号关系
            for symbol in original_symbols:
                db.execute(
                    product_symbol.insert().values(
                        product_id=new_product_id,
                        symbol_id=symbol.id
                    )
                )
            
            # 材质关系
            for material in original_materials:
                db.execute(
                    product_material.insert().values(
                        product_id=new_product_id,
                        material_id=material.id
                    )
                )
            
            # 主题关系
            for theme in original_themes:
                db.execute(
                    product_theme.insert().values(
                        product_id=new_product_id,
                        theme_id=theme.id
                    )
                )
            
            # 目标群体关系
            for target_group in original_target_groups:
                db.execute(
                    product_target_group.insert().values(
                        product_id=new_product_id,
                        target_group_id=target_group.id
                    )
                )
            
            print(f"✅ 副本 {i} 创建完成 (新商品ID: {new_product_id})")
        
        # 提交事务
        db.commit()
        print(f"\n🎉 成功创建 {copies_count} 个商品副本！")
        print(f"📝 总结:")
        print(f"   - 每个商品都与 {len(all_categories)} 个分类建立了关联")
        print(f"   - 现在每个分类下都至少有 {copies_count} 个商品")
        print(f"   - C端点击任何分类都能看到这些商品")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ 复制过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 商品数据复制工具 (全分类关联版)")
    print("=" * 60)
    
    # 获取用户输入
    try:
        product_id = input("\n请输入要复制的商品UUID: ").strip()
        if not product_id:
            print("❌ 商品UUID不能为空")
            return
        
        # 验证UUID格式
        uuid.UUID(product_id)
        
        copies_count = input("请输入复制数量 (默认4个): ").strip()
        if not copies_count:
            copies_count = 4
        else:
            copies_count = int(copies_count)
            if copies_count <= 0:
                print("❌ 复制数量必须大于0")
                return
    
    except ValueError as e:
        print(f"❌ 输入格式错误: {str(e)}")
        return
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
        return
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 确认操作
        print(f"\n📋 操作确认:")
        print(f"   商品UUID: {product_id}")
        print(f"   复制数量: {copies_count}")
        print(f"   ⚠️  新商品将与数据库中所有活跃分类建立关联")
        
        confirm = input("\n确认执行复制操作？(y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("👋 操作已取消")
            return
        
        # 执行复制
        print(f"\n🔄 开始复制商品数据...")
        success = copy_product_data(db, product_id, copies_count)
        
        if success:
            print(f"\n✨ 复制操作完成！")
        else:
            print(f"\n💥 复制操作失败！")
            
    finally:
        db.close()


if __name__ == "__main__":
    main()
