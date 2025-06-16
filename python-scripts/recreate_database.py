#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库重建脚本
删除所有表并重新创建数据库结构
"""
import logging
from app.db.base import Base
from app.db.session import engine
from app.db.init_db import init_db, create_initial_data
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    """删除所有表并重新创建"""
    logger.info("开始重建数据库...")
    
    # 删除所有表
    logger.info("正在删除所有数据库表...")
    Base.metadata.drop_all(bind=engine)
    logger.info("所有表删除完成")
    
    # 重新创建所有表
    logger.info("正在重新创建数据库表...")
    init_db()
    logger.info("数据库表重新创建完成")
    
    # 创建初始数据
    logger.info("正在创建初始数据...")
    db = SessionLocal()
    try:
        create_initial_data(db)
        logger.info("初始数据创建完成")
    finally:
        db.close()
    
    logger.info("数据库重建完成!")

if __name__ == "__main__":
    recreate_database() 