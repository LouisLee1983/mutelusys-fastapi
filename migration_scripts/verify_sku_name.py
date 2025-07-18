#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证sku_name字段是否已添加到数据库
"""
import os
from sqlalchemy import create_engine, text

# 使用环境变量中的数据库URL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:Postgre,.1@localhost:5432/muteludb')

def verify_sku_name_column():
    """验证sku_name列是否存在"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 检查products表的sku_name列
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'products' 
                AND column_name = 'sku_name';
            """))
            
            products_column = result.fetchone()
            if products_column:
                print(f"✅ products.sku_name 列存在 - 类型: {products_column[1]}, 可为空: {products_column[2]}")
            else:
                print("❌ products.sku_name 列不存在")
            
            # 检查product_skus表的sku_name列
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'product_skus' 
                AND column_name = 'sku_name';
            """))
            
            skus_column = result.fetchone()
            if skus_column:
                print(f"✅ product_skus.sku_name 列存在 - 类型: {skus_column[1]}, 可为空: {skus_column[2]}")
            else:
                print("❌ product_skus.sku_name 列不存在")
                
            # 检查一些示例数据
            result = conn.execute(text("""
                SELECT id, sku_code, sku_name 
                FROM products 
                LIMIT 5;
            """))
            
            print("\n📋 示例产品数据:")
            for row in result:
                print(f"  - ID: {row['id']}, SKU: {row['sku_code']}, SKU名称: {row['sku_name']}")
                
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    verify_sku_name_column()