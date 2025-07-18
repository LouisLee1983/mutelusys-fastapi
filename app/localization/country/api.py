from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.localization.country.service import (
    CountryService, RegionService, CountryTranslationService, RegionTranslationService
)
from app.localization.country.schema import (
    Country, CountryCreate, CountryUpdate, CountryListResponse, CountrySimple,
    Region, RegionCreate, RegionUpdate, RegionListResponse, RegionWithCountries,
    CountryTranslation, CountryTranslationCreate, CountryTranslationUpdate,
    RegionTranslation, RegionTranslationCreate, RegionTranslationUpdate,
    CountryRegionResponse
)

router = APIRouter()


# ========================================
# 国家管理接口
# ========================================

@router.post("/", response_model=Country, summary="创建国家")
def create_country(
    country_data: CountryCreate,
    db: Session = Depends(get_db)
):
    """创建新国家"""
    service = CountryService(db)
    
    # 检查代码是否已存在
    existing = service.get_country_by_code(country_data.code)
    if existing:
        raise HTTPException(status_code=400, detail=f"Country code {country_data.code} already exists")
    
    return service.create_country(country_data)


@router.get("/", response_model=CountryListResponse, summary="获取国家列表")
def get_countries(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    status: Optional[str] = Query(None, description="状态筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取国家列表"""
    service = CountryService(db)
    countries, total = service.get_countries(skip=skip, limit=limit, status=status, search=search)
    
    return CountryListResponse(
        countries=countries,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/simple", response_model=List[CountrySimple], summary="获取简化国家列表")
def get_countries_simple(
    status: str = Query("active", description="状态"),
    db: Session = Depends(get_db)
):
    """获取简化的国家列表，用于下拉选择"""
    service = CountryService(db)
    return service.get_countries_simple(status=status)


@router.get("/{country_id}", response_model=Country, summary="获取国家详情")
def get_country(
    country_id: str,
    db: Session = Depends(get_db)
):
    """根据ID获取国家详情"""
    service = CountryService(db)
    country = service.get_country_by_id(country_id)
    
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return country


@router.get("/code/{country_code}", response_model=Country, summary="根据代码获取国家")
def get_country_by_code(
    country_code: str,
    db: Session = Depends(get_db)
):
    """根据国家代码获取国家详情"""
    service = CountryService(db)
    country = service.get_country_by_code(country_code)
    
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return country


@router.put("/{country_id}", response_model=Country, summary="更新国家")
def update_country(
    country_id: str,
    country_data: CountryUpdate,
    db: Session = Depends(get_db)
):
    """更新国家信息"""
    service = CountryService(db)
    country = service.update_country(country_id, country_data)
    
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return country


@router.delete("/{country_id}", summary="删除国家")
def delete_country(
    country_id: str,
    db: Session = Depends(get_db)
):
    """删除国家"""
    service = CountryService(db)
    success = service.delete_country(country_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return {"message": "Country deleted successfully"}


@router.get("/{country_id}/regions", response_model=CountryRegionResponse, summary="获取国家及其地区信息")
def get_country_with_regions(
    country_id: str,
    db: Session = Depends(get_db)
):
    """获取国家及其所属地区信息"""
    country_service = CountryService(db)
    region_service = RegionService(db)
    
    country = country_service.get_country_by_id(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    regions = region_service.get_regions_by_country(country_id)
    
    return CountryRegionResponse(
        country=country,
        regions=regions
    )


# ========================================
# 地区管理接口
# ========================================

regions_router = APIRouter(prefix="/regions")


@regions_router.post("/", response_model=Region, summary="创建地区")
def create_region(
    region_data: RegionCreate,
    db: Session = Depends(get_db)
):
    """创建新地区"""
    service = RegionService(db)
    
    # 检查代码是否已存在
    existing = service.get_region_by_code(region_data.code)
    if existing:
        raise HTTPException(status_code=400, detail=f"Region code {region_data.code} already exists")
    
    return service.create_region(region_data)


@regions_router.get("/", response_model=List[Region], summary="获取地区列表")
def get_regions(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    status: Optional[str] = Query(None, description="状态筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取地区列表"""
    service = RegionService(db)
    regions, total = service.get_regions(skip=skip, limit=limit, status=status, search=search)
    return regions


@regions_router.get("/{region_id}", response_model=RegionWithCountries, summary="获取地区详情")
def get_region(
    region_id: str,
    db: Session = Depends(get_db)
):
    """根据ID获取地区详情"""
    service = RegionService(db)
    region = service.get_region_by_id(region_id)
    
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    # 转换为包含国家信息的地区
    countries = [
        {
            "id": str(cr.country.id),
            "code": cr.country.code,
            "name": cr.country.name,
            "currency": cr.country.currency
        }
        for cr in region.countries
    ]
    
    region_dict = region.__dict__.copy()
    region_dict['countries'] = countries
    return RegionWithCountries(**region_dict)


@regions_router.put("/{region_id}", response_model=Region, summary="更新地区")
def update_region(
    region_id: str,
    region_data: RegionUpdate,
    db: Session = Depends(get_db)
):
    """更新地区信息"""
    service = RegionService(db)
    region = service.update_region(region_id, region_data)
    
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    return region


@regions_router.delete("/{region_id}", summary="删除地区")
def delete_region(
    region_id: str,
    db: Session = Depends(get_db)
):
    """删除地区"""
    service = RegionService(db)
    success = service.delete_region(region_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Region not found")
    
    return {"message": "Region deleted successfully"}


@regions_router.post("/{region_id}/countries/{country_id}", summary="将国家添加到地区")
def add_country_to_region(
    region_id: str,
    country_id: str,
    db: Session = Depends(get_db)
):
    """将国家添加到地区"""
    service = RegionService(db)
    success = service.add_country_to_region(region_id, country_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add country to region")
    
    return {"message": "Country added to region successfully"}


@regions_router.delete("/{region_id}/countries/{country_id}", summary="从地区移除国家")
def remove_country_from_region(
    region_id: str,
    country_id: str,
    db: Session = Depends(get_db)
):
    """从地区移除国家"""
    service = RegionService(db)
    success = service.remove_country_from_region(region_id, country_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Country not found in region")
    
    return {"message": "Country removed from region successfully"}


@regions_router.get("/{region_id}/countries", response_model=List[CountrySimple], summary="获取地区下的国家")
def get_countries_by_region(
    region_id: str,
    db: Session = Depends(get_db)
):
    """获取地区下的所有国家"""
    service = RegionService(db)
    countries = service.get_countries_by_region(region_id)
    
    return [
        CountrySimple(
            id=str(country.id),
            code=country.code,
            name=country.name,
            currency=country.currency
        )
        for country in countries
    ]


# ========================================
# 翻译管理接口
# ========================================

@router.post("/{country_id}/translations", response_model=CountryTranslation, summary="创建或更新国家翻译")
def create_or_update_country_translation(
    country_id: str,
    translation_data: CountryTranslationCreate,
    db: Session = Depends(get_db)
):
    """创建或更新国家翻译"""
    service = CountryTranslationService(db)
    return service.create_or_update_translation(
        country_id=country_id,
        language=translation_data.language,
        name=translation_data.name
    )


@router.delete("/{country_id}/translations/{language}", summary="删除国家翻译")
def delete_country_translation(
    country_id: str,
    language: str,
    db: Session = Depends(get_db)
):
    """删除国家翻译"""
    service = CountryTranslationService(db)
    success = service.delete_translation(country_id, language)
    
    if not success:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    return {"message": "Translation deleted successfully"}


@regions_router.post("/{region_id}/translations", response_model=RegionTranslation, summary="创建或更新地区翻译")
def create_or_update_region_translation(
    region_id: str,
    translation_data: RegionTranslationCreate,
    db: Session = Depends(get_db)
):
    """创建或更新地区翻译"""
    service = RegionTranslationService(db)
    return service.create_or_update_translation(
        region_id=region_id,
        language=translation_data.language,
        name=translation_data.name,
        description=translation_data.description
    )


@regions_router.delete("/{region_id}/translations/{language}", summary="删除地区翻译")
def delete_region_translation(
    region_id: str,
    language: str,
    db: Session = Depends(get_db)
):
    """删除地区翻译"""
    service = RegionTranslationService(db)
    success = service.delete_translation(region_id, language)
    
    if not success:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    return {"message": "Translation deleted successfully"}


# 将地区路由添加到主路由
router.include_router(regions_router)