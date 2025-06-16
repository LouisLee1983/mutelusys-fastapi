#!/usr/bin/env python3
"""
创建样本订单数据的脚本
用于测试订单管理功能

运行方式：
1. 先激活虚拟环境：conda activate mutelu310
2. 进入fastapi目录：cd fastapi
3. 运行脚本：python python-scripts/create_sample_orders.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.order.models import Order, OrderItem, OrderStatus, PaymentStatus, ShippingStatus, OrderItemStatus
from app.customer.models import Customer
from app.product.models import Product, ProductSku
from decimal import Decimal
import uuid
from datetime import datetime, timedelta
import random

# 数据库连接
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/mutelusys"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_sample_customers(db):
    """创建样本客户"""
    customers = []
    customer_data = [
        {"email": "john.doe@email.com", "first_name": "John", "last_name": "Doe", "phone": "+65 8123 4567"},
        {"email": "jane.smith@email.com", "first_name": "Jane", "last_name": "Smith", "phone": "+60 12 345 6789"},
        {"email": "alice.wong@email.com", "first_name": "Alice", "last_name": "Wong", "phone": "+66 81 234 5678"},
        {"email": "bob.chen@email.com", "first_name": "Bob", "last_name": "Chen", "phone": "+84 90 123 4567"},
        {"email": "linda.tan@email.com", "first_name": "Linda", "last_name": "Tan", "phone": "+63 915 123 4567"},
    ]
    
    for data in customer_data:
        # 检查客户是否已存在
        existing_customer = db.query(Customer).filter(Customer.email == data["email"]).first()
        if not existing_customer:
            customer = Customer(
                id=uuid.uuid4(),
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone_number=data["phone"],
                registration_source="sample_data",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(customer)
            customers.append(customer)
        else:
            customers.append(existing_customer)
    
    db.commit()
    return customers

def create_sample_products(db):
    """创建样本产品"""
    products = []
    product_data = [
        {"name": "佛教护身符", "sku_code": "BUD001", "price": "29.99"},
        {"name": "水晶能量手链", "sku_code": "CRY001", "price": "49.99"},
        {"name": "冥想垫", "sku_code": "MED001", "price": "89.99"},
        {"name": "藏香套装", "sku_code": "INC001", "price": "19.99"},
        {"name": "风水摆件", "sku_code": "FEN001", "price": "199.99"},
        {"name": "能量水晶球", "sku_code": "CRY002", "price": "129.99"},
        {"name": "佛教念珠", "sku_code": "BUD002", "price": "79.99"},
        {"name": "灵性塔罗牌", "sku_code": "TAR001", "price": "39.99"},
    ]
    
    for data in product_data:
        # 检查产品是否已存在
        existing_product = db.query(Product).filter(Product.name == data["name"]).first()
        if not existing_product:
            product = Product(
                id=uuid.uuid4(),
                name=data["name"],
                slug=data["name"].lower().replace(" ", "-"),
                status="ACTIVE",
                created_at=datetime.utcnow()
            )
            db.add(product)
            db.flush()  # 获取产品ID
            
            # 创建SKU
            sku = ProductSku(
                id=uuid.uuid4(),
                product_id=product.id,
                sku_code=data["sku_code"],
                price=Decimal(data["price"]),
                stock_quantity=100,
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(sku)
            products.append((product, sku))
        else:
            # 获取现有产品的SKU
            sku = db.query(ProductSku).filter(ProductSku.product_id == existing_product.id).first()
            products.append((existing_product, sku))
    
    db.commit()
    return products

def generate_order_number():
    """生成订单编号"""
    date_prefix = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"{date_prefix}{random_suffix}"

def create_sample_orders(db, customers, products):
    """创建样本订单"""
    orders = []
    
    # 订单状态分布
    statuses = [
        (OrderStatus.PENDING, PaymentStatus.PENDING, ShippingStatus.PENDING),
        (OrderStatus.PROCESSING, PaymentStatus.PAID, ShippingStatus.PROCESSING),
        (OrderStatus.SHIPPED, PaymentStatus.PAID, ShippingStatus.SHIPPED),
        (OrderStatus.DELIVERED, PaymentStatus.PAID, ShippingStatus.DELIVERED),
        (OrderStatus.CANCELLED, PaymentStatus.CANCELLED, ShippingStatus.PENDING),
    ]
    
    countries = ["Singapore", "Malaysia", "Thailand", "Indonesia", "Vietnam", "Philippines"]
    currencies = ["SGD", "MYR", "THB", "IDR", "VND", "PHP"]
    
    for i in range(20):  # 创建20个订单
        customer = random.choice(customers)
        order_status, payment_status, shipping_status = random.choice(statuses)
        country = random.choice(countries)
        currency = random.choice(currencies)
        
        # 选择1-3个产品
        num_items = random.randint(1, 3)
        selected_products = random.sample(products, num_items)
        
        # 计算订单金额
        subtotal = Decimal('0')
        order_items_data = []
        
        for product, sku in selected_products:
            quantity = random.randint(1, 3)
            unit_price = sku.price if sku else Decimal('29.99')
            item_subtotal = unit_price * quantity
            subtotal += item_subtotal
            
            order_items_data.append({
                'product': product,
                'sku': sku,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': item_subtotal
            })
        
        shipping_amount = Decimal('5.99')
        tax_amount = subtotal * Decimal('0.07')  # 7% 税率
        discount_amount = Decimal('0')
        if random.random() < 0.3:  # 30% 的订单有折扣
            discount_amount = subtotal * Decimal('0.1')  # 10% 折扣
        
        total_amount = subtotal + shipping_amount + tax_amount - discount_amount
        
        # 创建订单
        order = Order(
            id=uuid.uuid4(),
            order_number=generate_order_number(),
            customer_id=customer.id,
            status=order_status,
            payment_status=payment_status,
            shipping_status=shipping_status,
            currency_code=currency,
            subtotal=subtotal,
            shipping_amount=shipping_amount,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            total_amount=total_amount,
            paid_amount=total_amount if payment_status == PaymentStatus.PAID else Decimal('0'),
            # 收货信息
            shipping_name=f"{customer.first_name} {customer.last_name}",
            shipping_phone=customer.phone_number,
            shipping_email=customer.email,
            shipping_address1=f"{random.randint(1, 999)} Sample Street",
            shipping_city=random.choice(["Singapore", "Kuala Lumpur", "Bangkok", "Jakarta", "Ho Chi Minh", "Manila"]),
            shipping_country=country,
            shipping_postcode=str(random.randint(10000, 99999)),
            # 其他信息
            is_gift=random.random() < 0.2,  # 20% 是礼品订单
            customer_note="Sample order for testing" if random.random() < 0.3 else None,
            source="website",
            # 时间信息
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            paid_at=datetime.utcnow() - timedelta(days=random.randint(0, 25)) if payment_status == PaymentStatus.PAID else None,
            shipped_at=datetime.utcnow() - timedelta(days=random.randint(0, 20)) if shipping_status in [ShippingStatus.SHIPPED, ShippingStatus.DELIVERED] else None,
            delivered_at=datetime.utcnow() - timedelta(days=random.randint(0, 10)) if shipping_status == ShippingStatus.DELIVERED else None,
        )
        
        db.add(order)
        db.flush()  # 获取订单ID
        
        # 创建订单项
        for item_data in order_items_data:
            product = item_data['product']
            sku = item_data['sku']
            
            order_item = OrderItem(
                id=uuid.uuid4(),
                order_id=order.id,
                product_id=product.id,
                sku_id=sku.id if sku else None,
                status=OrderItemStatus.PENDING,
                name=product.name,
                sku_code=sku.sku_code if sku else "DEFAULT",
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                subtotal=item_data['subtotal'],
                discount_amount=Decimal('0'),
                tax_amount=item_data['subtotal'] * Decimal('0.07'),
                final_price=item_data['subtotal'] + (item_data['subtotal'] * Decimal('0.07')),
                created_at=order.created_at
            )
            db.add(order_item)
        
        orders.append(order)
    
    db.commit()
    return orders

def main():
    """主函数"""
    print("开始创建样本订单数据...")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建样本客户
        print("创建样本客户...")
        customers = create_sample_customers(db)
        print(f"创建了 {len(customers)} 个客户")
        
        # 创建样本产品
        print("创建样本产品...")
        products = create_sample_products(db)
        print(f"创建了 {len(products)} 个产品")
        
        # 创建样本订单
        print("创建样本订单...")
        orders = create_sample_orders(db, customers, products)
        print(f"创建了 {len(orders)} 个订单")
        
        print("样本数据创建完成！")
        
    except Exception as e:
        print(f"创建样本数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 