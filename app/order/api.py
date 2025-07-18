from typing import Optional, List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_admin_user, get_current_customer
from app.order.schema import (
    OrderCreate, OrderResponse, OrderDetailResponse, OrderListResponse,
    OrderStatusUpdate, OrderPaymentStatusUpdate, OrderShippingStatusUpdate,
    OrderListParams, ResponseBase
)
from app.order.service import OrderService
from app.security.user.models import User


# 创建路由 - 兼容性保持
router = APIRouter()

# 管理端路由
admin_router = APIRouter(prefix="/admin")

# 用户端路由  
user_router = APIRouter(prefix="/user")

# 公开路由
public_router = APIRouter(prefix="/public")


# 用户端接口 - 订单创建（无需登录）
@public_router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: dict,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """创建订单
    
    用户可以创建新订单，包括商品、收货地址、支付方式等信息
    """
    try:
        from app.order.schema import OrderItemCreate, AddressInfo
        from app.customer.service import CustomerService
        
        # 解析订单项
        items = []
        for item_data in order_data["items"]:
            item = OrderItemCreate(**item_data)
            items.append(item)
        
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
        
        # 如果用户已登录且有客户ID，直接使用
        if current_user and current_user.customer_id:
            customer_id = current_user.customer_id
        else:
            # 如果用户已登录但没有客户ID，或者是游客，尝试基于邮箱查找/创建客户
            customer_email = shipping_address.email
            
            if customer_email:
                try:
                    # 查找现有客户
                    customer = CustomerService.get_customer_by_email(db, customer_email)
                    if customer:
                        customer_id = customer.id
                        # 如果用户已登录但没有关联客户，建立关联
                        if current_user and not current_user.customer_id:
                            current_user.customer_id = customer_id
                            db.commit()
                    else:
                        # 创建新的客户
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
                        # 如果用户已登录，建立关联
                        if current_user:
                            current_user.customer_id = customer_id
                            db.commit()
                except Exception as e:
                    # 如果客户创建失败，继续处理订单但不关联客户
                    print(f"创建客户失败: {e}")
        
        # 计算订单金额
        from decimal import Decimal
        subtotal = Decimal('0')
        for item in items:
            subtotal += item.unit_price * item.quantity
        
        shipping_amount = Decimal(str(order_data.get("shipping_amount", 0)))
        tax_amount = Decimal(str(order_data.get("tax_amount", 0)))
        discount_amount = Decimal(str(order_data.get("discount_amount", 0)))
        total_amount = subtotal + shipping_amount + tax_amount - discount_amount
        
        # 创建订单
        from app.order.schema import OrderCreate
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


# 用户端接口 - 需要登录
@user_router.get("/my-orders")
async def get_my_orders(
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """获取当前用户的订单列表
    
    已登录用户可以查看自己的订单历史
    """
    # 直接使用客户ID
    orders, total = OrderService.get_customer_orders(db, current_customer.id, page, page_size)
    pages = (total + page_size - 1) // page_size
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_items = [OrderResponse.model_validate(order) for order in orders]
    
    return {
        "code": 200,
        "message": "获取订单列表成功",
        "data": {
            "items": order_items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    }


@user_router.get("/my-orders/{order_id}")
async def get_my_order_detail(
    order_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """获取当前用户的订单详情
    
    用户可以查看自己的订单详细信息
    """
    # 获取订单
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 验证订单所有权
    if order.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此订单"
        )
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_data = OrderResponse.model_validate(order)
    
    return {
        "code": 200,
        "message": "获取订单详情成功",
        "data": order_data
    }


# 管理员接口
@admin_router.get("/orders", response_model=OrderListResponse)
async def get_orders_admin(
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    sort_by: str = Query("created_at"),
    sort_desc: bool = Query(True),
    # 过滤参数
    order_number: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    shipping_status: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    is_gift: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单列表（管理员）
    
    管理员可以获取所有订单，支持分页、排序和过滤
    """
    from app.order.schema import OrderFilter, OrderListParams
    from app.order.models import OrderStatus, PaymentStatus, ShippingStatus
    from datetime import datetime
    from uuid import UUID
    
    # 构造过滤条件
    filters = OrderFilter()
    if order_number:
        filters.order_number = order_number
    if customer_id:
        try:
            filters.customer_id = UUID(customer_id)
        except ValueError:
            pass
    if status:
        try:
            filters.status = OrderStatus(status)
        except ValueError:
            pass
    if payment_status:
        try:
            filters.payment_status = PaymentStatus(payment_status)
        except ValueError:
            pass
    if shipping_status:
        try:
            filters.shipping_status = ShippingStatus(shipping_status)
        except ValueError:
            pass
    if date_from:
        try:
            filters.date_from = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
        except ValueError:
            pass
    if date_to:
        try:
            filters.date_to = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
        except ValueError:
            pass
    if min_amount is not None:
        filters.min_amount = min_amount
    if max_amount is not None:
        filters.max_amount = max_amount
    if is_gift is not None:
        filters.is_gift = is_gift
    
    # 构造查询参数
    params = OrderListParams(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_desc=sort_desc,
        filters=filters if any([
            order_number, customer_id, status, payment_status, shipping_status,
            date_from, date_to, min_amount is not None, max_amount is not None, is_gift is not None
        ]) else None
    )
    
    orders, total = OrderService.get_orders(db, params)
    pages = (total + params.page_size - 1) // params.page_size
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_items = [OrderResponse.model_validate(order) for order in orders]
    
    return OrderListResponse(
        data={
            "items": order_items,
            "total": total,
            "page": params.page,
            "page_size": params.page_size,
            "pages": pages
        }
    )


@admin_router.get("/orders/{order_id}", response_model=OrderDetailResponse)
async def get_order_detail_admin(
    order_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单详情（管理员）
    
    管理员可以查看任何订单的详细信息
    """
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_data = OrderResponse.model_validate(order)
    
    return OrderDetailResponse(data=order_data)


@admin_router.get("/orders/number/{order_number}", response_model=OrderDetailResponse)
async def get_order_by_number_admin(
    order_number: str = Path(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """通过订单号获取订单详情（管理员）
    
    管理员可以通过订单号查询订单
    """
    order = OrderService.get_order_by_number(db, order_number)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_data = OrderResponse.model_validate(order)
    
    return OrderDetailResponse(data=order_data)


@admin_router.put("/orders/{order_id}/status", response_model=OrderDetailResponse)
async def update_order_status_admin(
    order_id: UUID,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新订单状态（管理员）
    
    管理员可以更新订单的状态
    """
    order = OrderService.update_order_status(db, order_id, status_data)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_data = OrderResponse.model_validate(order)
    
    return OrderDetailResponse(
        message=f"订单状态已更新为 {status_data.status.value}",
        data=order_data
    )


@admin_router.put("/orders/{order_id}/payment-status", response_model=OrderDetailResponse)
async def update_payment_status_admin(
    order_id: UUID,
    status_data: OrderPaymentStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新支付状态（管理员）
    
    管理员可以更新订单的支付状态
    """
    order = OrderService.update_payment_status(db, order_id, status_data)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_data = OrderResponse.model_validate(order)
    
    return OrderDetailResponse(
        message=f"支付状态已更新为 {status_data.payment_status.value}",
        data=order_data
    )


@admin_router.put("/orders/{order_id}/shipping-status", response_model=OrderDetailResponse)
async def update_shipping_status_admin(
    order_id: UUID,
    status_data: OrderShippingStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新物流状态（管理员）
    
    管理员可以更新订单的物流状态
    """
    order = OrderService.update_shipping_status(db, order_id, status_data)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_data = OrderResponse.model_validate(order)
    
    return OrderDetailResponse(
        message=f"物流状态已更新为 {status_data.shipping_status.value}",
        data=order_data
    )


# 关税相关接口
@admin_router.get("/orders/{order_id}/duty", response_model=Dict[str, Any])
async def get_order_duty_info(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单关税信息（管理员）
    
    管理员可以查看订单的关税计算详情
    """
    duty_info = OrderService.get_order_duty_info(db, order_id)
    if not duty_info:
        return ResponseBase(
            message="该订单无关税信息",
            data=None
        )
    
    return ResponseBase(
        message="获取订单关税信息成功",
        data=duty_info
    )


@admin_router.put("/orders/{order_id}/duty/status", response_model=Dict[str, Any])
async def update_order_duty_status(
    order_id: UUID,
    status_data: Dict[str, str] = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新订单关税状态（管理员）
    
    管理员可以更新订单的关税状态：calculated, confirmed, paid, disputed
    """
    new_status = status_data.get("status")
    if not new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="状态参数不能为空"
        )
    
    valid_statuses = ["calculated", "confirmed", "paid", "disputed"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的关税状态，支持的状态: {valid_statuses}"
        )
    
    duty_info = OrderService.update_order_duty_status(db, order_id, new_status)
    if not duty_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在或无关税信息"
        )
    
    return ResponseBase(
        message=f"关税状态已更新为 {new_status}",
        data=duty_info
    )


@admin_router.post("/orders/{order_id}/duty/recalculate", response_model=Dict[str, Any])
async def recalculate_order_duty(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """重新计算订单关税（管理员）
    
    当订单内容发生变化时，管理员可以重新计算关税
    """
    result = OrderService.recalculate_order_duty(db, order_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    return ResponseBase(
        message="关税重新计算完成",
        data=result
    )


@admin_router.get("/orders-with-duty", response_model=Dict[str, Any])
async def get_orders_with_duty(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取包含关税信息的订单列表（管理员）
    
    管理员可以查看所有有关税记录的订单
    """
    orders_with_duty, total = OrderService.get_orders_with_duty(db, page, page_size)
    
    return {
        "message": "获取关税订单列表成功",
        "data": {
            "items": orders_with_duty,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    }


# 用户端关税信息查询
@user_router.get("/my-orders/{order_id}/duty", response_model=Dict[str, Any])
async def get_my_order_duty_info(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    """获取用户订单关税信息
    
    用户可以查看自己订单的关税详情
    """
    # 先验证订单是否属于当前用户
    order = OrderService.get_order_by_id(db, order_id)
    if not order or order.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    duty_info = OrderService.get_order_duty_info(db, order_id)
    if not duty_info:
        return ResponseBase(
            message="该订单无关税信息",
            data=None
        )
    
    # 过滤敏感信息，只返回用户需要的信息
    user_duty_info = {
        "duty_amount": duty_info["duty_amount"],
        "currency": duty_info["currency"],
        "tax_rate": duty_info["tax_rate"],
        "taxable_amount": duty_info["taxable_amount"],
        "status": duty_info["status"],
        "created_at": duty_info["created_at"]
    }
    
    return ResponseBase(
        message="获取订单关税信息成功",
        data=user_duty_info
    )


@admin_router.get("/orders-count", response_model=ResponseBase)
async def count_orders_by_status_admin(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """统计各状态订单数量（管理员）
    
    管理员可以获取各种状态的订单数量统计
    """
    counts = OrderService.count_orders_by_status(db)
    return ResponseBase(data=counts)


@admin_router.get("/search-orders", response_model=OrderListResponse)
async def search_orders_admin(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """搜索订单（管理员）
    
    管理员可以搜索订单（订单号、客户名称、电话等）
    """
    orders, total = OrderService.search_orders(db, keyword, page, page_size)
    pages = (total + page_size - 1) // page_size
    
    # 将SQLAlchemy模型转换为Pydantic模型
    from app.order.schema import OrderResponse
    order_items = [OrderResponse.model_validate(order) for order in orders]
    
    return OrderListResponse(
        data={
            "items": order_items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        }
    )
