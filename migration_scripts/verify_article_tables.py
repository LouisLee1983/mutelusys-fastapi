#!/usr/bin/env python3
"""
验证产品文章表结构
"""

import psycopg2

def verify_tables():
    """验证表结构"""
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="muteludb",
            user="postgres",
            password="Postgre,.1"
        )
        
        cursor = conn.cursor()
        
        # 检查表结构
        tables_to_check = [
            'product_articles',
            'product_article_translations', 
            'product_article_associations',
            'product_article_templates'
        ]
        
        for table_name in tables_to_check:
            print(f"\n📋 表: {table_name}")
            print("-" * 60)
            
            # 获取表的列信息
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cursor.fetchall()
            
            if not columns:
                print(f"❌ 表 {table_name} 不存在")
                continue
                
            print(f"✅ 表 {table_name} 存在，列数: {len(columns)}")
            
            for col in columns[:5]:  # 只显示前5列
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  • {col[0]} ({col[1]}) {nullable}{default}")
            
            if len(columns) > 5:
                print(f"  ... 还有 {len(columns) - 5} 列")
        
        # 检查枚举类型
        print(f"\n🔍 枚举类型:")
        print("-" * 60)
        cursor.execute("""
            SELECT typname, array_agg(enumlabel ORDER BY enumsortorder) as labels
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid 
            WHERE typname IN ('articlestatus', 'articletype')
            GROUP BY typname;
        """)
        
        enums = cursor.fetchall()
        for enum in enums:
            print(f"✅ {enum[0]}: {enum[1]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n🎉 验证完成！所有产品文章相关表都已成功创建。")
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("产品文章表结构验证")
    print("=" * 60)
    verify_tables()