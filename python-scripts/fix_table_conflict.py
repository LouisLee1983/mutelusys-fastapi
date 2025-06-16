#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复shipping表名冲突的脚本
"""

import sys
import os
from sqlalchemy import text

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal

def fix_table_conflicts():
    """修复表名冲突"""
    print("🔧 修复shipping表名冲突...")
    
    db = SessionLocal()
    
    try:
        # 删除可能冲突的shipping相关表
        conflict_tables = [
            'shipping_tracking_events',
            'shipping_order_shipments', 
            'shipping_addresses',
            'shipping_methods',
            'shipping_carriers'
        ]
        
        for table_name in conflict_tables:
            try:
                # 检查表是否存在
                result = db.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table_name}'
                    );
                """))
                table_exists = result.scalar()
                
                if table_exists:
                    # 删除表
                    db.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
                    print(f"   ✅ 删除表: {table_name}")
                else:
                    print(f"   ⚠️  表不存在: {table_name}")
                    
            except Exception as e:
                print(f"   ❌ 删除表 {table_name} 失败: {str(e)}")
        
        # 提交删除操作
        db.commit()
        print("💾 删除操作已提交")
        
        print("✅ 表名冲突修复完成！")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ 修复失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    fix_table_conflicts() 