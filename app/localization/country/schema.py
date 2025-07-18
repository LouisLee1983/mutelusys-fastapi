from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# 基础schemas
class CountryTranslationBase(BaseModel):
    language: str = Field(..., description="语言代码")
    name: str = Field(..., description="翻译名称")


class CountryTranslationCreate(CountryTranslationBase):
    pass


class CountryTranslationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="翻译名称")


class CountryTranslation(CountryTranslationBase):
    id: str
    country_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class RegionTranslationBase(BaseModel):
    language: str = Field(..., description="语言代码")
    name: str = Field(..., description="翻译名称")
    description: Optional[str] = Field(None, description="翻译描述")


class RegionTranslationCreate(RegionTranslationBase):
    pass


class RegionTranslationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="翻译名称")
    description: Optional[str] = Field(None, description="翻译描述")


class RegionTranslation(RegionTranslationBase):
    id: str
    region_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


# 国家schemas
class CountryBase(BaseModel):
    code: str = Field(..., max_length=2, description="ISO 3166-1 alpha-2 国家代码")
    code3: str = Field(..., max_length=3, description="ISO 3166-1 alpha-3 国家代码")
    name: str = Field(..., max_length=100, description="英文名称")
    native_name: Optional[str] = Field(None, max_length=100, description="本地名称")
    currency: Optional[str] = Field(None, max_length=3, description="默认货币代码")
    phone_code: Optional[str] = Field(None, max_length=10, description="电话区号")
    status: str = Field(default="active", description="状态")


class CountryCreate(CountryBase):
    translations: Optional[List[CountryTranslationCreate]] = Field(default=[], description="翻译列表")


class CountryUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=2, description="ISO 3166-1 alpha-2 国家代码")
    code3: Optional[str] = Field(None, max_length=3, description="ISO 3166-1 alpha-3 国家代码")
    name: Optional[str] = Field(None, max_length=100, description="英文名称")
    native_name: Optional[str] = Field(None, max_length=100, description="本地名称")
    currency: Optional[str] = Field(None, max_length=3, description="默认货币代码")
    phone_code: Optional[str] = Field(None, max_length=10, description="电话区号")
    status: Optional[str] = Field(None, description="状态")


class Country(CountryBase):
    id: str
    created_at: datetime
    updated_at: datetime
    translations: List[CountryTranslation] = Field(default=[], description="翻译列表")
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class CountrySimple(BaseModel):
    """简化的国家信息，用于下拉选择等场景"""
    id: str
    code: str
    name: str
    currency: Optional[str] = None
    
    class Config:
        from_attributes = True


# 地区schemas
class RegionBase(BaseModel):
    name: str = Field(..., max_length=100, description="地区名称")
    code: str = Field(..., max_length=10, description="地区代码")
    description: Optional[str] = Field(None, description="地区描述")
    status: str = Field(default="active", description="状态")


class RegionCreate(RegionBase):
    translations: Optional[List[RegionTranslationCreate]] = Field(default=[], description="翻译列表")
    country_ids: Optional[List[str]] = Field(default=[], description="关联的国家ID列表")


class RegionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="地区名称")
    code: Optional[str] = Field(None, max_length=10, description="地区代码")
    description: Optional[str] = Field(None, description="地区描述")
    status: Optional[str] = Field(None, description="状态")


class Region(RegionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    # translations: List[RegionTranslation] = Field(default=[], description="翻译列表")
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class RegionWithCountries(Region):
    """包含国家信息的地区"""
    countries: List[CountrySimple] = Field(default=[], description="包含的国家列表")


# 国家地区关联schemas
class CountryRegionCreate(BaseModel):
    country_id: str = Field(..., description="国家ID")
    region_id: str = Field(..., description="地区ID")


class CountryRegion(BaseModel):
    id: str
    country_id: str
    region_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# 批量操作schemas
class CountryBatchCreate(BaseModel):
    countries: List[CountryCreate] = Field(..., description="批量创建的国家列表")


class RegionBatchCreate(BaseModel):
    regions: List[RegionCreate] = Field(..., description="批量创建的地区列表")


# 查询和响应schemas
class CountryListResponse(BaseModel):
    countries: List[Country]
    total: int
    page: int
    size: int


class RegionListResponse(BaseModel):
    regions: List[RegionWithCountries]
    total: int
    page: int
    size: int


class CountryRegionResponse(BaseModel):
    """国家及其地区信息"""
    country: Country
    regions: List[Region] = Field(default=[], description="所属地区列表")