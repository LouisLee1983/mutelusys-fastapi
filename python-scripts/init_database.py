#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
"""
from app.db.init_db import init_db, create_initial_data
from app.db.session import SessionLocal

def main():
    print("正在初始化数据库...")
    
    # 创建所有表
    init_db()
    print("数据库表创建完成")
    
    # 创建初始数据
    db = SessionLocal()
    try:
        create_initial_data(db)
        print("初始数据创建完成")
    finally:
        db.close()
    
    print("数据库初始化完成!")

if __name__ == "__main__":
    main() 