#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
执行数据库迁移脚本
使用方法: python run_migration.py <migration_file.sql>
"""
import sys
import os
from sqlalchemy import create_engine, text
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

def run_migration(sql_file: str):
    """执行指定的SQL迁移脚本"""
    # 使用环境变量中的数据库URL
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:Postgre,.1@localhost:5432/muteludb')
    
    try:
        # 检查SQL文件是否存在
        if not os.path.exists(sql_file):
            print(f'❌ SQL文件不存在: {sql_file}')
            return False
            
        # 读取SQL脚本
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print(f'📄 正在执行迁移脚本: {sql_file}')
        print(f'🔗 数据库连接: {DATABASE_URL.replace(":Postgre,.1@", ":****@")}')  # 隐藏密码
        
        # 创建数据库连接
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 执行SQL脚本
            # 使用text()包装SQL语句以支持原生SQL执行
            conn.execute(text(sql_script))
            conn.commit()
            print('✅ 数据库迁移成功完成！')
            
    except Exception as e:
        print(f'❌ 数据库迁移失败: {e}')
        return False
    
    return True

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('使用方法: python run_migration.py <migration_file.sql>')
        print('示例: python run_migration.py 008_add_customer_role_and_country.sql')
        sys.exit(1)
    
    sql_file = sys.argv[1]
    
    # 如果没有提供完整路径，假设文件在当前目录
    if not os.path.isabs(sql_file):
        sql_file = os.path.join(os.path.dirname(__file__), sql_file)
    
    success = run_migration(sql_file)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()