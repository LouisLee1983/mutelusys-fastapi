from typing import List, Optional, Dict, Union, Any
from uuid import UUID
import uuid
import os
import shutil
from pathlib import Path
from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import func, select, desc, or_, and_
from fastapi import HTTPException, status, UploadFile
from datetime import datetime
import json
from PIL import Image

from app.product.models import ProductCategory, ProductCategoryTranslation, Product, product_category
from app.product.category.schema import ProductCategoryCreate, ProductCategoryUpdate
from app.product.category.schema import ProductCategoryTranslationCreate, ProductCategoryTranslationUpdate


class ProductCategoryService:
    """商品分类服务类，提供分类的增删改查功能"""
    
    # 配置常量
    UPLOAD_DIR = "static/uploads/category-images"
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def _ensure_upload_dir(category_slug: str, category_id: UUID) -> Path:
        """确保上传目录存在"""
        upload_path = Path(ProductCategoryService.UPLOAD_DIR) / f"{category_slug}+{category_id}"
        upload_path.mkdir(parents=True, exist_ok=True)
        return upload_path
    
    @staticmethod
    def _validate_image_file(file: UploadFile) -> None:
        """验证图片文件"""
        # 检查文件扩展名
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ProductCategoryService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件格式。支持的格式: {', '.join(ProductCategoryService.ALLOWED_EXTENSIONS)}"
            )
        
        # 检查文件大小
        if file.size and file.size > ProductCategoryService.MAX_FILE_SIZE:
            max_size_mb = ProductCategoryService.MAX_FILE_SIZE // 1024 // 1024
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"图片文件大小超过限制，最大允许 {max_size_mb}MB"
            )
    
    @staticmethod
    async def upload_category_image(
        db: Session, 
        category_id: UUID, 
        file: UploadFile, 
        image_type: str = "hero"  # "hero" 或 "icon"
    ) -> Dict[str, Any]:
        """
        上传分类图片
        """
        # 验证分类是否存在
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类ID {category_id} 不存在"
            )
        
        # 验证文件
        ProductCategoryService._validate_image_file(file)
        
        # 确保上传目录存在
        upload_dir = ProductCategoryService._ensure_upload_dir(category.slug, category_id)
        
        # 设置文件名
        file_extension = Path(file.filename).suffix.lower()
        if image_type == "hero":
            filename = f"hero_image{file_extension}"
        else:
            filename = f"icon_image{file_extension}"
        
        file_path = upload_dir / filename
        
        try:
            # 保存文件
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # 验证图片完整性并获取尺寸
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    img.verify()
            except Exception:
                # 如果图片损坏，删除文件
                if file_path.exists():
                    file_path.unlink()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="图片文件损坏"
                )
            
            # 生成访问URL
            relative_path = f"uploads/category-images/{category.slug}+{category_id}/{filename}"
            file_url = f"/static/{relative_path}"
            
            # 更新数据库中的图片URL
            if image_type == "hero":
                category.image_url = file_url
            else:
                category.icon_url = file_url
            
            db.commit()
            
            return {
                "success": True,
                "filename": filename,
                "file_path": str(file_path),
                "file_url": file_url,
                "file_size": len(content),
                "width": width,
                "height": height,
                "image_type": image_type,
                "upload_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            # 清理已上传的文件
            if file_path.exists():
                file_path.unlink()
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"文件上传失败: {str(e)}"
            )
    
    @staticmethod
    async def delete_category_image(
        db: Session, 
        category_id: UUID, 
        image_type: str = "hero"  # "hero" 或 "icon"
    ) -> Dict[str, Any]:
        """
        删除分类图片
        """
        # 验证分类是否存在
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类ID {category_id} 不存在"
            )
        
        # 获取当前图片URL
        current_image_url = category.image_url if image_type == "hero" else category.icon_url
        
        if not current_image_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类{image_type}图片不存在"
            )
        
        # 构建文件路径
        upload_dir = ProductCategoryService._ensure_upload_dir(category.slug, category_id)
        filename = f"{image_type}_image.jpg"  # 假设是jpg格式，实际需要从URL解析
        
        # 从URL中解析实际文件名
        if current_image_url.startswith('/static/'):
            relative_path = current_image_url[8:]  # 去掉 '/static/' 前缀
            file_path = Path("static") / relative_path
        else:
            file_path = upload_dir / filename
        
        try:
            # 删除物理文件
            deleted_file_path = None
            if file_path.exists():
                file_path.unlink()
                deleted_file_path = str(file_path)
            
            # 更新数据库
            if image_type == "hero":
                category.image_url = None
            else:
                category.icon_url = None
            
            db.commit()
            
            return {
                "success": True,
                "message": f"分类{image_type}图片删除成功",
                "deleted_file_path": deleted_file_path
            }
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"删除图片失败: {str(e)}"
            )

    @staticmethod
    def _category_to_dict(category: ProductCategory, language_code: str = "zh-CN") -> Dict[str, Any]:
        """将ProductCategory对象转换为字典，用于JSON序列化"""
        # 先设置默认值
        result = {
            "id": str(category.id),
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "parent_id": str(category.parent_id) if category.parent_id else None,
            "level": category.level.value if category.level else None,
            "image_url": category.image_url,
            "icon_url": category.icon_url,
            "is_active": category.is_active,
            "is_featured": category.is_featured,
            "sort_order": category.sort_order,
            "seo_title": category.seo_title,
            "seo_description": category.seo_description,
            "seo_keywords": category.seo_keywords,
            "created_at": category.created_at.isoformat(),
            "updated_at": category.updated_at.isoformat(),
            "translations": []
        }
        
        # 查找对应语言的翻译并覆盖字段
        if hasattr(category, 'translations') and category.translations:
            for translation in category.translations:
                result["translations"].append({
                    "id": str(translation.id),
                    "category_id": str(translation.category_id),
                    "language_code": translation.language_code,
                    "name": translation.name,
                    "description": translation.description,
                    "seo_title": translation.seo_title,
                    "seo_description": translation.seo_description,
                    "seo_keywords": translation.seo_keywords,
                    "created_at": translation.created_at.isoformat(),
                    "updated_at": translation.updated_at.isoformat(),
                })
                
                # 如果找到对应语言的翻译，使用翻译内容覆盖
                if translation.language_code == language_code:
                    result["name"] = translation.name or result["name"]
                    result["description"] = translation.description or result["description"]
                    result["seo_title"] = translation.seo_title or result["seo_title"]
                    result["seo_description"] = translation.seo_description or result["seo_description"]
                    result["seo_keywords"] = translation.seo_keywords or result["seo_keywords"]
        
        return result

    @staticmethod
    def _build_category_tree(categories: List[ProductCategory], parent_id: Optional[UUID] = None, language_code: str = "zh-CN") -> List[Dict[str, Any]]:
        """构建分类树结构"""
        tree = []
        for category in categories:
            if category.parent_id == parent_id:
                category_dict = ProductCategoryService._category_to_dict(category, language_code)
                # 递归获取子分类
                children = ProductCategoryService._build_category_tree(categories, category.id, language_code)
                if children:
                    category_dict["children"] = children
                tree.append(category_dict)
        
        # 按sort_order和名称排序
        tree.sort(key=lambda x: (x["sort_order"], x["name"]))
        return tree

    @staticmethod
    def get_public_category_tree(db: Session, language_code: str = "zh-CN") -> List[Dict[str, Any]]:
        """
        获取公开的分类树形结构（只返回激活状态的分类）
        用于C端网站显示
        """
        # 查询所有激活的分类
        categories = db.query(ProductCategory).filter(
            ProductCategory.is_active == True
        ).options(
            joinedload(ProductCategory.translations)
        ).order_by(
            ProductCategory.sort_order,
            ProductCategory.name
        ).all()
        
        # 构建树形结构
        tree = ProductCategoryService._build_category_tree(categories, None, language_code)
        return tree

    @staticmethod
    def get_categories(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        parent_id: Optional[UUID] = None,
        level: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        search: Optional[str] = None,
        include_children: bool = False
    ) -> Dict[str, Any]:
        """
        获取分类列表，支持分页、过滤和搜索
        """
        query = db.query(ProductCategory)
        
        # 应用过滤条件
        if parent_id is not None:
            query = query.filter(ProductCategory.parent_id == parent_id)
        if level is not None:
            query = query.filter(ProductCategory.level == level)
        if is_active is not None:
            query = query.filter(ProductCategory.is_active == is_active)
        if is_featured is not None:
            query = query.filter(ProductCategory.is_featured == is_featured)
        if search:
            search_term = f"%{search}%"
            query = query.filter(or_(
                ProductCategory.name.ilike(search_term),
                ProductCategory.slug.ilike(search_term),
                ProductCategory.description.ilike(search_term) if ProductCategory.description else False
            ))

        # 计算总数
        total = query.count()
        
        # 排序和分页
        query = query.order_by(ProductCategory.sort_order, ProductCategory.name).offset(skip).limit(limit)
        
        categories = query.all()
        
        # 获取关联的产品和子分类数量
        result_categories = []
        for category in categories:
            # 产品数量 - 使用多对多关系查询
            products_count = db.query(func.count(Product.id)).join(
                product_category, Product.id == product_category.c.product_id
            ).filter(
                product_category.c.category_id == category.id
            ).scalar()
            
            # 子分类数量
            children_count = db.query(func.count(ProductCategory.id)).filter(
                ProductCategory.parent_id == category.id
            ).scalar()
            
            category_dict = {
                **category.__dict__,
                "products_count": products_count,
                "children_count": children_count
            }
            
            # 如果需要包含子分类
            if include_children and children_count > 0:
                children = ProductCategoryService.get_children(db, category.id, recursive=True)
                category_dict["children"] = children
                
            result_categories.append(category_dict)
            
        return {
            "items": result_categories,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }

    @staticmethod
    def get_children(db: Session, parent_id: UUID, recursive: bool = False, language_code: str = "zh-CN") -> List[Dict[str, Any]]:
        """获取指定分类的子分类"""
        children = db.query(ProductCategory).filter(
            ProductCategory.parent_id == parent_id
        ).options(
            joinedload(ProductCategory.translations)
        ).all()
        
        result = []
        for child in children:
            child_dict = ProductCategoryService._category_to_dict(child, language_code)
            
            # 递归获取子分类
            if recursive:
                child_dict["children"] = ProductCategoryService.get_children(db, child.id, recursive=True, language_code=language_code)
            else:
                child_dict["children"] = []
                
            result.append(child_dict)
            
        return result

    @staticmethod
    def get_category_tree(db: Session, parent_id: Optional[UUID] = None) -> Dict[str, Any]:
        """获取分类树结构"""
        # 获取根分类或指定父分类的子分类
        query = db.query(ProductCategory)
        if parent_id:
            query = query.filter(ProductCategory.parent_id == parent_id)
        else:
            query = query.filter(ProductCategory.parent_id.is_(None))
            
        categories = query.order_by(ProductCategory.sort_order, ProductCategory.name).all()
        
        # 构建树结构
        result = []
        for category in categories:
            category_dict = {
                **category.__dict__,
                "children": ProductCategoryService.get_children(db, category.id, recursive=True)
            }
            
            # 产品数量 - 使用多对多关系查询
            products_count = db.query(func.count(Product.id)).join(
                product_category, Product.id == product_category.c.product_id
            ).filter(
                product_category.c.category_id == category.id
            ).scalar()
            
            category_dict["products_count"] = products_count
            result.append(category_dict)
            
        return {
            "items": result,
            "total": len(result)
        }

    @staticmethod
    def get_category_by_id(db: Session, category_id: UUID) -> Dict[str, Any]:
        """根据ID获取分类详情"""
        category = db.query(ProductCategory).options(
            joinedload(ProductCategory.translations)
        ).filter(ProductCategory.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类ID {category_id} 不存在"
            )
        return ProductCategoryService._category_to_dict(category)

    @staticmethod
    def get_category_by_slug(db: Session, slug: str) -> ProductCategory:
        """根据别名获取分类详情"""
        category = db.query(ProductCategory).filter(ProductCategory.slug == slug).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类别名 {slug} 不存在"
            )
        return category

    @staticmethod
    def create_category(db: Session, category_data: ProductCategoryCreate) -> Dict[str, Any]:
        """创建新分类"""
        # 检查别名是否已存在
        existing = db.query(ProductCategory).filter(ProductCategory.slug == category_data.slug).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"分类别名 '{category_data.slug}' 已存在"
            )
            
        # 检查父分类是否存在
        if category_data.parent_id:
            parent = db.query(ProductCategory).filter(ProductCategory.id == category_data.parent_id).first()
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"父分类ID {category_data.parent_id} 不存在"
                )
                
        # 创建分类
        category_dict = category_data.dict(exclude={"translations"})
        
        # 设置默认图片（如果未提供）
        if not category_dict.get('image_url'):
            category_dict['image_url'] = "/static/uploads/category-hero-images/category-default-hero-image.jpg"
        if not category_dict.get('icon_url'):
            category_dict['icon_url'] = "/static/uploads/category-hero-images/category-default-icon.jpg"
            
        new_category = ProductCategory(**category_dict)
        db.add(new_category)
        db.flush()  # 获取新创建的ID
        
        # 创建翻译 (如果提供了翻译数据)
        if category_data.translations:
            for translation_data in category_data.translations:
                translation = ProductCategoryTranslation(
                    **translation_data.dict(),
                    category_id=new_category.id
                )
                db.add(translation)
            
        db.commit()
        # 重新查询以获取完整的对象（包括关联数据）
        created_category = db.query(ProductCategory).options(
            joinedload(ProductCategory.translations)
        ).filter(ProductCategory.id == new_category.id).first()
        
        return ProductCategoryService._category_to_dict(created_category)

    @staticmethod
    def update_category(
        db: Session, 
        category_id: UUID, 
        category_data: ProductCategoryUpdate
    ) -> Dict[str, Any]:
        """更新分类信息"""
        # 先获取原始的SQLAlchemy对象进行更新
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类ID {category_id} 不存在"
            )
        
        # 检查别名是否已被其他分类使用
        if category_data.slug and category_data.slug != category.slug:
            existing = db.query(ProductCategory).filter(
                ProductCategory.slug == category_data.slug, 
                ProductCategory.id != category_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"分类别名 '{category_data.slug}' 已被其他分类使用"
                )
                
        # 检查父分类是否存在且不是自己或自己的子分类(避免循环引用)
        if category_data.parent_id and category_data.parent_id != category.parent_id:
            if category_data.parent_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="分类不能是自己的父分类"
                )
                
            # 检查是否是自己的子分类
            children_ids = [child.id for child in ProductCategoryService.get_children(db, category_id, recursive=True)]
            if category_data.parent_id in children_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="不能选择子分类作为父分类(避免循环引用)"
                )
                
            # 确认父分类存在
            parent = db.query(ProductCategory).filter(ProductCategory.id == category_data.parent_id).first()
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"父分类ID {category_data.parent_id} 不存在"
                )
        
        # 更新基本信息
        update_data = category_data.dict(exclude_unset=True, exclude={"translations"})
        for key, value in update_data.items():
            setattr(category, key, value)
            
        # 更新翻译信息
        if category_data.translations:
            for translation_data in category_data.translations:
                # 尝试查找现有翻译
                translation = db.query(ProductCategoryTranslation).filter(
                    ProductCategoryTranslation.category_id == category_id,
                    ProductCategoryTranslation.language_code == translation_data.language_code
                ).first()
                
                # 如果存在则更新，否则创建新翻译
                if translation:
                    for key, value in translation_data.dict(exclude_unset=True).items():
                        setattr(translation, key, value)
                else:
                    new_translation = ProductCategoryTranslation(
                        **translation_data.dict(),
                        category_id=category_id
                    )
                    db.add(new_translation)
        
        category.updated_at = datetime.utcnow()
        db.commit()
        # 重新查询以获取完整的对象（包括关联数据）
        updated_category = db.query(ProductCategory).options(
            joinedload(ProductCategory.translations)
        ).filter(ProductCategory.id == category_id).first()
        
        return ProductCategoryService._category_to_dict(updated_category)

    @staticmethod
    def delete_category(db: Session, category_id: UUID) -> Dict[str, Any]:
        """删除分类"""
        # 获取分类对象用于删除操作
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类ID {category_id} 不存在"
            )
        
        # 检查是否有子分类
        children = db.query(ProductCategory).filter(ProductCategory.parent_id == category_id).all()
        if children:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该分类下有子分类，无法删除。请先删除或移动子分类。"
            )
            
        # 检查是否有关联产品 - 使用多对多关系查询
        products_count = db.query(func.count(Product.id)).join(
            product_category, Product.id == product_category.c.product_id
        ).filter(
            product_category.c.category_id == category_id
        ).scalar()
        
        if products_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该分类下有关联产品，无法删除。请先删除或移动产品。"
            )
            
        # 删除分类的翻译
        db.query(ProductCategoryTranslation).filter(
            ProductCategoryTranslation.category_id == category_id
        ).delete()
        
        # 删除分类
        db.delete(category)
        db.commit()
        
        return {
            "success": True,
            "message": f"分类 '{category.name}' 已成功删除"
        }
        
    @staticmethod
    def get_category_translation(
        db: Session, 
        category_id: UUID, 
        language_code: str
    ) -> ProductCategoryTranslation:
        """获取指定语言的分类翻译"""
        translation = db.query(ProductCategoryTranslation).filter(
            ProductCategoryTranslation.category_id == category_id,
            ProductCategoryTranslation.language_code == language_code
        ).first()
        
        if not translation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类ID {category_id} 的 {language_code} 翻译不存在"
            )
            
        return translation
        
    @staticmethod
    def create_category_translation(
        db: Session, 
        category_id: UUID, 
        translation_data: ProductCategoryTranslationCreate
    ) -> ProductCategoryTranslation:
        """为分类创建新的语言翻译"""
        # 确认分类存在
        category = ProductCategoryService.get_category_by_id(db, category_id)
        
        # 检查该语言的翻译是否已存在
        existing = db.query(ProductCategoryTranslation).filter(
            ProductCategoryTranslation.category_id == category_id,
            ProductCategoryTranslation.language_code == translation_data.language_code
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"分类ID {category_id} 的 {translation_data.language_code} 翻译已存在"
            )
            
        # 创建翻译
        translation = ProductCategoryTranslation(
            **translation_data.dict(),
            category_id=category_id
        )
        db.add(translation)
        db.commit()
        db.refresh(translation)
        
        return translation
        
    @staticmethod
    def update_category_translation(
        db: Session, 
        category_id: UUID, 
        language_code: str,
        translation_data: ProductCategoryTranslationUpdate
    ) -> ProductCategoryTranslation:
        """更新分类的语言翻译"""
        # 获取翻译记录
        translation = ProductCategoryService.get_category_translation(db, category_id, language_code)
        
        # 更新翻译
        update_data = translation_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(translation, key, value)
            
        translation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(translation)
        
        return translation
        
    @staticmethod
    def delete_category_translation(
        db: Session, 
        category_id: UUID, 
        language_code: str
    ) -> Dict[str, Any]:
        """删除分类的语言翻译"""
        # 获取翻译记录
        translation = ProductCategoryService.get_category_translation(db, category_id, language_code)
        
        # 删除翻译
        db.delete(translation)
        db.commit()
        
        return {
            "success": True,
            "message": f"分类ID {category_id} 的 {language_code} 翻译已成功删除"
        }
        
    @staticmethod
    def import_categories(db: Session, root_category_guid: UUID, categories: List[ProductCategoryCreate]) -> Dict[str, Any]:
        """通过json格式的数据批量导入多级分类"""
        # 从categories第一层开始，这一层的父类是root_category_guid，如果root_category_guid为空，则这一层的父类是None
        # 然后从categories第二层开始，这一层的父类是categories第一层的guid（自动生成）
        # 因为是批量导入，这些类都是没有guid的，也没有parent_id
        # 要循环所有的子类，直到所有的子类都生成成功并存入数据库
        # [
        #     {
        #         "name": "分类名称",
        #         "level": "分类层级",
        #         "slug": "分类别名",
        #         "description": "分类描述",
        #         "image_url": "分类图片URL",
        #         "icon_url": "分类图标URL",
        #         "is_active": true,
        #         "is_featured": true,
        #         "sort_order": 0,
        #         "seo_title": "SEO标题",
        #         "seo_description": "SEO描述",
        #         "seo_keywords": "SEO关键词",
        #         "children": [
        #             {
        #                 "name": "子分类名称",
        #                 "level": "子分类层级",
        #                 "slug": "子分类别名",
        #                 "description": "子分类描述",
        #                 "image_url": "子分类图片URL",
        #                 "icon_url": "子分类图标URL",
        #                 "is_active": true,
        #                 "is_featured": true,
        #                 "sort_order": 0,
        #                 "seo_title": "子分类SEO标题",
        #                 "seo_description": "子分类SEO描述",
        #                 "seo_keywords": "子分类SEO关键词",
        #                 "children": [
        #                     {
        #                         "name": "孙子分类名称",
        #                         "level": "孙子分类层级",
        #                         "slug": "孙子分类别名",
        #                         "description": "孙子分类描述",
        #                         "image_url": "孙子分类图片URL",
        #                         "icon_url": "孙子分类图标URL",
        #                         "is_active": true,
        #                         "is_featured": true,
        #                         "sort_order": 0,
        #                         "seo_title": "孙子分类SEO标题",
        #                         "seo_description": "孙子分类SEO描述",
        #                         "seo_keywords": "孙子分类SEO关键词",
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # ]
        # 最多三层分类
        for category in categories:
            guid = uuid.uuid4()
            new_category = ProductCategory(
                id=guid,
                name=category.name,
                slug=category.slug,
                description=category.description,
                image_url=category.image_url,
                icon_url=category.icon_url,
                is_active=category.is_active,
                is_featured=category.is_featured,
                sort_order=category.sort_order,
                seo_title=category.seo_title,
                seo_description=category.seo_description,
                seo_keywords=category.seo_keywords,
                parent_id=root_category_guid if root_category_guid else None,
                level=category.level,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(new_category)
            
            # 递归处理子分类
            if getattr(category, "children", None):
                ProductCategoryService.import_categories(db, guid, category.children)
        db.commit()

        
        
        
        
        
