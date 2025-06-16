# 商品分类导入脚本使用说明

## 概述
这个脚本用于将JSON格式的商品分类数据导入到数据库中。

## 文件说明
- `import_category.py` - 主要的导入脚本
- `run_import_category.bat` - Windows批处理运行脚本
- `run_import_category.ps1` - PowerShell运行脚本
- `README_import_category.md` - 本说明文档

## 使用方法

### 方法一：直接运行Python脚本
1. 打开PowerShell
2. 激活conda环境：
   ```powershell
   conda activate mutelu310
   ```
3. 进入脚本目录：
   ```powershell
   cd fastapi/python-scripts
   ```
4. 运行脚本：
   ```powershell
   python import_category.py
   ```

### 方法二：使用PowerShell脚本
1. 打开PowerShell
2. 进入脚本目录：
   ```powershell
   cd fastapi/python-scripts
   ```
3. 运行PowerShell脚本：
   ```powershell
   .\run_import_category.ps1
   ```

### 方法三：使用批处理文件
1. 双击 `run_import_category.bat` 文件

## 功能特性

### 数据导入
- 支持三级分类结构（LEVEL_1, LEVEL_2, LEVEL_3）
- 自动创建分类翻译记录（默认中文）
- 递归导入子分类
- 防重复导入（基于slug检查）

### 数据验证
- JSON文件格式验证
- 数据库完整性检查
- 错误处理和回滚机制

### 统计信息
- 显示导入进度
- 提供分类统计信息
- 按层级统计分类数量

## 数据源
脚本会自动读取 `design-media/json-data/all-category.json` 文件中的分类数据。

## 注意事项

1. **数据库连接**：确保数据库服务正在运行且连接配置正确
2. **环境依赖**：需要激活 `mutelu310` conda环境
3. **数据备份**：建议在导入前备份现有数据
4. **清空选项**：脚本会询问是否清空现有分类数据，请谨慎选择

## 错误处理
- 如果JSON文件不存在或格式错误，脚本会提示错误并退出
- 如果数据库操作失败，会自动回滚事务
- 重复的slug会被跳过，不会导致错误

## 输出示例
```
开始导入商品分类数据...
成功加载JSON文件: /path/to/all-category.json
是否清空现有分类数据? (y/N): n
成功导入分类: 珠宝首饰 (JEWELRY) - Level: LEVEL_1
成功导入分类: 目录 (CATEGORIES) - Level: LEVEL_2
成功导入分类: 手链 (BRACELETS) - Level: LEVEL_3
...

导入完成! 总共导入了 XX 个分类

分类统计:
  一级分类: X
  二级分类: XX
  三级分类: XXX
  总计: XXX

分类数据导入成功!
```

## 技术细节
- 使用SQLAlchemy ORM进行数据库操作
- 支持事务管理和错误回滚
- 递归处理嵌套分类结构
- 自动生成UUID主键
- 支持多语言翻译扩展 