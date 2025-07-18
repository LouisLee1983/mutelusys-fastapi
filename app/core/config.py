# 配置文件

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    # 数据库配置 - 移除默认值避免密码泄露
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # JWT配置
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24)))
    
    # 项目配置
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "MUTELU")
    
    # SMTP邮件配置 - 移除敏感信息的默认值
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.163.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USER: str = os.getenv("SMTP_USER")  # 移除默认邮箱地址
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")  # 移除默认密码
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "false").lower() == "true"
    SMTP_SSL: bool = os.getenv("SMTP_SSL", "true").lower() == "true"
    SMTP_TIMEOUT: int = int(os.getenv("SMTP_TIMEOUT", "30"))
    SMTP_USE_SSL_CONTEXT: bool = os.getenv("SMTP_USE_SSL_CONTEXT", "true").lower() == "true"
    SMTP_DEBUG: bool = os.getenv("SMTP_DEBUG", "false").lower() == "true"

def check_required_env_vars():
    """检查必要的环境变量是否已设置"""
    required_vars = {
        'DATABASE_URL': '数据库连接字符串',
    }
    
    missing_vars = []
    for var_name, description in required_vars.items():
        if not os.getenv(var_name):
            missing_vars.append(f"{var_name} ({description})")
    
    if missing_vars:
        error_msg = f"缺少必要的环境变量:\n" + "\n".join([f"  - {var}" for var in missing_vars])
        error_msg += f"\n\n请参考 .env.example 文件配置环境变量"
        raise ValueError(error_msg)

# 创建配置实例前先检查环境变量
check_required_env_vars()
settings = Settings()
