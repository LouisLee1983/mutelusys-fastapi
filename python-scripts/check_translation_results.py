# -*- coding: utf-8 -*-
"""
检查分类翻译结果的脚本

使用方法：
python python-scripts/check_translation_results.py
"""

import sys
import os
from typing import Dict, List
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.product.models import ProductCategoryTranslation, ProductCategory


def check_translation_results():
    """检查翻译结果统计"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("分类翻译结果检查")
        print("=" * 60)
        
        # 1. 统计各语言记录数量
        print("\n1. 各语言记录数量统计:")
        print("-" * 30)
        
        language_stats = (
            db.query(
                ProductCategoryTranslation.language_code,
                db.func.count(ProductCategoryTranslation.id).label('count')
            )
            .group_by(ProductCategoryTranslation.language_code)
            .all()
        )
        
        for lang_code, count in language_stats:
            print(f"{lang_code}: {count} 条记录")
        
        # 2. 检查翻译完整性
        print("\n2. 翻译完整性检查:")
        print("-" * 30)
        
        # 获取所有分类ID
        all_categories = db.query(ProductCategory.id, ProductCategory.name).all()
        total_categories = len(all_categories)
        print(f"总分类数量: {total_categories}")
        
        # 检查每个分类的翻译情况
        languages = ["zh-CN", "en-US", "th-TH"]
        complete_translations = 0
        incomplete_categories = []
        
        for category_id, category_name in all_categories:
            translations = (
                db.query(ProductCategoryTranslation.language_code)
                .filter(ProductCategoryTranslation.category_id == category_id)
                .all()
            )
            
            existing_languages = [t[0] for t in translations]
            missing_languages = [lang for lang in languages if lang not in existing_languages]
            
            if not missing_languages:
                complete_translations += 1
            else:
                incomplete_categories.append({
                    'category_id': str(category_id),
                    'category_name': category_name or 'Unknown',
                    'missing_languages': missing_languages
                })
        
        print(f"完整翻译的分类: {complete_translations}/{total_categories}")
        print(f"不完整翻译的分类: {len(incomplete_categories)}")
        
        # 3. 显示不完整的分类详情
        if incomplete_categories:
            print("\n3. 不完整翻译的分类详情:")
            print("-" * 50)
            for item in incomplete_categories[:10]:  # 只显示前10个
                print(f"分类: {item['category_name']}")
                print(f"缺失语言: {', '.join(item['missing_languages'])}")
                print("-" * 20)
            
            if len(incomplete_categories) > 10:
                print(f"... 还有 {len(incomplete_categories) - 10} 个分类")
        
        # 4. 随机抽样检查翻译质量
        print("\n4. 翻译质量抽样检查:")
        print("-" * 40)
        
        # 获取一个有完整翻译的分类作为示例
        sample_category = (
            db.query(ProductCategoryTranslation)
            .filter(ProductCategoryTranslation.language_code == "zh-CN")
            .first()
        )
        
        if sample_category:
            print(f"示例分类ID: {sample_category.category_id}")
            
            # 获取该分类的所有语言版本
            all_translations = (
                db.query(ProductCategoryTranslation)
                .filter(ProductCategoryTranslation.category_id == sample_category.category_id)
                .order_by(ProductCategoryTranslation.language_code)
                .all()
            )
            
            for translation in all_translations:
                print(f"\n语言: {translation.language_code}")
                print(f"名称: {translation.name}")
                print(f"描述: {translation.description[:100] if translation.description else 'N/A'}...")
                print(f"SEO标题: {translation.seo_title or 'N/A'}")
        
        # 5. 生成汇总报告
        print("\n" + "=" * 60)
        print("汇总报告:")
        print(f"• 总分类数: {total_categories}")
        print(f"• 完整翻译: {complete_translations} ({complete_translations/total_categories*100:.1f}%)")
        print(f"• 不完整翻译: {len(incomplete_categories)} ({len(incomplete_categories)/total_categories*100:.1f}%)")
        
        for lang_code, count in language_stats:
            coverage = count / total_categories * 100 if total_categories > 0 else 0
            print(f"• {lang_code} 覆盖率: {count}/{total_categories} ({coverage:.1f}%)")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"检查过程发生错误: {str(e)}")
    finally:
        db.close()


def export_translation_data():
    """导出翻译数据到CSV文件（可选功能）"""
    if not HAS_PANDAS:
        print("需要安装pandas库才能导出CSV: pip install pandas")
        return
        
    db = SessionLocal()
    
    try:
        print("\n导出翻译数据到CSV文件...")
        
        # 查询所有翻译数据
        translations = (
            db.query(
                ProductCategoryTranslation.category_id,
                ProductCategoryTranslation.language_code,
                ProductCategoryTranslation.name,
                ProductCategoryTranslation.description,
                ProductCategoryTranslation.seo_title,
                ProductCategoryTranslation.created_at
            )
            .order_by(
                ProductCategoryTranslation.category_id,
                ProductCategoryTranslation.language_code
            )
            .all()
        )
        
        # 转换为DataFrame
        data = []
        for t in translations:
            data.append({
                'category_id': str(t.category_id),
                'language_code': t.language_code,
                'name': t.name,
                'description': t.description or '',
                'seo_title': t.seo_title or '',
                'created_at': t.created_at
            })
        
        df = pd.DataFrame(data)
        
        # 导出到CSV
        filename = f"category_translations_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"翻译数据已导出到: {filename}")
        print(f"总记录数: {len(data)}")
        
    except Exception as e:
        print(f"导出数据失败: {str(e)}")
    finally:
        db.close()


def main():
    """主函数"""
    try:
        check_translation_results()
        
        # 询问是否导出数据
        export_choice = input("\n是否要导出翻译数据到CSV文件？(y/n): ").strip().lower()
        if export_choice in ['y', 'yes']:
            export_translation_data()
        
    except KeyboardInterrupt:
        print("\n用户中断执行")
    except Exception as e:
        print(f"脚本执行失败: {str(e)}")


if __name__ == "__main__":
    main()