from typing import List, Optional, Dict, Union, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import func, select, desc, or_, and_, case, distinct
from fastapi import HTTPException, status
from datetime import datetime, timedelta

# 从核心models导入基础模型
from app.product.models import Product, ProductCategory, product_category, ProductTranslation

# 从相应子模块导入具体模型
from app.product.models import ProductSku, ProductInventory, ProductPrice

from app.product.inventory.schema import (
    ProductInventoryCreate,
    ProductInventoryUpdate,
    ProductInventoryAdjustment,
    ProductInventoryAdjustmentResult,
    ProductInventoryReservation,
    ProductInventoryReservationResult,
    InventoryMovement
)


class ProductInventoryService:
    """库存服务类，提供库存的管理功能"""

    @staticmethod
    def get_inventories(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        product_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
        warehouse_id: Optional[UUID] = None,
        sku_code: Optional[str] = None,
        is_low_stock: Optional[bool] = None,
        is_out_of_stock: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: str = "updated_at",
        sort_desc: bool = True
    ) -> Dict[str, Any]:
        """
        获取库存列表，支持分页、过滤和搜索
        """
        # 基础查询
        query = db.query(
            ProductInventory,
            ProductSku.sku_code,
            ProductSku.barcode,
            ProductSku.is_active,
            Product.sku_code.label("product_code"),
            func.coalesce(ProductInventory.quantity - ProductInventory.reserved_quantity, 0).label("available_quantity"),
            case(
                (ProductInventory.quantity <= 0, "out_of_stock"),
                (ProductInventory.quantity <= ProductInventory.alert_threshold, "low_stock"),
                else_="in_stock"
            ).label("status")
        ).join(
            ProductSku, ProductInventory.sku_id == ProductSku.id
        ).join(
            Product, ProductInventory.product_id == Product.id
        )
        
        # 应用过滤条件
        if product_id:
            query = query.filter(ProductInventory.product_id == product_id)
        
        if category_id:
            # 使用多对多关系查询 - 通过关联表连接
            query = query.join(
                product_category, Product.id == product_category.c.product_id
            ).filter(
                product_category.c.category_id == category_id
            )
            
        if warehouse_id:
            query = query.filter(ProductInventory.warehouse_id == warehouse_id)
            
        if sku_code:
            query = query.filter(ProductSku.sku_code.ilike(f"%{sku_code}%"))
            
        if is_low_stock is not None:
            if is_low_stock:
                query = query.filter(
                    ProductInventory.quantity > 0,
                    ProductInventory.quantity <= ProductInventory.alert_threshold
                )
            else:
                query = query.filter(
                    or_(
                        ProductInventory.quantity > ProductInventory.alert_threshold,
                        ProductInventory.quantity <= 0
                    )
                )
                
        if is_out_of_stock is not None:
            if is_out_of_stock:
                query = query.filter(ProductInventory.quantity <= 0)
            else:
                query = query.filter(ProductInventory.quantity > 0)
                
        # 搜索功能
        if search:
            search_term = f"%{search}%"
            query = query.filter(or_(
                ProductSku.sku_code.ilike(search_term),
                ProductSku.barcode.ilike(search_term),
                Product.sku_code.ilike(search_term)
            ))
        
        # 计算总数
        total = query.count()
        
        # 排序
        if sort_by == "quantity":
            if sort_desc:
                query = query.order_by(desc(ProductInventory.quantity))
            else:
                query = query.order_by(ProductInventory.quantity)
        elif sort_by == "available_quantity":
            if sort_desc:
                query = query.order_by(desc("available_quantity"))
            else:
                query = query.order_by("available_quantity")
        else:
            # 按其他字段排序
            sort_column = getattr(ProductInventory, sort_by, ProductInventory.updated_at)
            if sort_desc:
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)
        
        # 应用分页
        query = query.offset(skip).limit(limit)
        
        # 执行查询
        results = query.all()
        
        # 格式化结果
        items = []
        for result in results:
            inventory, sku_code, barcode, sku_is_active, product_code, available_quantity, status = result
            
            # 获取产品信息
            product_info = db.query(Product).filter(Product.id == inventory.product_id).first()
            
            # 获取产品翻译名称（默认中文）
            product_name = None
            if product_info:
                product_translation = db.query(ProductTranslation).filter(
                    ProductTranslation.product_id == product_info.id,
                    ProductTranslation.language_code == "zh-CN"
                ).first()
                if product_translation:
                    product_name = product_translation.name
            
            # 获取分类信息 - 使用多对多关系查询
            category_info = None
            if product_info:
                category = db.query(ProductCategory).join(
                    product_category, ProductCategory.id == product_category.c.category_id
                ).filter(
                    product_category.c.product_id == product_info.id
                ).first()
                if category:
                    category_info = category
            
            # 格式化结果
            item = {
                "id": inventory.id,
                "sku_id": inventory.sku_id,
                "sku_code": sku_code,
                "barcode": barcode,
                "sku_is_active": sku_is_active,
                "product_id": inventory.product_id,
                "product_code": product_code,
                "product_name": product_name,
                "category_id": category_info.id if category_info else None,
                "category_name": category_info.name if category_info else None,
                "quantity": inventory.quantity,
                "reserved_quantity": inventory.reserved_quantity,
                "available_quantity": available_quantity,
                "alert_threshold": inventory.alert_threshold,
                "warehouse_id": inventory.warehouse_id,
                "warehouse_location": inventory.location,
                "status": status,
                "created_at": inventory.created_at,
                "updated_at": inventory.updated_at
            }
            
            items.append(item)
            
        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }

    @staticmethod
    def get_inventory_by_id(db: Session, inventory_id: UUID) -> ProductInventory:
        """根据ID获取库存详情"""
        inventory = db.query(ProductInventory).filter(ProductInventory.id == inventory_id).first()
        
        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"库存ID {inventory_id} 不存在"
            )
            
        return inventory
    
    @staticmethod
    def get_inventory_by_sku(db: Session, sku_id: UUID) -> ProductInventory:
        """根据SKU ID获取库存详情"""
        inventory = db.query(ProductInventory).filter(ProductInventory.sku_id == sku_id).first()
        
        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SKU ID {sku_id} 的库存不存在"
            )
            
        return inventory
    
    @staticmethod
    def create_inventory(db: Session, inventory_data: ProductInventoryCreate) -> ProductInventory:
        """创建库存记录"""
        # 检查产品是否存在
        product = db.query(Product).filter(Product.id == inventory_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"产品ID {inventory_data.product_id} 不存在"
            )
            
        # 如果指定了SKU，检查SKU是否存在且属于该产品
        if inventory_data.sku_id:
            sku = db.query(ProductSku).filter(
                ProductSku.id == inventory_data.sku_id,
                ProductSku.product_id == inventory_data.product_id
            ).first()
            if not sku:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"SKU ID {inventory_data.sku_id} 不存在或不属于产品 {inventory_data.product_id}"
                )
        
        # 仓库功能已简化，跨境电商不需要复杂的仓库管理
        # if inventory_data.warehouse_id:
        #     # 仓库功能已删除
        
        # 检查是否已存在相同的库存记录（同一产品+SKU+仓库组合）
        existing_query = db.query(ProductInventory).filter(
            ProductInventory.product_id == inventory_data.product_id
        )
        
        if inventory_data.sku_id:
            existing_query = existing_query.filter(ProductInventory.sku_id == inventory_data.sku_id)
        else:
            existing_query = existing_query.filter(ProductInventory.sku_id.is_(None))
            
        # 仓库功能已简化
        # if inventory_data.warehouse_id:
        #     existing_query = existing_query.filter(ProductInventory.warehouse_id == inventory_data.warehouse_id)
        # else:
        #     existing_query = existing_query.filter(ProductInventory.warehouse_id.is_(None))
            
        existing = existing_query.first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该产品在指定SKU和仓库的库存记录已存在"
            )
            
        # 创建库存记录
        inventory_dict = inventory_data.dict()
        
        new_inventory = ProductInventory(**inventory_dict)
        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)
        
        return new_inventory
    
    @staticmethod
    def update_inventory(
        db: Session, 
        inventory_id: UUID, 
        inventory_data: ProductInventoryUpdate
    ) -> ProductInventory:
        """更新库存记录"""
        inventory = ProductInventoryService.get_inventory_by_id(db, inventory_id)
        
        # 更新字段
        update_data = inventory_data.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(inventory, key, value)
            
        inventory.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(inventory)
        
        return inventory
    
    @staticmethod
    def delete_inventory(db: Session, inventory_id: UUID) -> Dict[str, Any]:
        """删除库存记录"""
        inventory = ProductInventoryService.get_inventory_by_id(db, inventory_id)
        
        # 删除库存记录
        db.delete(inventory)
        db.commit()
        
        return {
            "success": True,
            "message": f"库存记录ID {inventory_id} 已成功删除"
        }
    
    @staticmethod
    def adjust_inventory(
        db: Session, 
        adjustment_data: ProductInventoryAdjustment
    ) -> ProductInventoryAdjustmentResult:
        """调整库存数量"""
        # 获取库存记录
        inventory = db.query(ProductInventory).filter(ProductInventory.sku_id == adjustment_data.sku_id).first()
        if not inventory:
            # 尝试通过SKU获取产品ID
            sku = db.query(ProductSku).filter(ProductSku.id == adjustment_data.sku_id).first()
            if not sku:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"SKU ID {adjustment_data.sku_id} 不存在"
                )
                
            # 创建新的库存记录
            new_inventory = ProductInventory(
                sku_id=adjustment_data.sku_id,
                product_id=sku.product_id,
                quantity=max(0, adjustment_data.quantity),  # 如果是负数调整，初始库存为0
                alert_threshold=5,
                reserved_quantity=0
            )
            db.add(new_inventory)
            db.flush()
            inventory = new_inventory
        else:
            # 保存调整前数量
            previous_quantity = inventory.quantity
            
            # 调整数量
            if adjustment_data.quantity < 0 and abs(adjustment_data.quantity) > inventory.quantity:
                # 如果减少的数量大于当前库存，抛出异常
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"库存不足，当前库存为 {inventory.quantity}，无法减少 {abs(adjustment_data.quantity)}"
                )
                
            inventory.quantity += adjustment_data.quantity
            inventory.updated_at = datetime.utcnow()
        
        # 创建库存调整记录 TODO: 实现库存调整记录表
        
        db.commit()
        db.refresh(inventory)
        
        # 获取SKU信息
        sku = db.query(ProductSku).filter(ProductSku.id == adjustment_data.sku_id).first()
        
        # 返回结果
        return ProductInventoryAdjustmentResult(
            success=True,
            message=f"库存已调整 {adjustment_data.quantity}，当前库存为 {inventory.quantity}",
            sku_id=adjustment_data.sku_id,
            sku_code=sku.sku_code if sku else None,
            product_id=inventory.product_id,
            previous_quantity=previous_quantity if 'previous_quantity' in locals() else 0,
            current_quantity=inventory.quantity,
            adjustment=adjustment_data.quantity,
            is_low_stock=inventory.quantity <= inventory.alert_threshold and inventory.quantity > 0,
            is_out_of_stock=inventory.quantity <= 0
        )
    
    @staticmethod
    def reserve_inventory(
        db: Session, 
        reservation_data: ProductInventoryReservation
    ) -> ProductInventoryReservationResult:
        """预留库存"""
        # 获取库存记录
        inventory = db.query(ProductInventory).filter(ProductInventory.sku_id == reservation_data.sku_id).first()
        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SKU ID {reservation_data.sku_id} 的库存不存在"
            )
            
        # 检查可用库存是否足够
        available = inventory.quantity - inventory.reserved_quantity
        if available < reservation_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"可用库存不足，当前可用库存为 {available}，无法预留 {reservation_data.quantity}"
            )
            
        # 更新预留数量
        inventory.reserved_quantity += reservation_data.quantity
        inventory.updated_at = datetime.utcnow()
        
        # 创建预留记录 TODO: 实现库存预留记录表
        
        db.commit()
        db.refresh(inventory)
        
        # 返回结果
        return ProductInventoryReservationResult(
            success=True,
            message=f"成功预留 {reservation_data.quantity} 个库存",
            sku_id=reservation_data.sku_id,
            quantity=reservation_data.quantity,
            available_after_reservation=inventory.quantity - inventory.reserved_quantity
        )
    
    @staticmethod
    def release_reservation(
        db: Session, 
        sku_id: UUID,
        quantity: int,
        order_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """释放预留库存"""
        # 获取库存记录
        inventory = db.query(ProductInventory).filter(ProductInventory.sku_id == sku_id).first()
        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SKU ID {sku_id} 的库存不存在"
            )
            
        # 检查预留数量
        if inventory.reserved_quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"预留数量不足，当前预留数量为 {inventory.reserved_quantity}，无法释放 {quantity}"
            )
            
        # 更新预留数量
        inventory.reserved_quantity -= quantity
        inventory.updated_at = datetime.utcnow()
        
        # 更新预留记录 TODO: 实现库存预留记录表
        
        db.commit()
        db.refresh(inventory)
        
        # 返回结果
        return {
            "success": True,
            "message": f"成功释放 {quantity} 个预留库存",
            "sku_id": sku_id,
            "quantity": quantity,
            "available_after_release": inventory.quantity - inventory.reserved_quantity
        }
    
    @staticmethod
    def get_inventory_statistics(db: Session) -> Dict[str, Any]:
        """获取库存统计信息"""
        # 计算基本指标
        total_products = db.query(func.count(Product.id)).scalar()
        total_skus = db.query(func.count(ProductSku.id)).scalar()
        total_quantity = db.query(func.sum(ProductInventory.quantity)).scalar() or 0
        
        # 计算库存状态
        low_stock_count = db.query(func.count(ProductInventory.id)).filter(
            ProductInventory.quantity > 0,
            ProductInventory.quantity <= ProductInventory.alert_threshold
        ).scalar()
        
        out_of_stock_count = db.query(func.count(ProductInventory.id)).filter(
            ProductInventory.quantity <= 0
        ).scalar()
        
        # 计算库存价值
        inventory_value_query = db.query(
            func.sum(
                ProductInventory.quantity * ProductPrice.regular_price
            )
        ).join(
            ProductSku, ProductInventory.sku_id == ProductSku.id
        ).join(
            ProductPrice, ProductSku.product_id == ProductPrice.product_id
        ).filter(
            ProductPrice.is_default == True
        )
        
        inventory_value = inventory_value_query.scalar() or 0
        
        # 按分类统计
        category_stats = db.query(
            ProductCategory.id,
            ProductCategory.name,
            func.count(distinct(Product.id)).label("product_count"),
            func.count(distinct(ProductSku.id)).label("sku_count"),
            func.sum(ProductInventory.quantity).label("total_quantity"),
            func.sum(
                case((ProductInventory.quantity > 0, 1), else_=0)
            ).label("in_stock_count"),
            func.sum(
                case((ProductInventory.quantity <= 0, 1), else_=0)
            ).label("out_of_stock_count"),
        ).outerjoin(
            product_category, ProductCategory.id == product_category.c.category_id
        ).outerjoin(
            Product, product_category.c.product_id == Product.id
        ).outerjoin(
            ProductSku, Product.id == ProductSku.product_id
        ).outerjoin(
            ProductInventory, ProductSku.id == ProductInventory.sku_id
        ).group_by(
            ProductCategory.id, ProductCategory.name
        ).all()
        
        category_results = []
        for cat in category_stats:
            if cat.product_count > 0:  # 只包含有产品的分类
                category_results.append({
                    "id": cat.id,
                    "name": cat.name,
                    "product_count": cat.product_count,
                    "sku_count": cat.sku_count,
                    "total_quantity": cat.total_quantity or 0,
                    "in_stock_count": cat.in_stock_count or 0,
                    "out_of_stock_count": cat.out_of_stock_count or 0,
                })
        
        return {
            "total_products": total_products,
            "total_skus": total_skus,
            "total_quantity": total_quantity,
            "low_stock_count": low_stock_count,
            "out_of_stock_count": out_of_stock_count,
            "inventory_value": inventory_value,
            "categories": category_results
        }
        
    @staticmethod
    def transfer_inventory(
        db: Session,
        movement_data: InventoryMovement
    ) -> Dict[str, Any]:
        """转移库存从一个仓库到另一个仓库"""
        # 获取源仓库库存
        source_inventory = db.query(ProductInventory).filter(
            ProductInventory.sku_id == movement_data.sku_id,
            ProductInventory.warehouse_id == movement_data.source_warehouse_id
        ).first()
        
        if not source_inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SKU ID {movement_data.sku_id} 在源仓库中不存在库存记录"
            )
            
        # 检查可用库存
        available = source_inventory.quantity - source_inventory.reserved_quantity
        if available < movement_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"源仓库可用库存不足，当前可用库存为 {available}，无法转移 {movement_data.quantity}"
            )
            
        # 获取目标仓库库存
        destination_inventory = db.query(ProductInventory).filter(
            ProductInventory.sku_id == movement_data.sku_id,
            ProductInventory.warehouse_id == movement_data.destination_warehouse_id
        ).first()
        
        # 如果目标仓库没有该SKU的库存记录，创建一个
        if not destination_inventory:
            destination_inventory = ProductInventory(
                sku_id=movement_data.sku_id,
                product_id=source_inventory.product_id,
                quantity=0,
                reserved_quantity=0,
                alert_threshold=source_inventory.alert_threshold,
                warehouse_id=movement_data.destination_warehouse_id
            )
            db.add(destination_inventory)
            db.flush()
            
        # 减少源仓库库存
        source_inventory.quantity -= movement_data.quantity
        source_inventory.updated_at = datetime.utcnow()
        
        # 增加目标仓库库存
        destination_inventory.quantity += movement_data.quantity
        destination_inventory.updated_at = datetime.utcnow()
        
        # 创建库存转移记录 TODO: 实现库存转移记录表
        
        db.commit()
        db.refresh(source_inventory)
        db.refresh(destination_inventory)
        
        # 返回结果
        return {
            "success": True,
            "message": f"成功从仓库 {movement_data.source_warehouse_id} 转移 {movement_data.quantity} 个库存到仓库 {movement_data.destination_warehouse_id}",
            "sku_id": movement_data.sku_id,
            "quantity": movement_data.quantity,
            "source_warehouse": {
                "id": movement_data.source_warehouse_id,
                "current_quantity": source_inventory.quantity,
                "available_quantity": source_inventory.quantity - source_inventory.reserved_quantity
            },
            "destination_warehouse": {
                "id": movement_data.destination_warehouse_id,
                "current_quantity": destination_inventory.quantity,
                "available_quantity": destination_inventory.quantity - destination_inventory.reserved_quantity
            }
        }
