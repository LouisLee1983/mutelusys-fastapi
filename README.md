# Mutelusys FastAPI Backend

这是 Mutelusys 项目的 FastAPI 后端服务。

## 功能特性

- 基于 FastAPI 的高性能 API 服务
- JWT 认证机制
- 数据库支持（MySQL/PostgreSQL）
- 自动化 API 文档生成
- Docker 容器化部署
- GitHub Actions 自动部署

## 本地开发

### 环境要求

- Python 3.10+
- MySQL 或 PostgreSQL 数据库
- 推荐使用 conda 虚拟环境

### 安装依赖

```bash
# 激活虚拟环境
conda activate mutelu310

# 安装依赖
pip install -r requirements.txt
```

### 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 启动服务

```bash
python main.py
```

API 文档将在 http://localhost:8008/docs 可用。

## Docker 部署

### 构建镜像

```bash
docker build -t mutelusys-fastapi .
```

### 使用 Docker Compose 启动

```bash
docker-compose up -d
```

## 自动化部署

项目配置了 GitHub Actions 自动部署：

1. 推送代码到 main 分支
2. GitHub Actions 自动触发部署
3. 在服务器上拉取最新代码并重新构建容器

### 需要在 GitHub 仓库设置的 Secrets：

- `SERVER_HOST`: 服务器 IP 地址
- `SERVER_USERNAME`: 服务器用户名
- `SERVER_SSH_KEY`: 服务器 SSH 私钥
- `SERVER_PORT`: SSH 端口（可选，默认 22）

## API 接口

- 基础路径：`/api/v1/`
- 公共接口：`/api/v1/public/`
- 用户接口：`/api/v1/user/`
- 管理员接口：`/api/v1/admin/`

详细 API 文档请访问：http://your-domain:8008/docs

## 目录结构

```
fastapi/
├── app/                 # 应用代码
├── static/             # 静态文件
├── main.py             # 应用入口
├── requirements.txt    # Python 依赖
├── Dockerfile         # Docker 镜像配置
├── docker-compose.yml # Docker Compose 配置
└── .github/           # GitHub Actions 配置
``` 