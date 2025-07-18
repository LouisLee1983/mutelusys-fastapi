# -*- coding: utf-8 -*-
"""
商品服务类
提供简单的商品管理功能，仅涉及Product表的基本操作
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_, and_
from fastapi import HTTPException, status
from datetime import datetime

from app.product.models import Product, ProductTranslation, ProductStatus, ProductCategory, product_category
from app.product.schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    ProductQueryParams
)
from app.product.category.service import ProductCategoryService


class ProductService:
    """简单的商品服务类，只处理基本的CRUD操作"""

    @staticmethod
    def get_products(
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        search: Optional[str] = None,
        category_id: Optional[UUID] = None,
        status: Optional[ProductStatus] = None,
        is_featured: Optional[bool] = None,
        is_new: Optional[bool] = None,
        is_bestseller: Optional[bool] = None,
        sort_by: str = "updated_at",
        sort_desc: bool = True
    ) -> ProductListResponse:
        """
        获取商品列表，支持基本的筛选和搜索
        """
        # 基础查询
        query = db.query(Product)
        
        # 应用筛选条件
        if search:
            # 搜索商品编码
            query = query.filter(Product.sku_code.ilike(f"%{search}%"))
            
        if category_id:
            # 通过product_category关联表筛选分类
            query = query.join(product_category).filter(product_category.c.category_id == category_id)
            
        if status:
            query = query.filter(Product.status == status)
            
        if is_featured is not None:
            query = query.filter(Product.is_featured == is_featured)
            
        if is_new is not None:
            query = query.filter(Product.is_new == is_new)
            
        if is_bestseller is not None:
            query = query.filter(Product.is_bestseller == is_bestseller)
        
        # 计算总数
        total = query.count()
        
        # 排序
        if hasattr(Product, sort_by):
            sort_column = getattr(Product, sort_by)
            if sort_desc:
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
        else:
            # 默认按更新时间降序
            query = query.order_by(desc(Product.updated_at))
        
        # 应用分页
        products = query.offset(skip).limit(limit).all()
        
        # 转换为响应格式
        items = []
        for product in products:
            product_data = ProductResponse.from_orm(product)
            items.append(product_data)
        
        return ProductListResponse(
            items=items,
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            size=limit,
            pages=(total + limit - 1) // limit if limit > 0 else 1
        )

    @staticmethod
    def get_product_by_id(db: Session, product_id: UUID) -> ProductResponse:
        """根据ID获取商品详情"""
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        # 直接使用Product表中的字段
        product_data = ProductResponse.from_orm(product)
        
        return product_data
    
    @staticmethod
    def get_product_by_sku(db: Session, sku_code: str) -> ProductResponse:
        """根据SKU编码获取商品详情"""
        product = db.query(Product).filter(Product.sku_code == sku_code).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SKU编码 {sku_code} 不存在"
            )
        
        # 直接使用Product表中的字段
        product_data = ProductResponse.from_orm(product)
        
        return product_data
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> ProductResponse:
        """创建商品"""
        # 检查SKU编码是否已存在
        existing = db.query(Product).filter(Product.sku_code == product_data.sku_code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SKU编码 {product_data.sku_code} 已存在"
            )
        
        # 创建商品，包含name和description
        create_data = product_data.dict()
        
        # 如果sku_name没有填写，默认使用sku_code的值
        if not create_data.get("sku_name"):
            create_data["sku_name"] = create_data["sku_code"]
        
        new_product = Product(**create_data)
        db.add(new_product)
        
        db.commit()
        db.refresh(new_product)
        
        # 返回商品信息
        product_response = ProductResponse.from_orm(new_product)
        
        return product_response
    
    @staticmethod
    def update_product(
        db: Session, 
        product_id: UUID, 
        product_data: ProductUpdate
    ) -> ProductResponse:
        """更新商品"""
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        # 如果更新SKU编码，检查是否重复
        if product_data.sku_code and product_data.sku_code != product.sku_code:
            existing = db.query(Product).filter(
                Product.sku_code == product_data.sku_code,
                Product.id != product_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"SKU编码 {product_data.sku_code} 已存在"
                )
        
        # 更新商品基本信息
        update_data = product_data.dict(exclude_unset=True)
        
        # 如果更新了sku_code但没有设置sku_name，则使用sku_code作为sku_name
        if "sku_code" in update_data and "sku_name" not in update_data:
            update_data["sku_name"] = update_data["sku_code"]
        # 如果sku_name被设置为空值，则使用sku_code作为默认值
        elif "sku_name" in update_data and not update_data["sku_name"]:
            update_data["sku_name"] = update_data.get("sku_code", product.sku_code)
        
        for key, value in update_data.items():
            setattr(product, key, value)
        
        product.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(product)
        
        # 直接返回Product表中的数据
        product_response = ProductResponse.from_orm(product)
        
        return product_response
    
    @staticmethod
    def delete_product(db: Session, product_id: UUID) -> Dict[str, Any]:
        """删除商品"""
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        # 软删除：更新状态为已删除
        product.status = ProductStatus.DELETED
        product.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": f"商品 {product.sku_code} 已成功删除"
        }
    
    @staticmethod
    def update_product_status(
        db: Session, 
        product_id: UUID, 
        new_status: ProductStatus
    ) -> ProductResponse:
        """更新商品状态"""
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在"
            )
        
        product.status = new_status
        product.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(product)
        
        # 直接返回Product表中的数据
        product_response = ProductResponse.from_orm(product)
        
        return product_response
    
    @staticmethod
    def get_product_statistics(db: Session) -> Dict[str, Any]:
        """获取商品统计信息"""
        total_products = db.query(func.count(Product.id)).filter(
            Product.status != ProductStatus.DELETED
        ).scalar()
        
        active_products = db.query(func.count(Product.id)).filter(
            Product.status == ProductStatus.ACTIVE
        ).scalar()
        
        featured_products = db.query(func.count(Product.id)).filter(
            Product.is_featured == True,
            Product.status != ProductStatus.DELETED
        ).scalar()
        
        new_products = db.query(func.count(Product.id)).filter(
            Product.is_new == True,
            Product.status != ProductStatus.DELETED
        ).scalar()
        
        bestseller_products = db.query(func.count(Product.id)).filter(
            Product.is_bestseller == True,
            Product.status != ProductStatus.DELETED
        ).scalar()
        
        return {
            "total_products": total_products,
            "active_products": active_products,
            "featured_products": featured_products,
            "new_products": new_products,
            "bestseller_products": bestseller_products
        }

    # ========== 公开API方法 ==========
    
    @staticmethod
    def _product_to_public_dict(product: Product) -> Dict[str, Any]:
        """将Product对象转换为公开API返回的字典格式"""
        # 获取主图片URL - 如果没有设置，使用默认图片
        primary_image = "/static/images/product-placeholder.svg"
        if hasattr(product, 'primary_image') and product.primary_image:
            if product.primary_image.startswith('http'):
                # 如果是完整URL，直接使用
                primary_image = product.primary_image
            elif product.primary_image.startswith('/static/'):
                # 如果已经是完整的相对路径，直接使用
                primary_image = product.primary_image
            else:
                # 如果只是文件路径，添加静态资源路径前缀
                primary_image = f"/static/uploads/{product.primary_image}"
        
        # 获取分类名称
        category_name = "未分类"
        if hasattr(product, 'categories') and product.categories:
            category_name = product.categories[0].name
        
        # 获取价格信息（优先使用默认币种的价格）
        regular_price = 0.0
        sale_price = None
        currency_code = 'CNY'
        
        if hasattr(product, 'prices') and product.prices:
            # 优先找默认币种的价格
            default_price = next((p for p in product.prices if p.is_default), None)
            if not default_price and product.prices:
                # 如果没有默认价格，使用第一个价格
                default_price = product.prices[0]
            
            if default_price:
                regular_price = float(default_price.regular_price)
                sale_price = float(default_price.sale_price) if default_price.sale_price else None
                currency_code = default_price.currency_code
        
        # 获取主图片（优先使用主图类型的图片）
        if hasattr(product, 'images') and product.images:
            # 优先找主图类型的图片
            main_image = next((img for img in product.images if img.image_type.value == 'main' and img.is_active), None)
            if not main_image:
                # 如果没有主图，使用第一个激活的图片
                main_image = next((img for img in product.images if img.is_active), None)
            
            if main_image:
                if main_image.image_url.startswith('http'):
                    # 如果是完整URL，直接使用
                    primary_image = main_image.image_url
                elif main_image.image_url.startswith('/static/'):
                    # 如果已经是完整的相对路径，直接使用
                    primary_image = main_image.image_url
                else:
                    # 如果只是文件路径，添加静态资源路径前缀
                    primary_image = f"/static/uploads/{main_image.image_url}"
        
        return {
            "id": str(product.id),
            "sku_code": product.sku_code,
            "name": product.name,
            "description": product.description,
            "primary_image": primary_image,
            "regular_price": regular_price,
            "sale_price": sale_price,
            "currency_code": currency_code,
            "status": product.status.value if product.status else None,
            "weight": product.weight,
            "width": product.width,
            "height": product.height,
            "length": product.length,
            "is_featured": product.is_featured,
            "is_new": product.is_new,
            "is_bestseller": product.is_bestseller,
            "is_customizable": product.is_customizable,
            "category_name": category_name,
            "rating": getattr(product, 'rating', None),
            "reviews_count": getattr(product, 'reviews_count', 0),
            "tax_class": product.tax_class,
            "sort_order": product.sort_order,
            "seo_title": product.seo_title,
            "seo_description": product.seo_description,
            "seo_keywords": product.seo_keywords,
            "meta_data": product.meta_data,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
        }

    @staticmethod
    def get_public_category_products_by_slug(
        db: Session,
        slug: str,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        include_children: bool = True
    ) -> Dict[str, Any]:
        """根据分类slug获取该分类及其子分类下的所有商品（公开接口）"""
        
        # 获取主分类
        category = ProductCategoryService.get_category_by_slug(db, slug)
        if not category or not category.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类slug {slug} 不存在或已下架"
            )
        
        # 收集所有要查询的分类ID
        category_ids = [category.id]
        
        if include_children:
            # 递归获取所有子分类ID
            def get_all_child_ids(parent_id: UUID) -> List[UUID]:
                children = db.query(ProductCategory).filter(
                    ProductCategory.parent_id == parent_id,
                    ProductCategory.is_active == True
                ).all()
                
                child_ids = []
                for child in children:
                    child_ids.append(child.id)
                    # 递归获取子分类的子分类
                    child_ids.extend(get_all_child_ids(child.id))
                
                return child_ids
            
            child_ids = get_all_child_ids(category.id)
            category_ids.extend(child_ids)
        
        # 先计算总数（不使用joinedload避免JSON字段问题）
        count_subquery = db.query(Product.id).join(
            product_category, Product.id == product_category.c.product_id
        ).filter(
            product_category.c.category_id.in_(category_ids),
            Product.status == ProductStatus.ACTIVE
        ).distinct().subquery()
        
        total = db.query(count_subquery).count()
        
        # 创建有效的排序字段映射
        sort_field_map = {
            "created": "created_at",
            "updated": "updated_at", 
            "name": "name",
            "price": "created_at",  # 价格排序比较复杂，暂时用创建时间
            "created_at": "created_at",
            "updated_at": "updated_at"
        }
        
        # 获取有效的排序字段
        valid_sort_field = sort_field_map.get(sort_by, "created_at")
        sort_column = getattr(Product, valid_sort_field)
        
        # 第一步：查询符合条件的商品基础信息（包含排序字段）
        # 为了避免DISTINCT + ORDER BY的冲突，我们查询所需的字段
        product_query = db.query(Product.id, sort_column).join(
            product_category, Product.id == product_category.c.product_id
        ).filter(
            product_category.c.category_id.in_(category_ids),
            Product.status == ProductStatus.ACTIVE
        )
        
        # 使用GROUP BY代替DISTINCT来去重
        product_query = product_query.group_by(Product.id, sort_column)
        
        # 添加排序
        if sort_order.lower() == "desc":
            product_query = product_query.order_by(desc(sort_column))
        else:
            product_query = product_query.order_by(sort_column)
            
        # 分页获取商品ID
        product_results = product_query.offset(skip).limit(limit).all()
        product_id_list = [result.id for result in product_results]
        
        if not product_id_list:
            return {
                "items": [],
                "total": total,
                "page": skip // limit + 1 if limit > 0 else 1,
                "size": limit,
                "category_slug": slug,
                "include_children": include_children
            }
        
        # 第二步：根据ID列表查询完整商品信息，预加载关联数据
        if product_id_list:
            query = db.query(Product).options(
                joinedload(Product.prices),
                joinedload(Product.images),
                joinedload(Product.categories)
            ).filter(Product.id.in_(product_id_list))
            
            # 保持与第一步查询相同的排序
            sort_column = getattr(Product, valid_sort_field)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
                
            products = query.all()
        else:
            products = []
        
        # 转换为字典格式
        items = [ProductService._product_to_public_dict(product) for product in products]
        
        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "category_slug": slug,
            "include_children": include_children
        }

    @staticmethod
    def get_public_category_products(
        db: Session,
        category_id: UUID,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """获取指定分类下的商品（公开接口）"""
        
        # 验证分类是否存在且激活
        category = db.query(ProductCategory).filter(
            ProductCategory.id == category_id,
            ProductCategory.is_active == True
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类ID {category_id} 不存在或已下架"
            )
        
        # 先计算总数（不使用joinedload避免JSON字段问题）
        count_query = db.query(Product.id).join(
            product_category, Product.id == product_category.c.product_id
        ).filter(
            product_category.c.category_id == category_id,
            Product.status == ProductStatus.ACTIVE
        )
        total = count_query.count()
        
        # 创建有效的排序字段映射
        sort_field_map = {
            "created": "created_at",
            "updated": "updated_at", 
            "name": "name",
            "price": "created_at",  # 价格排序比较复杂，暂时用创建时间
            "created_at": "created_at",
            "updated_at": "updated_at"
        }
        
        # 获取有效的排序字段
        valid_sort_field = sort_field_map.get(sort_by, "created_at")
        
        # 查询该分类下的商品，预加载关联数据
        query = db.query(Product).options(
            joinedload(Product.prices),
            joinedload(Product.images),
            joinedload(Product.categories)
        ).join(
            product_category, Product.id == product_category.c.product_id
        ).filter(
            product_category.c.category_id == category_id,
            Product.status == ProductStatus.ACTIVE
        )
        
        # 排序
        sort_column = getattr(Product, valid_sort_field)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)
        
        # 分页
        products = query.offset(skip).limit(limit).all()
        
        # 转换为字典格式
        items = [ProductService._product_to_public_dict(product) for product in products]
        
        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "category_id": str(category_id)
        }

    @staticmethod
    def get_public_products(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[UUID] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取公开商品列表（公开接口）"""
        
        # 基础查询，预加载关联数据
        query = db.query(Product).options(
            joinedload(Product.prices),
            joinedload(Product.images),
            joinedload(Product.categories)
        ).filter(
            Product.status == ProductStatus.ACTIVE  # 只返回上架的商品
        )
        
        # 分类筛选
        if category_id:
            query = query.join(
                product_category, Product.id == product_category.c.product_id
            ).filter(product_category.c.category_id == category_id)
        
        # 搜索筛选
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.sku_code.ilike(search_term)
                )
            )
        
        # 创建不带joinedload的查询来计算总数
        count_query = db.query(Product).filter(
            Product.status == ProductStatus.ACTIVE
        )
        
        # 分类筛选
        if category_id:
            count_query = count_query.join(
                product_category, Product.id == product_category.c.product_id
            ).filter(product_category.c.category_id == category_id)
        
        # 搜索筛选
        if search:
            search_term = f"%{search}%"
            count_query = count_query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.sku_code.ilike(search_term)
                )
            )
        
        # 计算总数
        total = count_query.count()
        
        # 创建有效的排序字段映射
        sort_field_map = {
            "created": "created_at",
            "updated": "updated_at", 
            "name": "name",
            "price": "created_at",  # 价格排序比较复杂，暂时用创建时间
            "created_at": "created_at",
            "updated_at": "updated_at"
        }
        
        # 获取有效的排序字段
        valid_sort_field = sort_field_map.get(sort_by, "created_at")
        
        # 排序
        sort_column = getattr(Product, valid_sort_field)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)
        
        # 分页
        products = query.offset(skip).limit(limit).all()
        
        # 转换为字典格式
        items = [ProductService._product_to_public_dict(product) for product in products]
        
        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit
        }

    @staticmethod
    def search_public_products(
        db: Session,
        query_text: str,
        skip: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """商品搜索（公开接口）"""
        
        search_term = f"%{query_text}%"
        
        # 先计算总数（不使用joinedload避免JSON字段问题）
        count_query = db.query(Product).filter(
            Product.status == ProductStatus.ACTIVE,
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.sku_code.ilike(search_term),
                Product.seo_keywords.ilike(search_term)
            )
        )
        total = count_query.count()
        
        # 搜索查询，预加载关联数据
        query = db.query(Product).options(
            joinedload(Product.prices),
            joinedload(Product.images),
            joinedload(Product.categories)
        ).filter(
            Product.status == ProductStatus.ACTIVE,
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.sku_code.ilike(search_term),
                Product.seo_keywords.ilike(search_term)
            )
        )
        
        # 按相关性排序（这里简单按创建时间排序）
        query = query.order_by(desc(Product.created_at))
        
        # 分页
        products = query.offset(skip).limit(limit).all()
        
        # 转换为字典格式
        items = [ProductService._product_to_public_dict(product) for product in products]
        
        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "query": query_text
        }

    @staticmethod
    def get_public_product_detail(
        db: Session,
        product_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """获取公开商品详情（公开接口）"""
        
        # 查询商品详情，预加载关联数据
        product = db.query(Product).options(
            joinedload(Product.prices),
            joinedload(Product.images),
            joinedload(Product.categories),
            joinedload(Product.skus),
            joinedload(Product.inventories),
            joinedload(Product.translations)
        ).filter(
            Product.id == product_id,
            Product.status == ProductStatus.ACTIVE
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商品ID {product_id} 不存在或已下架"
            )
        
        # 转换为详细字典格式
        product_dict = ProductService._product_to_public_dict(product)
        
        # 添加额外的详细信息
        if hasattr(product, 'images') and product.images:
            gallery_images = []
            for img in product.images:
                if img.is_active:
                    # 处理图片URL（与_product_to_public_dict保持一致）
                    image_url = img.image_url
                    if img.image_url.startswith('http'):
                        image_url = img.image_url
                    elif img.image_url.startswith('/static/'):
                        image_url = img.image_url
                    else:
                        image_url = f"/static/uploads/{img.image_url}"
                    
                    gallery_images.append({
                        "id": str(img.id),
                        "url": image_url,
                        "alt_text": img.alt_text,
                        "title": img.title,
                        "description": img.description,
                        "type": img.image_type.value,
                        "width": img.width,
                        "height": img.height,
                        "is_video": img.is_video,
                        "thumbnail_url": img.thumbnail_url,
                        "sort_order": img.sort_order
                    })
            
            product_dict["gallery_images"] = sorted(gallery_images, key=lambda x: x["sort_order"])
        
        # 添加SKU信息
        if hasattr(product, 'skus') and product.skus:
            available_skus = []
            for sku in product.skus:
                if sku.is_active:
                    sku_data = {
                        "id": str(sku.id),
                        "sku_code": sku.sku_code,
                        "barcode": sku.barcode,
                        "image_url": sku.image_url,
                        "price_adjustment": float(sku.price_adjustment) if sku.price_adjustment else 0.0,
                        "weight_adjustment": float(sku.weight_adjustment) if sku.weight_adjustment else 0.0,
                        "is_default": sku.is_default,
                        "is_active": sku.is_active,
                        "sort_order": sku.sort_order,
                        "meta_data": sku.meta_data
                    }
                    
                    # 计算SKU的实际价格
                    if product_dict.get("regular_price"):
                        sku_data["actual_regular_price"] = product_dict["regular_price"] + sku_data["price_adjustment"]
                        if product_dict.get("sale_price"):
                            sku_data["actual_sale_price"] = product_dict["sale_price"] + sku_data["price_adjustment"]
                    
                    available_skus.append(sku_data)
            
            product_dict["available_skus"] = sorted(available_skus, key=lambda x: x["sort_order"])
        else:
            product_dict["available_skus"] = []
        
        # 添加分类详细信息
        if hasattr(product, 'categories') and product.categories:
            categories_info = []
            for category in product.categories:
                categories_info.append({
                    "id": str(category.id),
                    "name": category.name,
                    "slug": category.slug,
                    "description": category.description,
                    "level": category.level.value if category.level else None,
                    "image_url": category.image_url,
                    "icon_url": category.icon_url
                })
            product_dict["categories_detail"] = categories_info
        else:
            product_dict["categories_detail"] = []
        
        # 添加多语言翻译信息
        if hasattr(product, 'translations') and product.translations:
            translations = {}
            for trans in product.translations:
                translations[trans.language_code] = {
                    "name": trans.name,
                    "short_description": trans.short_description,
                    "description": trans.description,
                    "specifications": trans.specifications,
                    "benefits": trans.benefits,
                    "instructions": trans.instructions,
                    "seo_title": trans.seo_title,
                    "seo_description": trans.seo_description,
                    "seo_keywords": trans.seo_keywords
                }
            product_dict["translations"] = translations
        else:
            product_dict["translations"] = {}
        
        # 添加库存信息（从inventories获取）
        if hasattr(product, 'inventories') and product.inventories:
            total_quantity = sum([inv.quantity for inv in product.inventories if inv.is_managed])
            total_reserved = sum([inv.reserved_quantity for inv in product.inventories if inv.is_managed])
            product_dict["inventory"] = {
                "total_quantity": total_quantity,
                "available_quantity": total_quantity - total_reserved,
                "reserved_quantity": total_reserved,
                "is_in_stock": total_quantity > total_reserved,
                "low_stock_threshold": min([inv.alert_threshold for inv in product.inventories if inv.alert_threshold]) if any(inv.alert_threshold for inv in product.inventories) else None
            }
        else:
            product_dict["inventory"] = {
                "total_quantity": 0,
                "available_quantity": 0,
                "reserved_quantity": 0,
                "is_in_stock": False,
                "low_stock_threshold": None
            }
        
        return product_dict
