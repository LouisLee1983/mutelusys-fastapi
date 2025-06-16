#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品分类导入脚本
从JSON文件导入商品分类数据到数据库
"""
from datetime import datetime
import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.db.session import SessionLocal
from app.product.models import ProductCategory, ProductCategoryTranslation, CategoryLevel


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """加载JSON文件数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"成功加载JSON文件: {file_path}")
        return data
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON文件格式错误 - {e}")
        sys.exit(1)


def create_category_translation(db: Session, category_id: str, category_data: Dict[str, Any], language_code: str = "zh-CN"):
    """创建分类翻译记录"""
    translation = ProductCategoryTranslation(
        category_id=category_id,
        language_code=language_code,
        name=category_data.get("name", ""),
        description=category_data.get("description", ""),
        seo_title=category_data.get("seo_title", ""),
        seo_description=category_data.get("seo_description", ""),
        seo_keywords=category_data.get("seo_keywords", "")
    )
    db.add(translation)
    return translation


def import_category(db: Session, category_data: Dict[str, Any], parent_id: str = None) -> ProductCategory:
    """导入单个分类及其子分类"""
    
    # 检查分类是否已存在
    existing_category = db.query(ProductCategory).filter(
        ProductCategory.slug == category_data["slug"]
    ).first()
    
    if existing_category:
        print(f"分类已存在，跳过: {category_data['name']} ({category_data['slug']})")
        return existing_category
    
    # 创建分类
    category_id = uuid.uuid4()
    category = ProductCategory(
        id=category_id,
        name=category_data["name"],
        slug=category_data["slug"],
        description=category_data.get("description", ""),
        parent_id=parent_id,
        level=CategoryLevel(category_data["level"].lower()),
        is_active=True,
        is_featured=False,
        sort_order=category_data.get("sort_order", 0),
        seo_title=category_data.get("seo_title", ""),
        seo_description=category_data.get("seo_description", ""),
        seo_keywords=category_data.get("seo_keywords", ""),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    try:
        db.add(category)
        
        # 创建中文翻译
        create_category_translation(db, category_id, category_data, "zh-CN")
        
        print(f"成功导入分类: {category_data['name']} ({category_data['slug']}) - Level: {category_data['level']}")
        
        # 递归导入子分类
        if "children" in category_data and category_data["children"]:
            for child_data in category_data["children"]:
                import_category(db, child_data, category_id)
        
        return category
        
    except IntegrityError as e:
        db.rollback()
        print(f"导入分类时发生错误: {category_data['name']} - {e}")
        raise


def clear_existing_categories(db: Session):
    """清空现有分类数据"""
    try:
        # 先删除翻译数据
        db.query(ProductCategoryTranslation).delete()
        # 再删除分类数据
        db.query(ProductCategory).delete()
        db.commit()
        print("已清空现有分类数据")
    except Exception as e:
        db.rollback()
        print(f"清空分类数据时发生错误: {e}")
        raise


def import_categories_from_json(json_file_path: str, clear_existing: bool = False):
    """从JSON文件导入分类数据"""
    
    # 加载JSON数据
    categories_data = load_json_data(json_file_path)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 是否清空现有数据
        if clear_existing:
            clear_existing_categories(db)
        
        # 导入分类数据
        total_categories = 0
        for category_data in categories_data:
            import_category(db, category_data)
            total_categories += 1
            
            # 计算子分类数量
            def count_children(data):
                count = 0
                if "children" in data and data["children"]:
                    for child in data["children"]:
                        count += 1 + count_children(child)
                return count
            
            total_categories += count_children(category_data)
        
        # 提交事务
        db.commit()
        print(f"\n导入完成! 总共导入了 {total_categories} 个分类")
        
        # 显示统计信息
        level1_count = db.query(ProductCategory).filter(ProductCategory.level == CategoryLevel.LEVEL_1).count()
        level2_count = db.query(ProductCategory).filter(ProductCategory.level == CategoryLevel.LEVEL_2).count()
        level3_count = db.query(ProductCategory).filter(ProductCategory.level == CategoryLevel.LEVEL_3).count()
        
        print(f"分类统计:")
        print(f"  一级分类: {level1_count}")
        print(f"  二级分类: {level2_count}")
        print(f"  三级分类: {level3_count}")
        print(f"  总计: {level1_count + level2_count + level3_count}")
        
    except Exception as e:
        db.rollback()
        print(f"导入过程中发生错误: {e}")
        raise
    finally:
        db.close()


def main():
    """主函数"""
    print("开始导入商品分类数据...")
    
    # JSON文件路径
    json_file_path = os.path.join(project_root.parent, "design-media", "json-data", "all-category.json")
    
    if not os.path.exists(json_file_path):
        print(f"错误: JSON文件不存在 - {json_file_path}")
        sys.exit(1)
    
    # 询问是否清空现有数据
    clear_existing = input("是否清空现有分类数据? (y/N): ").lower().strip() == 'y'
    
    try:
        import_categories_from_json(json_file_path, clear_existing)
        print("\n分类数据导入成功!")
    except Exception as e:
        print(f"\n导入失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
