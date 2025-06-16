"""
API路由注册文件 (V1版本)
用于集中管理和注册所有模块的API路由
"""
from fastapi import APIRouter

# 创建主API路由器
api_router = APIRouter(prefix="/api/v1")

# C端公开API路由 - 无需认证
from app.api.v1.public_api import public_router
api_router.include_router(public_router)

# 安全模块 - 用户、角色与权限
from app.security.user.api import router as user_router
api_router.include_router(user_router, tags=["用户管理"])

from app.security.role.api import router as role_router
api_router.include_router(role_router, tags=["角色管理"])

from app.security.permission.api import router as permission_router
api_router.include_router(permission_router, tags=["权限管理"])

# 客户模块
from app.customer.api import admin_router as customer_admin_router
from app.customer.api import user_router as customer_user_router
from app.customer.api import public_router as customer_public_router
api_router.include_router(customer_admin_router, tags=["客户管理-后台"])
api_router.include_router(customer_user_router, tags=["客户管理-用户端"])
api_router.include_router(customer_public_router, tags=["客户管理-公开"])

from app.customer.address.api import admin_router as address_admin_router
from app.customer.address.api import user_router as address_user_router
api_router.include_router(address_admin_router, tags=["客户地址-后台"])
api_router.include_router(address_user_router, tags=["客户地址-用户端"])

# 产品模块
from app.product.api import router as product_router
api_router.include_router(product_router, prefix="/products", tags=["商品管理"])

from app.product.category.api import router as category_router
api_router.include_router(category_router, prefix="/categories", tags=["产品类别"])

from app.product.attribute.api import router as attribute_router
api_router.include_router(attribute_router, prefix="/product", tags=["商品属性管理"])

from app.product.sku.api import router as sku_router
api_router.include_router(sku_router, prefix="/product", tags=["产品SKU"])

from app.product.inventory.api import router as inventory_router
api_router.include_router(inventory_router, prefix="/inventories", tags=["库存管理"])

from app.product.image.api import router as product_image_router
api_router.include_router(product_image_router, prefix="/product-images", tags=["商品图片管理"])

from app.product.price.api import router as product_price_router
api_router.include_router(product_price_router, tags=["商品价格管理"])

from app.product.translation.api import router as product_translation_router
api_router.include_router(product_translation_router, tags=["商品翻译管理"])

# 订单模块
from app.order.api import admin_router as order_admin_router, user_router as order_user_router, public_router as order_public_router
api_router.include_router(order_admin_router, tags=["订单管理-后台"])
api_router.include_router(order_user_router, tags=["订单管理-用户端"])
api_router.include_router(order_public_router, tags=["订单管理-公开"])

from app.order.shipment.api import router as shipment_router
api_router.include_router(shipment_router, tags=["订单发货"])

from app.order.return_.api import router as return_router
api_router.include_router(return_router, tags=["退货管理"])

# 支付模块
from app.payment.api import router as payment_router
api_router.include_router(payment_router, tags=["支付管理"])

# 物流模块已删除，使用order.shipment模块代替

# 营销模块
from app.marketing.coupon.api import router as coupon_router
api_router.include_router(coupon_router, tags=["优惠券管理"])

# 本地化模块
from app.localization.translation.api import router as translation_router
api_router.include_router(translation_router, tags=["翻译管理"])

# 内容管理模块
from app.content.blog.api import router as blog_router
api_router.include_router(blog_router, tags=["博客管理"])

from app.content.page.api import router as page_router
api_router.include_router(page_router, tags=["页面管理"])

# 分析模块
from app.analytics.sales_report.api import router as sales_report_router
api_router.include_router(sales_report_router, tags=["销售报表"])

# AI助手模块
from app.api.v1.admin.ai_copilot import router as ai_copilot_router
api_router.include_router(ai_copilot_router, prefix="/admin/ai-copilot", tags=["AI助手"])

# 文件上传模块
from app.api.v1.admin.file_upload import router as file_upload_router
api_router.include_router(file_upload_router, prefix="/admin/file-upload", tags=["文件上传"])

# 政策管理模块
from app.api.v1.admin.policies import router as policies_router
api_router.include_router(policies_router, prefix="/admin", tags=["政策管理"])

# 注意：添加新模块的路由时，需要按照以上格式加入相应的import和include_router语句
# 如果模块的API还未开发完成，请使用注释标记待引入的路由 