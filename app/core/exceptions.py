"""
核心异常类
定义应用程序中使用的自定义异常
"""


class BusinessException(Exception):
    """业务逻辑异常"""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationException(Exception):
    """数据验证异常"""
    
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class NotFoundException(Exception):
    """资源未找到异常"""
    
    def __init__(self, message: str, resource_type: str = None):
        self.message = message
        self.resource_type = resource_type
        super().__init__(self.message)