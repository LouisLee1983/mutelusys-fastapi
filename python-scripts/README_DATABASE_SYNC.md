# 数据库表结构同步工具使用说明

## 概述

这个工具用于将代码中的SQLAlchemy模型定义与PostgreSQL数据库中的实际表结构进行同步。当您修改了models.py文件中的类定义后，可以使用此工具自动生成ALTER TABLE语句来更新数据库结构。

新版本特性：
- 🔍 逐个模型类显示详细对比信息
- 🎨 彩色输出，更清晰的视觉反馈
- 📊 按模块分组展示模型变更
- 🔧 直接使用.env文件中的数据库配置
- 📝 生成结构化的SQL文件，便于审查

## 功能特性

- ✅ 自动检测新增的表和列
- ✅ 检测列类型、NULL约束的变化
- ✅ 生成PostgreSQL兼容的ALTER TABLE语句
- ✅ 支持数据库备份
- ✅ 交互式命令行界面
- ✅ 支持环境变量配置
- ✅ 安全的批量执行

## 支持的数据库

- PostgreSQL 9.6+
- 已测试版本：PostgreSQL 12, 13, 14, 15

## 安装依赖

```powershell
# 激活conda环境
conda activate mutelu310

# 安装依赖
pip install sqlalchemy psycopg2-binary
```

## 使用方法

### 快速开始

工具会自动从 `fastapi/.env` 文件读取数据库配置，无需手动设置。

双击运行批处理文件：
```
sync_models.bat
```

或者手动运行：
```bash
cd fastapi/python-scripts
python sync_models.py
```

### 交互式菜单

运行后会显示以下选项：
1. **分析差异（推荐）** - 只分析并显示差异，不生成SQL文件
2. **分析并生成SQL文件** - 分析差异并生成SQL文件供审查
3. **分析、生成并执行SQL（谨慎）** - 直接执行数据库修改

### 高级用法

使用详细同步工具获得更多控制：
```bash
# 显示详细的模型对比信息
python sync_models_detailed.py

# 直接执行SQL（谨慎使用）
python sync_models_detailed.py --execute

# 过滤特定模块（即将支持）
python sync_models_detailed.py --filter product
```

## 输出示例

工具会逐个模型显示详细的对比信息：

```
================================================================================
分析模型: Product
模块: app.product.models
表名: products
================================================================================
✓ 表已存在于数据库中

列对比:
  + new_field: VARCHAR(255)        # 新增列
  ~ price: NUMERIC → DECIMAL(10,2) # 类型变更
  ~ status: nullable True → False  # NULL约束变更
  - old_field (数据库中存在但模型中不存在) # 需要删除的列
```

## 安全建议

⚠️ **重要提醒：**

1. **生产环境操作前必须备份数据库**
2. **先在测试环境验证SQL语句**
3. **仔细检查生成的SQL文件**
4. **建议先使用"生成SQL"模式，手动审查后再执行**

## 支持的数据库变更

### 自动处理的变更
- 新增表
- 新增列（自动处理默认值和NULL约束）
- 修改列类型
- 修改NULL约束

### 需要手动处理的变更
- 删除表（会生成注释提醒）
- 删除列（会生成注释提醒）
- 重命名表或列
- 复杂的数据迁移

## 生成的SQL示例

```sql
-- 创建表: product_bundles
CREATE TABLE product_bundles (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 修改表: products
ALTER TABLE products ADD COLUMN main_image_url VARCHAR(512);
ALTER TABLE products ALTER COLUMN weight TYPE REAL;
```

## 故障排除

### 1. 连接数据库失败
- 检查数据库服务是否运行
- 验证用户名、密码、主机、端口
- 确认防火墙设置

### 2. 导入模块失败
```powershell
# 确保在正确的目录下运行
cd fastapi/python-scripts

# 检查Python路径
python -c "import sys; print(sys.path)"
```

### 3. SQLAlchemy错误
```powershell
# 重新安装依赖
pip uninstall sqlalchemy psycopg2-binary
pip install sqlalchemy psycopg2-binary
```

### 4. 权限不足
- 确保数据库用户有CREATE、ALTER、DROP权限
- 对于备份功能，需要有pg_dump访问权限

## 文件说明

### 主要脚本
- `sync_models.py` - 简化版同步工具，提供友好的交互界面
- `sync_models_detailed.py` - 详细版同步工具，提供完整的模型对比功能
- `sync_models.bat` - Windows批处理文件，快速启动工具

### 其他工具
- `init_database.py` - 初始化数据库，创建所有表
- `recreate_database.py` - 删除并重建所有表（危险操作）
- `import_category.py` - 导入商品分类数据

## 日志文件

工具会自动生成日志文件：
- `database_sync_YYYYMMDD_HHMMSS.log` - 详细执行日志
- `database_sync_YYYYMMDD_HHMMSS.sql` - 生成的SQL语句

## 最佳实践

1. **开发流程建议：**
   ```
   修改models.py → 运行同步工具 → 查看生成的SQL → 在测试环境验证 → 在生产环境执行
   ```

2. **定期备份：**
   - 每次执行前都备份数据库
   - 保留多个版本的备份文件

3. **版本控制：**
   - 将生成的SQL文件纳入版本控制
   - 记录每次数据库变更的原因

4. **团队协作：**
   - 在团队共享的测试环境验证
   - 统一的数据库迁移流程

## 联系支持

如果遇到问题，请检查：
1. 日志文件中的详细错误信息
2. 数据库连接配置
3. Python环境和依赖包版本 