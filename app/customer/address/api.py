from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security.dependencies import get_current_active_admin, get_current_customer
from app.customer.models import AddressType
from app.customer.address.schema import (
    AddressCreate,
    AddressUserCreate,
    AddressUpdate,
    AddressResponse,
    AddressList,
    SetDefaultAddressRequest
)
from app.customer.address.service import AddressService

# 管理端API路由
admin_router = APIRouter(prefix="/admin/customers/{customer_id}/addresses")

# C端用户API路由
user_router = APIRouter(prefix="/user/addresses")


# ----- 管理端API -----

@admin_router.get("", response_model=AddressList)
def get_customer_addresses(
    customer_id: UUID = Path(..., description="客户ID"),
    skip: int = Query(0, description="跳过前N个记录"),
    limit: int = Query(100, description="返回记录数量"), 
    address_type: Optional[AddressType] = Query(None, description="地址类型筛选"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_desc: bool = Query(True, description="是否降序排序"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> AddressList:
    """
    获取特定客户的地址列表（管理员接口）
    """
    result = AddressService.get_addresses(
        db=db,
        customer_id=customer_id,
        skip=skip,
        limit=limit,
        address_type=address_type,
        sort_by=sort_by,
        sort_desc=sort_desc
    )
    
    # 计算总页数
    pages = (result["total"] + limit - 1) // limit if limit > 0 else 1
    
    # 转换items为AddressResponse对象
    items = [AddressResponse.model_validate(item) for item in result["items"]]
    
    return AddressList(
        items=items,
        total=result["total"],
        page=result["page"],
        size=limit,
        pages=pages
    )


@admin_router.get("/{address_id}", response_model=AddressResponse)
def get_customer_address(
    customer_id: UUID = Path(..., description="客户ID"),
    address_id: UUID = Path(..., description="地址ID"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> AddressResponse:
    """
    获取特定客户的地址详情（管理员接口）
    """
    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    
    # 确保地址属于该客户
    if address.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"地址ID {address_id} 不属于客户ID {customer_id}"
        )
    
    return address


@admin_router.post("", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_customer_address(
    customer_id: UUID = Path(..., description="客户ID"),
    address_data: AddressCreate = Body(..., description="地址信息"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> AddressResponse:
    """
    为特定客户创建新地址（管理员接口）
    """
    # 确保请求体中的客户ID与路径参数一致
    if address_data.customer_id != customer_id:
        address_data.customer_id = customer_id
    
    return AddressService.create_address(db=db, address_data=address_data)


@admin_router.put("/{address_id}", response_model=AddressResponse)
def update_customer_address(
    customer_id: UUID = Path(..., description="客户ID"),
    address_id: UUID = Path(..., description="地址ID"),
    address_data: AddressUpdate = Body(..., description="更新的地址信息"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> AddressResponse:
    """
    更新特定客户的地址信息（管理员接口）
    """
    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    
    # 确保地址属于该客户
    if address.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"地址ID {address_id} 不属于客户ID {customer_id}"
        )
    
    return AddressService.update_address(db=db, address_id=address_id, address_data=address_data)


@admin_router.delete("/{address_id}", response_model=Dict[str, Any])
def delete_customer_address(
    customer_id: UUID = Path(..., description="客户ID"),
    address_id: UUID = Path(..., description="地址ID"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
) -> Dict[str, Any]:
    """
    删除特定客户的地址（管理员接口）
    """
    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    
    # 确保地址属于该客户
    if address.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"地址ID {address_id} 不属于客户ID {customer_id}"
        )
    
    return AddressService.delete_address(db=db, address_id=address_id)


# ----- C端用户API -----

@user_router.get("", response_model=Dict[str, Any])
def get_current_user_addresses(
    skip: int = Query(0, description="跳过前N个记录"),
    limit: int = Query(100, description="返回记录数量"), 
    address_type: Optional[AddressType] = Query(None, description="地址类型筛选"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_desc: bool = Query(True, description="是否降序排序"),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    获取当前登录用户的地址列表
    """
    result = AddressService.get_addresses(
        db=db,
        customer_id=current_customer.id,
        skip=skip,
        limit=limit,
        address_type=address_type,
        sort_by=sort_by,
        sort_desc=sort_desc
    )
    
    # 计算页码
    page = skip // limit + 1 if limit else 1
    
    # 转换items为AddressResponse对象
    items = [AddressResponse.model_validate(item) for item in result["items"]]
    
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "total": result["total"],
            "page": page,
            "size": limit,
            "items": items
        }
    }


@user_router.get("/{address_id}", response_model=Dict[str, Any])
def get_current_user_address(
    address_id: UUID = Path(..., description="地址ID"),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    获取当前登录用户的特定地址详情
    """
    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    
    # 确保地址属于当前用户
    if address.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"地址ID {address_id} 不存在或不属于您"
        )
    
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "address": AddressResponse.model_validate(address)
        }
    }


@user_router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_current_user_address(
    address_data: AddressUserCreate = Body(..., description="地址信息"),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    为当前登录用户创建新地址
    """
    # 转换为完整的地址创建模型
    create_data = AddressCreate(
        customer_id=current_customer.id,
        **address_data.dict(exclude={"customer_id"})
    )
    
    result = AddressService.create_address(db=db, address_data=create_data)
    
    return {
        "code": 201,
        "message": "地址创建成功",
        "data": {
            "address": AddressResponse.model_validate(result)
        }
    }


@user_router.put("/{address_id}", response_model=Dict[str, Any])
def update_current_user_address(
    address_id: UUID = Path(..., description="地址ID"),
    address_data: AddressUpdate = Body(..., description="更新的地址信息"),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    更新当前登录用户的地址信息
    """
    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    
    # 确保地址属于当前用户
    if address.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"地址ID {address_id} 不存在或不属于您"
        )
    
    result = AddressService.update_address(db=db, address_id=address_id, address_data=address_data)
    
    return {
        "code": 200,
        "message": "地址更新成功",
        "data": {
            "address": AddressResponse.model_validate(result)
        }
    }


@user_router.delete("/{address_id}", response_model=Dict[str, Any])
def delete_current_user_address(
    address_id: UUID = Path(..., description="地址ID"),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    删除当前登录用户的地址
    """
    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    
    # 确保地址属于当前用户
    if address.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"地址ID {address_id} 不存在或不属于您"
        )
    
    result = AddressService.delete_address(db=db, address_id=address_id)
    
    return {
        "code": 200,
        "message": "地址删除成功",
        "data": result
    }


@user_router.post("/set-default", response_model=Dict[str, Any])
def set_default_address(
    request_data: SetDefaultAddressRequest = Body(..., description="设置默认地址请求"),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
) -> Dict[str, Any]:
    """
    设置当前登录用户的默认地址
    """
    result = AddressService.set_default_address(
        db=db,
        customer_id=current_customer.id,
        request_data=request_data
    )
    
    return {
        "code": 200,
        "message": "默认地址设置成功",
        "data": {
            "address": AddressResponse.model_validate(result)
        }
    }
