#!/usr/bin/env python3
"""
产品文章表迁移执行脚本
"""

import os
import sys
import psycopg2
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def run_migration():
    """执行产品文章表迁移"""
    
    # 读取SQL文件
    sql_file = os.path.join(os.path.dirname(__file__), "20250626_product_articles_tables.sql")
    
    if not os.path.exists(sql_file):
        print(f"错误: SQL文件不存在: {sql_file}")
        return False
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 连接数据库
    try:
        conn = psycopg2.connect(
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            database=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD
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
        
    except Exception as e:
        print(f"❌ 迁移执行失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)