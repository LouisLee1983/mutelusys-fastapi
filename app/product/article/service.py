"""
产品文章管理服务层
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_, or_, desc, func

from app.product.article.models import (
    ProductArticle, 
    ProductArticleTranslation, 
    ProductArticleTemplate,
    ArticleStatus,
    ArticleType,
    product_article_association
)
from app.product.models import Product, ProductMaterial, ProductCategory, ProductTag
from app.product.article.schema import (
    ProductArticleCreateRequest,
    ProductArticleUpdateRequest,
    ProductArticleTranslationCreateRequest,
    ProductArticleTranslationUpdateRequest,
    ProductArticleAssignRequest
)


class ProductArticleService:
    """产品文章服务类"""

    def __init__(self, db: Session):
        self.db = db

    # ==================== 文章管理 ====================

    def create_article(self, request: ProductArticleCreateRequest, author_id: Optional[str] = None) -> ProductArticle:
        """创建产品文章"""
        article_data = request.dict(exclude={'auto_assign_materials', 'auto_assign_categories', 'auto_assign_tags'})
        
        article = ProductArticle(
            **article_data,
            author_id=author_id,
            auto_assign_materials=request.auto_assign_materials,
            auto_assign_categories=request.auto_assign_categories,
            auto_assign_tags=request.auto_assign_tags
        )
        
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        
        # 如果有自动分配规则，执行自动分配
        if any([request.auto_assign_materials, request.auto_assign_categories, request.auto_assign_tags]):
            self._auto_assign_article_to_products(article)
        
        return article

    def get_article_by_id(self, article_id: str, include_translations: bool = True) -> Optional[ProductArticle]:
        """根据ID获取文章"""
        query = self.db.query(ProductArticle).filter(ProductArticle.id == article_id)
        
        if include_translations:
            query = query.options(selectinload(ProductArticle.translations))
            
        return query.first()

    def get_article_by_slug(self, slug: str, language_code: Optional[str] = None) -> Optional[ProductArticle]:
        """根据slug获取文章"""
        article = self.db.query(ProductArticle).filter(ProductArticle.slug == slug).first()
        
        if article and language_code:
            # 加载指定语言的翻译
            translation = self.db.query(ProductArticleTranslation).filter(
                and_(
                    ProductArticleTranslation.article_id == article.id,
                    ProductArticleTranslation.language_code == language_code
                )
            ).first()
            
            if translation:
                # 将翻译内容赋值给文章对象
                article.title = translation.title
                article.summary = translation.summary
                article.content = translation.content
                article.category = translation.category
                article.tags = translation.tags
                
        return article

    def get_articles(
        self, 
        page: int = 1, 
        limit: int = 20,
        article_type: Optional[ArticleType] = None,
        status: Optional[ArticleStatus] = None,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        author_id: Optional[str] = None
    ) -> Tuple[List[ProductArticle], int]:
        """获取文章列表"""
        query = self.db.query(ProductArticle)
        
        # 添加筛选条件
        if article_type:
            query = query.filter(ProductArticle.article_type == article_type)
        
        if status:
            query = query.filter(ProductArticle.status == status)
            
        if category:
            query = query.filter(ProductArticle.category == category)
            
        if author_id:
            query = query.filter(ProductArticle.author_id == author_id)
            
        if keyword:
            query = query.filter(
                or_(
                    ProductArticle.title.ilike(f"%{keyword}%"),
                    ProductArticle.summary.ilike(f"%{keyword}%"),
                    ProductArticle.content.ilike(f"%{keyword}%"),
                    ProductArticle.tags.ilike(f"%{keyword}%")
                )
            )
        
        # 获取总数
        total = query.count()
        
        # 分页和排序
        articles = query.order_by(desc(ProductArticle.created_at)).offset((page - 1) * limit).limit(limit).all()
        
        return articles, total

    def update_article(self, article_id: str, request: ProductArticleUpdateRequest) -> Optional[ProductArticle]:
        """更新文章"""
        article = self.db.query(ProductArticle).filter(ProductArticle.id == article_id).first()
        if not article:
            return None
            
        # 更新字段
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(article, field, value)
        
        article.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(article)
        
        return article

    def delete_article(self, article_id: str) -> bool:
        """删除文章"""
        article = self.db.query(ProductArticle).filter(ProductArticle.id == article_id).first()
        if not article:
            return False
            
        # 删除关联关系
        self.db.execute(
            product_article_association.delete().where(
                product_article_association.c.article_id == article_id
            )
        )
        
        # 删除文章
        self.db.delete(article)
        self.db.commit()
        
        return True

    def publish_article(self, article_id: str) -> Optional[ProductArticle]:
        """发布文章"""
        article = self.db.query(ProductArticle).filter(ProductArticle.id == article_id).first()
        if not article:
            return None
            
        article.status = ArticleStatus.PUBLISHED
        article.published_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(article)
        
        return article

    # ==================== 翻译管理 ====================

    def create_translation(
        self, 
        article_id: str, 
        request: ProductArticleTranslationCreateRequest,
        translator_id: Optional[str] = None
    ) -> Optional[ProductArticleTranslation]:
        """创建文章翻译"""
        # 检查文章是否存在
        article = self.db.query(ProductArticle).filter(ProductArticle.id == article_id).first()
        if not article:
            return None
            
        # 检查是否已有该语言的翻译
        existing = self.db.query(ProductArticleTranslation).filter(
            and_(
                ProductArticleTranslation.article_id == article_id,
                ProductArticleTranslation.language_code == request.language_code
            )
        ).first()
        
        if existing:
            return None  # 已存在该语言翻译
            
        translation = ProductArticleTranslation(
            article_id=article_id,
            translator_id=translator_id,
            **request.dict()
        )
        
        self.db.add(translation)
        self.db.commit()
        self.db.refresh(translation)
        
        return translation

    def update_translation(
        self, 
        translation_id: str, 
        request: ProductArticleTranslationUpdateRequest
    ) -> Optional[ProductArticleTranslation]:
        """更新翻译"""
        translation = self.db.query(ProductArticleTranslation).filter(
            ProductArticleTranslation.id == translation_id
        ).first()
        
        if not translation:
            return None
            
        # 更新字段
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(translation, field, value)
        
        translation.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(translation)
        
        return translation

    def get_article_translations(self, article_id: str) -> List[ProductArticleTranslation]:
        """获取文章的所有翻译"""
        return self.db.query(ProductArticleTranslation).filter(
            ProductArticleTranslation.article_id == article_id
        ).all()

    # ==================== 产品关联管理 ====================

    def assign_article_to_products(self, article_id: str, request: ProductArticleAssignRequest) -> bool:
        """将文章分配给产品"""
        article = self.db.query(ProductArticle).filter(ProductArticle.id == article_id).first()
        if not article:
            return False
            
        for product_id in request.product_ids:
            # 检查关联是否已存在
            existing = self.db.execute(
                product_article_association.select().where(
                    and_(
                        product_article_association.c.product_id == product_id,
                        product_article_association.c.article_id == article_id
                    )
                )
            ).first()
            
            if not existing:
                # 插入新关联
                self.db.execute(
                    product_article_association.insert().values(
                        product_id=product_id,
                        article_id=article_id,
                        is_default=request.is_default,
                        sort_order=request.sort_order,
                        created_at=datetime.utcnow()
                    )
                )
        
        self.db.commit()
        return True

    def remove_article_from_product(self, article_id: str, product_id: str) -> bool:
        """将文章从产品移除"""
        result = self.db.execute(
            product_article_association.delete().where(
                and_(
                    product_article_association.c.product_id == product_id,
                    product_article_association.c.article_id == article_id
                )
            )
        )
        
        self.db.commit()
        return result.rowcount > 0

    def get_product_articles(self, product_id: str, language_code: Optional[str] = None) -> List[ProductArticle]:
        """获取产品关联的文章"""
        query = self.db.query(ProductArticle).join(
            product_article_association,
            ProductArticle.id == product_article_association.c.article_id
        ).filter(
            product_article_association.c.product_id == product_id
        ).filter(
            ProductArticle.status == ArticleStatus.PUBLISHED
        ).order_by(
            product_article_association.c.sort_order
        )
        
        articles = query.all()
        
        # 如果指定了语言，加载翻译
        if language_code and articles:
            for article in articles:
                translation = self.db.query(ProductArticleTranslation).filter(
                    and_(
                        ProductArticleTranslation.article_id == article.id,
                        ProductArticleTranslation.language_code == language_code
                    )
                ).first()
                
                if translation:
                    article.title = translation.title
                    article.summary = translation.summary
                    article.content = translation.content
                    article.category = translation.category
                    article.tags = translation.tags
        
        return articles

    def get_article_products(self, article_id: str) -> List[Product]:
        """获取关联某文章的产品"""
        return self.db.query(Product).join(
            product_article_association,
            Product.id == product_article_association.c.product_id
        ).filter(
            product_article_association.c.article_id == article_id
        ).all()

    # ==================== 自动分配功能 ====================

    def _auto_assign_article_to_products(self, article: ProductArticle):
        """根据规则自动分配文章到产品"""
        products_to_assign = set()
        
        # 根据材质分配
        if article.auto_assign_materials:
            material_names = [name.strip() for name in article.auto_assign_materials.split(',')]
            products = self.db.query(Product).join(Product.materials).filter(
                Product.materials.any(func.lower(ProductMaterial.name).in_([name.lower() for name in material_names]))
            ).all()
            products_to_assign.update([p.id for p in products])
        
        # 根据分类分配
        if article.auto_assign_categories:
            category_names = [name.strip() for name in article.auto_assign_categories.split(',')]
            products = self.db.query(Product).join(Product.categories).filter(
                Product.categories.any(func.lower(ProductCategory.name).in_([name.lower() for name in category_names]))
            ).all()
            products_to_assign.update([p.id for p in products])
        
        # 根据标签分配
        if article.auto_assign_tags:
            tag_names = [name.strip() for name in article.auto_assign_tags.split(',')]
            products = self.db.query(Product).join(Product.tags).filter(
                Product.tags.any(func.lower(ProductTag.name).in_([name.lower() for name in tag_names]))
            ).all()
            products_to_assign.update([p.id for p in products])
        
        # 执行分配
        for product_id in products_to_assign:
            # 检查是否已经关联
            existing = self.db.execute(
                product_article_association.select().where(
                    and_(
                        product_article_association.c.product_id == product_id,
                        product_article_association.c.article_id == article.id
                    )
                )
            ).first()
            
            if not existing:
                self.db.execute(
                    product_article_association.insert().values(
                        product_id=product_id,
                        article_id=article.id,
                        is_default=False,
                        sort_order=0,
                        created_at=datetime.utcnow()
                    )
                )
        
        self.db.commit()

    def run_auto_assignment_for_new_product(self, product: Product):
        """为新产品自动分配符合条件的文章"""
        # 获取所有有自动分配规则的文章
        articles = self.db.query(ProductArticle).filter(
            or_(
                ProductArticle.auto_assign_materials.isnot(None),
                ProductArticle.auto_assign_categories.isnot(None),
                ProductArticle.auto_assign_tags.isnot(None)
            )
        ).filter(
            ProductArticle.status == ArticleStatus.PUBLISHED
        ).all()
        
        for article in articles:
            should_assign = False
            
            # 检查材质匹配
            if article.auto_assign_materials and product.materials:
                material_names = [name.strip().lower() for name in article.auto_assign_materials.split(',')]
                product_materials = [m.name.lower() for m in product.materials]
                if any(material in product_materials for material in material_names):
                    should_assign = True
            
            # 检查分类匹配
            if article.auto_assign_categories and product.categories:
                category_names = [name.strip().lower() for name in article.auto_assign_categories.split(',')]
                product_categories = [c.name.lower() for c in product.categories]
                if any(category in product_categories for category in category_names):
                    should_assign = True
            
            # 检查标签匹配
            if article.auto_assign_tags and product.tags:
                tag_names = [name.strip().lower() for name in article.auto_assign_tags.split(',')]
                product_tags = [t.name.lower() for t in product.tags]
                if any(tag in product_tags for tag in tag_names):
                    should_assign = True
            
            if should_assign:
                # 检查是否已经关联
                existing = self.db.execute(
                    product_article_association.select().where(
                        and_(
                            product_article_association.c.product_id == product.id,
                            product_article_association.c.article_id == article.id
                        )
                    )
                ).first()
                
                if not existing:
                    self.db.execute(
                        product_article_association.insert().values(
                            product_id=product.id,
                            article_id=article.id,
                            is_default=False,
                            sort_order=0,
                            created_at=datetime.utcnow()
                        )
                    )
        
        self.db.commit()

    # ==================== 统计功能 ====================

    def get_article_stats(self) -> Dict[str, Any]:
        """获取文章统计信息"""
        total_articles = self.db.query(ProductArticle).count()
        published_articles = self.db.query(ProductArticle).filter(
            ProductArticle.status == ArticleStatus.PUBLISHED
        ).count()
        draft_articles = self.db.query(ProductArticle).filter(
            ProductArticle.status == ArticleStatus.DRAFT
        ).count()
        
        # 按类型统计
        articles_by_type = {}
        for article_type in ArticleType:
            count = self.db.query(ProductArticle).filter(
                ProductArticle.article_type == article_type
            ).count()
            articles_by_type[article_type.value] = count
        
        # 使用最多的文章（按关联产品数量）
        most_used_articles = self.db.query(
            ProductArticle,
            func.count(product_article_association.c.product_id).label('product_count')
        ).outerjoin(
            product_article_association,
            ProductArticle.id == product_article_association.c.article_id
        ).group_by(ProductArticle.id).order_by(
            desc('product_count')
        ).limit(5).all()
        
        # 最近创建的文章
        recent_articles = self.db.query(ProductArticle).order_by(
            desc(ProductArticle.created_at)
        ).limit(5).all()
        
        return {
            "total_articles": total_articles,
            "published_articles": published_articles,
            "draft_articles": draft_articles,
            "articles_by_type": articles_by_type,
            "most_used_articles": [
                {
                    "id": str(article.id),
                    "title": article.title,
                    "product_count": product_count
                }
                for article, product_count in most_used_articles
            ],
            "recent_articles": recent_articles
        }