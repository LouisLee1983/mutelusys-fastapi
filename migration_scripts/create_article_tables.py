#!/usr/bin/env python3
"""
产品文章表创建脚本
"""

import os
import psycopg2
from datetime import datetime

def run_migration():
    """执行产品文章表迁移"""
    
    # 读取SQL文件
    sql_file = os.path.join(os.path.dirname(__file__), "20250626_product_articles_tables.sql")
    
    if not os.path.exists(sql_file):
        print(f"错误: SQL文件不存在: {sql_file}")
        return False
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 连接数据库（使用.env文件中的配置）
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="muteludb",
            user="postgres",
            password="Postgre,.1"
        )
        
        cursor = conn.cursor()
        
        print("开始执行产品文章表迁移...")
        print(f"时间: {datetime.now()}")
        
        # 执行SQL
        cursor.execute(sql_content)
        conn.commit()
        
        print("✅ 产品文章表迁移执行成功!")
        
        # 验证表是否创建成功
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('product_articles', 'product_article_translations', 'product_article_associations', 'product_article_templates')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"✅ 成功创建表: {[t[0] for t in tables]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ 数据库连接或执行失败: {str(e)}")
        print("请检查数据库连接参数，或手动执行SQL文件")
        return False
    except Exception as e:
        print(f"❌ 迁移执行失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("产品文章表创建脚本")
    print("=" * 50)
    success = run_migration()
    
    if not success:
        print("\n💡 提示：如果自动迁移失败，请手动执行以下步骤：")
        print("1. 连接到PostgreSQL数据库 muteludb")
        print("2. 执行 20250626_product_articles_tables.sql 文件中的SQL语句")
    
    exit(0 if success else 1)