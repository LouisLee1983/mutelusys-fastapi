from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Any, Dict
from uuid import UUID

from app.core.dependencies import get_db, get_current_admin_user

# 初始化路由器
router = APIRouter(
    prefix="/blogs",
    tags=["Blog Posts"],
    dependencies=[Depends(get_current_admin_user)]
)

# 这里暂时不添加具体的路由端点，只提供router实例
