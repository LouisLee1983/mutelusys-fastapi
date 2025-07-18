# -*- coding: utf-8 -*-
"""
订单运费记录Pydantic模型
包含订单收费项目和运费记录的请求、响应模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


# ==================== 订单收费项目模型 ====================

class OrderChargeItemBase(BaseModel):
    """订单收费项目基础模型"""
    order_id: str = Field(..., max_length=50, description="订单号")
    item_type: str = Field(..., max_length=20, description="收费项目类型")
    item_code: Optional[str] = Field(None, max_length=50, description="项目代码")
    item_name: str = Field(..., max_length=100, description="项目名称")
    item_description: Optional[str] = Field(None, description="项目描述")
    amount: Decimal = Field(..., description="收费金额")
    currency_code: str = Field("USD", max_length=3, description="货币代码")
    metadata: Optional[Dict[str, Any]] = Field(None, description="扩展元数据")


class OrderChargeItemCreate(OrderChargeItemBase):
    """订单收费项目创建模型"""
    shipping_method_id: Optional[UUID] = Field(None, description="快递方式ID")
    shipping_zone_id: Optional[UUID] = Field(None, description="运费地区ID")
    free_shipping_rule_id: Optional[UUID] = Field(None, description="免运费规则ID")


class OrderChargeItemUpdate(BaseModel):
    """订单收费项目更新模型"""
    item_name: Optional[str] = Field(None, max_length=100, description="项目名称")
    item_description: Optional[str] = Field(None, description="项目描述")
    amount: Optional[Decimal] = Field(None, description="收费金额")
    metadata: Optional[Dict[str, Any]] = Field(None, description="扩展元数据")
    is_active: Optional[bool] = Field(None, description="是否启用")


class OrderChargeItemResponse(OrderChargeItemBase):
    """订单收费项目响应模型"""
    id: UUID = Field(..., description="收费项目ID")
    shipping_method_id: Optional[UUID] = Field(None, description="快递方式ID")
    shipping_zone_id: Optional[UUID] = Field(None, description="运费地区ID")
    free_shipping_rule_id: Optional[UUID] = Field(None, description="免运费规则ID")
    is_active: bool = Field(..., description="是否启用")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


# ==================== 订单运费记录模型 ====================

class OrderShippingInfoBase(BaseModel):
    """订单运费记录基础模型"""
    order_id: str = Field(..., max_length=50, description="订单号")
    
    # 收货地址信息
    country_code: str = Field(..., max_length=2, description="收货国家代码")
    state_province: Optional[str] = Field(None, max_length=50, description="州/省")
    city: Optional[str] = Field(None, max_length=50, description="城市")
    postal_code: Optional[str] = Field(None, max_length=20, description="邮政编码")
    full_address: Optional[str] = Field(None, description="完整地址")
    
    # 商品信息
    total_quantity: int = Field(..., ge=1, description="商品总件数")
    total_amount: Decimal = Field(..., ge=0, description="商品总金额")
    currency_code: str = Field("USD", max_length=3, description="货币代码")


class OrderShippingInfoCreate(OrderShippingInfoBase):
    """订单运费记录创建模型"""
    # 快递信息
    shipping_method_id: UUID = Field(..., description="选择的快递方式ID")
    shipping_method_code: str = Field(..., max_length=20, description="快递方式代码")
    shipping_method_name: str = Field(..., max_length=100, description="快递方式名称")
    shipping_company: Optional[str] = Field(None, max_length=100, description="快递公司名称")
    transport_type: Optional[str] = Field(None, max_length=20, description="运输类型")
    
    # 运费地区信息
    shipping_zone_id: UUID = Field(..., description="运费地区ID")
    shipping_zone_name: str = Field(..., max_length=100, description="运费地区名称")
    
    # 运费计算结果
    base_shipping_cost: Decimal = Field(..., description="基础运费")
    discount_amount: Decimal = Field(0, description="折扣金额")
    final_shipping_cost: Decimal = Field(..., description="最终运费")
    
    # 免运费信息
    is_free_shipping: bool = Field(False, description="是否免运费")
    free_shipping_rule_id: Optional[UUID] = Field(None, description="应用的免运费规则ID")
    free_shipping_rule_name: Optional[str] = Field(None, max_length=100, description="免运费规则名称")
    free_shipping_reason: Optional[str] = Field(None, max_length=200, description="免运费原因")
    savings_amount: Optional[Decimal] = Field(None, description="节省的运费金额")
    
    # 配送时间预估
    estimated_delivery_days: Optional[int] = Field(None, description="预估配送天数")
    min_delivery_days: Optional[int] = Field(None, description="最小配送天数")
    max_delivery_days: Optional[int] = Field(None, description="最大配送天数")
    delivery_time_text: Optional[str] = Field(None, max_length=100, description="配送时间文本描述")
    
    # 计算详情
    calculation_details: Optional[Dict[str, Any]] = Field(None, description="运费计算详情")
    calculation_metadata: Optional[Dict[str, Any]] = Field(None, description="计算过程元数据")


class OrderShippingInfoUpdate(BaseModel):
    """订单运费记录更新模型"""
    # 跟踪信息
    tracking_number: Optional[str] = Field(None, max_length=100, description="快递单号")
    tracking_url: Optional[str] = Field(None, max_length=500, description="跟踪链接")
    shipping_status: Optional[str] = Field(None, max_length=20, description="发货状态")
    shipped_at: Optional[datetime] = Field(None, description="发货时间")
    delivered_at: Optional[datetime] = Field(None, description="签收时间")
    
    # 地址信息更新
    country_code: Optional[str] = Field(None, max_length=2, description="收货国家代码")
    state_province: Optional[str] = Field(None, max_length=50, description="州/省")
    city: Optional[str] = Field(None, max_length=50, description="城市")
    postal_code: Optional[str] = Field(None, max_length=20, description="邮政编码")
    full_address: Optional[str] = Field(None, description="完整地址")


class OrderShippingInfoResponse(OrderShippingInfoBase):
    """订单运费记录响应模型"""
    id: UUID = Field(..., description="运费记录ID")
    
    # 快递信息
    shipping_method_id: UUID = Field(..., description="选择的快递方式ID")
    shipping_method_code: str = Field(..., description="快递方式代码")
    shipping_method_name: str = Field(..., description="快递方式名称")
    shipping_company: Optional[str] = Field(None, description="快递公司名称")
    transport_type: Optional[str] = Field(None, description="运输类型")
    
    # 运费地区信息
    shipping_zone_id: UUID = Field(..., description="运费地区ID")
    shipping_zone_name: str = Field(..., description="运费地区名称")
    
    # 运费计算结果
    base_shipping_cost: Decimal = Field(..., description="基础运费")
    discount_amount: Decimal = Field(..., description="折扣金额")
    final_shipping_cost: Decimal = Field(..., description="最终运费")
    
    # 免运费信息
    is_free_shipping: bool = Field(..., description="是否免运费")
    free_shipping_rule_id: Optional[UUID] = Field(None, description="应用的免运费规则ID")
    free_shipping_rule_name: Optional[str] = Field(None, description="免运费规则名称")
    free_shipping_reason: Optional[str] = Field(None, description="免运费原因")
    savings_amount: Optional[Decimal] = Field(None, description="节省的运费金额")
    
    # 配送时间预估
    estimated_delivery_days: Optional[int] = Field(None, description="预估配送天数")
    min_delivery_days: Optional[int] = Field(None, description="最小配送天数")
    max_delivery_days: Optional[int] = Field(None, description="最大配送天数")
    delivery_time_text: Optional[str] = Field(None, description="配送时间文本描述")
    
    # 跟踪信息
    tracking_number: Optional[str] = Field(None, description="快递单号")
    tracking_url: Optional[str] = Field(None, description="跟踪链接")
    shipping_status: str = Field(..., description="发货状态")
    shipped_at: Optional[datetime] = Field(None, description="发货时间")
    delivered_at: Optional[datetime] = Field(None, description="签收时间")
    
    # 计算详情
    calculation_details: Optional[Dict[str, Any]] = Field(None, description="运费计算详情")
    calculation_metadata: Optional[Dict[str, Any]] = Field(None, description="计算过程元数据")
    
    # 时间戳
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


# ==================== 业务操作模型 ====================

class CreateOrderShippingRequest(BaseModel):
    """创建订单运费记录请求模型"""
    # 基础订单信息
    order_id: str = Field(..., description="订单号")
    country_code: str = Field(..., description="收货国家代码")
    total_quantity: int = Field(..., ge=1, description="商品总件数")
    total_amount: Decimal = Field(..., ge=0, description="商品总金额")
    
    # 可选地址信息
    state_province: Optional[str] = Field(None, description="州/省")
    city: Optional[str] = Field(None, description="城市")
    postal_code: Optional[str] = Field(None, description="邮政编码")
    full_address: Optional[str] = Field(None, description="完整地址")
    
    # 快递选择
    shipping_method_code: str = Field(..., description="选择的快递方式代码")
    
    # 用户信息（用于免运费检查）
    member_level: Optional[str] = Field(None, description="会员等级")
    promotion_codes: Optional[list] = Field(None, description="促销代码列表")
    
    # 其他选项
    currency_code: str = Field("USD", description="货币代码")
    language_code: str = Field("zh-CN", description="语言代码")


class OrderShippingStatsResponse(BaseModel):
    """订单运费统计响应模型"""
    total_orders: int = Field(..., description="总订单数")
    free_shipping_orders: int = Field(..., description="免运费订单数")
    free_shipping_rate: float = Field(..., description="免运费比例")
    average_shipping_cost: Optional[Decimal] = Field(None, description="平均运费")
    total_shipping_revenue: Decimal = Field(..., description="总运费收入")
    total_savings: Decimal = Field(..., description="总节省金额")
    most_popular_method: Optional[str] = Field(None, description="最受欢迎的快递方式")
    most_popular_zone: Optional[str] = Field(None, description="最受欢迎的地区") 