"""
简化版API路由 - 仅包含基本功能以便启动
"""
from fastapi import APIRouter

# 创建主API路由器
api_router = APIRouter(prefix="/api/v1")

# 基本健康检查端点
@api_router.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok", "message": "FastAPI server is running"}

# 安全模块 - 基本认证
try:
    from app.security.user.api import router as user_router
    api_router.include_router(user_router, tags=["用户管理"])
except Exception as e:
    print(f"Warning: Could not load user router: {e}")

try:
    from app.security.role.api import router as role_router
    api_router.include_router(role_router, tags=["角色管理"])
except Exception as e:
    print(f"Warning: Could not load role router: {e}")

# 产品模块 - 核心功能
try:
    from app.product.api import router as product_router
    api_router.include_router(product_router, prefix="/products", tags=["商品管理"])
except Exception as e:
    print(f"Warning: Could not load product router: {e}")

try:
    from app.product.category.api import router as category_router
    api_router.include_router(category_router, prefix="/categories", tags=["产品类别"])
except Exception as e:
    print(f"Warning: Could not load category router: {e}")

# 客户模块
try:
    from app.customer.api import admin_router as customer_admin_router
    api_router.include_router(customer_admin_router, tags=["客户管理-后台"])
except Exception as e:
    print(f"Warning: Could not load customer router: {e}")

# 订单模块
try:
    from app.order.api import admin_router as order_admin_router
    api_router.include_router(order_admin_router, tags=["订单管理-后台"])
except Exception as e:
    print(f"Warning: Could not load order router: {e}")

print("简化版API路由加载完成")