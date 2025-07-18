"""
Common response utilities for FastAPI
"""
from typing import Any, Optional, Dict
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """Standard response model"""
    code: int = 200
    message: str = "Success"
    data: Optional[Any] = None


def success_response(data: Any = None, message: str = "操作成功") -> Dict[str, Any]:
    """Create a success response"""
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error_response(message: str = "操作失败", code: int = 400, data: Any = None) -> Dict[str, Any]:
    """Create an error response"""
    return {
        "code": code,
        "message": message,
        "data": data
    }


def paginated_response(items: list, total: int, page: int = 1, page_size: int = 10, message: str = "查询成功") -> Dict[str, Any]:
    """Create a paginated response"""
    return {
        "code": 200,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if total > 0 else 0
        }
    }