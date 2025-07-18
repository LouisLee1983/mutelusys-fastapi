#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接执行数据库同步SQL脚本
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from sqlalchemy import create_engine, text
from colorama import init, Fore, Style

init()

def execute_sql_file(sql_file_path: str):
    """执行SQL文件"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print(f"{Fore.RED}❌ 未找到DATABASE_URL环境变量{Style.RESET_ALL}")
        return False
        
    print(f"{Fore.CYAN}数据库连接: {database_url.split('@')[1] if '@' in database_url else 'localhost'}{Style.RESET_ALL}")
    
    try:
        # 读取SQL文件
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        # 分割SQL语句
        statements = []
        for line in sql_content.split('\n'):
            line = line.strip()
            if line and not line.startswith('--'):
                statements.append(line)
                
        # 过滤掉空语句
        sql_statements = []
        current_statement = ""
        for stmt in statements:
            if stmt:
                current_statement += stmt + " "
                if stmt.rstrip().endswith(';'):
                    sql_statements.append(current_statement.strip())
                    current_statement = ""
        
        print(f"{Fore.YELLOW}找到 {len(sql_statements)} 条SQL语句{Style.RESET_ALL}")
        
        if not sql_statements:
            print(f"{Fore.YELLOW}没有需要执行的SQL语句{Style.RESET_ALL}")
            return True
            
        # 执行SQL语句
        engine = create_engine(database_url, echo=False)
        
        with engine.connect() as conn:
            trans = conn.begin()
            
            success_count = 0
            error_count = 0
            
            for i, statement in enumerate(sql_statements):
                try:
                    print(f"{Fore.CYAN}执行 [{i+1}/{len(sql_statements)}]: {statement[:60]}...{Style.RESET_ALL}")
                    conn.execute(text(statement))
                    success_count += 1
                except Exception as e:
                    print(f"{Fore.RED}❌ 错误: {statement[:60]}... - {e}{Style.RESET_ALL}")
                    error_count += 1
                    # 继续执行其他语句，不中断
                    
            if error_count == 0:
                trans.commit()
                print(f"\n{Fore.GREEN}✅ 所有SQL语句执行成功! ({success_count} 条){Style.RESET_ALL}")
            else:
                trans.rollback()
                print(f"\n{Fore.RED}❌ 执行过程中发生错误: {error_count} 条失败, {success_count} 条成功{Style.RESET_ALL}")
                print(f"{Fore.RED}事务已回滚{Style.RESET_ALL}")
                return False
                
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ 执行SQL文件时发生错误: {e}{Style.RESET_ALL}")
        return False


def main():
    """主函数"""
    print(f"{Fore.CYAN}数据库SQL同步执行工具{Style.RESET_ALL}")
    
    # 查找最新的SQL文件
    sql_files = [f for f in os.listdir('.') if f.startswith('model_sync_') and f.endswith('.sql')]
    if not sql_files:
        print(f"{Fore.RED}❌ 未找到同步SQL文件{Style.RESET_ALL}")
        return
        
    # 使用最新的SQL文件
    latest_sql_file = sorted(sql_files)[-1]
    print(f"使用SQL文件: {latest_sql_file}")
    
    # 执行SQL
    if execute_sql_file(latest_sql_file):
        print(f"\n{Fore.GREEN}🎉 数据库同步完成!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}💥 数据库同步失败!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()