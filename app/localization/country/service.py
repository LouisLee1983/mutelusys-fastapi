import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from app.localization.country.models import (
    Country, CountryTranslation, Region, RegionTranslation, CountryRegion
)
from app.localization.country.schema import (
    CountryCreate, CountryUpdate, RegionCreate, RegionUpdate
)


class CountryService:
    """国家服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_country(self, country_data: CountryCreate) -> Country:
        """创建国家"""
        country = Country(
            id=str(uuid.uuid4()),
            code=country_data.code.upper(),
            code3=country_data.code3.upper(),
            name=country_data.name,
            native_name=country_data.native_name,
            currency=country_data.currency,
            phone_code=country_data.phone_code,
            status=country_data.status
        )
        
        self.db.add(country)
        
        # 添加翻译
        for trans_data in country_data.translations:
            translation = CountryTranslation(
                id=str(uuid.uuid4()),
                country_id=country.id,
                language=trans_data.language,
                name=trans_data.name
            )
            self.db.add(translation)
        
        self.db.commit()
        self.db.refresh(country)
        return country
    
    def get_countries(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Country], int]:
        """获取国家列表"""
        query = self.db.query(Country).options(
            joinedload(Country.translations)
        )
        
        if status:
            query = query.filter(Country.status == status)
        
        if search:
            query = query.filter(
                or_(
                    Country.name.ilike(f"%{search}%"),
                    Country.code.ilike(f"%{search}%"),
                    Country.native_name.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        countries = query.order_by(Country.name).offset(skip).limit(limit).all()
        
        return countries, total
    
    def get_country_by_id(self, country_id: str) -> Optional[Country]:
        """根据ID获取国家"""
        return (
            self.db.query(Country)
            .options(joinedload(Country.translations))
            .filter(Country.id == country_id)
            .first()
        )
    
    def get_country_by_code(self, country_code: str) -> Optional[Country]:
        """根据代码获取国家"""
        return (
            self.db.query(Country)
            .options(joinedload(Country.translations))
            .filter(Country.code == country_code.upper())
            .first()
        )
    
    def update_country(self, country_id: str, country_data: CountryUpdate) -> Optional[Country]:
        """更新国家"""
        country = self.get_country_by_id(country_id)
        if not country:
            return None
        
        # 更新基础信息
        update_data = country_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key in ['code', 'code3'] and value:
                value = value.upper()
            setattr(country, key, value)
        
        country.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(country)
        return country
    
    def delete_country(self, country_id: str) -> bool:
        """删除国家"""
        country = self.get_country_by_id(country_id)
        if not country:
            return False
        
        self.db.delete(country)
        self.db.commit()
        return True
    
    def get_countries_simple(self, status: str = "active") -> List[Dict[str, Any]]:
        """获取简化的国家列表，用于下拉选择"""
        countries = (
            self.db.query(Country)
            .filter(Country.status == status)
            .order_by(Country.name)
            .all()
        )
        
        return [
            {
                "id": str(country.id),
                "code": country.code,
                "name": country.name,
                "currency": country.currency
            }
            for country in countries
        ]


class RegionService:
    """地区服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_region(self, region_data: RegionCreate) -> Region:
        """创建地区"""
        region = Region(
            id=str(uuid.uuid4()),
            name=region_data.name,
            code=region_data.code.upper(),
            description=region_data.description,
            status=region_data.status
        )
        
        self.db.add(region)
        
        # 添加翻译
        for trans_data in region_data.translations:
            translation = RegionTranslation(
                id=str(uuid.uuid4()),
                region_id=region.id,
                language=trans_data.language,
                name=trans_data.name,
                description=trans_data.description
            )
            self.db.add(translation)
        
        # 关联国家
        for country_id in region_data.country_ids:
            country_region = CountryRegion(
                id=str(uuid.uuid4()),
                country_id=country_id,
                region_id=region.id
            )
            self.db.add(country_region)
        
        self.db.commit()
        self.db.refresh(region)
        return region
    
    def get_regions(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Region], int]:
        """获取地区列表"""
        query = self.db.query(Region)
        
        if status:
            query = query.filter(Region.status == status)
        
        if search:
            query = query.filter(
                or_(
                    Region.name.ilike(f"%{search}%"),
                    Region.code.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        regions = query.order_by(Region.name).offset(skip).limit(limit).all()
        
        return regions, total
    
    def get_region_by_id(self, region_id: str) -> Optional[Region]:
        """根据ID获取地区"""
        return (
            self.db.query(Region)
            .options(
                joinedload(Region.translations),
                joinedload(Region.countries).joinedload(CountryRegion.country)
            )
            .filter(Region.id == region_id)
            .first()
        )
    
    def get_region_by_code(self, region_code: str) -> Optional[Region]:
        """根据代码获取地区"""
        return (
            self.db.query(Region)
            .options(
                joinedload(Region.translations),
                joinedload(Region.countries).joinedload(CountryRegion.country)
            )
            .filter(Region.code == region_code.upper())
            .first()
        )
    
    def update_region(self, region_id: str, region_data: RegionUpdate) -> Optional[Region]:
        """更新地区"""
        region = self.get_region_by_id(region_id)
        if not region:
            return None
        
        # 更新基础信息
        update_data = region_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key == 'code' and value:
                value = value.upper()
            setattr(region, key, value)
        
        region.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(region)
        return region
    
    def delete_region(self, region_id: str) -> bool:
        """删除地区"""
        region = self.get_region_by_id(region_id)
        if not region:
            return False
        
        self.db.delete(region)
        self.db.commit()
        return True
    
    def add_country_to_region(self, region_id: str, country_id: str) -> bool:
        """将国家添加到地区"""
        # 检查是否已存在关联
        existing = (
            self.db.query(CountryRegion)
            .filter(
                and_(
                    CountryRegion.region_id == region_id,
                    CountryRegion.country_id == country_id
                )
            )
            .first()
        )
        
        if existing:
            return True
        
        # 创建新关联
        country_region = CountryRegion(
            id=str(uuid.uuid4()),
            country_id=country_id,
            region_id=region_id
        )
        
        self.db.add(country_region)
        self.db.commit()
        return True
    
    def remove_country_from_region(self, region_id: str, country_id: str) -> bool:
        """从地区移除国家"""
        country_region = (
            self.db.query(CountryRegion)
            .filter(
                and_(
                    CountryRegion.region_id == region_id,
                    CountryRegion.country_id == country_id
                )
            )
            .first()
        )
        
        if not country_region:
            return False
        
        self.db.delete(country_region)
        self.db.commit()
        return True
    
    def get_countries_by_region(self, region_id: str) -> List[Country]:
        """获取地区下的所有国家"""
        return (
            self.db.query(Country)
            .join(CountryRegion)
            .filter(CountryRegion.region_id == region_id)
            .order_by(Country.name)
            .all()
        )
    
    def get_regions_by_country(self, country_id: str) -> List[Region]:
        """获取国家所属的所有地区"""
        return (
            self.db.query(Region)
            .join(CountryRegion)
            .filter(CountryRegion.country_id == country_id)
            .order_by(Region.name)
            .all()
        )


class CountryTranslationService:
    """国家翻译服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_or_update_translation(
        self, 
        country_id: str, 
        language: str, 
        name: str
    ) -> CountryTranslation:
        """创建或更新国家翻译"""
        translation = (
            self.db.query(CountryTranslation)
            .filter(
                and_(
                    CountryTranslation.country_id == country_id,
                    CountryTranslation.language == language
                )
            )
            .first()
        )
        
        if translation:
            translation.name = name
            translation.updated_at = datetime.utcnow()
        else:
            translation = CountryTranslation(
                id=str(uuid.uuid4()),
                country_id=country_id,
                language=language,
                name=name
            )
            self.db.add(translation)
        
        self.db.commit()
        self.db.refresh(translation)
        return translation
    
    def delete_translation(self, country_id: str, language: str) -> bool:
        """删除国家翻译"""
        translation = (
            self.db.query(CountryTranslation)
            .filter(
                and_(
                    CountryTranslation.country_id == country_id,
                    CountryTranslation.language == language
                )
            )
            .first()
        )
        
        if not translation:
            return False
        
        self.db.delete(translation)
        self.db.commit()
        return True
    
    def get_translations_by_country(self, country_id: str) -> List[CountryTranslation]:
        """获取国家的所有翻译"""
        return (
            self.db.query(CountryTranslation)
            .filter(CountryTranslation.country_id == country_id)
            .all()
        )


class RegionTranslationService:
    """地区翻译服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_or_update_translation(
        self, 
        region_id: str, 
        language: str, 
        name: str,
        description: Optional[str] = None
    ) -> RegionTranslation:
        """创建或更新地区翻译"""
        translation = (
            self.db.query(RegionTranslation)
            .filter(
                and_(
                    RegionTranslation.region_id == region_id,
                    RegionTranslation.language == language
                )
            )
            .first()
        )
        
        if translation:
            translation.name = name
            if description is not None:
                translation.description = description
            translation.updated_at = datetime.utcnow()
        else:
            translation = RegionTranslation(
                id=str(uuid.uuid4()),
                region_id=region_id,
                language=language,
                name=name,
                description=description
            )
            self.db.add(translation)
        
        self.db.commit()
        self.db.refresh(translation)
        return translation
    
    def delete_translation(self, region_id: str, language: str) -> bool:
        """删除地区翻译"""
        translation = (
            self.db.query(RegionTranslation)
            .filter(
                and_(
                    RegionTranslation.region_id == region_id,
                    RegionTranslation.language == language
                )
            )
            .first()
        )
        
        if not translation:
            return False
        
        self.db.delete(translation)
        self.db.commit()
        return True