import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from app.duty.models import (
    DutyZone, DutyZoneTranslation, DutyZoneCountry,
    ProductDutyCategory, ProductDutyCategoryTranslation,
    DutyRule, OrderDutyCharge
)
from app.localization.country.models import Country
from app.duty.schema import (
    DutyCalculationRequest, DutyCalculationResult,
    DutyCalculationItem, OrderDutyChargeCreate
)


class DutyCalculationService:
    """关税计算服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_duty(self, request: DutyCalculationRequest) -> DutyCalculationResult:
        """
        计算订单关税
        
        Args:
            request: 关税计算请求
            
        Returns:
            DutyCalculationResult: 关税计算结果
        """
        # 1. 根据国家代码查找关税区域
        duty_zone = self._find_duty_zone_by_country(request.country_code)
        if not duty_zone:
            return self._create_no_duty_result(request)
        
        # 2. 计算应税金额
        items_total = sum(item.quantity * item.price for item in request.items)
        taxable_amount = items_total + request.shipping_cost
        
        # 3. 检查免税阈值
        if taxable_amount <= duty_zone.tax_free_threshold:
            return self._create_tax_free_result(request, duty_zone, taxable_amount)
        
        # 4. 查找适用的关税规则
        applicable_rule = self._find_applicable_duty_rule(duty_zone.id, request.items)
        
        # 5. 计算关税金额
        tax_rate = applicable_rule.tax_rate if applicable_rule else duty_zone.default_tax_rate
        duty_amount = max(
            taxable_amount * tax_rate,
            applicable_rule.min_tax_amount if applicable_rule else 0.0
        )
        
        # 6. 应用最高征税限制
        if applicable_rule and applicable_rule.max_tax_amount:
            duty_amount = min(duty_amount, applicable_rule.max_tax_amount)
        
        # 7. 创建计算结果
        calculation_details = {
            "items_total": items_total,
            "shipping_cost": request.shipping_cost,
            "taxable_amount": taxable_amount,
            "tax_free_threshold": duty_zone.tax_free_threshold,
            "applied_rule_id": str(applicable_rule.id) if applicable_rule else None,
            "applied_rate": tax_rate,
            "min_tax_amount": applicable_rule.min_tax_amount if applicable_rule else 0.0,
            "max_tax_amount": applicable_rule.max_tax_amount if applicable_rule else None,
            "calculated_at": datetime.utcnow().isoformat()
        }
        
        return DutyCalculationResult(
            country_code=request.country_code,
            duty_zone_id=str(duty_zone.id),
            duty_zone_name=duty_zone.name,
            taxable_amount=taxable_amount,
            tax_rate=tax_rate,
            duty_amount=round(duty_amount, 2),
            is_tax_free=False,
            currency=duty_zone.currency,
            calculation_details=calculation_details
        )
    
    def _find_duty_zone_by_country(self, country_code: str) -> Optional[DutyZone]:
        """根据国家代码查找关税区域"""
        return (
            self.db.query(DutyZone)
            .join(DutyZoneCountry)
            .join(Country)
            .filter(
                and_(
                    Country.code == country_code.upper(),
                    DutyZone.status == 'active'
                )
            )
            .first()
        )
    
    def _find_applicable_duty_rule(self, zone_id: str, items: List[DutyCalculationItem]) -> Optional[DutyRule]:
        """查找适用的关税规则"""
        # 获取商品分类ID列表
        category_ids = [item.category_id for item in items if item.category_id]
        
        # 查询规则，按优先级排序
        query = (
            self.db.query(DutyRule)
            .filter(
                and_(
                    DutyRule.zone_id == zone_id,
                    DutyRule.status == 'active',
                    or_(
                        DutyRule.valid_to.is_(None),
                        DutyRule.valid_to >= datetime.utcnow()
                    ),
                    DutyRule.valid_from <= datetime.utcnow()
                )
            )
            .order_by(DutyRule.priority)
        )
        
        # 优先查找特定分类的规则
        if category_ids:
            specific_rule = query.filter(DutyRule.category_id.in_(category_ids)).first()
            if specific_rule:
                return specific_rule
        
        # 查找通用规则
        general_rule = query.filter(DutyRule.category_id.is_(None)).first()
        return general_rule
    
    def _create_no_duty_result(self, request: DutyCalculationRequest) -> DutyCalculationResult:
        """创建无关税结果"""
        items_total = sum(item.quantity * item.price for item in request.items)
        taxable_amount = items_total + request.shipping_cost
        
        return DutyCalculationResult(
            country_code=request.country_code,
            duty_zone_id=None,
            duty_zone_name=None,
            taxable_amount=taxable_amount,
            tax_rate=0.0,
            duty_amount=0.0,
            is_tax_free=True,
            currency=request.currency,
            calculation_details={
                "items_total": items_total,
                "shipping_cost": request.shipping_cost,
                "taxable_amount": taxable_amount,
                "reason": "No duty zone found for country",
                "calculated_at": datetime.utcnow().isoformat()
            }
        )
    
    def _create_tax_free_result(
        self, 
        request: DutyCalculationRequest, 
        duty_zone: DutyZone, 
        taxable_amount: float
    ) -> DutyCalculationResult:
        """创建免税结果"""
        return DutyCalculationResult(
            country_code=request.country_code,
            duty_zone_id=str(duty_zone.id),
            duty_zone_name=duty_zone.name,
            taxable_amount=taxable_amount,
            tax_rate=0.0,
            duty_amount=0.0,
            is_tax_free=True,
            currency=duty_zone.currency,
            calculation_details={
                "items_total": sum(item.quantity * item.price for item in request.items),
                "shipping_cost": request.shipping_cost,
                "taxable_amount": taxable_amount,
                "tax_free_threshold": duty_zone.tax_free_threshold,
                "reason": "Below tax-free threshold",
                "calculated_at": datetime.utcnow().isoformat()
            }
        )
    
    def create_order_duty_charge(
        self, 
        order_id: str, 
        calculation_result: DutyCalculationResult
    ) -> OrderDutyCharge:
        """创建订单关税记录"""
        # 查找国家ID
        country = self.db.query(Country).filter(
            Country.code == calculation_result.country_code.upper()
        ).first()
        
        if not country:
            raise ValueError(f"Country not found: {calculation_result.country_code}")
        
        # 创建关税记录
        duty_charge = OrderDutyCharge(
            id=str(uuid.uuid4()),
            order_id=order_id,
            country_id=str(country.id),
            duty_zone_id=calculation_result.duty_zone_id,
            taxable_amount=calculation_result.taxable_amount,
            tax_rate=calculation_result.tax_rate,
            duty_amount=calculation_result.duty_amount,
            currency=calculation_result.currency,
            calculation_details=json.dumps(calculation_result.calculation_details),
            status='pending'
        )
        
        self.db.add(duty_charge)
        self.db.commit()
        self.db.refresh(duty_charge)
        
        return duty_charge
    
    def get_supported_countries(self) -> List[Dict[str, Any]]:
        """获取支持关税计算的国家列表"""
        query = (
            self.db.query(
                Country.id,
                Country.code,
                Country.name,
                DutyZone.id.label('duty_zone_id'),
                DutyZone.name.label('duty_zone_name'),
                DutyZone.tax_free_threshold,
                DutyZone.default_tax_rate
            )
            .outerjoin(DutyZoneCountry, Country.id == DutyZoneCountry.country_id)
            .outerjoin(DutyZone, DutyZoneCountry.zone_id == DutyZone.id)
            .filter(Country.status == 'active')
            .order_by(Country.name)
        )
        
        countries = []
        for row in query.all():
            countries.append({
                "id": str(row.id),
                "code": row.code,
                "name": row.name,
                "duty_zone_id": str(row.duty_zone_id) if row.duty_zone_id else None,
                "duty_zone_name": row.duty_zone_name,
                "has_duty": row.duty_zone_id is not None,
                "tax_free_threshold": float(row.tax_free_threshold) if row.tax_free_threshold else 0.0,
                "default_tax_rate": float(row.default_tax_rate) if row.default_tax_rate else 0.0
            })
        
        return countries


class DutyZoneService:
    """关税区域服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_duty_zone(self, zone_data: dict) -> DutyZone:
        """创建关税区域"""
        zone = DutyZone(
            id=str(uuid.uuid4()),
            **{k: v for k, v in zone_data.items() if k != 'translations' and k != 'country_ids'}
        )
        
        self.db.add(zone)
        
        # 添加翻译
        if 'translations' in zone_data:
            for trans_data in zone_data['translations']:
                translation = DutyZoneTranslation(
                    id=str(uuid.uuid4()),
                    zone_id=zone.id,
                    **trans_data
                )
                self.db.add(translation)
        
        # 关联国家
        if 'country_ids' in zone_data:
            for country_id in zone_data['country_ids']:
                zone_country = DutyZoneCountry(
                    id=str(uuid.uuid4()),
                    zone_id=zone.id,
                    country_id=country_id
                )
                self.db.add(zone_country)
        
        self.db.commit()
        self.db.refresh(zone)
        return zone
    
    def get_duty_zones(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> tuple[List[DutyZone], int]:
        """获取关税区域列表"""
        query = self.db.query(DutyZone).options(
            joinedload(DutyZone.translations),
            joinedload(DutyZone.countries)
        )
        
        if status:
            query = query.filter(DutyZone.status == status)
        
        total = query.count()
        zones = query.offset(skip).limit(limit).all()
        
        return zones, total
    
    def get_duty_zone_by_id(self, zone_id: str) -> Optional[DutyZone]:
        """根据ID获取关税区域"""
        return (
            self.db.query(DutyZone)
            .options(
                joinedload(DutyZone.translations),
                joinedload(DutyZone.countries)
            )
            .filter(DutyZone.id == zone_id)
            .first()
        )
    
    def update_duty_zone(self, zone_id: str, zone_data: dict) -> Optional[DutyZone]:
        """更新关税区域"""
        zone = self.get_duty_zone_by_id(zone_id)
        if not zone:
            return None
        
        # 更新基础信息
        for key, value in zone_data.items():
            if key not in ['translations', 'country_ids'] and hasattr(zone, key):
                setattr(zone, key, value)
        
        zone.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(zone)
        return zone
    
    def delete_duty_zone(self, zone_id: str) -> bool:
        """删除关税区域"""
        zone = self.get_duty_zone_by_id(zone_id)
        if not zone:
            return False
        
        self.db.delete(zone)
        self.db.commit()
        return True


class ProductDutyCategoryService:
    """商品关税分类服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_category(self, category_data: dict) -> ProductDutyCategory:
        """创建商品关税分类"""
        category = ProductDutyCategory(
            id=str(uuid.uuid4()),
            **{k: v for k, v in category_data.items() if k != 'translations'}
        )
        
        self.db.add(category)
        
        # 添加翻译
        if 'translations' in category_data:
            for trans_data in category_data['translations']:
                translation = ProductDutyCategoryTranslation(
                    id=str(uuid.uuid4()),
                    category_id=category.id,
                    **trans_data
                )
                self.db.add(translation)
        
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_categories(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> tuple[List[ProductDutyCategory], int]:
        """获取商品关税分类列表"""
        query = self.db.query(ProductDutyCategory).options(
            joinedload(ProductDutyCategory.translations)
        )
        
        if status:
            query = query.filter(ProductDutyCategory.status == status)
        
        total = query.count()
        categories = query.offset(skip).limit(limit).all()
        
        return categories, total
    
    def get_category_by_id(self, category_id: str) -> Optional[ProductDutyCategory]:
        """根据ID获取商品关税分类"""
        return (
            self.db.query(ProductDutyCategory)
            .options(joinedload(ProductDutyCategory.translations))
            .filter(ProductDutyCategory.id == category_id)
            .first()
        )


class DutyRuleService:
    """关税规则服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_rule(self, rule_data: dict) -> DutyRule:
        """创建关税规则"""
        rule = DutyRule(
            id=str(uuid.uuid4()),
            **rule_data
        )
        
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule
    
    def get_rules(
        self, 
        skip: int = 0, 
        limit: int = 100,
        zone_id: Optional[str] = None,
        category_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> tuple[List[DutyRule], int]:
        """获取关税规则列表"""
        query = self.db.query(DutyRule).options(
            joinedload(DutyRule.zone),
            joinedload(DutyRule.category)
        )
        
        if zone_id:
            query = query.filter(DutyRule.zone_id == zone_id)
        if category_id:
            query = query.filter(DutyRule.category_id == category_id)
        if status:
            query = query.filter(DutyRule.status == status)
        
        total = query.count()
        rules = query.order_by(DutyRule.priority).offset(skip).limit(limit).all()
        
        return rules, total