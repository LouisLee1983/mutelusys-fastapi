"""
主API路由注册文件
用于集中管理和注册所有API路由，并按版本进行组织
"""
from fastapi import APIRouter

# 创建主API路由器
api_router = APIRouter()

# 导入并包含v1版本的API路由
from app.api.v1.routes import api_router as api_v1_router
api_router.include_router(api_v1_router)

# 未来可以添加其他版本的API路由
# 例如:
# from app.api.v2.routes import api_router as api_v2_router
# api_router.include_router(api_v2_router) 