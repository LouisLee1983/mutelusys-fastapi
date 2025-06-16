from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

# 权限简单模�?
class PermissionSimple(BaseModel):
    id: UUID
    name: str
    code: str
    
    class Config:
        from_attributes = True

# 角色基础模型
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_default: bool = False

# 创建角色请求模型
class RoleCreate(RoleBase):
    pass

# 更新角色请求模型
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    
    class Config:
        from_attributes = True

# 角色响应模型（包含权限）
class RoleResponse(RoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    permissions: List[PermissionSimple] = []
    
    class Config:
        from_attributes = True

# 简化的角色响应模型
class RoleSimple(BaseModel):
    id: UUID
    name: str
    
    class Config:
        from_attributes = True

# 角色列表响应模型
class RoleListResponse(BaseModel):
    total: int
    items: List[RoleResponse]
    
    class Config:
        from_attributes = True

# 角色权限分配请求模型
class RolePermissionAssign(BaseModel):
    permission_ids: List[UUID] = Field(..., description="权限ID列表")

# 系统预定义角�?
class SystemRoles:
    SUPER_ADMIN = "super_admin"  # 超级管理�?
    ADMIN = "admin"              # 普通管理员
    OPERATOR = "operator"        # 运营
    CUSTOMER_SERVICE = "customer_service"  # 客服
    WAREHOUSE = "warehouse"      # 仓库管理�?
    FINANCE = "finance"          # 财务
