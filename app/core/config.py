# 配置文件
# 数据库使用postgresql，ip：localhost，端口：5432，用户名：postgres，密码：Postgre,.1，数据库名：muteludb

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Postgre,.1@localhost:5432/muteludb")
    
    # JWT配置
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))
    
    # 项目配置
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "MUTELU")
    
    # SMTP邮件配置 - 163邮箱
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.163.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 465))  # 163邮箱SSL端口
    SMTP_USER: str = os.getenv("SMTP_USER", "muteluservice@163.com")  # 163邮箱地址
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "CX8wYdPeiRpsvAKF")  # 163邮箱应用密码
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "false").lower() == "true"  # 163使用SSL，不是TLS
    SMTP_SSL: bool = os.getenv("SMTP_SSL", "true").lower() == "true"  # 使用SSL
    SMTP_TIMEOUT: int = int(os.getenv("SMTP_TIMEOUT", 30))  # 连接超时时间
    SMTP_USE_SSL_CONTEXT: bool = os.getenv("SMTP_USE_SSL_CONTEXT", "true").lower() == "true"  # 使用SSL上下文
    SMTP_DEBUG: bool = os.getenv("SMTP_DEBUG", "false").lower() == "true"  # 调试模式

settings = Settings()
