#!/usr/bin/env python3
"""
运行国家和地区数据迁移脚本

使用方法:
    python run_countries_regions_migration.py

或者直接运行:
    chmod +x run_countries_regions_migration.py
    ./run_countries_regions_migration.py

此脚本将执行以下操作:
1. 创建countries和regions相关表结构
2. 插入全球国家数据（包含简体中文翻译）
3. 插入全球地区数据（包含地区分组和关联关系）

注意: 请确保数据库连接配置正确，建议先在测试环境运行
"""

import os
import sys
import logging
from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """获取数据库连接"""
    try:
        # 从环境变量读取数据库配置
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'mutelu')
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return None

def execute_sql_file(conn, file_path):
    """执行SQL文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_content)
        cursor.close()
        
        logger.info(f"✅ 成功执行: {file_path}")
        return True
    except Exception as e:
        logger.error(f"❌ 执行失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始执行国家和地区数据迁移...")
    
    # 获取脚本目录
    script_dir = Path(__file__).parent
    
    # 迁移文件列表（按顺序执行）
    migration_files = [
        '20250625_171748_create_countries_and_regions_tables.sql',
        '20250625_171748_insert_global_countries_data.sql',
        '20250625_171748_insert_global_regions_data.sql'
    ]
    
    # 检查文件是否存在
    for file_name in migration_files:
        file_path = script_dir / file_name
        if not file_path.exists():
            logger.error(f"❌ 找不到迁移文件: {file_path}")
            sys.exit(1)
    
    # 获取数据库连接
    conn = get_db_connection()
    if not conn:
        logger.error("❌ 无法连接数据库，请检查配置")
        sys.exit(1)
    
    try:
        # 依次执行迁移文件
        all_success = True
        for file_name in migration_files:
            file_path = script_dir / file_name
            logger.info(f"正在执行: {file_name}")
            
            if not execute_sql_file(conn, file_path):
                all_success = False
                break
        
        if all_success:
            logger.info("🎉 所有迁移文件执行成功！")
            
            # 查询统计信息
            cursor = conn.cursor()
            
            # 统计国家数量
            cursor.execute("SELECT COUNT(*) FROM countries")
            country_count = cursor.fetchone()[0]
            
            # 统计地区数量
            cursor.execute("SELECT COUNT(*) FROM regions")
            region_count = cursor.fetchone()[0]
            
            # 统计翻译数量
            cursor.execute("SELECT COUNT(*) FROM country_translations WHERE language = 'zh-CN'")
            translation_count = cursor.fetchone()[0]
            
            # 统计国家地区关联数量
            cursor.execute("SELECT COUNT(*) FROM country_regions")
            association_count = cursor.fetchone()[0]
            
            cursor.close()
            
            logger.info("📊 数据统计:")
            logger.info(f"   - 国家数量: {country_count}")
            logger.info(f"   - 地区数量: {region_count}")
            logger.info(f"   - 中文翻译数量: {translation_count}")
            logger.info(f"   - 国家地区关联数量: {association_count}")
            
        else:
            logger.error("❌ 部分迁移文件执行失败")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ 执行过程中发生错误: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()