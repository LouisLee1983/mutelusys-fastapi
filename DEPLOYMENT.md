# Mutelusys FastAPI 部署指南

## 第一步：创建 GitHub 仓库

1. 登录 GitHub，创建新仓库 `mutelusys-fastapi`
2. 复制仓库的 HTTPS 或 SSH URL

## 第二步：推送代码到 GitHub

在本地 fastapi 目录运行：

```bash
# 添加远程仓库（替换为你的仓库 URL）
git remote add origin https://github.com/你的用户名/mutelusys-fastapi.git

# 推送代码
git push -u origin main
```

## 第三步：配置 GitHub Secrets

在 GitHub 仓库的 Settings > Secrets and variables > Actions 中添加：

- `SERVER_HOST`: 你的云服务器 IP 地址
- `SERVER_USERNAME`: 服务器用户名（如 ubuntu）
- `SERVER_SSH_KEY`: 服务器的 SSH 私钥内容
- `SERVER_PORT`: SSH 端口（可选，默认 22）

### 如何获取 SSH 私钥：

在你的本地电脑生成 SSH 密钥对：

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

将公钥添加到阿里云服务器（推荐在阿里云控制台配置，或使用以下命令）：

```bash
ssh-copy-id username@your-server-ip
```

如果是阿里云 ECS，也可以在控制台的"网络与安全" > "密钥对"中管理 SSH 密钥。

将私钥内容复制到 GitHub Secrets 中。

## 第四步：云服务器环境准备

在你的阿里云 Linux 服务器上运行：

```bash
# 更新系统（阿里云 Linux 使用 yum）
sudo yum update -y

# 安装必要软件
sudo yum install -y git

# 安装 Docker（阿里云 Linux 推荐方式）
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证 Docker Compose 安装
docker-compose --version

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 重新登录或运行
newgrp docker

# 创建项目目录
sudo mkdir -p /var/www/fastapi
sudo chown $USER:$USER /var/www/fastapi

# 克隆仓库
cd /var/www/fastapi
git clone https://github.com/LouisLee1983/mutelusys-fastapi.git .

# 配置环境变量
cp .env.example .env
vi .env  # 阿里云 Linux 默认使用 vi 编辑器

# 创建 Docker 网络
docker network create mutelusys-network

# 首次部署
docker-compose up -d
```

## 第五步：配置环境变量

编辑 `/var/www/fastapi/.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name

# JWT 配置
SECRET_KEY=your-very-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 其他配置
DEBUG=False
```

## 第六步：测试自动部署

1. 在本地修改一些代码
2. 提交并推送到 main 分支：

```bash
git add .
git commit -m "Test auto deployment"
git push origin main
```

3. 查看 GitHub Actions 页面，应该能看到部署流程自动执行
4. 部署完成后，访问 `http://你的服务器IP:8008/docs` 查看 API 文档

## 常用命令

### 查看容器状态
```bash
cd /var/www/fastapi
docker-compose ps
```

### 查看日志
```bash
docker-compose logs -f fastapi
```

### 手动重新部署
```bash
cd /var/www/fastapi
git pull origin main
docker-compose up -d --build
```

### 停止服务
```bash
docker-compose down
```

## 阿里云特殊配置

### 安全组配置
在阿里云 ECS 控制台配置安全组，开放以下端口：
- SSH 端口：22
- API 服务端口：8008
- 其他需要的端口

### 防火墙配置（如果启用了 firewalld）
```bash
# 检查防火墙状态
sudo systemctl status firewalld

# 如果启用了防火墙，开放必要端口
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --permanent --add-port=8008/tcp
sudo firewall-cmd --reload
```

## 故障排除

1. **GitHub Actions 失败**：检查 Secrets 配置是否正确
2. **容器启动失败**：检查 `.env` 文件配置和数据库连接
3. **端口冲突**：修改 `docker-compose.yml` 中的端口映射
4. **权限问题**：确保用户在 docker 组中
5. **阿里云网络问题**：检查安全组和防火墙配置

## 部署流程说明

每次推送代码到 main 分支时，GitHub Actions 会自动：

1. 连接到你的服务器
2. 拉取最新代码
3. 停止现有容器
4. 重新构建并启动容器
5. 清理未使用的镜像

这样你就不需要手动部署了，只需要专注于代码开发！ 