from app.security.models import User, Role, OperationLog, LoginLog

# 定义用户状态枚举
import enum


# 用户状态枚举
class UserStatus(str, enum.Enum):
    ACTIVE = "active"       # 活跃
    INACTIVE = "inactive"   # 非活跃
    SUSPENDED = "suspended" # 已停用
    DELETED = "deleted"     # 已删除


# 重新导出这些模型，以便在app.security.user.models中可用
__all__ = [
    "User",
    "Role",
    "OperationLog", 
    "LoginLog",
    "UserStatus"
] 