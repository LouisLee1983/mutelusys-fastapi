# 国家和地区数据迁移说明

## 概述

此迁移包含了完整的全球国家和地区数据，专为MuteluSys佛教护身符电商系统设计，用于支持运费计算、关税管理和多语言国际化。

## 文件说明

### 1. 表结构迁移
**文件**: `20250625_171748_create_countries_and_regions_tables.sql`
- 创建 `countries` 表（国家主表）
- 创建 `country_translations` 表（国家翻译表）
- 创建 `regions` 表（地区表）
- 创建 `region_translations` 表（地区翻译表）
- 更新 `country_regions` 表（国家地区关联表）
- 创建必要的索引和触发器

### 2. 国家数据
**文件**: `20250625_171748_insert_global_countries_data.sql`
- 插入全球195个国家和地区的完整数据
- 包含ISO 3166-1 alpha-2和alpha-3代码
- 包含货币代码、电话区号等信息
- 提供完整的简体中文翻译

### 3. 地区数据
**文件**: `20250625_171748_insert_global_regions_data.sql`
- 插入30个地理和经济地区分组
- 包含洲际分组（亚洲、欧洲、北美等）
- 包含经济组织分组（欧盟、东盟、海合会等）
- 包含发展水平分组（发达国家、发展中国家等）
- 建立完整的国家-地区关联关系

### 4. 运行脚本
**文件**: `run_countries_regions_migration.py`
- 自动化执行所有迁移文件
- 提供执行进度和结果反馈
- 包含数据统计和验证

## 数据结构

### Countries 表字段
```sql
id           UUID        主键
code         VARCHAR(2)  ISO 3166-1 alpha-2代码 (如: CN, US, JP)
code3        VARCHAR(3)  ISO 3166-1 alpha-3代码 (如: CHN, USA, JPN)
name         VARCHAR(100) 英文名称
native_name  VARCHAR(100) 本地名称
currency     VARCHAR(3)  默认货币代码 (如: CNY, USD, JPY)
phone_code   VARCHAR(10) 电话区号 (如: +86, +1, +81)
status       VARCHAR(20) 状态 (active/inactive)
created_at   TIMESTAMP   创建时间
updated_at   TIMESTAMP   更新时间
```

### Country Translations 表字段
```sql
id          UUID        主键
country_id  UUID        国家ID (外键)
language    VARCHAR(10) 语言代码 (zh-CN, en-US, th-TH)
name        VARCHAR(100) 翻译名称
created_at  TIMESTAMP   创建时间
updated_at  TIMESTAMP   更新时间
```

### Regions 表字段
```sql
id          UUID        主键
code        VARCHAR(10) 地区代码 (如: ASIA, EU, ASEAN)
name        VARCHAR(100) 地区名称
description TEXT        地区描述
status      VARCHAR(20) 状态 (active/inactive)
created_at  TIMESTAMP   创建时间
updated_at  TIMESTAMP   更新时间
```

### Region Translations 表字段
```sql
id          UUID        主键
region_id   UUID        地区ID (外键)
language    VARCHAR(10) 语言代码
name        VARCHAR(100) 翻译名称
description TEXT        翻译描述
created_at  TIMESTAMP   创建时间
updated_at  TIMESTAMP   更新时间
```

### Country Regions 表字段
```sql
id          UUID        主键
country_id  UUID        国家ID (外键)
region_id   UUID        地区ID (外键)
created_at  TIMESTAMP   创建时间
```

## 地区分组说明

### 洲际分组
- **ASIA**: 亚洲国家和地区
- **EUROPE**: 欧洲国家和地区
- **NORTH_AMERICA**: 北美洲国家和地区
- **SOUTH_AMERICA**: 南美洲国家和地区
- **AFRICA**: 非洲国家和地区
- **OCEANIA**: 大洋洲国家和地区

### 细分地理区域
- **EAST_ASIA**: 东亚（中日韩等）
- **SOUTHEAST_ASIA**: 东南亚（东盟地区）
- **CENTRAL_ASIA**: 中亚国家
- **MIDDLE_EAST**: 中东国家
- **WESTERN_EUROPE**: 西欧国家
- **EASTERN_EUROPE**: 东欧国家
- **NORTHERN_EUROPE**: 北欧国家
- **SOUTHERN_EUROPE**: 南欧国家
- **NORTH_AFRICA**: 北非国家
- **WEST_AFRICA**: 西非国家
- **EAST_AFRICA**: 东非国家
- **SOUTHERN_AFRICA**: 南非地区国家
- **CENTRAL_AFRICA**: 中非国家
- **CARIBBEAN**: 加勒比海地区

### 经济组织分组
- **EU**: 欧盟成员国
- **ASEAN**: 东南亚国家联盟
- **GCC**: 海湾合作委员会
- **NAFTA**: 美墨加协定
- **MERCOSUR**: 南方共同市场
- **AU**: 非洲联盟
- **SAARC**: 南亚区域合作联盟

### 发展水平分组
- **DEVELOPED**: 发达国家（运费较低）
- **DEVELOPING**: 发展中国家（标准运费）
- **REMOTE_ISLANDS**: 偏远岛屿（运费较高）

## 使用方法

### 1. 环境准备
确保已设置数据库连接环境变量：
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_NAME=mutelu
```

### 2. 执行迁移

#### 方法一：使用Python脚本（推荐）
```bash
cd fastapi/migration_scripts
python run_countries_regions_migration.py
```

#### 方法二：手动执行SQL文件
```bash
cd fastapi/migration_scripts

# 1. 创建表结构
psql -h localhost -U postgres -d mutelu -f 20250625_171748_create_countries_and_regions_tables.sql

# 2. 插入国家数据
psql -h localhost -U postgres -d mutelu -f 20250625_171748_insert_global_countries_data.sql

# 3. 插入地区数据
psql -h localhost -U postgres -d mutelu -f 20250625_171748_insert_global_regions_data.sql
```

### 3. 验证数据
执行以下查询验证数据是否正确插入：

```sql
-- 检查国家数量
SELECT COUNT(*) as country_count FROM countries;

-- 检查地区数量
SELECT COUNT(*) as region_count FROM regions;

-- 检查中文翻译数量
SELECT COUNT(*) as translation_count 
FROM country_translations 
WHERE language = 'zh-CN';

-- 检查国家地区关联数量
SELECT COUNT(*) as association_count FROM country_regions;

-- 查看中国的信息和翻译
SELECT c.code, c.name, ct.name as chinese_name 
FROM countries c 
LEFT JOIN country_translations ct ON c.id = ct.country_id 
WHERE c.code = 'CN' AND ct.language = 'zh-CN';

-- 查看亚洲地区包含的国家数量
SELECT r.name, COUNT(cr.country_id) as country_count
FROM regions r
LEFT JOIN country_regions cr ON r.id = cr.region_id
WHERE r.code = 'ASIA'
GROUP BY r.id, r.name;
```

## 预期结果

成功执行后，您将获得：
- **195个国家和地区**的完整数据
- **195条简体中文翻译**
- **30个地区分组**
- **600+条国家地区关联关系**

## 注意事项

1. **备份数据库**: 执行前请备份现有数据库
2. **测试环境**: 建议先在测试环境验证
3. **权限要求**: 确保数据库用户有CREATE、INSERT权限
4. **编码设置**: 数据库应使用UTF-8编码以正确显示中文
5. **重复执行**: 脚本使用IF NOT EXISTS，可安全重复执行

## 故障排除

### 常见问题

1. **连接错误**: 检查数据库连接参数和网络连接
2. **权限错误**: 确保数据库用户有足够权限
3. **编码问题**: 确保数据库和客户端使用UTF-8编码
4. **重复键错误**: 检查是否已存在相同代码的国家或地区

### 日志位置
执行过程中的详细日志将输出到控制台，包括：
- 每个步骤的执行状态
- 错误信息和建议
- 最终的数据统计

## 扩展说明

此数据结构支持：
- **多语言扩展**: 可轻松添加泰语、英语等其他语言翻译
- **地区自定义**: 可根据业务需要添加自定义地区分组
- **运费计算**: 与shipping系统集成，支持基于地区的运费计算
- **关税管理**: 与duty系统集成，支持基于地区的关税计算
- **客户地址**: 与customer系统集成，支持地址验证和自动填充