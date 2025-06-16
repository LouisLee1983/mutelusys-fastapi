from typing import List, Optional, Dict, Union, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import func, select, desc, or_, and_, cast, String
from fastapi import HTTPException, status
from datetime import datetime

# 从核心models导入基础模型
from app.product.models import Product, ProductStatus

# 从相应子模块导入具体模型
from app.product.models import ProductSku, ProductAttributeValue, ProductAttribute, ProductInventory, ProductPrice, ProductImage, sku_attribute_value, ImageType

from app.product.sku.schema import (
    ProductSkuCreate,
    ProductSkuUpdate,
    ProductAttributeValueCreate,
    ProductAttributeValueUpdate,
    ProductSkuInventoryUpdate,
    ProductSkuBulkStatusUpdate
)


class ProductSkuService:
    """SKU服务类，提供SKU的增删改查功能"""

    @staticmethod
    def get_all_skus(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        product_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
        low_stock: Optional[bool] = None,
        sort_field: str = "created_at",
        sort_order: str = "desc",
        include_product: bool = True,
        include_inventory: bool = True
    ) -> Dict[str, Any]:
        """
        获取所有SKU列表，支持分页、过滤、搜索和排序
        """
        # 基础查询
        query = db.query(ProductSku)
        
        # 如果需要包含产品信息，使用joinedload
        if include_product:
            query = query.options(joinedload(ProductSku.product))
            
        # 应用过滤条件
        if product_id:
            query = query.filter(ProductSku.product_id == product_id)
            
        if is_active is not None:
            query = query.filter(ProductSku.is_active == is_active)
            
        # 搜索功能 - 搜索SKU编码、条形码和产品名称
        if search:
            search_term = f"%{search}%"
            # 需要join Product表来搜索产品名称
            query = query.join(Product).filter(or_(
                ProductSku.sku_code.ilike(search_term),
                ProductSku.barcode.ilike(search_term),
                Product.name.ilike(search_term),
                Product.sku_code.ilike(search_term)
            ))
            
        # 低库存过滤
        if low_stock is True:
            # 子查询获取库存信息
            inventory_subq = db.query(
                ProductInventory.sku_id,
                ProductInventory.quantity,
                ProductInventory.reserved_quantity,
                ProductInventory.alert_threshold
            ).subquery()
            
            query = query.join(inventory_subq, ProductSku.id == inventory_subq.c.sku_id).filter(
                (inventory_subq.c.quantity - inventory_subq.c.reserved_quantity) <= inventory_subq.c.alert_threshold
            )
        
        # 计算总数
        total = query.count()
        
        # 排序
        order_by_column = getattr(ProductSku, sort_field, ProductSku.created_at)
        if sort_order.lower() == "desc":
            order_by_column = desc(order_by_column)
            
        # 加载关联数据并分页
        query_options = [
            joinedload(ProductSku.attribute_values).joinedload(ProductAttributeValue.attribute),
            joinedload(ProductSku.inventories)
        ]
        
        # 如果需要包含产品信息，加载产品及其价格和图片
        if include_product:
            query_options.extend([
                joinedload(ProductSku.product).joinedload(Product.prices),
                joinedload(ProductSku.product).joinedload(Product.images)
            ])
        
        skus = (
            query.order_by(order_by_column)
            .options(*query_options)
            .offset(skip).limit(limit).all()
        )
        
        # 格式化结果
        result_skus = []
        for sku in skus:
            # 处理属性值信息
            attribute_values = []
            for av in sku.attribute_values:
                attribute_values.append({
                    "id": str(av.id),
                    "attribute_id": str(av.attribute_id),
                    "value": av.value,
                    "label": av.label,
                    "color_code": av.color_code,
                    "attribute_name": av.attribute.name if av.attribute else None
                })
            
            # 处理库存信息
            inventory_info = None
            if include_inventory and sku.inventories:
                inv = sku.inventories[0]  # 取第一个库存记录
                inventory_info = {
                    "quantity": inv.quantity,
                    "reserved_quantity": inv.reserved_quantity,
                    "available_quantity": inv.quantity - inv.reserved_quantity,
                    "low_stock_threshold": inv.alert_threshold or 5,
                    "is_low_stock": (inv.quantity - inv.reserved_quantity) <= (inv.alert_threshold or 5)
                }
            
            sku_dict = {
                "id": str(sku.id),
                "sku_code": sku.sku_code,
                "product_id": str(sku.product_id),
                "barcode": sku.barcode,
                "price_adjustment": sku.price_adjustment,
                "weight": sku.weight_adjustment,
                "width": sku.width_adjustment,
                "height": sku.height_adjustment,
                "length": sku.length_adjustment,
                "is_active": sku.is_active,
                "is_default": sku.is_default,
                "sort_order": sku.sort_order,
                "image_url": sku.image_url,
                "attribute_values": attribute_values,
                "inventory": inventory_info,
                "created_at": sku.created_at.isoformat() if sku.created_at else None,
                "updated_at": sku.updated_at.isoformat() if sku.updated_at else None
            }
            
            # 添加产品信息
            if include_product and sku.product:
                # 获取产品的默认价格
                default_price = 0
                if sku.product.prices:
                    # 查找默认货币的价格，或使用第一个价格
                    default_price_record = next(
                        (p for p in sku.product.prices if p.is_default), 
                        sku.product.prices[0] if sku.product.prices else None
                    )
                    if default_price_record:
                        # 使用sale_price（如果有）或regular_price
                        default_price = default_price_record.sale_price or default_price_record.regular_price
                
                sku_dict["product"] = {
                    "id": str(sku.product.id),
                    "name": sku.product.name,
                    "sku_code": sku.product.sku_code,
                    "status": sku.product.status.value if sku.product.status else None,
                    "base_price": float(default_price),
                    "images": [{"url": img.image_url, "is_primary": img.image_type == ImageType.MAIN} 
                              for img in sku.product.images] if hasattr(sku.product, 'images') else []
                }
            
            result_skus.append(sku_dict)
            
        return {
            "code": 200,
            "message": "操作成功",
            "data": {
                "items": result_skus,
                "total": total,
                "page": skip // limit + 1 if limit > 0 else 1,
                "size": limit
            }
        }

    @staticmethod
    def get_product_skus(
        db: Session, 
        product_id: UUID,
        skip: int = 0, 
        limit: int = 100,
        status: Optional[ProductStatus] = None,
        search: Optional[str] = None,
        include_inventory: bool = True
    ) -> Dict[str, Any]:
        """
        获取产品的SKU列表，支持分页、过滤和搜索
        """
        # 基础查询
        query = db.query(ProductSku).filter(ProductSku.product_id == product_id)
        
        # 应用过滤条件
        if status:
            query = query.filter(ProductSku.status == status)
            
        # 搜索功能
        if search:
            search_term = f"%{search}%"
            query = query.filter(or_(
                ProductSku.sku_code.ilike(search_term),
                ProductSku.barcode.ilike(search_term)
            ))
        
        # 计算总数
        total = query.count()
        
        # 排序和分页
        skus = (
            query.order_by(ProductSku.is_default.desc(), ProductSku.sort_order, ProductSku.created_at)
            .options(
                joinedload(ProductSku.attribute_values).joinedload(ProductAttributeValue.attribute),
                joinedload(ProductSku.inventories)
            )
            .offset(skip).limit(limit).all()
        )
        
        # 格式化结果
        result_skus = []
        for sku in skus:
            # 处理属性值信息
            attribute_values = []
            for av in sku.attribute_values:
                attribute_values.append({
                    "id": str(av.id),
                    "attribute_id": str(av.attribute_id),
                    "value": av.value,
                    "label": av.label,
                    "color_code": av.color_code,
                    "attribute_name": av.attribute.name if av.attribute else None
                })
            
            # 处理库存信息
            inventory_info = None
            if include_inventory and sku.inventories:
                inv = sku.inventories[0]  # 取第一个库存记录
                inventory_info = {
                    "quantity": inv.quantity,
                    "reserved_quantity": inv.reserved_quantity,
                    "low_stock_threshold": inv.alert_threshold or 5
                }
            
            sku_dict = {
                "id": str(sku.id),
                "sku_code": sku.sku_code,
                "product_id": str(sku.product_id),
                "barcode": sku.barcode,
                "price_adjustment": sku.price_adjustment,
                "weight": sku.weight_adjustment,
                "width": sku.width_adjustment,
                "height": sku.height_adjustment,
                "length": sku.length_adjustment,
                "is_active": sku.is_active,
                "is_default": sku.is_default,
                "sort_order": sku.sort_order,
                "image_url": sku.image_url,
                "attribute_values": attribute_values,
                "inventory": inventory_info,
                "created_at": sku.created_at.isoformat() if sku.created_at else None,
                "updated_at": sku.updated_at.isoformat() if sku.updated_at else None
            }
            
            result_skus.append(sku_dict)
            
        return {
            "items": result_skus,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }

    @staticmethod
    def get_sku_by_id(db: Session, sku_id: UUID) -> ProductSku:
        """根据ID获取SKU详情"""
        sku = db.query(ProductSku).filter(ProductSku.id == sku_id).first()
        
        if not sku:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SKU ID {sku_id} 不存在"
            )
            
        return sku
        
    @staticmethod
    def get_sku_by_code(db: Session, sku_code: str) -> ProductSku:
        """根据SKU编码获取SKU详情"""
        sku = db.query(ProductSku).filter(ProductSku.sku_code == sku_code).first()
        
        if not sku:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SKU编码 {sku_code} 不存在"
            )
            
        return sku
        
    @staticmethod
    def create_sku(db: Session, sku_data: ProductSkuCreate) -> ProductSku:
        """创建新SKU"""
        # 检查产品是否存在
        product = db.query(Product).filter(Product.id == sku_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"产品ID {sku_data.product_id} 不存在"
            )
            
        # 检查SKU编码是否已存在
        existing = db.query(ProductSku).filter(ProductSku.sku_code == sku_data.sku_code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SKU编码 '{sku_data.sku_code}' 已存在"
            )
            
        # 如果是默认SKU，检查产品是否已有默认SKU
        if sku_data.is_default:
            default_sku = db.query(ProductSku).filter(
                ProductSku.product_id == sku_data.product_id,
                ProductSku.is_default == True
            ).first()
            
            # 如果存在，则取消其默认状态
            if default_sku:
                default_sku.is_default = False
                db.add(default_sku)
        
        # 创建SKU基础信息
        sku_dict = sku_data.dict(exclude={
            "attribute_values", 
            "quantity", 
            "low_stock_threshold"
        })
        
        new_sku = ProductSku(**sku_dict)
        db.add(new_sku)
        db.flush()  # 获取新创建的ID
        
        # 创建属性值关联
        for attribute_value_data in sku_data.attribute_values:
            # 验证属性存在
            attribute = db.query(ProductAttribute).filter(ProductAttribute.id == attribute_value_data.attribute_id).first()
            if not attribute:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"属性ID {attribute_value_data.attribute_id} 不存在"
                )
            
            # 查找或创建属性值
            attr_value = db.query(ProductAttributeValue).filter(
                ProductAttributeValue.attribute_id == attribute_value_data.attribute_id,
                ProductAttributeValue.value == attribute_value_data.value
            ).first()
            
            if not attr_value:
                # 创建新的属性值
                attr_value = ProductAttributeValue(
                    attribute_id=attribute_value_data.attribute_id,
                    value=attribute_value_data.value,
                    label=attribute_value_data.value,  # 默认使用value作为label
                    sort_order=0
                )
                db.add(attr_value)
                db.flush()  # 获取ID
            
            # 通过多对多关系添加关联
            new_sku.attribute_values.append(attr_value)
        
        # 如果提供了库存信息，创建库存记录
        if sku_data.quantity is not None:
            inventory = ProductInventory(
                sku_id=new_sku.id,
                product_id=sku_data.product_id,
                quantity=sku_data.quantity,
                alert_threshold=sku_data.low_stock_threshold
            )
            db.add(inventory)
            
        db.commit()
        db.refresh(new_sku)
        return new_sku
        
    @staticmethod
    def update_sku(db: Session, sku_id: UUID, sku_data: ProductSkuUpdate) -> ProductSku:
        """更新SKU信息"""
        sku = ProductSkuService.get_sku_by_id(db, sku_id)
        
        # 检查SKU编码是否已被其他SKU使用
        if sku_data.sku_code and sku_data.sku_code != sku.sku_code:
            existing = db.query(ProductSku).filter(
                ProductSku.sku_code == sku_data.sku_code,
                ProductSku.id != sku_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"SKU编码 '{sku_data.sku_code}' 已被其他SKU使用"
                )
                
        # 如果要设置为默认SKU，检查产品是否已有默认SKU
        if sku_data.is_default is True and not sku.is_default:
            default_sku = db.query(ProductSku).filter(
                ProductSku.product_id == sku.product_id,
                ProductSku.is_default == True,
                ProductSku.id != sku_id
            ).first()
            
            # 如果存在，则取消其默认状态
            if default_sku:
                default_sku.is_default = False
                db.add(default_sku)
                
        # 更新基本信息
        update_data = sku_data.dict(exclude_unset=True, exclude={"attribute_values"})
        
        for key, value in update_data.items():
            setattr(sku, key, value)
        
        # 更新属性值关联
        if sku_data.attribute_values:
            # 清除现有的属性值关联
            sku.attribute_values.clear()
            
            # 添加新的属性值关联
            for attribute_value_data in sku_data.attribute_values:
                # 验证属性存在
                attribute = db.query(ProductAttribute).filter(
                    ProductAttribute.id == attribute_value_data.attribute_id
                ).first()
                if not attribute:
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"属性ID {attribute_value_data.attribute_id} 不存在"
                    )
                
                # 查找或创建属性值
                attr_value = db.query(ProductAttributeValue).filter(
                    ProductAttributeValue.attribute_id == attribute_value_data.attribute_id,
                    ProductAttributeValue.value == attribute_value_data.value
                ).first()
                
                if not attr_value:
                    # 创建新的属性值
                    attr_value = ProductAttributeValue(
                        attribute_id=attribute_value_data.attribute_id,
                        value=attribute_value_data.value,
                        label=attribute_value_data.value,  # 默认使用value作为label
                        sort_order=0
                    )
                    db.add(attr_value)
                    db.flush()  # 获取ID
                
                # 通过多对多关系添加关联
                sku.attribute_values.append(attr_value)
        
        sku.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(sku)
        return sku
        
    @staticmethod
    def delete_sku(db: Session, sku_id: UUID) -> Dict[str, Any]:
        """删除SKU"""
        sku = ProductSkuService.get_sku_by_id(db, sku_id)
        
        # 检查是否有关联的订单，如有则不允许删除
        # TODO: 添加订单关联检查
        
        # 删除SKU的库存记录
        db.query(ProductInventory).filter(ProductInventory.sku_id == sku_id).delete()
        
        # 如果是默认SKU，且产品有其他SKU，将其中一个设为默认
        if sku.is_default:
            other_sku = db.query(ProductSku).filter(
                ProductSku.product_id == sku.product_id,
                ProductSku.id != sku_id
            ).first()
            
            if other_sku:
                other_sku.is_default = True
                db.add(other_sku)
        
        # 删除SKU（多对多关系会自动处理）
        db.delete(sku)
        db.commit()
        
        return {
            "success": True,
            "message": f"SKU '{sku.sku_code}' 已成功删除"
        }
        
    @staticmethod
    def update_inventory(
        db: Session, 
        sku_id: UUID, 
        inventory_data: ProductSkuInventoryUpdate
    ) -> Dict[str, Any]:
        """更新SKU库存"""
        sku = ProductSkuService.get_sku_by_id(db, sku_id)
        
        # 查找库存记录
        inventory = db.query(ProductInventory).filter(ProductInventory.sku_id == sku_id).first()
        
        if inventory:
            # 更新库存
            inventory.quantity = inventory_data.quantity
            if inventory_data.low_stock_threshold is not None:
                inventory.alert_threshold = inventory_data.low_stock_threshold
                
            inventory.updated_at = datetime.utcnow()
        else:
            # 创建新库存记录
            inventory = ProductInventory(
                sku_id=sku_id,
                product_id=sku.product_id,
                quantity=inventory_data.quantity,
                alert_threshold=inventory_data.low_stock_threshold if inventory_data.low_stock_threshold is not None else 5
            )
            db.add(inventory)
            
        db.commit()
        
        return {
            "success": True,
            "message": f"SKU '{sku.sku_code}' 库存已更新为 {inventory_data.quantity}"
        }
        
    @staticmethod
    def adjust_inventory(
        db: Session, 
        sku_id: UUID, 
        adjustment: int,
        reason: str = "手动调整"
    ) -> Dict[str, Any]:
        """调整SKU库存，正数为增加，负数为减少"""
        sku = ProductSkuService.get_sku_by_id(db, sku_id)
        
        # 查找库存记录
        inventory = db.query(ProductInventory).filter(ProductInventory.sku_id == sku_id).first()
        
        if not inventory:
            # 创建新库存记录
            inventory = ProductInventory(
                sku_id=sku_id,
                product_id=sku.product_id,
                quantity=max(0, adjustment),  # 如果是负数调整，初始库存为0
                low_stock_threshold=5
            )
            db.add(inventory)
        else:
            # 调整库存
            new_quantity = inventory.quantity + adjustment
            if new_quantity < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"库存不足，当前库存为 {inventory.quantity}，无法减少 {abs(adjustment)}"
                )
                
            inventory.quantity = new_quantity
            inventory.updated_at = datetime.utcnow()
            
        # TODO: 添加库存调整记录
            
        db.commit()
        
        return {
            "success": True,
            "message": f"SKU '{sku.sku_code}' 库存已调整 {adjustment}，当前库存为 {inventory.quantity}",
            "current_quantity": inventory.quantity
        }
        
    @staticmethod
    def bulk_update_status(
        db: Session, 
        bulk_update: ProductSkuBulkStatusUpdate
    ) -> Dict[str, Any]:
        """批量更新SKU状态"""
        update_count = 0
        for sku_id in bulk_update.sku_ids:
            try:
                sku = db.query(ProductSku).filter(ProductSku.id == sku_id).first()
                if sku:
                    sku.status = bulk_update.status
                    sku.updated_at = datetime.utcnow()
                    update_count += 1
            except Exception as e:
                continue
                
        db.commit()
        
        return {
            "success": True,
            "message": f"成功更新 {update_count}/{len(bulk_update.sku_ids)} 个SKU状态"
        }

    @staticmethod
    def get_sku_stats(db: Session) -> Dict[str, Any]:
        """
        获取SKU统计数据，使用数据库聚合查询，更高效
        """
        from sqlalchemy import func, and_
        
        # 总SKU数
        total_skus = db.query(func.count(ProductSku.id)).scalar()
        
        # 启用的SKU数
        active_skus = db.query(func.count(ProductSku.id)).filter(
            ProductSku.is_active == True
        ).scalar()
        
        # 低库存SKU数 - 需要关联库存表
        low_stock_skus = db.query(func.count(ProductSku.id)).join(
            ProductInventory, ProductSku.id == ProductInventory.sku_id
        ).filter(
            and_(
                ProductInventory.quantity <= ProductInventory.alert_threshold,
                ProductInventory.alert_threshold.isnot(None)
            )
        ).scalar()
        
        # 缺货SKU数
        out_of_stock_skus = db.query(func.count(ProductSku.id)).join(
            ProductInventory, ProductSku.id == ProductInventory.sku_id
        ).filter(
            ProductInventory.quantity == 0
        ).scalar()
        
        return {
            "code": 200,
            "message": "操作成功",
            "data": {
                "total_skus": total_skus or 0,
                "active_skus": active_skus or 0,
                "low_stock_skus": low_stock_skus or 0,
                "out_of_stock_skus": out_of_stock_skus or 0
            }
        }
