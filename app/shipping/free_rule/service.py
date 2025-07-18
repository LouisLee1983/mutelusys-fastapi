# -*- coding: utf-8 -*-
"""
免运费规则服务层
包含CRUD操作和免运费检查业务逻辑
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import FreeShippingRule, FreeShippingRuleTranslation, FreeShippingRuleType
from .schema import (
    FreeShippingRuleCreate, FreeShippingRuleUpdate, FreeShippingRuleResponse,
    FreeShippingRuleTranslationCreate, FreeShippingRuleTranslationUpdate,
    ApplyFreeShippingRequest, FreeShippingCheckResult, FreeShippingRuleTypeEnum
)


class FreeShippingRuleService:
    """免运费规则服务类"""

    def __init__(self, db: Session):
        self.db = db

    # ==================== 免运费规则CRUD操作 ====================

    def create_rule(self, rule_data: FreeShippingRuleCreate) -> FreeShippingRuleResponse:
        """创建免运费规则"""
        # 检查代码是否重复
        existing_rule = self.db.query(FreeShippingRule).filter(
            FreeShippingRule.code == rule_data.code
        ).first()
        if existing_rule:
            raise ValueError(f"免运费规则代码 '{rule_data.code}' 已存在")

        # 创建规则
        rule_dict = rule_data.dict(exclude={'translations'})
        db_rule = FreeShippingRule(**rule_dict)
        self.db.add(db_rule)
        self.db.flush()

        # 创建翻译
        if rule_data.translations:
            for translation_data in rule_data.translations:
                db_translation = FreeShippingRuleTranslation(
                    free_shipping_rule_id=db_rule.id,
                    **translation_data.dict()
                )
                self.db.add(db_translation)

        self.db.commit()
        self.db.refresh(db_rule)
        return FreeShippingRuleResponse.from_orm(db_rule)

    def get_rule_by_id(self, rule_id: UUID, language_code: str = "zh-CN") -> Optional[FreeShippingRuleResponse]:
        """根据ID获取免运费规则"""
        db_rule = self.db.query(FreeShippingRule).filter(
            FreeShippingRule.id == rule_id
        ).first()
        if not db_rule:
            return None

        # 获取翻译
        self._load_translations(db_rule, language_code)
        return FreeShippingRuleResponse.from_orm(db_rule)

    def get_rule_by_code(self, code: str, language_code: str = "zh-CN") -> Optional[FreeShippingRuleResponse]:
        """根据代码获取免运费规则"""
        db_rule = self.db.query(FreeShippingRule).filter(
            FreeShippingRule.code == code
        ).first()
        if not db_rule:
            return None

        self._load_translations(db_rule, language_code)
        return FreeShippingRuleResponse.from_orm(db_rule)

    def list_rules(
        self,
        rule_type: Optional[FreeShippingRuleTypeEnum] = None,
        is_active: Optional[bool] = None,
        language_code: str = "zh-CN",
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[FreeShippingRuleResponse], int]:
        """获取免运费规则列表"""
        query = self.db.query(FreeShippingRule)

        # 筛选条件
        if rule_type is not None:
            query = query.filter(FreeShippingRule.rule_type == rule_type.value)
        if is_active is not None:
            query = query.filter(FreeShippingRule.is_active == is_active)

        # 排序
        query = query.order_by(FreeShippingRule.priority.desc(), FreeShippingRule.sort_order.asc())

        # 分页
        total = query.count()
        offset = (page - 1) * page_size
        db_rules = query.offset(offset).limit(page_size).all()

        # 加载翻译
        for db_rule in db_rules:
            self._load_translations(db_rule, language_code)

        rules = [FreeShippingRuleResponse.from_orm(rule) for rule in db_rules]
        return rules, total

    def update_rule(self, rule_id: UUID, rule_data: FreeShippingRuleUpdate) -> Optional[FreeShippingRuleResponse]:
        """更新免运费规则"""
        db_rule = self.db.query(FreeShippingRule).filter(
            FreeShippingRule.id == rule_id
        ).first()
        if not db_rule:
            return None

        # 检查代码是否重复
        if rule_data.code and rule_data.code != db_rule.code:
            existing_rule = self.db.query(FreeShippingRule).filter(
                and_(
                    FreeShippingRule.code == rule_data.code,
                    FreeShippingRule.id != rule_id
                )
            ).first()
            if existing_rule:
                raise ValueError(f"免运费规则代码 '{rule_data.code}' 已存在")

        # 更新字段
        update_data = rule_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rule, field, value)

        db_rule.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_rule)
        return FreeShippingRuleResponse.from_orm(db_rule)

    def delete_rule(self, rule_id: UUID) -> bool:
        """删除免运费规则"""
        db_rule = self.db.query(FreeShippingRule).filter(
            FreeShippingRule.id == rule_id
        ).first()
        if not db_rule:
            return False

        self.db.delete(db_rule)
        self.db.commit()
        return True

    # ==================== 翻译管理 ====================

    def create_translation(
        self,
        rule_id: UUID,
        translation_data: FreeShippingRuleTranslationCreate
    ) -> Optional[dict]:
        """创建规则翻译"""
        # 检查规则是否存在
        db_rule = self.db.query(FreeShippingRule).filter(
            FreeShippingRule.id == rule_id
        ).first()
        if not db_rule:
            return None

        # 检查翻译是否已存在
        existing_translation = self.db.query(FreeShippingRuleTranslation).filter(
            and_(
                FreeShippingRuleTranslation.free_shipping_rule_id == rule_id,
                FreeShippingRuleTranslation.language_code == translation_data.language_code
            )
        ).first()
        if existing_translation:
            raise ValueError(f"语言 '{translation_data.language_code}' 的翻译已存在")

        # 创建翻译
        db_translation = FreeShippingRuleTranslation(
            free_shipping_rule_id=rule_id,
            **translation_data.dict()
        )
        self.db.add(db_translation)
        self.db.commit()
        self.db.refresh(db_translation)
        return {
            "id": str(db_translation.id),
            "free_shipping_rule_id": str(db_translation.free_shipping_rule_id),
            "language_code": db_translation.language_code,
            "name": db_translation.name,
            "description": db_translation.description,
            "created_at": db_translation.created_at,
            "updated_at": db_translation.updated_at
        }

    def update_translation(
        self,
        rule_id: UUID,
        language_code: str,
        translation_data: FreeShippingRuleTranslationUpdate
    ) -> Optional[dict]:
        """更新规则翻译"""
        db_translation = self.db.query(FreeShippingRuleTranslation).filter(
            and_(
                FreeShippingRuleTranslation.free_shipping_rule_id == rule_id,
                FreeShippingRuleTranslation.language_code == language_code
            )
        ).first()
        if not db_translation:
            return None

        # 更新字段
        update_data = translation_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_translation, field, value)

        db_translation.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_translation)
        return {
            "id": str(db_translation.id),
            "free_shipping_rule_id": str(db_translation.free_shipping_rule_id),
            "language_code": db_translation.language_code,
            "name": db_translation.name,
            "description": db_translation.description,
            "created_at": db_translation.created_at,
            "updated_at": db_translation.updated_at
        }

    def delete_translation(self, rule_id: UUID, language_code: str) -> bool:
        """删除规则翻译"""
        db_translation = self.db.query(FreeShippingRuleTranslation).filter(
            and_(
                FreeShippingRuleTranslation.free_shipping_rule_id == rule_id,
                FreeShippingRuleTranslation.language_code == language_code
            )
        ).first()
        if not db_translation:
            return False

        self.db.delete(db_translation)
        self.db.commit()
        return True

    # ==================== 免运费检查业务逻辑 ====================

    def check_free_shipping(self, request: ApplyFreeShippingRequest) -> FreeShippingCheckResult:
        """检查是否符合免运费条件"""
        current_time = datetime.utcnow()
        
        # 获取所有有效的免运费规则（按优先级排序）
        query = self.db.query(FreeShippingRule).filter(
            and_(
                FreeShippingRule.is_active == True,
                or_(
                    FreeShippingRule.start_date.is_(None),
                    FreeShippingRule.start_date <= current_time
                ),
                or_(
                    FreeShippingRule.end_date.is_(None),
                    FreeShippingRule.end_date > current_time
                )
            )
        ).order_by(FreeShippingRule.priority.desc(), FreeShippingRule.sort_order.asc())

        active_rules = query.all()

        # 检查每个规则
        for rule in active_rules:
            if self._check_rule_applicable(rule, request):
                # 检查规则条件
                if self._check_rule_conditions(rule, request):
                    # 获取规则名称（带翻译）
                    rule_name = self._get_translated_rule_name(rule, request.language_code)
                    return FreeShippingCheckResult(
                        is_free=True,
                        applied_rule_id=str(rule.id),
                        applied_rule_name=rule_name,
                        applied_rule_type=FreeShippingRuleTypeEnum(rule.rule_type.value),
                        reason=self._get_free_shipping_reason(rule, request),
                        savings_amount=None  # 需要计算原运费才能知道节省金额
                    )

        # 没有符合条件的免运费规则，计算下一个门槛
        next_threshold, next_quantity = self._calculate_next_threshold(active_rules, request)
        
        return FreeShippingCheckResult(
            is_free=False,
            applied_rule_id=None,
            applied_rule_name=None,
            applied_rule_type=None,
            reason=None,
            savings_amount=None,
            next_threshold=next_threshold,
            next_quantity=next_quantity
        )

    def _check_rule_applicable(self, rule: FreeShippingRule, request: ApplyFreeShippingRequest) -> bool:
        """检查规则是否适用于当前请求"""
        # 检查地区限制
        if rule.applicable_zones:
            zone_codes = [code.strip() for code in rule.applicable_zones.split(',')]
            if request.country_code not in zone_codes:
                return False

        # 检查快递方式限制
        if rule.applicable_methods and request.shipping_method_code:
            method_codes = [code.strip() for code in rule.applicable_methods.split(',')]
            if request.shipping_method_code not in method_codes:
                return False

        return True

    def _check_rule_conditions(self, rule: FreeShippingRule, request: ApplyFreeShippingRequest) -> bool:
        """检查规则条件是否满足"""
        if rule.rule_type == FreeShippingRuleType.AMOUNT_BASED:
            # 满额免费
            return rule.min_amount and request.total_amount >= rule.min_amount

        elif rule.rule_type == FreeShippingRuleType.QUANTITY_BASED:
            # 满件免费
            return rule.min_quantity and request.total_quantity >= rule.min_quantity

        elif rule.rule_type == FreeShippingRuleType.MEMBER_BASED:
            # 会员免费
            if not request.member_level or not rule.member_levels:
                return False
            member_levels = [level.strip() for level in rule.member_levels.split(',')]
            return request.member_level in member_levels

        elif rule.rule_type == FreeShippingRuleType.PROMOTION_BASED:
            # 促销免费
            if not request.promotion_codes or not rule.promotion_codes:
                return False
            promotion_codes = [code.strip() for code in rule.promotion_codes.split(',')]
            return any(code in promotion_codes for code in request.promotion_codes)

        return False

    def _get_translated_rule_name(self, rule: FreeShippingRule, language_code: str) -> str:
        """获取翻译后的规则名称"""
        # 查找对应语言的翻译
        translation = self.db.query(FreeShippingRuleTranslation).filter(
            and_(
                FreeShippingRuleTranslation.free_shipping_rule_id == rule.id,
                FreeShippingRuleTranslation.language_code == language_code
            )
        ).first()

        if translation:
            return translation.name
        return rule.name

    def _get_free_shipping_reason(self, rule: FreeShippingRule, request: ApplyFreeShippingRequest) -> str:
        """获取免运费原因描述"""
        if rule.rule_type == FreeShippingRuleType.AMOUNT_BASED:
            return f"订单满 ${rule.min_amount} 免运费"
        elif rule.rule_type == FreeShippingRuleType.QUANTITY_BASED:
            return f"购买满 {rule.min_quantity} 件免运费"
        elif rule.rule_type == FreeShippingRuleType.MEMBER_BASED:
            return f"{request.member_level} 会员免运费"
        elif rule.rule_type == FreeShippingRuleType.PROMOTION_BASED:
            return "促销活动免运费"
        return "免运费"

    def _calculate_next_threshold(
        self,
        rules: List[FreeShippingRule],
        request: ApplyFreeShippingRequest
    ) -> Tuple[Optional[Decimal], Optional[int]]:
        """计算下一个免运费门槛"""
        next_amount = None
        next_quantity = None

        for rule in rules:
            if not self._check_rule_applicable(rule, request):
                continue

            if rule.rule_type == FreeShippingRuleType.AMOUNT_BASED and rule.min_amount:
                if request.total_amount < rule.min_amount:
                    if next_amount is None or rule.min_amount < next_amount:
                        next_amount = rule.min_amount

            elif rule.rule_type == FreeShippingRuleType.QUANTITY_BASED and rule.min_quantity:
                if request.total_quantity < rule.min_quantity:
                    if next_quantity is None or rule.min_quantity < next_quantity:
                        next_quantity = rule.min_quantity

        return next_amount, next_quantity

    def _load_translations(self, rule: FreeShippingRule, language_code: str):
        """加载规则的翻译信息"""
        # 这个方法用于确保翻译关系被正确加载
        # SQLAlchemy 的 relationship 会自动处理，这里只是确保访问
        _ = rule.translations 