# -*- coding: utf-8 -*-
"""
商品价格管理服务
提供商品多币种价格的业务逻辑处理
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status

from app.product.models import ProductPrice, Product
from app.product.price.schema import (
    ProductPriceCreate,
    ProductPriceUpdate,
    ProductPriceResponse,
    ProductPriceListResponse,
    ProductPriceSummary,
    CurrencyPriceInfo
)


class ProductPriceService:
    """商品价格服务类"""

    @staticmethod
    def get_product_prices(
        db: Session,
        product_id: UUID,
        skip: int = 0,
        limit: int = 100,
        currency_code: Optional[str] = None,
        is_default: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> ProductPriceListResponse:
        """
        获取商品价格列表
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 构建查询条件
            query = db.query(ProductPrice).filter(ProductPrice.product_id == product_id)
            
            if currency_code:
                query = query.filter(ProductPrice.currency_code == currency_code)
            
            if is_default is not None:
                query = query.filter(ProductPrice.is_default == is_default)

            # 总数统计
            total = query.count()

            # 排序
            if hasattr(ProductPrice, sort_by):
                order_column = getattr(ProductPrice, sort_by)
                if sort_desc:
                    query = query.order_by(order_column.desc())
                else:
                    query = query.order_by(order_column.asc())

            # 分页
            prices = query.offset(skip).limit(limit).all()

            # 计算分页信息
            pages = (total + limit - 1) // limit if limit > 0 else 0
            page = (skip // limit) + 1 if limit > 0 else 1

            return ProductPriceListResponse(
                items=[ProductPriceResponse.from_orm(price) for price in prices],
                total=total,
                page=page,
                size=len(prices),
                pages=pages
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取价格列表失败: {str(e)}")

    @staticmethod
    def get_price_by_id(db: Session, price_id: UUID) -> ProductPriceResponse:
        """
        根据ID获取价格详情
        """
        try:
            price = db.query(ProductPrice).filter(ProductPrice.id == price_id).first()
            if not price:
                raise HTTPException(status_code=404, detail="价格记录不存在")
            
            return ProductPriceResponse.from_orm(price)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取价格详情失败: {str(e)}")

    @staticmethod
    def create_product_price(
        db: Session,
        product_id: UUID,
        price_data: ProductPriceCreate
    ) -> ProductPriceResponse:
        """
        创建商品价格
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 检查同币种价格是否已存在
            existing_price = db.query(ProductPrice).filter(
                and_(
                    ProductPrice.product_id == product_id,
                    ProductPrice.currency_code == price_data.currency_code
                )
            ).first()
            
            if existing_price:
                raise HTTPException(
                    status_code=400, 
                    detail=f"商品已存在 {price_data.currency_code} 币种的价格设置"
                )

            # 如果设置为默认币种，需要取消其他默认设置
            if price_data.is_default:
                db.query(ProductPrice).filter(
                    and_(
                        ProductPrice.product_id == product_id,
                        ProductPrice.is_default == True
                    )
                ).update({"is_default": False})

            # 创建价格记录
            db_price = ProductPrice(
                product_id=product_id,
                **price_data.dict()
            )
            
            db.add(db_price)
            db.commit()
            db.refresh(db_price)

            return ProductPriceResponse.from_orm(db_price)

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"创建价格失败: {str(e)}")

    @staticmethod
    def update_product_price(
        db: Session,
        price_id: UUID,
        price_data: ProductPriceUpdate
    ) -> ProductPriceResponse:
        """
        更新商品价格
        """
        try:
            # 查找价格记录
            db_price = db.query(ProductPrice).filter(ProductPrice.id == price_id).first()
            if not db_price:
                raise HTTPException(status_code=404, detail="价格记录不存在")

            # 如果要设置为默认币种，需要取消同商品其他默认设置
            if price_data.is_default:
                db.query(ProductPrice).filter(
                    and_(
                        ProductPrice.product_id == db_price.product_id,
                        ProductPrice.id != price_id,
                        ProductPrice.is_default == True
                    )
                ).update({"is_default": False})

            # 更新字段
            update_data = price_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_price, field, value)
            
            db_price.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_price)

            return ProductPriceResponse.from_orm(db_price)

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"更新价格失败: {str(e)}")

    @staticmethod
    def delete_product_price(db: Session, price_id: UUID) -> dict:
        """
        删除商品价格
        """
        try:
            db_price = db.query(ProductPrice).filter(ProductPrice.id == price_id).first()
            if not db_price:
                raise HTTPException(status_code=404, detail="价格记录不存在")

            db.delete(db_price)
            db.commit()

            return {"message": "价格删除成功"}

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"删除价格失败: {str(e)}")

    @staticmethod
    def get_product_price_summary(db: Session, product_id: UUID) -> ProductPriceSummary:
        """
        获取商品价格汇总信息
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 获取所有价格记录
            prices = db.query(ProductPrice).filter(ProductPrice.product_id == product_id).all()
            
            if not prices:
                raise HTTPException(status_code=404, detail="商品暂无价格设置")

            # 查找默认币种
            default_price = next((p for p in prices if p.is_default), prices[0])
            
            # 构建币种信息列表
            currencies = []
            for price in prices:
                # 检查特价是否生效
                is_special_active = False
                if price.special_price and price.special_price_start_date and price.special_price_end_date:
                    today = date.today()
                    is_special_active = price.special_price_start_date <= today <= price.special_price_end_date

                currencies.append(CurrencyPriceInfo(
                    currency_code=price.currency_code,
                    regular_price=price.regular_price,
                    sale_price=price.sale_price,
                    special_price=price.special_price,
                    is_special_active=is_special_active,
                    discount_percentage=price.discount_percentage,
                    min_quantity=price.min_quantity,
                    is_default=price.is_default
                ))

            return ProductPriceSummary(
                product_id=product_id,
                default_currency=default_price.currency_code,
                default_price=default_price.regular_price,
                currencies=currencies,
                total_currencies=len(currencies)
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取价格汇总失败: {str(e)}")

    @staticmethod
    def batch_create_prices(
        db: Session,
        product_id: UUID,
        prices_data: List[ProductPriceCreate]
    ) -> List[ProductPriceResponse]:
        """
        批量创建商品价格
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 检查币种重复
            currency_codes = [price.currency_code for price in prices_data]
            if len(currency_codes) != len(set(currency_codes)):
                raise HTTPException(status_code=400, detail="批量创建中存在重复的币种")

            # 检查是否已存在相同币种的价格
            existing_currencies = db.query(ProductPrice.currency_code).filter(
                ProductPrice.product_id == product_id,
                ProductPrice.currency_code.in_(currency_codes)
            ).all()
            
            if existing_currencies:
                existing_codes = [curr[0] for curr in existing_currencies]
                raise HTTPException(
                    status_code=400, 
                    detail=f"以下币种已存在价格设置: {', '.join(existing_codes)}"
                )

            # 处理默认币种设置
            default_count = sum(1 for price in prices_data if price.is_default)
            if default_count > 1:
                raise HTTPException(status_code=400, detail="只能设置一个默认币种")
            
            if default_count == 1:
                # 取消现有默认设置
                db.query(ProductPrice).filter(
                    and_(
                        ProductPrice.product_id == product_id,
                        ProductPrice.is_default == True
                    )
                ).update({"is_default": False})

            # 批量创建
            created_prices = []
            for price_data in prices_data:
                db_price = ProductPrice(
                    product_id=product_id,
                    **price_data.dict()
                )
                db.add(db_price)
                created_prices.append(db_price)

            db.commit()
            
            # 刷新所有记录
            for price in created_prices:
                db.refresh(price)

            return [ProductPriceResponse.from_orm(price) for price in created_prices]

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"批量创建价格失败: {str(e)}")

    @staticmethod
    def set_default_currency(db: Session, product_id: UUID, currency_code: str) -> dict:
        """
        设置默认币种
        """
        try:
            # 验证商品是否存在
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="商品不存在")

            # 查找指定币种的价格记录
            target_price = db.query(ProductPrice).filter(
                and_(
                    ProductPrice.product_id == product_id,
                    ProductPrice.currency_code == currency_code
                )
            ).first()
            
            if not target_price:
                raise HTTPException(status_code=404, detail=f"未找到 {currency_code} 币种的价格设置")

            # 取消所有默认设置
            db.query(ProductPrice).filter(
                ProductPrice.product_id == product_id
            ).update({"is_default": False})

            # 设置新的默认币种
            target_price.is_default = True
            target_price.updated_at = datetime.utcnow()
            
            db.commit()

            return {"message": f"已将 {currency_code} 设置为默认币种"}

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"设置默认币种失败: {str(e)}")
