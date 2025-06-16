import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    """系统用户模型，如管理员、客服、运营等"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    phone_number = Column(String(20), nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    login_logs = relationship("LoginLog", back_populates="user")
    operation_logs = relationship("OperationLog", back_populates="user")


class Role(Base):
    """用户角色模型，定义权限范围"""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联
    users = relationship("User", secondary="user_roles", back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")


class Permission(Base):
    """权限项模型，具体操作权限"""
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    module = Column(String(50), nullable=False, comment="权限所属模块，如'product', 'order', 'customer'等")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关联
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")


class UserRole(Base):
    """用户-角色关联表"""
    __tablename__ = "user_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class RolePermission(Base):
    """角色-权限关联表"""
    __tablename__ = "role_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LoginLog(Base):
    """登录日志，记录IP、设备、时间等"""
    __tablename__ = "login_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_address = Column(String(50), nullable=False)
    user_agent = Column(String(255), nullable=True)
    device_type = Column(String(50), nullable=True)
    login_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    login_status = Column(Boolean, default=True, comment="登录是否成功")
    status_message = Column(String(200), nullable=True, comment="登录失败原因等")

    # 关联
    user = relationship("User", back_populates="login_logs")


class OperationLog(Base):
    """操作日志，记录关键操作和变更"""
    __tablename__ = "operation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    operation_type = Column(String(50), nullable=False, comment="操作类型，如'create', 'update', 'delete'等")
    target_model = Column(String(50), nullable=False, comment="操作的目标模型，如'product', 'order'等")
    target_id = Column(String(100), nullable=True, comment="操作的目标ID")
    details = Column(Text, nullable=True, comment="操作详细信息，通常是JSON格式")
    ip_address = Column(String(50), nullable=False)
    operation_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联
    user = relationship("User", back_populates="operation_logs")


class DataBackup(Base):
    """数据备份记录"""
    __tablename__ = "data_backups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    backup_name = Column(String(100), nullable=False)
    backup_path = Column(String(255), nullable=False)
    backup_size = Column(Integer, nullable=True, comment="备份文件大小，单位KB")
    backup_type = Column(String(50), nullable=False, comment="备份类型，如'full', 'incremental'等")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(20), default="completed", comment="备份状态，如'in_progress', 'completed', 'failed'等")
    notes = Column(Text, nullable=True)


class SystemSetting(Base):
    """系统设置，包含安全配置等"""
    __tablename__ = "system_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text, nullable=True)
    setting_type = Column(String(20), default="string", comment="设置值类型，如'string', 'number', 'boolean', 'json'等")
    setting_group = Column(String(50), nullable=False, comment="设置分组，如'security', 'display', 'notification'等")
    description = Column(String(255), nullable=True)
    is_sensitive = Column(Boolean, default=False, comment="是否敏感信息，如密钥等")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
