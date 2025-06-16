from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from fastapi import HTTPException, status

from app.product.models import ProductAttribute, ProductAttributeValue
from app.product.attribute.schema import (
    ProductAttributeCreate,
    ProductAttributeUpdate,
    ProductAttributeValueCreate,
    ProductAttributeValueUpdate,
    ProductAttributeValue as ProductAttributeValueSchema
)


class ProductAttributeService:
    """商品属性服务"""

    @staticmethod
    def get_attributes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        type_filter: Optional[str] = None,
        is_configurable: Optional[bool] = None,
        is_visible: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        获取商品属性列表，支持分页、搜索和过滤
        """
        query = db.query(ProductAttribute)
        
        # 搜索条件
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    ProductAttribute.name.ilike(search_pattern),
                    ProductAttribute.code.ilike(search_pattern),
                    ProductAttribute.description.ilike(search_pattern)
                )
            )
        
        # 类型过滤
        if type_filter:
            query = query.filter(ProductAttribute.type == type_filter)
        
        # 是否可配置过滤
        if is_configurable is not None:
            query = query.filter(ProductAttribute.is_configurable == is_configurable)
        
        # 是否前端可见过滤
        if is_visible is not None:
            query = query.filter(ProductAttribute.is_visible_on_frontend == is_visible)
        
        # 计算总数
        total = query.count()
        
        # 排序和分页
        attributes = (
            query.order_by(ProductAttribute.display_order.asc(), ProductAttribute.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        # 获取每个属性的值数量
        attribute_ids = [attr.id for attr in attributes]
        value_counts = (
            db.query(
                ProductAttributeValue.attribute_id,
                func.count(ProductAttributeValue.id).label('count')
            )
            .filter(ProductAttributeValue.attribute_id.in_(attribute_ids))
            .group_by(ProductAttributeValue.attribute_id)
            .all()
        )
        
        value_count_dict = {item.attribute_id: item.count for item in value_counts}
        
        # 构建响应数据
        items = []
        for attr in attributes:
            item_data = {
                "id": attr.id,
                "name": attr.name,
                "code": attr.code,
                "type": attr.type,
                "display_order": attr.display_order,
                "is_required": attr.is_required,
                "is_configurable": attr.is_configurable,
                "is_searchable": attr.is_searchable,
                "is_comparable": attr.is_comparable,
                "is_filterable": attr.is_filterable,
                "is_visible_on_frontend": attr.is_visible_on_frontend,
                "values_count": value_count_dict.get(attr.id, 0),
                "created_at": attr.created_at,
                "updated_at": attr.updated_at
            }
            items.append(item_data)
        
        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1,
            "size": limit,
            "pages": (total + limit - 1) // limit
        }

    @staticmethod
    def get_attribute_by_id(db: Session, attribute_id: UUID) -> ProductAttribute:
        """根据ID获取商品属性详情"""
        attribute = db.query(ProductAttribute).filter(
            ProductAttribute.id == attribute_id
        ).first()
        
        if not attribute:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="商品属性不存在"
            )
        return attribute

    @staticmethod
    def get_attribute_by_code(db: Session, code: str) -> Optional[ProductAttribute]:
        """根据代码获取商品属性"""
        return db.query(ProductAttribute).filter(
            ProductAttribute.code == code
        ).first()

    @staticmethod
    def create_attribute(db: Session, attribute_data: ProductAttributeCreate) -> ProductAttribute:
        """创建商品属性"""
        # 检查代码是否已存在
        existing = ProductAttributeService.get_attribute_by_code(db, attribute_data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"属性代码 '{attribute_data.code}' 已存在"
            )
        
        # 创建属性
        db_attribute = ProductAttribute(
            name=attribute_data.name,
            code=attribute_data.code,
            description=attribute_data.description,
            type=attribute_data.type,
            display_order=attribute_data.display_order,
            is_required=attribute_data.is_required,
            is_configurable=attribute_data.is_configurable,
            is_searchable=attribute_data.is_searchable,
            is_comparable=attribute_data.is_comparable,
            is_filterable=attribute_data.is_filterable,
            is_visible_on_frontend=attribute_data.is_visible_on_frontend,
            configuration=attribute_data.configuration
        )
        
        db.add(db_attribute)
        db.flush()  # 获取ID
        
        # 创建预定义属性值
        if attribute_data.values:
            for value_data in attribute_data.values:
                db_value = ProductAttributeValue(
                    attribute_id=db_attribute.id,
                    value=value_data.value,
                    label=value_data.label,
                    color_code=value_data.color_code,
                    image_url=value_data.image_url,
                    sort_order=value_data.sort_order
                )
                db.add(db_value)
        
        db.commit()
        db.refresh(db_attribute)
        return db_attribute

    @staticmethod
    def update_attribute(
        db: Session,
        attribute_id: UUID,
        attribute_data: ProductAttributeUpdate
    ) -> ProductAttribute:
        """更新商品属性"""
        db_attribute = ProductAttributeService.get_attribute_by_id(db, attribute_id)
        
        # 检查代码是否冲突
        if attribute_data.code and attribute_data.code != db_attribute.code:
            existing = ProductAttributeService.get_attribute_by_code(db, attribute_data.code)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"属性代码 '{attribute_data.code}' 已存在"
                )
        
        # 更新字段
        update_data = attribute_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_attribute, field, value)
        
        db.commit()
        db.refresh(db_attribute)
        return db_attribute

    @staticmethod
    def delete_attribute(db: Session, attribute_id: UUID) -> None:
        """删除商品属性"""
        db_attribute = ProductAttributeService.get_attribute_by_id(db, attribute_id)
        
        # 检查是否有SKU在使用该属性
        value_count = db.query(ProductAttributeValue).filter(
            ProductAttributeValue.attribute_id == attribute_id
        ).count()
        
        if value_count > 0:
            # 检查是否有SKU在使用这些属性值
            from app.product.models import ProductSku, sku_attribute_value
            sku_count = (
                db.query(func.count(sku_attribute_value.c.sku_id))
                .join(ProductAttributeValue, 
                      sku_attribute_value.c.attribute_value_id == ProductAttributeValue.id)
                .filter(ProductAttributeValue.attribute_id == attribute_id)
                .scalar()
            )
            
            if sku_count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该属性正在被SKU使用，无法删除"
                )
        
        db.delete(db_attribute)
        db.commit()

    @staticmethod
    def get_configurable_attributes(db: Session) -> List[Dict[str, Any]]:
        """获取可配置的属性列表（用于SKU配置）"""
        attributes = (
            db.query(ProductAttribute)
            .filter(ProductAttribute.is_configurable == True)
            .order_by(ProductAttribute.display_order.asc(), ProductAttribute.name.asc())
            .all()
        )
        
        # 序列化为字典
        return [
            {
                "id": str(attr.id),
                "name": attr.name,
                "code": attr.code,
                "type": attr.type,
                "display_order": attr.display_order,
                "is_required": attr.is_required,
                "is_configurable": attr.is_configurable,
                "is_searchable": attr.is_searchable,
                "is_comparable": attr.is_comparable,
                "is_filterable": attr.is_filterable,
                "is_visible_on_frontend": attr.is_visible_on_frontend,
                "created_at": attr.created_at.isoformat() if attr.created_at else None,
                "updated_at": attr.updated_at.isoformat() if attr.updated_at else None
            }
            for attr in attributes
        ]


class ProductAttributeValueService:
    """商品属性值服务"""

    @staticmethod
    def get_attribute_values(
        db: Session,
        attribute_id: UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取指定属性的属性值列表"""
        query = db.query(ProductAttributeValue).filter(
            ProductAttributeValue.attribute_id == attribute_id
        )
        
        # 搜索条件
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    ProductAttributeValue.value.ilike(search_pattern),
                    ProductAttributeValue.label.ilike(search_pattern)
                )
            )
        
        # 计算总数
        total = query.count()
        
        # 排序和分页
        values = (
            query.order_by(ProductAttributeValue.sort_order.asc(), ProductAttributeValue.value.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        # 转换为Pydantic对象并返回字典格式
        pydantic_values = [ProductAttributeValueSchema.from_orm(value) for value in values]
        
        return {
            "items": [value.dict() for value in pydantic_values],
            "total": total,
            "page": skip // limit + 1,
            "size": limit,
            "pages": (total + limit - 1) // limit
        }

    @staticmethod
    def get_attribute_value_by_id(db: Session, value_id: UUID):
        """根据ID获取属性值详情"""
        value = db.query(ProductAttributeValue).filter(
            ProductAttributeValue.id == value_id
        ).first()
        
        if not value:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="属性值不存在"
            )
        
        # 转换为Pydantic对象
        pydantic_value = ProductAttributeValueSchema.from_orm(value)
        return pydantic_value.dict()

    @staticmethod
    def create_attribute_value(
        db: Session,
        attribute_id: UUID,
        value_data: ProductAttributeValueCreate
    ) -> ProductAttributeValue:
        """创建属性值"""
        # 验证属性是否存在
        ProductAttributeService.get_attribute_by_id(db, attribute_id)
        
        # 检查属性值是否已存在
        existing = db.query(ProductAttributeValue).filter(
            and_(
                ProductAttributeValue.attribute_id == attribute_id,
                ProductAttributeValue.value == value_data.value
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"属性值 '{value_data.value}' 已存在"
            )
        
        db_value = ProductAttributeValue(
            attribute_id=attribute_id,
            value=value_data.value,
            label=value_data.label,
            color_code=value_data.color_code,
            image_url=value_data.image_url,
            sort_order=value_data.sort_order
        )
        
        db.add(db_value)
        db.commit()
        db.refresh(db_value)
        return db_value

    @staticmethod
    def update_attribute_value(
        db: Session,
        value_id: UUID,
        value_data: ProductAttributeValueUpdate
    ) -> ProductAttributeValue:
        """更新属性值"""
        db_value = ProductAttributeValueService.get_attribute_value_by_id(db, value_id)
        
        # 检查属性值是否冲突
        if value_data.value and value_data.value != db_value.value:
            existing = db.query(ProductAttributeValue).filter(
                and_(
                    ProductAttributeValue.attribute_id == db_value.attribute_id,
                    ProductAttributeValue.value == value_data.value,
                    ProductAttributeValue.id != value_id
                )
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"属性值 '{value_data.value}' 已存在"
                )
        
        # 更新字段
        update_data = value_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_value, field, value)
        
        db.commit()
        db.refresh(db_value)
        return db_value

    @staticmethod
    def delete_attribute_value(db: Session, value_id: UUID) -> None:
        """删除属性值"""
        db_value = ProductAttributeValueService.get_attribute_value_by_id(db, value_id)
        
        # 检查是否有SKU在使用该属性值
        from app.product.models import sku_attribute_value
        sku_count = (
            db.query(func.count(sku_attribute_value.c.sku_id))
            .filter(sku_attribute_value.c.attribute_value_id == value_id)
            .scalar()
        )
        
        if sku_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该属性值正在被SKU使用，无法删除"
            )
        
        db.delete(db_value)
        db.commit()

    @staticmethod
    def batch_create_attribute_values(
        db: Session,
        attribute_id: UUID,
        values_data: List[ProductAttributeValueCreate]
    ) -> List[ProductAttributeValue]:
        """批量创建属性值"""
        # 验证属性是否存在
        ProductAttributeService.get_attribute_by_id(db, attribute_id)
        
        created_values = []
        for value_data in values_data:
            # 检查是否已存在
            existing = db.query(ProductAttributeValue).filter(
                and_(
                    ProductAttributeValue.attribute_id == attribute_id,
                    ProductAttributeValue.value == value_data.value
                )
            ).first()
            
            if not existing:
                db_value = ProductAttributeValue(
                    attribute_id=attribute_id,
                    value=value_data.value,
                    label=value_data.label,
                    color_code=value_data.color_code,
                    image_url=value_data.image_url,
                    sort_order=value_data.sort_order
                )
                db.add(db_value)
                created_values.append(db_value)
        
        db.commit()
        for value in created_values:
            db.refresh(value)
        
        return created_values
