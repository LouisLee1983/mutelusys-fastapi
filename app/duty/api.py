from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.duty.service import (
    DutyZoneService, ProductDutyCategoryService, DutyRuleService, DutyCalculationService
)
from app.duty.schema import (
    DutyZone, DutyZoneCreate, DutyZoneUpdate, DutyZoneListResponse, DutyZoneSimple,
    ProductDutyCategory, ProductDutyCategoryCreate, ProductDutyCategoryUpdate, 
    ProductDutyCategoryListResponse, ProductDutyCategorySimple,
    DutyRule, DutyRuleCreate, DutyRuleUpdate, DutyRuleListResponse, DutyRuleWithDetails,
    OrderDutyCharge, OrderDutyChargeListResponse,
    DutyCalculationRequest, DutyCalculationResult, DutyCalculationBatchRequest, DutyCalculationBatchResult,
    SupportedCountriesResponse, SupportedCountry,
    DutyStatistics, DutyZoneStatistics
)

router = APIRouter(prefix="/duty")


# ========================================
# 关税区域管理接口
# ========================================

@router.post("/zones", response_model=DutyZone, summary="创建关税区域")
def create_duty_zone(
    zone_data: DutyZoneCreate,
    db: Session = Depends(get_db)
):
    """创建新的关税区域"""
    service = DutyZoneService(db)
    return service.create_duty_zone(zone_data.dict())


@router.get("/zones", response_model=DutyZoneListResponse, summary="获取关税区域列表")
def get_duty_zones(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db)
):
    """获取关税区域列表"""
    service = DutyZoneService(db)
    zones, total = service.get_duty_zones(skip=skip, limit=limit, status=status)
    
    return DutyZoneListResponse(
        zones=zones,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/zones/{zone_id}", response_model=DutyZone, summary="获取关税区域详情")
def get_duty_zone(
    zone_id: str,
    db: Session = Depends(get_db)
):
    """根据ID获取关税区域详情"""
    service = DutyZoneService(db)
    zone = service.get_duty_zone_by_id(zone_id)
    
    if not zone:
        raise HTTPException(status_code=404, detail="Duty zone not found")
    
    return zone


@router.put("/zones/{zone_id}", response_model=DutyZone, summary="更新关税区域")
def update_duty_zone(
    zone_id: str,
    zone_data: DutyZoneUpdate,
    db: Session = Depends(get_db)
):
    """更新关税区域信息"""
    service = DutyZoneService(db)
    zone = service.update_duty_zone(zone_id, zone_data.dict(exclude_unset=True))
    
    if not zone:
        raise HTTPException(status_code=404, detail="Duty zone not found")
    
    return zone


@router.delete("/zones/{zone_id}", summary="删除关税区域")
def delete_duty_zone(
    zone_id: str,
    db: Session = Depends(get_db)
):
    """删除关税区域"""
    service = DutyZoneService(db)
    success = service.delete_duty_zone(zone_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Duty zone not found")
    
    return {"message": "Duty zone deleted successfully"}


# ========================================
# 商品关税分类管理接口
# ========================================

@router.post("/categories", response_model=ProductDutyCategory, summary="创建商品关税分类")
def create_duty_category(
    category_data: ProductDutyCategoryCreate,
    db: Session = Depends(get_db)
):
    """创建新的商品关税分类"""
    service = ProductDutyCategoryService(db)
    return service.create_category(category_data.dict())


@router.get("/categories", response_model=ProductDutyCategoryListResponse, summary="获取商品关税分类列表")
def get_duty_categories(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db)
):
    """获取商品关税分类列表"""
    service = ProductDutyCategoryService(db)
    categories, total = service.get_categories(skip=skip, limit=limit, status=status)
    
    return ProductDutyCategoryListResponse(
        categories=categories,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/categories/simple", response_model=List[ProductDutyCategorySimple], summary="获取简化分类列表")
def get_duty_categories_simple(
    status: str = Query("active", description="状态"),
    db: Session = Depends(get_db)
):
    """获取简化的商品关税分类列表，用于下拉选择"""
    service = ProductDutyCategoryService(db)
    categories, _ = service.get_categories(skip=0, limit=1000, status=status)
    
    return [
        ProductDutyCategorySimple(
            id=str(category.id),
            name=category.name,
            tax_rate=category.tax_rate
        )
        for category in categories
    ]


@router.get("/categories/{category_id}", response_model=ProductDutyCategory, summary="获取商品关税分类详情")
def get_duty_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    """根据ID获取商品关税分类详情"""
    service = ProductDutyCategoryService(db)
    category = service.get_category_by_id(category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail="Duty category not found")
    
    return category


# ========================================
# 关税规则管理接口
# ========================================

@router.post("/rules", response_model=DutyRule, summary="创建关税规则")
def create_duty_rule(
    rule_data: DutyRuleCreate,
    db: Session = Depends(get_db)
):
    """创建新的关税规则"""
    service = DutyRuleService(db)
    return service.create_rule(rule_data.dict())


@router.get("/rules", response_model=DutyRuleListResponse, summary="获取关税规则列表")
def get_duty_rules(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    zone_id: Optional[str] = Query(None, description="关税区域ID筛选"),
    category_id: Optional[str] = Query(None, description="商品分类ID筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db)
):
    """获取关税规则列表"""
    service = DutyRuleService(db)
    rules, total = service.get_rules(
        skip=skip, 
        limit=limit, 
        zone_id=zone_id, 
        category_id=category_id, 
        status=status
    )
    
    # 转换为包含详细信息的规则
    rules_with_details = []
    for rule in rules:
        rule_dict = rule.__dict__.copy()
        
        # 添加区域信息
        if rule.zone:
            rule_dict['zone'] = DutyZoneSimple(
                id=str(rule.zone.id),
                name=rule.zone.name,
                tax_free_threshold=rule.zone.tax_free_threshold,
                default_tax_rate=rule.zone.default_tax_rate,
                currency=rule.zone.currency
            )
        
        # 添加分类信息
        if rule.category:
            rule_dict['category'] = ProductDutyCategorySimple(
                id=str(rule.category.id),
                name=rule.category.name,
                tax_rate=rule.category.tax_rate
            )
        
        rules_with_details.append(DutyRuleWithDetails(**rule_dict))
    
    return DutyRuleListResponse(
        rules=rules_with_details,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# ========================================
# 关税计算接口
# ========================================

@router.post("/calculate", response_model=DutyCalculationResult, summary="计算关税")
def calculate_duty(
    request: DutyCalculationRequest,
    db: Session = Depends(get_db)
):
    """计算订单关税"""
    service = DutyCalculationService(db)
    return service.calculate_duty(request)


@router.post("/calculate/batch", response_model=DutyCalculationBatchResult, summary="批量计算关税")
def calculate_duty_batch(
    request: DutyCalculationBatchRequest,
    db: Session = Depends(get_db)
):
    """批量计算关税"""
    service = DutyCalculationService(db)
    results = []
    success_count = 0
    error_count = 0
    
    for calc_request in request.calculations:
        try:
            result = service.calculate_duty(calc_request)
            results.append(result)
            success_count += 1
        except Exception as e:
            error_count += 1
            # 创建错误结果
            error_result = DutyCalculationResult(
                country_code=calc_request.country_code,
                duty_zone_id=None,
                duty_zone_name=None,
                taxable_amount=0.0,
                tax_rate=0.0,
                duty_amount=0.0,
                is_tax_free=True,
                currency=calc_request.currency,
                calculation_details={
                    "error": str(e),
                    "calculated_at": service.datetime.utcnow().isoformat()
                }
            )
            results.append(error_result)
    
    return DutyCalculationBatchResult(
        results=results,
        total_count=len(request.calculations),
        success_count=success_count,
        error_count=error_count
    )


@router.get("/supported-countries", response_model=SupportedCountriesResponse, summary="获取支持的国家列表")
def get_supported_countries(
    db: Session = Depends(get_db)
):
    """获取支持关税计算的国家列表"""
    service = DutyCalculationService(db)
    countries_data = service.get_supported_countries()
    
    countries = [
        SupportedCountry(**country_data)
        for country_data in countries_data
    ]
    
    return SupportedCountriesResponse(
        countries=countries,
        total=len(countries)
    )


# ========================================
# 订单关税记录接口
# ========================================

@router.get("/charges", response_model=OrderDutyChargeListResponse, summary="获取订单关税记录列表")
def get_order_duty_charges(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    order_id: Optional[str] = Query(None, description="订单ID筛选"),
    country_id: Optional[str] = Query(None, description="国家ID筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db)
):
    """获取订单关税记录列表"""
    from app.duty.models import OrderDutyCharge
    from sqlalchemy import and_
    
    query = db.query(OrderDutyCharge)
    
    if order_id:
        query = query.filter(OrderDutyCharge.order_id == order_id)
    if country_id:
        query = query.filter(OrderDutyCharge.country_id == country_id)
    if status:
        query = query.filter(OrderDutyCharge.status == status)
    
    total = query.count()
    charges = query.order_by(OrderDutyCharge.created_at.desc()).offset(skip).limit(limit).all()
    
    return OrderDutyChargeListResponse(
        charges=charges,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/charges/{charge_id}", response_model=OrderDutyCharge, summary="获取订单关税记录详情")
def get_order_duty_charge(
    charge_id: str,
    db: Session = Depends(get_db)
):
    """根据ID获取订单关税记录详情"""
    from app.duty.models import OrderDutyCharge
    
    charge = db.query(OrderDutyCharge).filter(OrderDutyCharge.id == charge_id).first()
    
    if not charge:
        raise HTTPException(status_code=404, detail="Duty charge not found")
    
    return charge


@router.put("/charges/{charge_id}/status", response_model=OrderDutyCharge, summary="更新关税记录状态")
def update_duty_charge_status(
    charge_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """更新订单关税记录状态"""
    from app.duty.models import OrderDutyCharge
    from datetime import datetime
    
    charge = db.query(OrderDutyCharge).filter(OrderDutyCharge.id == charge_id).first()
    
    if not charge:
        raise HTTPException(status_code=404, detail="Duty charge not found")
    
    charge.status = status
    charge.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(charge)
    
    return charge


# ========================================
# 统计分析接口
# ========================================

@router.get("/statistics", response_model=DutyStatistics, summary="获取关税统计信息")
def get_duty_statistics(
    db: Session = Depends(get_db)
):
    """获取关税统计信息"""
    from app.duty.models import DutyZone, ProductDutyCategory, DutyRule, OrderDutyCharge
    from sqlalchemy import func
    
    # 统计各项数量
    total_duty_zones = db.query(func.count(DutyZone.id)).filter(DutyZone.status == 'active').scalar()
    total_categories = db.query(func.count(ProductDutyCategory.id)).filter(ProductDutyCategory.status == 'active').scalar()
    total_rules = db.query(func.count(DutyRule.id)).filter(DutyRule.status == 'active').scalar()
    total_orders_with_duty = db.query(func.count(OrderDutyCharge.id)).filter(OrderDutyCharge.duty_amount > 0).scalar()
    
    # 统计关税金额
    total_duty_amount = db.query(func.sum(OrderDutyCharge.duty_amount)).filter(
        OrderDutyCharge.status == 'paid'
    ).scalar() or 0.0
    
    # 平均税率
    average_duty_rate = db.query(func.avg(OrderDutyCharge.tax_rate)).filter(
        OrderDutyCharge.duty_amount > 0
    ).scalar() or 0.0
    
    return DutyStatistics(
        total_duty_zones=total_duty_zones,
        total_categories=total_categories,
        total_rules=total_rules,
        total_orders_with_duty=total_orders_with_duty,
        total_duty_amount=float(total_duty_amount),
        average_duty_rate=float(average_duty_rate)
    )


@router.get("/statistics/zones", response_model=List[DutyZoneStatistics], summary="获取关税区域统计")
def get_duty_zone_statistics(
    db: Session = Depends(get_db)
):
    """获取各关税区域的统计信息"""
    from app.duty.models import DutyZone, OrderDutyCharge
    from sqlalchemy import func
    
    results = (
        db.query(
            DutyZone.id,
            DutyZone.name,
            func.count(OrderDutyCharge.id).label('order_count'),
            func.sum(OrderDutyCharge.duty_amount).label('total_duty_amount'),
            func.avg(OrderDutyCharge.duty_amount).label('average_duty_amount'),
            func.mode().within_group(OrderDutyCharge.tax_rate).label('most_common_rate')
        )
        .outerjoin(OrderDutyCharge, DutyZone.id == OrderDutyCharge.duty_zone_id)
        .filter(DutyZone.status == 'active')
        .group_by(DutyZone.id, DutyZone.name)
        .all()
    )
    
    statistics = []
    for result in results:
        statistics.append(DutyZoneStatistics(
            zone_id=str(result.id),
            zone_name=result.name,
            order_count=result.order_count or 0,
            total_duty_amount=float(result.total_duty_amount or 0.0),
            average_duty_amount=float(result.average_duty_amount or 0.0),
            most_common_rate=float(result.most_common_rate or 0.0)
        ))
    
    return statistics