from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from uuid import UUID

from app.content.blog.models import Blog, BlogTranslation, BlogTag, BlogTagTranslation, blog_tag
from app.content.blog_category.models import BlogCategory
from app.content.blog.schema import (
    BlogCreate, BlogUpdate, BlogListQuery, BlogBatchUpdate,
    BlogTranslationCreate, BlogTranslationUpdate,
    BlogTagCreate, BlogTagUpdate,
    BlogCategoryCreate, BlogCategoryUpdate,
    BlogStatistics
)
from app.content.models import ContentStatus


class BlogService:
    """Blog service class"""

    @staticmethod
    def create_blog(db: Session, blog_data: BlogCreate, created_by: Optional[UUID] = None) -> Blog:
        """Create new blog"""
        # Create blog
        blog = Blog(
            slug=blog_data.slug,
            title=blog_data.title,
            content=blog_data.content,
            excerpt=blog_data.excerpt,
            category_id=UUID(blog_data.category_id) if blog_data.category_id else None,
            featured_image=blog_data.featured_image,
            is_featured=blog_data.is_featured,
            is_commentable=blog_data.is_commentable,
            meta_title=blog_data.meta_title,
            meta_description=blog_data.meta_description,
            meta_keywords=blog_data.meta_keywords,
            published_at=blog_data.published_at,
            status=ContentStatus.DRAFT,
            author_id=created_by,
            created_by=created_by,
            updated_by=created_by
        )
        
        db.add(blog)
        db.flush()  # Get ID first

        # Add tags
        if blog_data.tag_ids:
            for tag_id in blog_data.tag_ids:
                tag = db.query(BlogTag).filter(BlogTag.id == UUID(tag_id)).first()
                if tag:
                    blog.tags.append(tag)

        # Add translations
        for translation_data in blog_data.translations:
            translation = BlogTranslation(
                blog_id=blog.id,
                language_code=translation_data.language_code,
                title=translation_data.title,
                content=translation_data.content,
                excerpt=translation_data.excerpt,
                meta_title=translation_data.meta_title,
                meta_description=translation_data.meta_description,
                meta_keywords=translation_data.meta_keywords
            )
            db.add(translation)

        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def get_blog_by_id(db: Session, blog_id: UUID) -> Optional[Blog]:
        """Get blog by ID"""
        return db.query(Blog).filter(Blog.id == blog_id).first()

    @staticmethod
    def get_blog_by_slug(db: Session, slug: str) -> Optional[Blog]:
        """Get blog by slug"""
        return db.query(Blog).filter(Blog.slug == slug).first()

    @staticmethod
    def get_blogs_list(db: Session, query: BlogListQuery) -> tuple[List[Blog], int]:
        """Get blogs list"""
        base_query = db.query(Blog)

        # Apply filters
        if query.status:
            base_query = base_query.filter(Blog.status == query.status)
        
        if query.category_id:
            base_query = base_query.filter(Blog.category_id == UUID(query.category_id))
        
        if query.tag_id:
            base_query = base_query.join(blog_tag).filter(blog_tag.c.tag_id == UUID(query.tag_id))
        
        if query.is_featured is not None:
            base_query = base_query.filter(Blog.is_featured == query.is_featured)
            
        if query.author_id:
            base_query = base_query.filter(Blog.author_id == UUID(query.author_id))
        
        if query.search:
            search_term = f"%{query.search}%"
            base_query = base_query.filter(
                or_(
                    Blog.title.ilike(search_term),
                    Blog.content.ilike(search_term),
                    Blog.excerpt.ilike(search_term),
                    Blog.meta_keywords.ilike(search_term)
                )
            )

        # Get total count
        total = base_query.count()

        # Apply pagination
        blogs = (
            base_query
            .order_by(desc(Blog.is_featured), desc(Blog.published_at), desc(Blog.created_at))
            .offset((query.page - 1) * query.page_size)
            .limit(query.page_size)
            .all()
        )

        return blogs, total

    @staticmethod
    def update_blog(db: Session, blog_id: UUID, blog_data: BlogUpdate, updated_by: Optional[UUID] = None) -> Optional[Blog]:
        """Update blog"""
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return None

        # Update blog data
        update_data = blog_data.dict(exclude_unset=True)
        
        # Handle tags
        if 'tag_ids' in update_data:
            tag_ids = update_data.pop('tag_ids')
            if tag_ids is not None:
                # Clear existing tags
                blog.tags.clear()
                # Add new tags
                for tag_id in tag_ids:
                    tag = db.query(BlogTag).filter(BlogTag.id == UUID(tag_id)).first()
                    if tag:
                        blog.tags.append(tag)
        
        # Update other fields
        for field, value in update_data.items():
            if field == 'category_id' and value:
                value = UUID(value)
            setattr(blog, field, value)
        
        blog.updated_by = updated_by
        blog.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def delete_blog(db: Session, blog_id: UUID) -> bool:
        """Delete blog"""
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return False

        db.delete(blog)
        db.commit()
        return True

    @staticmethod
    def publish_blog(db: Session, blog_id: UUID, updated_by: Optional[UUID] = None) -> Optional[Blog]:
        """Publish blog"""
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return None

        blog.status = ContentStatus.PUBLISHED
        if not blog.published_at:
            blog.published_at = datetime.utcnow()
        blog.updated_by = updated_by
        blog.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def increment_view_count(db: Session, blog_id: UUID) -> Optional[Blog]:
        """Increment view count"""
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return None

        blog.view_count += 1
        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def get_published_blogs(db: Session, limit: int = 10, language_code: Optional[str] = None) -> List[Blog]:
        """Get published blogs"""
        query = db.query(Blog).filter(
            Blog.status == ContentStatus.PUBLISHED
        ).order_by(desc(Blog.published_at))

        if limit:
            query = query.limit(limit)

        return query.all()

    @staticmethod
    def get_featured_blogs(db: Session, limit: int = 5, language_code: Optional[str] = None) -> List[Blog]:
        """Get featured blogs"""
        query = db.query(Blog).filter(
            and_(
                Blog.status == ContentStatus.PUBLISHED,
                Blog.is_featured == True
            )
        ).order_by(desc(Blog.published_at))

        if limit:
            query = query.limit(limit)

        return query.all()

    @staticmethod
    def batch_update_status(db: Session, batch_data: BlogBatchUpdate, updated_by: Optional[UUID] = None) -> List[Blog]:
        """Batch update blog status"""
        blogs = db.query(Blog).filter(Blog.id.in_([UUID(id) for id in batch_data.blog_ids])).all()
        
        for blog in blogs:
            if batch_data.status:
                blog.status = batch_data.status
                if batch_data.status == ContentStatus.PUBLISHED and not blog.published_at:
                    blog.published_at = datetime.utcnow()
            
            if batch_data.is_featured is not None:
                blog.is_featured = batch_data.is_featured
                
            if batch_data.category_id:
                blog.category_id = UUID(batch_data.category_id)
            
            blog.updated_by = updated_by
            blog.updated_at = datetime.utcnow()

        db.commit()
        return blogs

    @staticmethod
    def get_statistics(db: Session) -> BlogStatistics:
        """Get blog statistics"""
        total_blogs = db.query(Blog).count()
        published_blogs = db.query(Blog).filter(Blog.status == ContentStatus.PUBLISHED).count()
        draft_blogs = db.query(Blog).filter(Blog.status == ContentStatus.DRAFT).count()
        featured_blogs = db.query(Blog).filter(Blog.is_featured == True).count()
        total_views = db.query(func.sum(Blog.view_count)).scalar() or 0
        total_categories = db.query(BlogCategory).count()
        total_tags = db.query(BlogTag).count()

        return BlogStatistics(
            total_blogs=total_blogs,
            published_blogs=published_blogs,
            draft_blogs=draft_blogs,
            featured_blogs=featured_blogs,
            total_views=total_views,
            total_categories=total_categories,
            total_tags=total_tags
        )

    # Translation methods
    @staticmethod
    def create_translation(db: Session, blog_id: UUID, translation_data: BlogTranslationCreate) -> Optional[BlogTranslation]:
        """Create blog translation"""
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return None

        # Check if translation already exists
        existing = db.query(BlogTranslation).filter(
            and_(
                BlogTranslation.blog_id == blog_id,
                BlogTranslation.language_code == translation_data.language_code
            )
        ).first()

        if existing:
            # Update existing translation
            for field, value in translation_data.dict(exclude_unset=True).items():
                setattr(existing, field, value)
            existing.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new translation
            translation = BlogTranslation(
                blog_id=blog_id,
                **translation_data.dict()
            )
            db.add(translation)
            db.commit()
            db.refresh(translation)
            return translation

    @staticmethod
    def update_translation(db: Session, translation_id: UUID, translation_data: BlogTranslationUpdate) -> Optional[BlogTranslation]:
        """Update blog translation"""
        translation = db.query(BlogTranslation).filter(BlogTranslation.id == translation_id).first()
        if not translation:
            return None

        update_data = translation_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(translation, field, value)
        
        translation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(translation)
        return translation


class BlogTagService:
    """Blog tag service"""

    @staticmethod
    def create_tag(db: Session, tag_data: BlogTagCreate) -> BlogTag:
        """Create blog tag"""
        tag = BlogTag(
            name=tag_data.name,
            slug=tag_data.slug,
            description=tag_data.description
        )
        
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def get_tag_by_id(db: Session, tag_id: UUID) -> Optional[BlogTag]:
        """Get tag by ID"""
        return db.query(BlogTag).filter(BlogTag.id == tag_id).first()

    @staticmethod
    def get_all_tags(db: Session) -> List[BlogTag]:
        """Get all tags"""
        return db.query(BlogTag).order_by(BlogTag.name).all()

    @staticmethod
    def update_tag(db: Session, tag_id: UUID, tag_data: BlogTagUpdate) -> Optional[BlogTag]:
        """Update tag"""
        tag = db.query(BlogTag).filter(BlogTag.id == tag_id).first()
        if not tag:
            return None

        update_data = tag_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tag, field, value)
        
        tag.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def delete_tag(db: Session, tag_id: UUID) -> bool:
        """Delete tag"""
        tag = db.query(BlogTag).filter(BlogTag.id == tag_id).first()
        if not tag:
            return False

        db.delete(tag)
        db.commit()
        return True


class BlogCategoryService:
    """Blog category service"""

    @staticmethod
    def create_category(db: Session, category_data: BlogCategoryCreate) -> BlogCategory:
        """Create blog category"""
        category = BlogCategory(
            name=category_data.name,
            slug=category_data.slug,
            description=category_data.description,
            parent_id=UUID(category_data.parent_id) if category_data.parent_id else None
        )
        
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_category_by_id(db: Session, category_id: UUID) -> Optional[BlogCategory]:
        """Get category by ID"""
        return db.query(BlogCategory).filter(BlogCategory.id == category_id).first()

    @staticmethod
    def get_all_categories(db: Session) -> List[BlogCategory]:
        """Get all categories"""
        return db.query(BlogCategory).order_by(BlogCategory.name).all()

    @staticmethod
    def update_category(db: Session, category_id: UUID, category_data: BlogCategoryUpdate) -> Optional[BlogCategory]:
        """Update category"""
        category = db.query(BlogCategory).filter(BlogCategory.id == category_id).first()
        if not category:
            return None

        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'parent_id' and value:
                value = UUID(value)
            setattr(category, field, value)
        
        category.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: UUID) -> bool:
        """Delete category"""
        category = db.query(BlogCategory).filter(BlogCategory.id == category_id).first()
        if not category:
            return False

        db.delete(category)
        db.commit()
        return True