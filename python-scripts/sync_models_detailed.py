#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库模型详细同步工具
逐个模型类显示对比和更新过程
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any, Optional
import logging
from pathlib import Path
from colorama import init, Fore, Style
import importlib
import inspect

# 初始化colorama
init()

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, MetaData, inspect as sql_inspect, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import DeclarativeMeta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'model_sync_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ModelSyncTool:
    """模型同步工具类"""
    
    def __init__(self):
        # 从.env文件读取数据库连接
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("未找到DATABASE_URL环境变量，请检查.env文件")
            
        self.engine = create_engine(self.database_url, echo=False)
        self.inspector = sql_inspect(self.engine)
        self.sql_statements = []
        self.models_registry = {}
        self.metadata = None
        self._load_all_models()
        
    def _load_all_models(self):
        """动态加载所有模型"""
        # 导入Base以获取所有模型
        from app.db.base import Base
        
        # 清理metadata避免重复定义错误
        Base.metadata.clear()
        
        # 导入所有models模块以确保模型被注册
        modules_to_import = [
            'app.product.models',
            'app.order.models',
            'app.customer.models',
            'app.marketing.models',
            'app.analytics.models',
            'app.content.models',
            'app.localization.models',
            'app.shipping.models',
            'app.payment.models',
            'app.security.models',
            'app.duty.models',
            'app.fortune.models',
        ]
        
        # 导入所有子模块
        app_path = Path(__file__).parent.parent / 'app'
        for module_dir in app_path.iterdir():
            if module_dir.is_dir() and not module_dir.name.startswith('__'):
                # 检查子目录中的models.py
                for subdir in module_dir.iterdir():
                    if subdir.is_dir() and not subdir.name.startswith('__'):
                        models_file = subdir / 'models.py'
                        if models_file.exists():
                            module_path = f'app.{module_dir.name}.{subdir.name}.models'
                            if module_path not in modules_to_import:
                                modules_to_import.append(module_path)
        
        # 导入所有模块
        for module_name in modules_to_import:
            try:
                module = importlib.import_module(module_name)
                # 获取模块中的所有模型类
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Base) and 
                        obj != Base and 
                        hasattr(obj, '__tablename__')):
                        table_name = obj.__tablename__
                        
                        # 如果表名已存在，跳过重复定义（保留第一个）
                        if table_name in self.models_registry:
                            logger.warning(f"⚠ 表 '{table_name}' 重复定义，跳过: {module_name}.{name}")
                            continue
                            
                        self.models_registry[table_name] = {
                            'class': obj,
                            'module': module_name,
                            'name': name
                        }
                logger.info(f"✓ 加载模块: {module_name}")
            except ImportError as e:
                logger.warning(f"⚠ 无法导入模块 {module_name}: {e}")
            except Exception as e:
                logger.warning(f"⚠ 模块 {module_name} 加载时发生错误: {e}")
                
        # 设置metadata
        self.metadata = Base.metadata
        logger.info(f"总共加载了 {len(self.models_registry)} 个模型")
        
    def get_database_tables(self) -> Set[str]:
        """获取数据库中已存在的表"""
        return set(self.inspector.get_table_names())
        
    def get_database_columns(self, table_name: str) -> Dict[str, Dict]:
        """获取数据库表的列信息"""
        columns = {}
        try:
            for col in self.inspector.get_columns(table_name):
                columns[col['name']] = {
                    'type': str(col['type']),
                    'nullable': col['nullable'],
                    'default': col.get('default'),
                    'autoincrement': col.get('autoincrement', False)
                }
        except Exception as e:
            logger.warning(f"无法获取表 {table_name} 的列信息: {e}")
        return columns
        
    def type_mapping(self, sqlalchemy_type) -> str:
        """将SQLAlchemy类型映射为PostgreSQL类型"""
        type_str = str(sqlalchemy_type).upper()
        
        # UUID类型
        if 'UUID' in type_str:
            return 'UUID'
        # 字符串类型
        elif 'VARCHAR' in type_str or 'STRING' in type_str:
            if '(' in type_str:
                return type_str.replace('STRING', 'VARCHAR')
            return 'VARCHAR'
        elif 'TEXT' in type_str:
            return 'TEXT'
        # 数字类型
        elif 'INTEGER' in type_str:
            return 'INTEGER'
        elif 'FLOAT' in type_str or 'REAL' in type_str:
            return 'REAL'
        elif 'NUMERIC' in type_str or 'DECIMAL' in type_str:
            return type_str
        # 布尔类型
        elif 'BOOLEAN' in type_str:
            return 'BOOLEAN'
        # 时间类型
        elif 'DATETIME' in type_str or 'TIMESTAMP' in type_str:
            return 'TIMESTAMP'
        elif 'DATE' in type_str:
            return 'DATE'
        # JSON类型
        elif 'JSON' in type_str:
            return 'JSONB'
        # 枚举类型
        elif 'ENUM' in type_str:
            return type_str
        # 数组类型
        elif 'ARRAY' in type_str:
            # PostgreSQL 数组类型格式
            if 'VARCHAR' in type_str:
                return 'VARCHAR[]'
            elif 'INTEGER' in type_str:
                return 'INTEGER[]'
            else:
                return 'TEXT[]'
        else:
            return type_str
            
    def compare_column_types(self, model_type, db_type) -> bool:
        """比较模型类型和数据库类型是否一致"""
        model_type_str = self.type_mapping(model_type).upper()
        db_type_str = str(db_type).upper()
        
        # 特殊处理一些类型映射
        if 'VARCHAR' in model_type_str and 'CHARACTER VARYING' in db_type_str:
            return True
        if 'TIMESTAMP' in model_type_str and ('TIMESTAMP' in db_type_str or 'DATETIME' in db_type_str):
            return True
        if 'UUID' in model_type_str and 'UUID' in db_type_str:
            return True
        if 'JSONB' in model_type_str and ('JSONB' in db_type_str or 'JSON' in db_type_str):
            return True
        
        return model_type_str == db_type_str
        
    def analyze_model(self, table_name: str, model_info: Dict) -> Dict[str, Any]:
        """分析单个模型的差异"""
        model_class = model_info['class']
        model_name = model_info['name']
        module_name = model_info['module']
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}分析模型: {model_name}{Style.RESET_ALL}")
        print(f"模块: {module_name}")
        print(f"表名: {table_name}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        result = {
            'table_name': table_name,
            'model_name': model_name,
            'module': module_name,
            'exists_in_db': False,
            'sql_statements': [],
            'changes': {
                'new_columns': [],
                'modified_columns': [],
                'removed_columns': [],
                'type_changes': [],
                'nullable_changes': []
            }
        }
        
        db_tables = self.get_database_tables()
        
        if table_name not in db_tables:
            # 表不存在，需要创建
            print(f"{Fore.RED}✗ 表不存在于数据库中{Style.RESET_ALL}")
            result['sql_statements'].append(self._generate_create_table_sql(model_class))
        else:
            # 表存在，比较差异
            result['exists_in_db'] = True
            print(f"{Fore.GREEN}✓ 表已存在于数据库中{Style.RESET_ALL}")
            
            # 获取数据库列信息
            db_columns = self.get_database_columns(table_name)
            model_columns = {col.name: col for col in model_class.__table__.columns}
            
            # 比较列差异
            print(f"\n{Fore.CYAN}列对比:{Style.RESET_ALL}")
            
            # 新增的列
            for col_name, col in model_columns.items():
                if col_name not in db_columns:
                    result['changes']['new_columns'].append(col_name)
                    print(f"  {Fore.GREEN}+ {col_name}: {self.type_mapping(col.type)}{Style.RESET_ALL}")
                    
            # 修改的列
            for col_name, col in model_columns.items():
                if col_name in db_columns:
                    db_col = db_columns[col_name]
                    
                    # 检查类型变化
                    if not self.compare_column_types(col.type, db_col['type']):
                        result['changes']['type_changes'].append({
                            'column': col_name,
                            'old_type': db_col['type'],
                            'new_type': self.type_mapping(col.type)
                        })
                        print(f"  {Fore.YELLOW}~ {col_name}: {db_col['type']} → {self.type_mapping(col.type)}{Style.RESET_ALL}")
                        
                    # 检查NULL约束变化
                    if col.nullable != db_col['nullable']:
                        result['changes']['nullable_changes'].append({
                            'column': col_name,
                            'old_nullable': db_col['nullable'],
                            'new_nullable': col.nullable
                        })
                        nullable_change = "NULL" if col.nullable else "NOT NULL"
                        print(f"  {Fore.YELLOW}~ {col_name}: nullable {db_col['nullable']} → {col.nullable} ({nullable_change}){Style.RESET_ALL}")
                        
            # 删除的列
            for col_name in db_columns:
                if col_name not in model_columns:
                    result['changes']['removed_columns'].append(col_name)
                    print(f"  {Fore.RED}- {col_name} (数据库中存在但模型中不存在){Style.RESET_ALL}")
                    
            # 生成SQL语句
            if any(result['changes'].values()):
                result['sql_statements'] = self._generate_alter_table_sql(
                    table_name, model_class, db_columns, result['changes']
                )
                
        return result
        
    def _generate_create_table_sql(self, model_class) -> str:
        """生成创建表的SQL语句"""
        table = model_class.__table__
        sql_parts = [f"CREATE TABLE {table.name} ("]
        
        column_definitions = []
        for column in table.columns:
            col_def = f"    {column.name} {self.type_mapping(column.type)}"
            
            if not column.nullable:
                col_def += " NOT NULL"
            
            if column.default is not None:
                if hasattr(column.default, 'arg') and callable(column.default.arg):
                    if 'uuid' in str(column.default.arg):
                        col_def += " DEFAULT gen_random_uuid()"
                    elif 'utcnow' in str(column.default.arg):
                        col_def += " DEFAULT CURRENT_TIMESTAMP"
                else:
                    # 处理默认值
                    default_val = str(column.default)
                    if 'ScalarElementColumnDefault' in default_val:
                        # 提取实际的默认值
                        if 'True' in default_val:
                            col_def += " DEFAULT TRUE"
                        elif 'False' in default_val:
                            col_def += " DEFAULT FALSE"
                        elif "''" in default_val or '""' in default_val:
                            col_def += " DEFAULT ''"
                        elif any(num in default_val for num in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                            # 尝试提取数字
                            import re
                            numbers = re.findall(r'[\d.]+', default_val)
                            if numbers:
                                col_def += f" DEFAULT {numbers[0]}"
                        elif "'USD'" in default_val:
                            col_def += " DEFAULT 'USD'"
                        elif "'daily'" in default_val:
                            col_def += " DEFAULT 'daily'"
                        elif "'pending'" in default_val:
                            col_def += " DEFAULT 'pending'"
                    else:
                        col_def += f" DEFAULT {column.default}"
                    
            column_definitions.append(col_def)
            
        # 添加主键约束
        primary_key_cols = [col.name for col in table.primary_key.columns]
        if primary_key_cols:
            column_definitions.append(f"    PRIMARY KEY ({', '.join(primary_key_cols)})")
            
        sql_parts.append(",\n".join(column_definitions))
        sql_parts.append(");")
        
        return "\n".join(sql_parts)
        
    def _generate_alter_table_sql(self, table_name: str, model_class, 
                                 db_columns: Dict, changes: Dict) -> List[str]:
        """生成修改表的SQL语句"""
        sql_statements = []
        table = model_class.__table__
        
        # 处理新增列
        for col_name in changes['new_columns']:
            column = table.columns[col_name]
            col_def = f"ADD COLUMN {column.name} {self.type_mapping(column.type)}"
            
            if not column.nullable:
                # 如果是非空列，先添加为可空，然后设置默认值，最后设为非空
                sql_statements.append(f"ALTER TABLE {table_name} {col_def.replace('NOT NULL', '')};")
                
                if column.default is not None:
                    if hasattr(column.default, 'arg') and callable(column.default.arg):
                        if 'uuid' in str(column.default.arg):
                            sql_statements.append(f"UPDATE {table_name} SET {column.name} = gen_random_uuid() WHERE {column.name} IS NULL;")
                        elif 'utcnow' in str(column.default.arg):
                            sql_statements.append(f"UPDATE {table_name} SET {column.name} = CURRENT_TIMESTAMP WHERE {column.name} IS NULL;")
                    else:
                        sql_statements.append(f"UPDATE {table_name} SET {column.name} = {column.default} WHERE {column.name} IS NULL;")
                
                sql_statements.append(f"ALTER TABLE {table_name} ALTER COLUMN {column.name} SET NOT NULL;")
            else:
                if column.default is not None:
                    if hasattr(column.default, 'arg') and callable(column.default.arg):
                        if 'uuid' in str(column.default.arg):
                            col_def += " DEFAULT gen_random_uuid()"
                        elif 'utcnow' in str(column.default.arg):
                            col_def += " DEFAULT CURRENT_TIMESTAMP"
                    else:
                        # 处理默认值
                        default_val = str(column.default)
                        if 'ScalarElementColumnDefault' in default_val:
                            # 提取实际的默认值
                            if 'True' in default_val:
                                col_def += " DEFAULT TRUE"
                            elif 'False' in default_val:
                                col_def += " DEFAULT FALSE"
                            elif "'USD'" in default_val:
                                col_def += " DEFAULT 'USD'"
                            elif "'daily'" in default_val:
                                col_def += " DEFAULT 'daily'"
                            elif "'pending'" in default_val:
                                col_def += " DEFAULT 'pending'"
                            elif any(num in default_val for num in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                                # 尝试提取数字
                                import re
                                numbers = re.findall(r'[\d.]+', default_val)
                                if numbers:
                                    col_def += f" DEFAULT {numbers[0]}"
                        else:
                            col_def += f" DEFAULT {column.default}"
                sql_statements.append(f"ALTER TABLE {table_name} {col_def};")
                
        # 处理类型变更
        for change in changes['type_changes']:
            sql_statements.append(
                f"ALTER TABLE {table_name} ALTER COLUMN {change['column']} TYPE {change['new_type']};"
            )
            
        # 处理NULL约束变更
        for change in changes['nullable_changes']:
            if change['new_nullable']:
                sql_statements.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {change['column']} DROP NOT NULL;"
                )
            else:
                sql_statements.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {change['column']} SET NOT NULL;"
                )
                
        # 处理删除列（仅生成注释）
        for col_name in changes['removed_columns']:
            sql_statements.append(
                f"-- ALTER TABLE {table_name} DROP COLUMN {col_name}; -- 请手动确认是否删除"
            )
            
        return sql_statements
        
    def sync_all_models(self, execute: bool = False) -> Dict[str, Any]:
        """同步所有模型"""
        print(f"\n{Fore.MAGENTA}开始分析所有模型...{Style.RESET_ALL}")
        print(f"共发现 {len(self.models_registry)} 个模型\n")
        
        all_results = []
        all_sql_statements = []
        
        # 按模块分组显示
        models_by_module = {}
        for table_name, model_info in self.models_registry.items():
            module = model_info['module'].split('.')[1]  # 获取主模块名
            if module not in models_by_module:
                models_by_module[module] = []
            models_by_module[module].append((table_name, model_info))
            
        # 逐模块处理
        for module, models in sorted(models_by_module.items()):
            print(f"\n{Fore.MAGENTA}▶ 模块: {module}{Style.RESET_ALL}")
            
            for table_name, model_info in sorted(models):
                result = self.analyze_model(table_name, model_info)
                all_results.append(result)
                
                if result['sql_statements']:
                    all_sql_statements.extend(result['sql_statements'])
                    
        # 汇总统计
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}同步汇总{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        # 统计信息
        new_tables = sum(1 for r in all_results if not r['exists_in_db'])
        modified_tables = sum(1 for r in all_results if r['exists_in_db'] and r['sql_statements'])
        
        print(f"需要创建的表: {new_tables}")
        print(f"需要修改的表: {modified_tables}")
        print(f"生成的SQL语句: {len(all_sql_statements)}")
        
        # 保存SQL文件
        if all_sql_statements:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sql_file = f"model_sync_{timestamp}.sql"
            
            with open(sql_file, 'w', encoding='utf-8') as f:
                f.write("-- 数据库模型同步SQL语句\n")
                f.write(f"-- 生成时间: {datetime.now()}\n")
                f.write("-- 注意: 执行前请备份数据库!\n\n")
                
                # 按模型分组写入SQL
                current_module = None
                for result in all_results:
                    if result['sql_statements']:
                        module = result['module'].split('.')[1]
                        if module != current_module:
                            f.write(f"\n-- ========== 模块: {module} ==========\n")
                            current_module = module
                            
                        f.write(f"\n-- 表: {result['table_name']} (模型: {result['model_name']})\n")
                        for stmt in result['sql_statements']:
                            f.write(stmt + "\n")
                            
            print(f"\n{Fore.GREEN}✓ SQL语句已保存到: {sql_file}{Style.RESET_ALL}")
            
        # 执行SQL（如果需要）
        if execute and all_sql_statements:
            confirm = input(f"\n{Fore.RED}确认执行 {len(all_sql_statements)} 条SQL语句吗? (yes/no): {Style.RESET_ALL}")
            if confirm.lower() == 'yes':
                self._execute_sql(all_sql_statements)
                
        return {
            'total_models': len(self.models_registry),
            'new_tables': new_tables,
            'modified_tables': modified_tables,
            'sql_count': len(all_sql_statements),
            'results': all_results
        }
        
    def _execute_sql(self, sql_statements: List[str]):
        """执行SQL语句"""
        print(f"\n{Fore.YELLOW}开始执行SQL语句...{Style.RESET_ALL}")
        
        try:
            with self.engine.connect() as conn:
                trans = conn.begin()
                
                for i, statement in enumerate(sql_statements):
                    if statement.strip() and not statement.strip().startswith('--'):
                        print(f"执行 [{i+1}/{len(sql_statements)}]: {statement[:50]}...")
                        conn.execute(text(statement))
                        
                trans.commit()
                print(f"{Fore.GREEN}✓ 所有SQL语句执行成功{Style.RESET_ALL}")
                
        except SQLAlchemyError as e:
            trans.rollback()
            print(f"{Fore.RED}✗ 执行SQL时发生错误: {e}{Style.RESET_ALL}")
            

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库模型详细同步工具')
    parser.add_argument('--execute', action='store_true', help='执行生成的SQL语句')
    parser.add_argument('--filter', type=str, help='只同步特定模块（如: product, order）')
    
    args = parser.parse_args()
    
    try:
        print(f"{Fore.CYAN}数据库模型详细同步工具{Style.RESET_ALL}")
        print(f"使用数据库配置: {os.getenv('DATABASE_URL').split('@')[1] if '@' in os.getenv('DATABASE_URL') else 'localhost'}")
        
        sync_tool = ModelSyncTool()
        
        if args.filter:
            # TODO: 实现过滤功能
            print(f"过滤模块: {args.filter}")
            
        sync_tool.sync_all_models(execute=args.execute)
        
    except Exception as e:
        print(f"{Fore.RED}✗ 发生错误: {e}{Style.RESET_ALL}")
        logger.error(f"同步过程中发生错误: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()