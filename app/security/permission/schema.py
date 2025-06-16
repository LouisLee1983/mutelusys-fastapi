from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

# 权限基础模型
class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    module: str

# 创建权限时的请求模型
class PermissionCreate(PermissionBase):
    pass

# 更新权限信息的请求模型
class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    module: Optional[str] = None
    
    class Config:
        from_attributes = True

# 返回给API的权限信息模型
class PermissionResponse(PermissionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 简化的权限信息模型
class PermissionSimple(BaseModel):
    id: UUID
    name: str
    code: str
    
    class Config:
        from_attributes = True

# 权限列表响应模型
class PermissionListResponse(BaseModel):
    total: int
    items: List[PermissionResponse]
    
    class Config:
        from_attributes = True
