#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
执行数据库迁移脚本
"""
import psycopg2
from sqlalchemy import create_engine

def run_migration():
    # 数据库连接URL
    DATABASE_URL = 'postgresql://postgres:123456@localhost:5432/muteludb'
    
    try:
        # 读取SQL脚本
        with open('change_product_ai_analysis_json_to_text.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 创建数据库连接
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 执行SQL脚本
            conn.execute(sql_script)
            print('✅ 数据库迁移成功完成！')
            print('📄 已将ProductAIAnalysis表中的JSON字段改为Text字段')
            
    except Exception as e:
        print(f'❌ 数据库迁移失败: {e}')
        return False
    
    return True

if __name__ == "__main__":
    success = run_migration()
    if not success:
        exit(1) 