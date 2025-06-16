# -*- coding: utf-8 -*-
"""
商品价格管理API接口
提供商品多币种价格的REST API
"""
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.product.price.service import ProductPriceService
from app.product.price.schema import (
    ProductPriceCreate,
    ProductPriceUpdate,
    ProductPriceResponse,
    ProductPriceListResponse,
    ProductPriceBatchCreate,
    ProductPriceSummary
)

router = APIRouter()


@router.get("/products/{product_id}/prices", response_model=ProductPriceListResponse)
def get_product_prices(
    product_id: UUID,
    skip: int = Query(default=0, ge=0, description="跳过记录数"),
    limit: int = Query(default=100, ge=1, le=100, description="返回记录数"),
    currency_code: Optional[str] = Query(None, description="货币代码筛选"),
    is_default: Optional[bool] = Query(None, description="是否默认币种筛选"),
    sort_by: str = Query(default="created_at", description="排序字段"),
    sort_desc: bool = Query(default=True, description="是否降序排序"),
    db: Session = Depends(get_db)
):
    """
    获取商品价格列表
    
    支持分页、筛选和排序功能
    """
    return ProductPriceService.get_product_prices(
        db=db,
        product_id=product_id,
        skip=skip,
        limit=limit,
        currency_code=currency_code,
        is_default=is_default,
        sort_by=sort_by,
        sort_desc=sort_desc
    )


@router.get("/products/{product_id}/prices/summary", response_model=ProductPriceSummary)
def get_product_price_summary(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    获取商品价格汇总信息
    
    包含所有币种的价格信息和默认币种
    """
    return ProductPriceService.get_product_price_summary(db, product_id)


@router.get("/prices/{price_id}", response_model=ProductPriceResponse)
def get_price_by_id(
    price_id: UUID,
    db: Session = Depends(get_db)
):
    """
    根据ID获取价格详情
    """
    return ProductPriceService.get_price_by_id(db, price_id)


@router.post("/products/{product_id}/prices", response_model=ProductPriceResponse, status_code=status.HTTP_201_CREATED)
def create_product_price(
    product_id: UUID,
    price_data: ProductPriceCreate,
    db: Session = Depends(get_db)
):
    """
    创建商品价格
    
    为指定商品添加新的币种价格设置
    """
    return ProductPriceService.create_product_price(db, product_id, price_data)


@router.post("/products/{product_id}/prices/batch", response_model=List[ProductPriceResponse], status_code=status.HTTP_201_CREATED)
def batch_create_product_prices(
    product_id: UUID,
    batch_data: ProductPriceBatchCreate,
    db: Session = Depends(get_db)
):
    """
    批量创建商品价格
    
    一次性为商品添加多个币种的价格设置
    """
    return ProductPriceService.batch_create_prices(db, product_id, batch_data.prices)


@router.put("/prices/{price_id}", response_model=ProductPriceResponse)
def update_product_price(
    price_id: UUID,
    price_data: ProductPriceUpdate,
    db: Session = Depends(get_db)
):
    """
    更新商品价格
    
    修改指定价格记录的信息
    """
    return ProductPriceService.update_product_price(db, price_id, price_data)


@router.patch("/products/{product_id}/prices/default/{currency_code}")
def set_default_currency(
    product_id: UUID,
    currency_code: str,
    db: Session = Depends(get_db)
):
    """
    设置默认币种
    
    将指定币种设置为商品的默认价格币种
    """
    return ProductPriceService.set_default_currency(db, product_id, currency_code)


@router.delete("/prices/{price_id}")
def delete_product_price(
    price_id: UUID,
    db: Session = Depends(get_db)
):
    """
    删除商品价格
    
    删除指定的价格记录
    """
    return ProductPriceService.delete_product_price(db, price_id)


# 统计接口
@router.get("/products/{product_id}/prices/statistics")
def get_price_statistics(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    获取商品价格统计信息
    
    包含价格数量、币种数量等统计数据
    """
    try:
        from app.product.models import ProductPrice
        
        # 基本统计
        total_prices = db.query(ProductPrice).filter(ProductPrice.product_id == product_id).count()
        
        # 币种统计
        currency_stats = db.query(ProductPrice.currency_code).filter(
            ProductPrice.product_id == product_id
        ).distinct().all()
        
        currency_count = len(currency_stats)
        currency_list = [curr[0] for curr in currency_stats]
        
        # 特价统计
        special_price_count = db.query(ProductPrice).filter(
            ProductPrice.product_id == product_id,
            ProductPrice.special_price.isnot(None)
        ).count()
        
        # 默认币种
        default_currency = db.query(ProductPrice.currency_code).filter(
            ProductPrice.product_id == product_id,
            ProductPrice.is_default == True
        ).first()
        
        return {
            "product_id": product_id,
            "total_prices": total_prices,
            "currency_count": currency_count,
            "currencies": currency_list,
            "special_price_count": special_price_count,
            "default_currency": default_currency[0] if default_currency else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取价格统计失败: {str(e)}")


# 价格验证接口
@router.post("/products/{product_id}/prices/validate")
def validate_price_data(
    product_id: UUID,
    price_data: ProductPriceCreate,
    db: Session = Depends(get_db)
):
    """
    验证价格数据
    
    在实际创建前验证价格数据的有效性
    """
    try:
        from app.product.models import Product, ProductPrice
        from sqlalchemy import and_
        
        # 验证商品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"valid": False, "message": "商品不存在"}
        
        # 检查币种是否已存在
        existing_price = db.query(ProductPrice).filter(
            and_(
                ProductPrice.product_id == product_id,
                ProductPrice.currency_code == price_data.currency_code
            )
        ).first()
        
        if existing_price:
            return {"valid": False, "message": f"币种 {price_data.currency_code} 已存在价格设置"}
        
        # 验证价格逻辑
        if price_data.sale_price and price_data.sale_price > price_data.regular_price:
            return {"valid": False, "message": "销售价格不能高于原始价格"}
        
        if price_data.special_price and price_data.special_price > price_data.regular_price:
            return {"valid": False, "message": "特价不能高于原始价格"}
        
        # 验证特价日期
        if price_data.special_price_start_date and price_data.special_price_end_date:
            if price_data.special_price_end_date <= price_data.special_price_start_date:
                return {"valid": False, "message": "特价结束日期必须晚于开始日期"}
        
        return {"valid": True, "message": "价格数据验证通过"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"价格验证失败: {str(e)}")
