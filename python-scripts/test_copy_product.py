#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试商品复制功能的简化脚本
"""

import sys
import os
from uuid import UUID

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.product.models import Product

def test_product_copy():
    """测试商品复制功能"""
    print("🧪 测试商品复制功能...")
    
    db = SessionLocal()
    try:
        # 查找一个测试商品
        test_product = db.query(Product).filter(Product.status == "active").first()
        
        if not test_product:
            print("❌ 没有找到可用的测试商品")
            return False
            
        print(f"✅ 找到测试商品: {test_product.name} (ID: {test_product.id})")
        print(f"   SKU: {test_product.sku_code}")
        print(f"   状态: {test_product.status}")
        
        # 检查商品的关联数据
        print(f"\n📊 商品关联数据统计:")
        print(f"   - SKU数量: {len(test_product.skus)}")
        print(f"   - 图片数量: {len(test_product.images)}")
        print(f"   - 翻译数量: {len(test_product.translations)}")
        print(f"   - 价格数量: {len(test_product.prices)}")
        print(f"   - 库存记录: {len(test_product.inventories)}")
        print(f"   - 分类数量: {len(test_product.categories)}")
        
        # 检查SKU的属性值
        for sku in test_product.skus:
            print(f"   - SKU {sku.sku_code} 属性值数量: {len(sku.attribute_values)}")
        
        print(f"\n✅ 商品数据结构正常，可以进行复制测试")
        print(f"💡 使用以下UUID进行复制测试: {test_product.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    test_product_copy() 