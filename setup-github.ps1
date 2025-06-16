# FastAPI 项目 GitHub 仓库设置脚本

Write-Host "=== Mutelusys FastAPI GitHub 仓库设置 ===" -ForegroundColor Green

# 检查是否已经是 Git 仓库
if (Test-Path ".git") {
    Write-Host "检测到现有 Git 仓库，重新初始化..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".git"
}

# 初始化 Git 仓库
Write-Host "初始化 Git 仓库..." -ForegroundColor Blue
git init

# 添加所有文件
Write-Host "添加项目文件..." -ForegroundColor Blue
git add .

# 创建初始提交
Write-Host "创建初始提交..." -ForegroundColor Blue
git commit -m "Initial commit: FastAPI backend with Docker and GitHub Actions"

# 设置主分支名称
git branch -M main

Write-Host "=== 手动步骤 ===" -ForegroundColor Yellow
Write-Host "1. 在 GitHub 上创建新仓库 'mutelusys-fastapi'"
Write-Host "2. 复制仓库的 HTTPS 或 SSH URL"
Write-Host "3. 运行以下命令添加远程仓库："
Write-Host "   git remote add origin <您的仓库URL>"
Write-Host "4. 推送代码："
Write-Host "   git push -u origin main"

Write-Host ""
Write-Host "=== GitHub Secrets 配置 ===" -ForegroundColor Cyan
Write-Host "在 GitHub 仓库的 Settings > Secrets and variables > Actions 中添加："
Write-Host "- SERVER_HOST: 您的服务器 IP 地址"
Write-Host "- SERVER_USERNAME: 服务器用户名"
Write-Host "- SERVER_SSH_KEY: 服务器的 SSH 私钥内容"
Write-Host "- SERVER_PORT: SSH 端口（可选，默认 22）"

Write-Host ""
Write-Host "=== 云服务器设置 ===" -ForegroundColor Magenta
Write-Host "在您的 Ubuntu 服务器上运行："
Write-Host "sudo apt update && sudo apt install -y git docker.io docker-compose"
Write-Host "sudo usermod -aG docker `$USER"
Write-Host "mkdir -p /var/www/fastapi"
Write-Host "cd /var/www/fastapi"
Write-Host "git clone <您的仓库URL> ."
Write-Host "cp .env.example .env"
Write-Host "# 编辑 .env 文件配置数据库等信息"
Write-Host "docker network create mutelusys-network"
Write-Host "docker-compose up -d"

Write-Host ""
Write-Host "设置完成！现在您可以通过推送代码到 main 分支来触发自动部署。" -ForegroundColor Green 