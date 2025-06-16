from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.router import api_router

# 导入所有模型以确保 SQLAlchemy 能正确建立关系映射
from app.db.init_db import *

app = FastAPI(
    title="Mutelusys API",
    description="Mutelusys后台管理系统API",
    version="0.1.0"
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 挂载测试图片目录
try:
    from pathlib import Path
    test_images_path = Path("../design-media/images")
    if test_images_path.exists():
        app.mount("/static/test-images", StaticFiles(directory=str(test_images_path)), name="test-images")
    
    # 挂载上传文件目录
    uploads_path = Path("../design-media/uploads")
    if uploads_path.exists():
        app.mount("/static/uploads", StaticFiles(directory=str(uploads_path)), name="uploads")
except Exception as e:
    print(f"挂载静态文件目录失败: {e}")

# 全局异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """处理HTTP异常，返回统一格式"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """处理其他异常"""
    print(f"未处理的异常: {type(exc).__name__}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )

# 注册API路由 (包含所有版本的API)
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"msg": "Mutelusys FastAPI 后端已启动"} 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True) 