#!/usr/bin/env python3
"""
验证customers表的role字段是否已添加
"""

import os
import sys
from pathlib import Path

# 添加父目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.session import get_db_session

def verify_customer_role():
    """验证customers表的role字段"""
    
    try:
        # 获取数据库会话
        db = next(get_db_session())
        
        # 查询customers表结构
        query = text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'customers' 
            AND column_name = 'role'
            ORDER BY ordinal_position;
        """)
        
        result = db.execute(query)
        columns = result.fetchall()
        
        if columns:
            print("✅ customers表的role字段信息:")
            for col in columns:
                print(f"   列名: {col.column_name}")
                print(f"   数据类型: {col.data_type}")
                print(f"   允许空值: {col.is_nullable}")
                print(f"   默认值: {col.column_default}")
            
            # 验证枚举类型
            enum_query = text("""
                SELECT enumlabel 
                FROM pg_enum 
                WHERE enumtypid = (
                    SELECT oid 
                    FROM pg_type 
                    WHERE typname = 'customerrole'
                )
                ORDER BY enumlabel;
            """)
            
            enum_result = db.execute(enum_query)
            enum_values = [row.enumlabel for row in enum_result.fetchall()]
            
            if enum_values:
                print(f"   枚举值: {enum_values}")
            
            return True
        else:
            print("❌ customers表中未找到role字段")
            return False
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🔍 验证customers表的role字段...")
    success = verify_customer_role()
    
    if success:
        print("\n✅ 验证成功！customers表的role字段已正确添加")
    else:
        print("\n❌ 验证失败！")