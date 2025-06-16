from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, and_, or_
from fastapi import HTTPException, status

from app.customer.models import CustomerAddress, Customer, AddressType
from app.customer.address.schema import AddressCreate, AddressUpdate, SetDefaultAddressRequest


class AddressService:
    """客户地址服务类，提供地址的CRUD操作"""
    
    @staticmethod
    def get_addresses(
        db: Session, 
        customer_id: UUID,
        skip: int = 0, 
        limit: int = 100,
        address_type: Optional[AddressType] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Dict[str, Any]:
        """
        获取客户的地址列表，支持过滤和排序
        """
        # 基础查询
        query = db.query(CustomerAddress).filter(CustomerAddress.customer_id == customer_id)
        
        # 应用过滤条件
        if address_type:
            query = query.filter(
                or_(
                    CustomerAddress.address_type == address_type,
                    CustomerAddress.address_type == AddressType.BOTH
                )
            )
        
        # 计算总数
        total = query.count()
        
        # 排序
        sort_column = getattr(CustomerAddress, sort_by, CustomerAddress.created_at)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # 分页
        addresses = query.offset(skip).limit(limit).all()
        
        # 添加计算字段
        for address in addresses:
            address.full_name = f"{address.first_name} {address.last_name}"
            address.full_address = AddressService._format_full_address(address)
        
        return {
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "items": addresses
        }
    
    @staticmethod
    def get_address_by_id(db: Session, address_id: UUID) -> CustomerAddress:
        """根据ID获取地址详情"""
        address = db.query(CustomerAddress).filter(CustomerAddress.id == address_id).first()
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"地址ID {address_id} 不存在"
            )
        
        # 添加计算字段
        address.full_name = f"{address.first_name} {address.last_name}"
        address.full_address = AddressService._format_full_address(address)
            
        return address
    
    @staticmethod
    def create_address(db: Session, address_data: AddressCreate) -> CustomerAddress:
        """创建新地址"""
        # 检查客户是否存在
        customer = db.query(Customer).filter(Customer.id == address_data.customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"客户ID {address_data.customer_id} 不存在"
            )
        
        # 如果设置为默认地址，需要取消同类型的其他默认地址
        if address_data.is_default:
            AddressService._unset_default_addresses(
                db=db, 
                customer_id=address_data.customer_id, 
                address_type=address_data.address_type
            )
        
        # 创建地址记录
        db_address = CustomerAddress(**address_data.dict())
        
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        
        # 添加计算字段
        db_address.full_name = f"{db_address.first_name} {db_address.last_name}"
        db_address.full_address = AddressService._format_full_address(db_address)
        
        return db_address
    
    @staticmethod
    def update_address(
        db: Session, 
        address_id: UUID, 
        address_data: AddressUpdate
    ) -> CustomerAddress:
        """更新地址信息"""
        address = AddressService.get_address_by_id(db, address_id)
        
        # 如果设置为默认地址，需要取消同类型的其他默认地址
        if address_data.is_default:
            AddressService._unset_default_addresses(
                db=db, 
                customer_id=address.customer_id, 
                address_type=address_data.address_type or address.address_type
            )
        
        # 更新地址字段
        for key, value in address_data.dict(exclude_unset=True).items():
            setattr(address, key, value)
        
        db.commit()
        db.refresh(address)
        
        # 添加计算字段
        address.full_name = f"{address.first_name} {address.last_name}"
        address.full_address = AddressService._format_full_address(address)
        
        return address
    
    @staticmethod
    def delete_address(db: Session, address_id: UUID) -> Dict[str, Any]:
        """删除地址"""
        address = AddressService.get_address_by_id(db, address_id)
        
        db.delete(address)
        db.commit()
        
        return {"message": "地址已成功删除"}
    
    @staticmethod
    def set_default_address(
        db: Session, 
        customer_id: UUID,
        request_data: SetDefaultAddressRequest
    ) -> CustomerAddress:
        """设置默认地址"""
        # 获取要设为默认的地址
        address = db.query(CustomerAddress).filter(
            CustomerAddress.id == request_data.address_id,
            CustomerAddress.customer_id == customer_id
        ).first()
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"地址ID {request_data.address_id} 不存在或不属于该客户"
            )
        
        # 解除同类型的其他默认地址
        address_type = request_data.address_type or address.address_type
        AddressService._unset_default_addresses(
            db=db, 
            customer_id=customer_id, 
            address_type=address_type
        )
        
        # 设置为默认地址
        address.is_default = True
        db.commit()
        db.refresh(address)
        
        # 添加计算字段
        address.full_name = f"{address.first_name} {address.last_name}"
        address.full_address = AddressService._format_full_address(address)
        
        return address
    
    @staticmethod
    def _unset_default_addresses(
        db: Session, 
        customer_id: UUID, 
        address_type: AddressType
    ) -> None:
        """取消该客户同类型的所有默认地址"""
        if address_type == AddressType.BOTH:
            # 如果是两者都是，则需要取消所有类型的默认地址
            db.query(CustomerAddress).filter(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_default == True
            ).update({"is_default": False})
        else:
            # 取消特定类型的默认地址
            db.query(CustomerAddress).filter(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_default == True,
                or_(
                    CustomerAddress.address_type == address_type,
                    CustomerAddress.address_type == AddressType.BOTH
                )
            ).update({"is_default": False})
        
        db.commit()
    
    @staticmethod
    def _format_full_address(address: CustomerAddress) -> str:
        """格式化完整地址"""
        components = [
            address.address_line1,
            address.address_line2,
            address.city,
            address.state_province,
            address.postal_code,
            address.country_code
        ]
        
        # 过滤掉None值
        components = [c for c in components if c]
        
        return ", ".join(components)
