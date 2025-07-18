# -*- coding: utf-8 -*-
"""
快递运费API路由集合
包含所有子模块的路由，统一对外提供接口
"""
from fastapi import APIRouter

# 导入子模块路由
from .method.api import router as method_router
from .zone.api import router as zone_router  
from .rate.api import router as rate_router
from .free_rule.api import router as free_rule_router
from .calculation.api import router as calculation_router

# 创建管理端主路由器
admin_router = APIRouter(prefix="/admin")

# 创建公开接口主路由器  
public_router = APIRouter(prefix="/public")

# 注册子模块路由到管理端
admin_router.include_router(method_router, tags=["快递方式管理"])
admin_router.include_router(zone_router, tags=["运费地区管理"])
admin_router.include_router(rate_router, tags=["运费规则管理"])
admin_router.include_router(free_rule_router, tags=["免运费规则管理"])

# 注册公开接口路由
public_router.include_router(free_rule_router, tags=["免运费检查"])
public_router.include_router(calculation_router, tags=["运费计算"])

# 主路由器（向后兼容）
router = APIRouter()

# 包含管理端和公开路由
router.include_router(admin_router)
router.include_router(public_router) 