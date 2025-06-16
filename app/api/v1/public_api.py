"""
C端公开API路由 - 无需认证
提供商品展示、分类浏览、内容展示等公开接口
"""
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.product.category.service import ProductCategoryService
from app.product.service import ProductService
from app.product.sku.service import ProductSkuService

# 创建公开API路由器
public_router = APIRouter(prefix="/public", tags=["C端公开API"])

# 首页相关接口
@public_router.get("/home/banners")
async def get_home_banners(db: Session = Depends(get_db)):
    """获取首页轮播图/Banner"""
    # TODO: 实现Banner获取逻辑
    return {
        "code": 200,
        "message": "获取成功", 
        "data": {
            "banners": [
                {
                    "id": "1",
                    "title": "2025蛇年新品",
                    "image_url": "/images/banners/snake-2025.jpg",
                    "link_url": "/collections/snake-2025",
                    "sort_order": 1,
                    "is_active": True
                }
            ]
        }
    }

@public_router.get("/home/featured-products")
async def get_featured_products(
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取首页精选商品"""
    # TODO: 实现精选商品获取逻辑
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "products": [],
            "total": 0
        }
    }

@public_router.get("/home/trending-collections")
async def get_trending_collections(db: Session = Depends(get_db)):
    """获取热门专题"""
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "collections": []
        }
    }

# 商品相关接口
@public_router.get("/products")
async def get_public_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[UUID] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取商品列表（公开接口，只返回上架商品）"""
    try:
        # 调用商品服务获取公开商品列表
        result = ProductService.get_public_products(
            db, skip, limit, category_id, sort_by, sort_order, search
        )
        return {
            "code": 200,
            "message": "获取成功",
            "data": result
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取商品列表失败: {str(e)}",
            "data": {
                "items": [],
                "total": 0,
                "page": skip // limit + 1,
                "size": limit
            }
        }

@public_router.get("/products/{product_id}")
async def get_public_product_detail(
    product_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """获取商品详情（公开接口）"""
    try:
        result = ProductService.get_public_product_detail(db, product_id)
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "product": result
            }
        }
    except Exception as e:
        return {
            "code": 404,
            "message": f"商品不存在或已下架: {str(e)}",
            "data": {
                "product": None
            }
        }

@public_router.get("/products/{product_id}/skus")
async def get_public_product_skus(
    product_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """获取商品SKU列表（公开接口）"""
    try:
        result = ProductSkuService.get_public_product_skus(db, product_id)
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "skus": result
            }
        }
    except Exception as e:
        return {
            "code": 404,
            "message": f"商品SKU不存在: {str(e)}",
            "data": {
                "skus": []
            }
        }

@public_router.get("/products/search")
async def search_public_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """商品搜索（公开接口）"""
    try:
        result = ProductService.search_public_products(db, q, skip, limit)
        return {
            "code": 200,
            "message": "搜索成功",
            "data": result
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"搜索失败: {str(e)}",
            "data": {
                "items": [],
                "total": 0,
                "query": q,
                "page": skip // limit + 1,
                "size": limit
            }
        }

# 分类相关接口
@public_router.get("/categories")
async def get_public_categories(
    language_code: str = Query("zh-CN", description="语言代码，如zh-CN, en-US"),
    db: Session = Depends(get_db)
):
    """获取分类树形结构（公开接口）"""
    try:
        # 获取公开的分类树，只返回激活状态的分类
        result = ProductCategoryService.get_public_category_tree(db, language_code)
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "categories": result
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取分类失败: {str(e)}",
            "data": {
                "categories": []
            }
        }

@public_router.get("/categories/slug/{slug}")
async def get_public_category_by_slug(
    slug: str = Path(...),
    language_code: str = Query("zh-CN", description="语言代码，如zh-CN, en-US"),
    db: Session = Depends(get_db)
):
    """根据slug获取分类信息（公开接口）"""
    try:
        category = ProductCategoryService.get_category_by_slug(db, slug)
        if not category or not category.is_active:
            return {
                "code": 404,
                "message": "分类不存在或已下架",
                "data": {
                    "category": None
                }
            }
        
        # 获取子分类
        children = ProductCategoryService.get_children(db, category.id, recursive=True, language_code=language_code)
        
        category_data = ProductCategoryService._category_to_dict(category, language_code)
        category_data["children"] = children
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "category": category_data
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取分类失败: {str(e)}",
            "data": {
                "category": None
            }
        }

@public_router.get("/categories/slug/{slug}/products")
async def get_public_category_products_by_slug(
    slug: str = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    include_children: bool = Query(True, description="是否包含子分类的商品"),
    db: Session = Depends(get_db)
):
    """根据slug获取分类下的商品（公开接口）"""
    try:
        # 首先获取分类
        category = ProductCategoryService.get_category_by_slug(db, slug)
        if not category or not category.is_active:
            return {
                "code": 404,
                "message": "分类不存在或已下架",
                "data": {
                    "items": [],
                    "total": 0,
                    "category": None,
                    "page": skip // limit + 1,
                    "size": limit
                }
            }
        
        # 获取分类下的商品
        result = ProductService.get_public_category_products_by_slug(
            db, slug, skip, limit, sort_by, sort_order, include_children
        )
        
        # 添加分类信息
        category_data = ProductCategoryService._category_to_dict(category)
        result["category"] = category_data
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": result
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取分类商品失败: {str(e)}",
            "data": {
                "items": [],
                "total": 0,
                "category": None,
                "page": skip // limit + 1,
                "size": limit
            }
        }

@public_router.get("/categories/{category_id}/products")
async def get_public_category_products(
    category_id: UUID = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    """获取分类下的商品（公开接口）"""
    try:
        result = ProductService.get_public_category_products(
            db, category_id, skip, limit, sort_by, sort_order
        )
        return {
            "code": 200,
            "message": "获取成功",
            "data": result
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取分类商品失败: {str(e)}",
            "data": {
                "items": [],
                "total": 0,
                "category_id": str(category_id),
                "page": skip // limit + 1,
                "size": limit
            }
        }

# 内容相关接口
@public_router.get("/content/symbols")
async def get_public_symbols(db: Session = Depends(get_db)):
    """获取符号字典（公开接口）"""
    # TODO: 实现符号字典获取逻辑
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "symbols": []
        }
    }

@public_router.get("/content/materials")
async def get_public_materials(db: Session = Depends(get_db)):
    """获取材质信息（公开接口）"""
    # TODO: 实现材质信息获取逻辑
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "materials": []
        }
    }

@public_router.get("/content/intentions")
async def get_public_intentions(db: Session = Depends(get_db)):
    """获取意图指南（公开接口）"""
    # TODO: 实现意图指南获取逻辑
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "intentions": []
        }
    }

# 库存状态查询（已存在的公开接口）
@public_router.get("/inventory/sku/{sku_id}/status")
async def get_public_sku_inventory_status(
    sku_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """获取SKU库存状态（公开接口）"""
    # TODO: 实现库存状态获取逻辑
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "sku_id": str(sku_id),
            "in_stock": True,
            "quantity": 100,
            "status": "available"
        }
    }

# 订单相关接口
@public_router.post("/orders", status_code=201)
async def create_public_order(
    order_data: dict,
    db: Session = Depends(get_db)
):
    """创建订单（公开接口，支持游客下单）"""
    try:
        from app.order.service import OrderService
        from app.order.schema import OrderCreate, AddressInfo, OrderItemCreate
        from uuid import UUID
        from decimal import Decimal
        import ipaddress
        from fastapi import Request
        from app.customer.service import CustomerService
        
        # 解析订单数据
        items = []
        for item in order_data.get("items", []):
            items.append(OrderItemCreate(
                product_id=UUID(item["product_id"]),
                sku_id=UUID(item["sku_id"]) if item.get("sku_id") else None,
                quantity=int(item["quantity"]),
                unit_price=Decimal(str(item["unit_price"])),
                product_name=item["product_name"],
                sku_name=item.get("sku_name"),
                attributes=item.get("attributes")
            ))
        
        # 解析收货地址
        shipping_address_data = order_data["shipping_address"]
        # 处理空字符串email
        shipping_email = shipping_address_data.get("email")
        if shipping_email == "":
            shipping_email = None
            
        shipping_address = AddressInfo(
            name=shipping_address_data["name"],
            phone=shipping_address_data["phone"],
            email=shipping_email,
            address1=shipping_address_data["address1"],
            address2=shipping_address_data.get("address2"),
            city=shipping_address_data["city"],
            state=shipping_address_data.get("state"),
            country=shipping_address_data["country"],
            postcode=shipping_address_data["postcode"]
        )
        
        # 解析账单地址（如果提供）
        billing_address = None
        if order_data.get("billing_address"):
            billing_address_data = order_data["billing_address"]
            # 处理空字符串email
            billing_email = billing_address_data.get("email")
            if billing_email == "":
                billing_email = None
                
            billing_address = AddressInfo(
                name=billing_address_data["name"],
                phone=billing_address_data["phone"],
                email=billing_email,
                address1=billing_address_data["address1"],
                address2=billing_address_data.get("address2"),
                city=billing_address_data["city"],
                state=billing_address_data.get("state"),
                country=billing_address_data["country"],
                postcode=billing_address_data["postcode"]
            )
        
        # 处理客户信息
        customer_id = None
        customer_email = shipping_address.email
        
        # 如果提供了邮箱，尝试查找或创建客户
        if customer_email:
            try:
                # 查找现有客户
                customer = CustomerService.get_customer_by_email(db, customer_email)
                if customer:
                    customer_id = customer.id
                else:
                    # 创建新的游客客户
                    from app.customer.schema import CustomerCreatePublic
                    
                    # 安全地处理姓名分割
                    name_parts = []
                    if shipping_address.name and isinstance(shipping_address.name, str):
                        name_parts = shipping_address.name.strip().split()
                    
                    first_name = name_parts[0] if name_parts else ""
                    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                    
                    customer_create = CustomerCreatePublic(
                        email=customer_email,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=shipping_address.phone,
                        registration_source="website"
                    )
                    customer = CustomerService.create_customer_public(db, customer_create)
                    customer_id = customer.id
            except Exception as e:
                # 如果客户创建失败，继续处理订单但不关联客户
                print(f"创建客户失败: {e}")
        
        # 计算订单金额
        subtotal = Decimal('0')
        for item in items:
            subtotal += item.unit_price * item.quantity
        
        shipping_amount = Decimal(str(order_data.get("shipping_amount", 0)))
        tax_amount = Decimal(str(order_data.get("tax_amount", 0)))
        discount_amount = Decimal(str(order_data.get("discount_amount", 0)))
        total_amount = subtotal + shipping_amount + tax_amount - discount_amount
        
        # 创建订单
        order_create = OrderCreate(
            customer_id=customer_id,
            currency_code=order_data.get("currency_code", "USD"),
            subtotal=subtotal,
            shipping_amount=shipping_amount,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            total_amount=total_amount,
            items=items,
            shipping_address=shipping_address,
            billing_address=billing_address,
            coupon_code=order_data.get("coupon_code"),
            is_gift=order_data.get("is_gift", False),
            gift_message=order_data.get("gift_message"),
            customer_note=order_data.get("customer_note"),
            source="website",
            ip_address=order_data.get("ip_address"),
            user_agent=order_data.get("user_agent")
        )
        
        # 创建订单
        order = OrderService.create_order(db, order_create)
        
        return {
            "code": 201,
            "message": "订单创建成功",
            "data": {
                "order_id": str(order.id),
                "order_number": order.order_number,
                "total_amount": float(order.total_amount),
                "currency_code": order.currency_code,
                "status": order.status.value,
                "payment_status": order.payment_status.value,
                "created_at": order.created_at.isoformat()
            }
        }
        
    except Exception as e:
        return {
            "code": 400,
            "message": f"订单创建失败: {str(e)}",
            "data": None
        }

@public_router.get("/orders/{order_number}")
async def get_public_order_by_number(
    order_number: str = Path(...),
    db: Session = Depends(get_db)
):
    """通过订单号获取订单详情（公开接口）"""
    try:
        from app.order.service import OrderService
        
        # 获取订单
        order = OrderService.get_order_by_number(db, order_number)
        if not order:
            return {
                "code": 404,
                "message": "订单不存在",
                "data": None
            }
        
        # 构建订单详情响应
        order_items = []
        for item in order.items:
            order_items.append({
                "id": str(item.id),
                "product_id": str(item.product_id),
                "sku_id": str(item.sku_id) if item.sku_id else None,
                "product_name": item.name,
                "sku_name": item.sku_code,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "subtotal": float(item.subtotal),
                "attributes": item.attributes,
                "image_url": item.image_url
            })
        
        order_detail = {
            "id": str(order.id),
            "order_number": order.order_number,
            "status": order.status.value,
            "payment_status": order.payment_status.value,
            "shipping_status": order.shipping_status.value,
            "currency_code": order.currency_code,
            "subtotal": float(order.subtotal),
            "shipping_amount": float(order.shipping_amount),
            "tax_amount": float(order.tax_amount),
            "discount_amount": float(order.discount_amount),
            "total_amount": float(order.total_amount),
            "paid_amount": float(order.paid_amount),
            "shipping_address": {
                "name": order.shipping_name,
                "phone": order.shipping_phone,
                "email": order.shipping_email,
                "address1": order.shipping_address1,
                "address2": order.shipping_address2,
                "city": order.shipping_city,
                "state": order.shipping_state,
                "country": order.shipping_country,
                "postcode": order.shipping_postcode
            },
            "coupon_code": order.coupon_code,
            "is_gift": order.is_gift,
            "gift_message": order.gift_message,
            "customer_note": order.customer_note,
            "items": order_items,
            "created_at": order.created_at.isoformat(),
            "updated_at": order.updated_at.isoformat(),
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
            "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None
        }
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "order": order_detail
            }
        }
        
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取订单详情失败: {str(e)}",
            "data": None
        }

# ============== 政策内容相关API ==============

@public_router.get(
    "/policies",
    summary="获取所有政策内容",
    description="获取商品详情页展示的政策内容，包括运输政策、退款政策、关于我们",
    tags=["商品展示"]
)
async def get_policies(language: str = "en"):
    """获取所有政策内容（支持多语言）"""
    try:
        from pathlib import Path
        import json
        
        policies_dir = Path("static/policies")
        policies = []
        
        # 政策类型定义
        policy_types = {
            "shipping": "SHIPPING POLICY",
            "refund": "REFUND POLICY",
            "about": "ABOUT MUTELU"
        }
        
        for policy_type, title in policy_types.items():
            # 构建文件名
            if language == "en":
                filename = f"{policy_type}.md"
            else:
                filename = f"{policy_type}_{language}.md"
            
            file_path = policies_dir / filename
            
            # 如果指定语言的文件不存在，回退到英文版本
            if not file_path.exists() and language != "en":
                file_path = policies_dir / f"{policy_type}.md"
            
            # 读取文件内容
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    policies.append({
                        "type": policy_type,
                        "title": title,
                        "content": content
                    })
                except Exception as e:
                    logger.error(f"读取政策文件失败 {file_path}: {e}")
                    continue
        
        return {
            "code": 200,
            "message": "成功",
            "data": {
                "policies": policies,
                "language": language
            }
        }
    except Exception as e:
        logger.error(f"获取政策内容失败: {e}")
        return {
            "code": 500,
            "message": "获取政策内容失败",
            "data": None
        }

@public_router.get(
    "/policies/{policy_type}",
    summary="获取指定政策内容",
    description="获取指定类型的政策内容",
    tags=["商品展示"]
)
async def get_policy(policy_type: str, language: str = "en"):
    """获取指定政策内容（支持多语言）"""
    try:
        from pathlib import Path
        
        policies_dir = Path("static/policies")
        
        # 政策类型定义
        policy_types = {
            "shipping": "SHIPPING POLICY",
            "refund": "REFUND POLICY",
            "about": "ABOUT MUTELU"
        }
        
        if policy_type not in policy_types:
            return {
                "code": 404,
                "message": "政策类型不存在",
                "data": None
            }
        
        # 构建文件名
        if language == "en":
            filename = f"{policy_type}.md"
        else:
            filename = f"{policy_type}_{language}.md"
        
        file_path = policies_dir / filename
        
        # 如果指定语言的文件不存在，回退到英文版本
        if not file_path.exists() and language != "en":
            file_path = policies_dir / f"{policy_type}.md"
        
        if not file_path.exists():
            return {
                "code": 404,
                "message": "政策内容不存在",
                "data": None
            }
        
        # 读取文件内容
        content = file_path.read_text(encoding='utf-8')
        
        return {
            "code": 200,
            "message": "成功",
            "data": {
                "policy": {
                    "type": policy_type,
                    "title": policy_types[policy_type],
                    "content": content
                },
                "language": language
            }
        }
    except Exception as e:
        logger.error(f"获取政策内容失败: {e}")
        return {
            "code": 500,
            "message": "获取政策内容失败",
            "data": None
        } 