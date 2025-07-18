#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版模型同步脚本 - 直接使用.env文件中的数据库配置
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

# 导入同步工具
from sync_models_detailed import ModelSyncTool


def main():
    """主函数 - 简化版接口"""
    print("=" * 60)
    print("PostgreSQL 数据库模型同步工具")
    print("=" * 60)
    
    # 检查数据库配置
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ 错误: 未找到DATABASE_URL环境变量")
        print(f"请检查 {env_path} 文件")
        sys.exit(1)
        
    # 显示数据库信息（隐藏密码）
    if '@' in database_url:
        db_info = database_url.split('@')[1]
    else:
        db_info = 'localhost'
    print(f"数据库: {db_info}")
    
    # 显示菜单
    print("\n请选择操作:")
    print("1. 分析差异（推荐）")
    print("2. 分析并生成SQL文件")
    print("3. 分析、生成并执行SQL（谨慎）")
    print("0. 退出")
    
    choice = input("\n请输入选项 [1]: ").strip() or "1"
    
    if choice == "0":
        print("退出程序")
        return
        
    try:
        sync_tool = ModelSyncTool()
        
        if choice in ["1", "2", "3"]:
            execute = (choice == "3")
            
            if execute:
                print("\n⚠️  警告: 您选择了直接执行SQL语句!")
                print("这将直接修改数据库结构，请确保已经备份数据库。")
                confirm = input("确认继续吗? (输入 'yes' 确认): ")
                if confirm.lower() != 'yes':
                    print("已取消操作")
                    return
                    
            # 执行同步分析
            results = sync_tool.sync_all_models(execute=execute)
            
            # 显示结果摘要
            print("\n" + "=" * 60)
            print("同步完成!")
            print(f"分析的模型总数: {results['total_models']}")
            print(f"需要创建的新表: {results['new_tables']}")
            print(f"需要修改的表: {results['modified_tables']}")
            print(f"生成的SQL语句数: {results['sql_count']}")
            
            if results['sql_count'] > 0 and not execute:
                print("\n✅ SQL文件已生成，请查看当前目录下的 model_sync_*.sql 文件")
                print("检查无误后可以手动执行SQL语句")
                
        else:
            print("无效的选项")
            
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()