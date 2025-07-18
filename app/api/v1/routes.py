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
api_router.include_router(attribute_router, prefix="/product/attributes", tags=["商品属性管理"])

from app.product.sku.api import router as sku_router
api_router.include_router(sku_router, prefix="/product/skus", tags=["产品SKU"])

from app.product.article.api import router as product_article_router
api_router.include_router(product_article_router, prefix="/admin/product/articles", tags=["产品文章管理"])

from app.product.inventory.api import router as inventory_router
api_router.include_router(inventory_router, prefix="/inventories", tags=["库存管理"])

from app.product.image.api import router as product_image_router
api_router.include_router(product_image_router, prefix="/product-images", tags=["商品图片管理"])

from app.product.price.api import router as product_price_router
api_router.include_router(product_price_router, tags=["商品价格管理"])

from app.product.translation.api import router as product_translation_router
api_router.include_router(product_translation_router, prefix="/product/translations", tags=["商品翻译管理"])

from app.product.article.api import router as product_article_router
api_router.include_router(product_article_router, prefix="/admin/product/articles", tags=["产品文章管理"])

# 订单模块
from app.order.api import admin_router as order_admin_router, user_router as order_user_router, public_router as order_public_router
api_router.include_router(order_admin_router, tags=["订单管理-后台"])
api_router.include_router(order_user_router, tags=["订单管理-用户端"])
api_router.include_router(order_public_router, tags=["订单管理-公开"])

from app.order.shipment.api import router as shipment_router
api_router.include_router(shipment_router, prefix="/order/shipments", tags=["订单发货"])

from app.order.return_.api import router as return_router
api_router.include_router(return_router, prefix="/order/returns", tags=["退货管理"])

# 支付模块
from app.payment.api import router as payment_router
api_router.include_router(payment_router, prefix="/payments", tags=["支付管理"])

# 物流模块已删除，使用order.shipment模块代替

# 营销模块
from app.marketing.coupon.api import router as coupon_router
api_router.include_router(coupon_router, prefix="/coupons", tags=["优惠券管理"])

from app.marketing.simple_promotion.api import router as simple_promotion_router
api_router.include_router(simple_promotion_router, prefix="/admin/promotions", tags=["促销管理"])

from app.order.promotion_api import router as order_promotion_router
api_router.include_router(order_promotion_router, prefix="/promotions", tags=["促销应用"])

# 算命模块
from app.fortune.api import router as fortune_router
from app.fortune.admin_api import router as fortune_admin_router
api_router.include_router(fortune_router, prefix="/fortune", tags=["算命功能"])
api_router.include_router(fortune_admin_router, prefix="/admin/fortune", tags=["算命管理-后台"])

from app.marketing.unified_promotion.api import router as unified_promotion_router
api_router.include_router(unified_promotion_router, prefix="/unified-promotions", tags=["统一促销"])

# 本地化模块
from app.localization.translation.api import router as translation_router
api_router.include_router(translation_router, prefix="/translations", tags=["翻译管理"])

# 内容管理模块
from app.content.blog.api import router as blog_router, public_router as blog_public_router, tag_router as blog_tag_router, category_router as blog_category_router
api_router.include_router(blog_router, prefix="/admin/blogs", tags=["博客管理-后台"])
api_router.include_router(blog_public_router, prefix="/public/blogs", tags=["博客管理-公开"])
api_router.include_router(blog_tag_router, prefix="/admin/blog-tags", tags=["博客标签管理"])
api_router.include_router(blog_category_router, prefix="/admin/blog-categories", tags=["博客分类管理"])

from app.content.page.api import router as page_router, public_router as page_public_router
api_router.include_router(page_router, prefix="/admin/pages", tags=["页面管理-后台"])
api_router.include_router(page_public_router, prefix="/public/pages", tags=["页面管理-公开"])

from app.content.banner.api import router as banner_router, public_router as banner_public_router
api_router.include_router(banner_router, prefix="/admin/banners", tags=["横幅管理-后台"])
api_router.include_router(banner_public_router, prefix="/public/banners", tags=["横幅管理-公开"])

from app.content.promotion.api import router as promotion_content_router, public_router as promotion_content_public_router, template_router as promotion_template_router
api_router.include_router(promotion_content_router, prefix="/admin/promotion-contents", tags=["促销内容管理-后台"])
api_router.include_router(promotion_content_public_router, prefix="/public/promotion-contents", tags=["促销内容管理-公开"])
api_router.include_router(promotion_template_router, prefix="/admin/promotion-templates", tags=["促销模板管理-后台"])

# 分析模块
from app.analytics.sales_report.api import router as sales_report_router
api_router.include_router(sales_report_router, prefix="/reports/sales", tags=["销售报表"])

from app.analytics.daily_summary.api import router as daily_summary_router
api_router.include_router(daily_summary_router, prefix="/admin/analytics", tags=["数据报表汇总"])

# AI助手模块
from app.api.v1.admin.ai_copilot import router as ai_copilot_router
api_router.include_router(ai_copilot_router, prefix="/admin/ai-copilot", tags=["AI助手"])

# 文件上传模块
from app.api.v1.admin.file_upload import router as file_upload_router
api_router.include_router(file_upload_router, prefix="/admin/file-upload", tags=["文件上传"])

# 政策管理模块
from app.api.v1.admin.policies import router as policies_router
api_router.include_router(policies_router, prefix="/admin", tags=["政策管理"])

# 快递运费模块
from app.shipping.api import admin_router as shipping_admin_router, public_router as shipping_public_router
api_router.include_router(shipping_admin_router, prefix="/admin/shipping", tags=["快递运费-后台"])
api_router.include_router(shipping_public_router, prefix="/public/shipping", tags=["快递运费-公开"])

# 国家地区管理模块
from app.localization.country.api import router as country_router
api_router.include_router(country_router, prefix="/admin/countries", tags=["国家地区管理"])

# 关税管理模块
from app.duty.api import router as duty_router
api_router.include_router(duty_router, prefix="/duty", tags=["关税管理"])

# 用户行为追踪模块
from app.modules.tracking.api import router as tracking_router
api_router.include_router(tracking_router, prefix="/tracking", tags=["用户行为追踪"])

# 注意：添加新模块的路由时，需要按照以上格式加入相应的import和include_router语句
# 如果模块的API还未开发完成，请使用注释标记待引入的路由 