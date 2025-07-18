# 配置文件

import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    # 数据库配置 - 设为必需字段
    DATABASE_URL: str = Field(..., description="数据库连接字符串")
    
    # JWT配置
    JWT_SECRET_KEY: str = Field(default="your_jwt_secret_key", description="JWT密钥")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT算法")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440, description="JWT过期时间(分钟)")
    
    # 项目配置
    PROJECT_NAME: str = Field(default="MUTELU", description="项目名称")
    
    # SMTP邮件配置
    SMTP_HOST: str = Field(default="smtp.163.com", description="SMTP服务器地址")
    SMTP_PORT: int = Field(default=465, description="SMTP服务器端口")
    SMTP_USER: str = Field(default="", description="SMTP用户名")
    SMTP_PASSWORD: str = Field(default="", description="SMTP密码")
    SMTP_TLS: bool = Field(default=False, description="是否使用TLS")
    SMTP_SSL: bool = Field(default=True, description="是否使用SSL")
    SMTP_TIMEOUT: int = Field(default=30, description="SMTP超时时间")
    SMTP_USE_SSL_CONTEXT: bool = Field(default=True, description="是否使用SSL上下文")
    SMTP_DEBUG: bool = Field(default=False, description="是否开启SMTP调试")

# 创建配置实例
settings = Settings()
