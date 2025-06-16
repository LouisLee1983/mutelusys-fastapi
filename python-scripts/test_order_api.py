#!/usr/bin/env python3
"""
测试订单API的脚本
用于验证订单管理API是否正常工作

运行方式：
1. 先激活虚拟环境：conda activate mutelu310
2. 进入fastapi目录：cd fastapi
3. 运行脚本：python python-scripts/test_order_api.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8008/api/v1"

def test_admin_login():
    """测试管理员登录"""
    print("测试管理员登录...")
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/admin/login", json=login_data)
    print(f"登录响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"登录成功: {result}")
        return result.get("data", {}).get("access_token")
    else:
        print(f"登录失败: {response.text}")
        return None

def test_order_list(token):
    """测试获取订单列表"""
    print("\n测试获取订单列表...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试基础列表
    response = requests.get(f"{BASE_URL}/admin/orders", headers=headers)
    print(f"订单列表响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"订单列表成功: 总数={result.get('data', {}).get('total', 0)}")
        items = result.get('data', {}).get('items', [])
        if items:
            print(f"第一个订单: {items[0].get('order_number', 'N/A')}")
            return items[0].get('id')
    else:
        print(f"订单列表失败: {response.text}")
        return None

def test_order_detail(token, order_id):
    """测试获取订单详情"""
    if not order_id:
        print("\n跳过订单详情测试 - 没有订单ID")
        return
        
    print(f"\n测试获取订单详情: {order_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/admin/orders/{order_id}", headers=headers)
    print(f"订单详情响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        order_data = result.get('data', {})
        print(f"订单详情成功: {order_data.get('order_number', 'N/A')}")
        print(f"订单状态: {order_data.get('status', 'N/A')}")
        print(f"订单金额: {order_data.get('total_amount', 'N/A')} {order_data.get('currency_code', 'N/A')}")
        print(f"订单项数量: {len(order_data.get('items', []))}")
    else:
        print(f"订单详情失败: {response.text}")

def test_order_stats(token):
    """测试获取订单统计"""
    print("\n测试获取订单统计...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/admin/orders-count", headers=headers)
    print(f"订单统计响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        stats = result.get('data', {})
        print(f"订单统计成功: {stats}")
    else:
        print(f"订单统计失败: {response.text}")

def test_order_search(token):
    """测试搜索订单"""
    print("\n测试搜索订单...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 搜索关键词
    params = {
        "keyword": "2024",
        "page": 1,
        "page_size": 10
    }
    
    response = requests.get(f"{BASE_URL}/admin/search-orders", headers=headers, params=params)
    print(f"搜索订单响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"搜索订单成功: 找到 {result.get('data', {}).get('total', 0)} 个订单")
    else:
        print(f"搜索订单失败: {response.text}")

def test_order_filters(token):
    """测试订单过滤"""
    print("\n测试订单过滤...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试状态过滤
    params = {
        "status": "PENDING",
        "page": 1,
        "page_size": 10
    }
    
    response = requests.get(f"{BASE_URL}/admin/orders", headers=headers, params=params)
    print(f"状态过滤响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"状态过滤成功: 找到 {result.get('data', {}).get('total', 0)} 个PENDING订单")
    else:
        print(f"状态过滤失败: {response.text}")

def main():
    """主函数"""
    print("开始测试订单API...")
    print(f"API基础URL: {BASE_URL}")
    print(f"测试时间: {datetime.now()}")
    
    # 1. 测试登录
    token = test_admin_login()
    if not token:
        print("登录失败，无法继续测试")
        return
    
    # 2. 测试订单列表
    order_id = test_order_list(token)
    
    # 3. 测试订单详情
    test_order_detail(token, order_id)
    
    # 4. 测试订单统计
    test_order_stats(token)
    
    # 5. 测试订单搜索
    test_order_search(token)
    
    # 6. 测试订单过滤
    test_order_filters(token)
    
    print("\n订单API测试完成！")

if __name__ == "__main__":
    main() 