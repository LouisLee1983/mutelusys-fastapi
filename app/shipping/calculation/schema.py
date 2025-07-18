# -*- coding: utf-8 -*-
"""
运费计算Pydantic模型
包含计算请求、响应和相关数据结构
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


# 运费计算请求模型
class ShippingCalculationRequest(BaseModel):
    """运费计算请求模型"""
    # 收货信息
    country_code: str = Field(..., max_length=2, description="收货国家代码（ISO 3166-1 alpha-2）")
    state_province: Optional[str] = Field(None, max_length=50, description="州/省")
    city: Optional[str] = Field(None, max_length=50, description="城市")
    postal_code: Optional[str] = Field(None, max_length=20, description="邮政编码")
    
    # 商品信息
    total_quantity: int = Field(..., ge=1, description="商品总件数")
    total_amount: Decimal = Field(..., ge=0, description="商品总金额")
    currency_code: str = Field("USD", max_length=3, description="货币代码")
    
    # 用户信息（用于免运费检查）
    member_level: Optional[str] = Field(None, description="会员等级")
    promotion_codes: Optional[List[str]] = Field(None, description="促销代码列表")
    
    # 快递方式筛选（可选）
    preferred_methods: Optional[List[str]] = Field(None, description="优先快递方式代码列表")
    exclude_methods: Optional[List[str]] = Field(None, description="排除快递方式代码列表")
    
    # 其他选项
    language_code: str = Field("zh-CN", description="语言代码")
    include_inactive: bool = Field(False, description="是否包含未启用的方式")

    @validator('country_code')
    def validate_country_code(cls, v):
        """验证国家代码格式"""
        if len(v) != 2 or not v.isupper():
            raise ValueError('国家代码必须是2位大写字母')
        return v

    @validator('currency_code')
    def validate_currency_code(cls, v):
        """验证货币代码格式"""
        if len(v) != 3 or not v.isupper():
            raise ValueError('货币代码必须是3位大写字母')
        return v


# 快递方式选项模型
class ShippingMethodOption(BaseModel):
    """快递方式选项"""
    method_id: str = Field(..., description="快递方式ID")
    method_code: str = Field(..., description="快递方式代码")
    method_name: str = Field(..., description="快递方式名称")
    company_name: str = Field(..., description="快递公司名称")
    description: Optional[str] = Field(None, description="描述")
    transport_type: str = Field(..., description="运输类型")
    min_delivery_days: Optional[int] = Field(None, description="最小配送天数")
    max_delivery_days: Optional[int] = Field(None, description="最大配送天数")
    delivery_time_text: Optional[str] = Field(None, description="配送时间文本描述")


# 运费明细模型
class ShippingBreakdown(BaseModel):
    """运费明细"""
    base_shipping_cost: Decimal = Field(..., description="基础运费")
    discount_amount: Decimal = Field(0, description="折扣金额")
    final_shipping_cost: Decimal = Field(..., description="最终运费")
    currency_code: str = Field(..., description="货币代码")
    
    # 免运费信息
    is_free_shipping: bool = Field(False, description="是否免运费")
    free_shipping_rule_id: Optional[str] = Field(None, description="应用的免运费规则ID")
    free_shipping_rule_name: Optional[str] = Field(None, description="免运费规则名称")
    free_shipping_reason: Optional[str] = Field(None, description="免运费原因")
    savings_amount: Optional[Decimal] = Field(None, description="节省的运费金额")
    
    # 下一个免运费门槛
    next_free_threshold: Optional[Decimal] = Field(None, description="下一个满额免运费门槛")
    next_free_quantity: Optional[int] = Field(None, description="下一个满件免运费件数")
    remaining_amount: Optional[Decimal] = Field(None, description="距离免运费还需金额")
    remaining_quantity: Optional[int] = Field(None, description="距离免运费还需件数")


# 运费估算模型
class ShippingEstimate(BaseModel):
    """单个快递方式的运费估算"""
    method: ShippingMethodOption = Field(..., description="快递方式信息")
    breakdown: ShippingBreakdown = Field(..., description="运费明细")
    is_recommended: bool = Field(False, description="是否推荐")
    sort_order: int = Field(0, description="排序权重")


# 运费计算响应模型
class ShippingCalculationResponse(BaseModel):
    """运费计算响应模型"""
    success: bool = Field(True, description="计算是否成功")
    message: str = Field("计算成功", description="响应消息")
    
    # 计算结果
    estimates: List[ShippingEstimate] = Field([], description="运费估算列表")
    total_estimates: int = Field(0, description="可用快递方式总数")
    
    # 推荐信息
    recommended_method: Optional[ShippingEstimate] = Field(None, description="推荐的快递方式")
    cheapest_method: Optional[ShippingEstimate] = Field(None, description="最便宜的快递方式")
    fastest_method: Optional[ShippingEstimate] = Field(None, description="最快的快递方式")
    
    # 地区信息
    zone_id: Optional[str] = Field(None, description="匹配的运费地区ID")
    zone_name: Optional[str] = Field(None, description="运费地区名称")
    
    # 统计信息
    calculation_time: Optional[float] = Field(None, description="计算耗时（秒）")
    calculated_at: datetime = Field(default_factory=datetime.utcnow, description="计算时间")


# 批量运费计算请求模型
class BatchShippingCalculationRequest(BaseModel):
    """批量运费计算请求模型"""
    requests: List[ShippingCalculationRequest] = Field(..., description="计算请求列表")
    max_requests: int = Field(10, ge=1, le=50, description="最大请求数量限制")


# 批量运费计算响应模型
class BatchShippingCalculationResponse(BaseModel):
    """批量运费计算响应模型"""
    success: bool = Field(True, description="批量计算是否成功")
    message: str = Field("批量计算完成", description="响应消息")
    results: List[ShippingCalculationResponse] = Field([], description="计算结果列表")
    total_requests: int = Field(0, description="请求总数")
    successful_count: int = Field(0, description="成功计算数量")
    failed_count: int = Field(0, description="失败计算数量")
    calculation_time: float = Field(0, description="总计算耗时（秒）")


# 运费计算统计模型
class ShippingCalculationStats(BaseModel):
    """运费计算统计"""
    total_calculations: int = Field(0, description="总计算次数")
    free_shipping_count: int = Field(0, description="免运费次数")
    average_shipping_cost: Optional[Decimal] = Field(None, description="平均运费")
    most_popular_method: Optional[str] = Field(None, description="最受欢迎的快递方式")
    most_popular_zone: Optional[str] = Field(None, description="最受欢迎的地区")


# 运费预估查询参数
class ShippingQuoteParams(BaseModel):
    """运费预估查询参数（简化版）"""
    country_code: str = Field(..., description="国家代码")
    quantity: int = Field(1, ge=1, description="商品件数")
    amount: Optional[Decimal] = Field(None, ge=0, description="商品金额（用于免运费检查）")
    method_code: Optional[str] = Field(None, description="指定快递方式代码")
    language_code: str = Field("zh-CN", description="语言代码") 