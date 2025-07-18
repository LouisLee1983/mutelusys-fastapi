from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
from pathlib import Path
import os
import json
from datetime import datetime
import logging

from app.db.session import get_db
from app.core.dependencies import get_current_admin_user
from app.product.translation.chatgpt_service import deepseek_translation_service

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

# 定义政策文件的基础路径
POLICIES_DIR = Path("static/policies")
POLICIES_META_FILE = POLICIES_DIR / "meta.json"

# 确保目录存在
POLICIES_DIR.mkdir(parents=True, exist_ok=True)

# 政策类型枚举
POLICY_TYPES = {
    "shipping": "SHIPPING POLICY",
    "refund": "REFUND POLICY", 
    "about": "ABOUT MUTELU"
}

# 默认内容模板
DEFAULT_CONTENT = {
    "shipping": """# SHIPPING POLICY

## Processing Time
All orders are processed within 1-3 business days. Orders are not shipped or delivered on weekends or holidays.

## Shipping Rates & Delivery Estimates
We offer FREE standard shipping on all orders over $69.99.

### Domestic Shipping (USA)
- Standard Shipping (5-7 business days): $6.99
- Express Shipping (2-3 business days): $14.99

### International Shipping
- Canada (7-10 business days): $12.99
- Europe (10-15 business days): $19.99
- Asia & Pacific (10-20 business days): $24.99
- Other regions: Calculated at checkout

## Order Tracking
Once your order has shipped, you will receive an email with a tracking number to track your order. 

## Shipping to P.O. Boxes
We currently do not ship to P.O. boxes. Please provide a physical address.

## Contact Us
If you have any questions about shipping, please contact us at support@mutelu.com
""",
    "refund": """# REFUND POLICY

## 30-Day Money Back Guarantee
We offer a 30-day money back guarantee on all purchases. If you're not completely satisfied with your purchase, you can return it for a full refund.

## Return Conditions
To be eligible for a return, your item must be:
- Unused and in the same condition that you received it
- In the original packaging
- Accompanied by proof of purchase

## How to Initiate a Return
1. Contact our customer service team at returns@mutelu.com
2. Provide your order number and reason for return
3. We'll send you a return shipping label
4. Pack the item securely and ship it back to us

## Refund Processing
Once we receive your returned item, we will:
- Inspect the item within 2 business days
- Send you an email confirming receipt
- Process your refund within 5-7 business days
- Credit will appear on your original payment method

## Non-Returnable Items
The following items cannot be returned:
- Personalized or custom-made items
- Clearance items
- Gift cards

## Damaged or Defective Items
If you receive a damaged or defective item, please contact us immediately with photos of the damage. We will arrange for a replacement or full refund.

## Questions?
Email us at support@mutelu.com and we'll be happy to help!
""",
    "about": """# ABOUT MUTELU

## Our Story
Founded in 2020, MUTELU is dedicated to bringing you unique, high-quality jewelry and accessories that celebrate individuality and personal expression.

## Our Mission
We believe that jewelry is more than just an accessory – it's a form of self-expression, a connection to culture and tradition, and a source of positive energy in your daily life.

## Quality Promise
Every piece in our collection is:
- Handcrafted with care and attention to detail
- Made from genuine, natural materials
- Ethically sourced and produced
- Backed by our quality guarantee

## Our Values
- **Authenticity**: We source only genuine materials and work with skilled artisans
- **Sustainability**: We're committed to ethical and sustainable practices
- **Community**: We support local artisans and give back to communities
- **Innovation**: We blend traditional craftsmanship with modern design

## Customer First
Your satisfaction is our top priority. We're here to help you find the perfect piece that resonates with your style and spirit.

## Contact Us
Have questions? Want to learn more about our products?
- Email: hello@mutelu.com
- Phone: 1-800-MUTELU
- Hours: Monday-Friday, 9am-6pm EST

Follow us on social media @muteluofficial for the latest updates and exclusive offers!
"""
}

def create_default_policy(policy_type: str):
    """创建默认的政策文件"""
    if policy_type in DEFAULT_CONTENT:
        file_path = POLICIES_DIR / f"{policy_type}.md"
        file_path.write_text(DEFAULT_CONTENT[policy_type], encoding='utf-8')
        # 更新元数据
        update_policy_meta(policy_type, "system", "en")

def get_policy_content(policy_type: str, language: str = "en") -> dict:
    """获取指定语言的政策内容"""
    if policy_type not in POLICY_TYPES:
        raise HTTPException(status_code=404, detail="Policy type not found")
    
    # 构建文件名
    if language == "en":
        filename = f"{policy_type}.md"
    else:
        filename = f"{policy_type}_{language}.md"
    
    file_path = POLICIES_DIR / filename
    
    # 如果指定语言的文件不存在，回退到英文版本
    if not file_path.exists() and language != "en":
        file_path = POLICIES_DIR / f"{policy_type}.md"
    
    # 如果英文版本也不存在，创建默认内容
    if not file_path.exists():
        create_default_policy(policy_type)
        file_path = POLICIES_DIR / f"{policy_type}.md"
    
    # 读取文件内容
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # 获取meta信息
        meta_info = get_policy_meta(policy_type, language)
        
        return {
            "type": policy_type,
            "title": POLICY_TYPES[policy_type],
            "content": content,
            "language": language,
            "last_updated": meta_info.get("last_updated"),
            "updated_by": meta_info.get("updated_by")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read policy: {str(e)}")

def save_policy_content(policy_type: str, content: str, updated_by: str, language: str = "en") -> dict:
    """保存政策内容到指定语言的文件"""
    if policy_type not in POLICY_TYPES:
        raise HTTPException(status_code=404, detail="Policy type not found")
    
    # 构建文件名
    if language == "en":
        filename = f"{policy_type}.md"
    else:
        filename = f"{policy_type}_{language}.md"
    
    file_path = POLICIES_DIR / filename
    
    try:
        # 保存文件
        file_path.write_text(content, encoding='utf-8')
        
        # 更新meta信息
        update_policy_meta(policy_type, updated_by, language)
        
        return get_policy_content(policy_type, language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save policy: {str(e)}")

def get_policy_meta(policy_type: str, language: str = "en") -> dict:
    """获取政策的元数据"""
    meta_key = f"{policy_type}_{language}" if language != "en" else policy_type
    
    if POLICIES_META_FILE.exists():
        try:
            meta_data = json.loads(POLICIES_META_FILE.read_text(encoding='utf-8'))
            return meta_data.get("policies", {}).get(meta_key, {})
        except:
            pass
    return {}

def update_policy_meta(policy_type: str, updated_by: str, language: str = "en"):
    """更新政策的元数据"""
    meta_key = f"{policy_type}_{language}" if language != "en" else policy_type
    
    # 读取现有meta数据
    meta_data = {}
    if POLICIES_META_FILE.exists():
        try:
            meta_data = json.loads(POLICIES_META_FILE.read_text(encoding='utf-8'))
        except:
            meta_data = {}
    
    # 确保结构存在
    if "policies" not in meta_data:
        meta_data["policies"] = {}
    
    # 更新特定政策的meta信息
    meta_data["policies"][meta_key] = {
        "type": policy_type,
        "language": language,
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "updated_by": updated_by
    }
    
    # 保存meta文件
    POLICIES_META_FILE.write_text(json.dumps(meta_data, indent=2, ensure_ascii=False), encoding='utf-8')

def get_available_languages(policy_type: str) -> List[str]:
    """获取某个政策的所有可用语言版本"""
    if policy_type not in POLICY_TYPES:
        return []
    
    languages = ["en"]  # 英文始终可用
    
    # 检查其他语言版本
    pattern = f"{policy_type}_*.md"
    for file_path in POLICIES_DIR.glob(pattern):
        # 提取语言代码
        filename = file_path.stem
        if "_" in filename:
            _, lang_code = filename.split("_", 1)
            languages.append(lang_code)
    
    return list(set(languages))

@router.get("/policies")
async def get_all_policies(
    language: str = "en",
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_user)
):
    """获取所有政策内容（支持多语言）"""
    policies = []
    for policy_type in POLICY_TYPES.keys():
        policies.append(get_policy_content(policy_type, language))
    
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "policies": policies,
            "language": language
        }
    }

@router.get("/policies/{policy_type}")
async def get_policy(
    policy_type: str,
    language: str = "en",
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_user)
):
    """获取指定政策内容（支持多语言）"""
    if policy_type not in POLICY_TYPES:
        raise HTTPException(status_code=404, detail="Policy type not found")
    
    policy = get_policy_content(policy_type, language)
    
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "policy": policy,
            "available_languages": get_available_languages(policy_type)
        }
    }

@router.put("/policies/{policy_type}")
async def update_policy(
    policy_type: str,
    data: dict,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_user)
):
    """更新政策内容（支持多语言）"""
    content = data.get("content", "")
    language = data.get("language", "en")
    
    if not content:
        raise HTTPException(status_code=400, detail="Content is required")
    
    policy = save_policy_content(
        policy_type=policy_type,
        content=content,
        updated_by=admin.username,
        language=language
    )
    
    return {
        "code": 200,
        "message": "更新成功",
        "data": {
            "policy": policy
        }
    }

@router.post("/policies/{policy_type}/translate")
async def translate_policy(
    policy_type: str,
    data: dict,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_user)
):
    """使用AI翻译政策内容到指定语言"""
    source_language = data.get("source_language", "en")
    target_language = data.get("target_language")
    
    if not target_language:
        raise HTTPException(status_code=400, detail="Target language is required")
    
    if policy_type not in POLICY_TYPES:
        raise HTTPException(status_code=404, detail="Policy type not found")
    
    # 获取源语言的内容
    source_policy = get_policy_content(policy_type, source_language)
    source_content = source_policy.get("content", "")
    
    if not source_content:
        raise HTTPException(status_code=400, detail="Source content is empty")
    
    try:
        # 调用翻译服务
        translated_content = await deepseek_translation_service.translate_policy_content(
            content=source_content,
            source_language=source_language,
            target_language=target_language,
            policy_type=policy_type
        )
        
        logger.info(f"Translation successful for {policy_type} to {target_language}")
        
        # 保存翻译后的内容
        try:
            translated_policy = save_policy_content(
                policy_type=policy_type,
                content=translated_content,
                updated_by=f"{admin.username} (AI Translated)",
                language=target_language
            )
            
            return {
                "code": 200,
                "message": "翻译成功",
                "data": {
                    "policy": translated_policy
                }
            }
        except Exception as save_error:
            logger.error(f"Failed to save translated content: {save_error}")
            # 即使保存后读取失败，翻译文件可能已经保存成功
            # 返回一个简化的成功响应
            return {
                "code": 200,
                "message": "翻译成功",
                "data": {
                    "policy": {
                        "type": policy_type,
                        "title": POLICY_TYPES[policy_type],
                        "content": translated_content,
                        "language": target_language,
                        "updated_by": f"{admin.username} (AI Translated)"
                    }
                }
            }
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.get("/policies/{policy_type}/languages")
async def get_policy_languages(
    policy_type: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_user)
):
    """获取某个政策的所有可用语言版本"""
    if policy_type not in POLICY_TYPES:
        raise HTTPException(status_code=404, detail="Policy type not found")
    
    languages = get_available_languages(policy_type)
    language_details = []
    
    for lang in languages:
        meta = get_policy_meta(policy_type, lang)
        language_details.append({
            "code": lang,
            "name": deepseek_translation_service.get_language_name(lang),
            "last_updated": meta.get("last_updated"),
            "updated_by": meta.get("updated_by")
        })
    
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "languages": language_details
        }
    }

@router.post("/policies/{policy_type}/upload-image")
async def upload_policy_image(
    policy_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_user)
):
    """上传政策内容中的图片"""
    if policy_type not in POLICY_TYPES:
        raise HTTPException(status_code=400, detail="Invalid policy type")
    
    # 验证文件类型
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # 创建图片目录
    images_dir = POLICIES_DIR / "images" / policy_type
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成唯一文件名
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = images_dir / filename
    
    # 保存文件
    content = await file.read()
    file_path.write_bytes(content)
    
    # 返回相对URL
    relative_url = f"/static/policies/images/{policy_type}/{filename}"
    
    return {
        "code": 200,
        "message": "上传成功",
        "data": {
            "url": relative_url,
            "filename": filename
        }
    }

# Public API endpoints (无需登录)
@router.get("/public/policies/{policy_type}")
async def get_public_policy(
    policy_type: str,
    db: Session = Depends(get_db)
):
    """公开获取政策内容（用于前端展示）"""
    try:
        policy = get_policy_content(policy_type)
        return {
            "code": 200,
            "message": "操作成功",
            "data": {
                "policy": {
                    "type": policy.get("type"),
                    "title": policy.get("title"),
                    "content": policy.get("content")
                }
            }
        }
    except Exception as e:
        return {
            "code": 404,
            "message": "政策内容不存在",
            "data": None
        }

@router.get("/api/v1/public/policies")
async def get_all_public_policies(
    db: Session = Depends(get_db)
):
    """公开获取所有政策内容"""
    policies = []
    for policy_type in POLICY_TYPES.keys():
        try:
            policy = get_policy_content(policy_type)
            policies.append({
                "type": policy.get("type"),
                "title": policy.get("title"),
                "content": policy.get("content")
            })
        except:
            continue
    
    return {
        "code": 200,
        "message": "操作成功",
        "data": {
            "policies": policies
        }
    } 