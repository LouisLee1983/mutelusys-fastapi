import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 配置JSON序列化器，确保中文字符不被转义为Unicode
def json_serializer(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

# 创建引擎时指定JSON序列化器
engine = create_engine(
    settings.DATABASE_URL, 
    echo=False,
    json_serializer=json_serializer  # 使用自定义JSON序列化器
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
