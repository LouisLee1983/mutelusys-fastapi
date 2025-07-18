# -*- coding: utf-8 -*-
"""
运费计算服务层
提供完整的运费计算引擎和相关业务逻辑
"""
import time
from decimal import Decimal
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .schema import (
    ShippingCalculationRequest, ShippingCalculationResponse,
    ShippingMethodOption, ShippingEstimate, ShippingBreakdown,
    BatchShippingCalculationRequest, BatchShippingCalculationResponse
)
from ..method.models import ShippingMethod, ShippingMethodTranslation
from ..zone.models import ShippingZone, ShippingZoneTranslation
from ..rate.models import ShippingRate
from ..free_rule.service import FreeShippingRuleService
from ..free_rule.schema import ApplyFreeShippingRequest


class ShippingCalculationService:
    """运费计算服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.free_rule_service = FreeShippingRuleService(db)

    def calculate_shipping(self, request: ShippingCalculationRequest) -> ShippingCalculationResponse:
        """计算运费主方法"""
        start_time = time.time()
        
        try:
            # 1. 根据国家代码匹配运费地区
            zone = self._find_shipping_zone(request.country_code)
            if not zone:
                return ShippingCalculationResponse(
                    success=False,
                    message=f"不支持配送到国家 '{request.country_code}'",
                    estimates=[],
                    total_estimates=0,
                    calculation_time=time.time() - start_time
                )

            # 2. 获取可用的快递方式
            available_methods = self._get_available_methods(zone.id)
            if not available_methods:
                return ShippingCalculationResponse(
                    success=False,
                    message="当前地区暂无可用的快递方式",
                    estimates=[],
                    total_estimates=0,
                    calculation_time=time.time() - start_time
                )

            # 3. 计算每种快递方式的运费
            estimates = []
            for method in available_methods:
                estimate = self._calculate_method_shipping(method, zone, request)
                if estimate:
                    estimates.append(estimate)

            # 4. 排序
            estimates = sorted(estimates, key=lambda x: x.breakdown.final_shipping_cost)

            # 5. 标记推荐
            if estimates:
                estimates[0].is_recommended = True

            calculation_time = time.time() - start_time

            return ShippingCalculationResponse(
                success=True,
                message="计算成功",
                estimates=estimates,
                total_estimates=len(estimates),
                recommended_method=estimates[0] if estimates else None,
                calculation_time=calculation_time
            )

        except Exception as e:
            return ShippingCalculationResponse(
                success=False,
                message=f"计算运费时发生错误: {str(e)}",
                estimates=[],
                total_estimates=0,
                calculation_time=time.time() - start_time
            )

    def calculate_batch_shipping(self, request: BatchShippingCalculationRequest) -> BatchShippingCalculationResponse:
        """批量计算运费"""
        start_time = time.time()
        results = []
        successful_count = 0
        failed_count = 0

        for calc_request in request.requests[:request.max_requests]:
            result = self.calculate_shipping(calc_request)
            results.append(result)
            
            if result.success:
                successful_count += 1
            else:
                failed_count += 1

        calculation_time = time.time() - start_time

        return BatchShippingCalculationResponse(
            success=True,
            message="批量计算完成",
            results=results,
            total_requests=len(results),
            successful_count=successful_count,
            failed_count=failed_count,
            calculation_time=calculation_time
        )

    def get_quick_quote(self, country_code: str, quantity: int, method_code: Optional[str] = None) -> Optional[Decimal]:
        """快速获取运费报价（简化版）"""
        try:
            # 构建简化请求
            request = ShippingCalculationRequest(
                country_code=country_code,
                total_quantity=quantity,
                total_amount=Decimal("0"),  # 不考虑免运费
                currency_code="USD",
                exclude_methods=[method_code] if method_code else None
            )

            result = self.calculate_shipping(request)
            if result.success and result.estimates:
                if method_code:
                    # 查找指定方式的运费
                    for estimate in result.estimates:
                        if estimate.method.method_code == method_code:
                            return estimate.breakdown.final_shipping_cost
                else:
                    # 返回最便宜的运费
                    cheapest = self._find_cheapest_method(result.estimates)
                    if cheapest:
                        return cheapest.breakdown.final_shipping_cost

            return None
        except Exception:
            return None

    # ==================== 私有方法 ====================

    def _find_shipping_zone(self, country_code: str) -> Optional[ShippingZone]:
        """根据国家代码查找运费地区"""
        zones = self.db.query(ShippingZone).filter(
            and_(
                ShippingZone.is_active == True,
                ShippingZone.country_codes.contains([country_code])
            )
        ).all()
        return zones[0] if zones else None

    def _get_available_methods(self, zone_id: str) -> List[ShippingMethod]:
        """获取可用的快递方式"""
        methods = self.db.query(ShippingMethod).join(ShippingRate).filter(
            and_(
                ShippingRate.zone_id == zone_id,
                ShippingRate.is_active == True,
                ShippingMethod.is_active == True
            )
        ).distinct().all()
        return methods

    def _calculate_method_shipping(
        self, method: ShippingMethod, zone: ShippingZone, request: ShippingCalculationRequest
    ) -> Optional[ShippingEstimate]:
        """计算单个快递方式的运费"""
        try:
            # 查找运费规则
            base_cost = self._find_shipping_rate(zone.id, method.id, request.total_quantity)
            if base_cost is None:
                return None

            # 检查免运费
            free_shipping_request = ApplyFreeShippingRequest(
                country_code=request.country_code,
                total_amount=request.total_amount,
                total_quantity=request.total_quantity,
                member_level=request.member_level,
                promotion_codes=request.promotion_codes,
                shipping_method_code=method.code,
                language_code=request.language_code
            )

            free_result = self.free_rule_service.check_free_shipping(free_shipping_request)

            # 计算最终运费
            final_cost = Decimal("0") if free_result.is_free else base_cost
            discount = base_cost if free_result.is_free else Decimal("0")

            # 构建响应
            breakdown = ShippingBreakdown(
                base_shipping_cost=base_cost,
                discount_amount=discount,
                final_shipping_cost=final_cost,
                currency_code=request.currency_code,
                is_free_shipping=free_result.is_free,
                free_shipping_rule_id=free_result.applied_rule_id,
                free_shipping_rule_name=free_result.applied_rule_name,
                free_shipping_reason=free_result.reason
            )

            method_option = ShippingMethodOption(
                method_id=str(method.id),
                method_code=method.code,
                method_name=method.name,
                company_name=method.company_name,
                description=method.description,
                transport_type=method.transport_type.value,
                min_delivery_days=method.min_delivery_days,
                max_delivery_days=method.max_delivery_days
            )

            return ShippingEstimate(
                method=method_option,
                breakdown=breakdown,
                is_recommended=False,
                sort_order=method.sort_order or 0
            )

        except Exception as e:
            print(f"计算快递方式 {method.code} 运费时出错: {str(e)}")
            return None

    def _find_shipping_rate(self, zone_id: str, method_id: str, quantity: int) -> Optional[Decimal]:
        """查找适用的运费规则"""
        rate = self.db.query(ShippingRate).filter(
            and_(
                ShippingRate.zone_id == zone_id,
                ShippingRate.method_id == method_id,
                ShippingRate.min_quantity <= quantity,
                ShippingRate.is_active == True,
                (ShippingRate.max_quantity.is_(None)) | (ShippingRate.max_quantity >= quantity)
            )
        ).order_by(ShippingRate.min_quantity.desc()).first()

        return rate.rate if rate else None

    def _find_cheapest_method(self, estimates: List[ShippingEstimate]) -> Optional[ShippingEstimate]:
        """找到最便宜的快递方式"""
        if not estimates:
            return None

        return min(estimates, key=lambda x: x.breakdown.final_shipping_cost)

    def _get_translated_zone_name(self, zone: ShippingZone, language_code: str) -> str:
        """获取翻译后的地区名称"""
        translation = self.db.query(ShippingZoneTranslation).filter(
            and_(
                ShippingZoneTranslation.shipping_zone_id == zone.id,
                ShippingZoneTranslation.language_code == language_code
            )
        ).first()

        return translation.name if translation else zone.name

    def _get_translated_method_name(self, method: ShippingMethod, language_code: str) -> str:
        """获取翻译后的快递方式名称"""
        translation = self.db.query(ShippingMethodTranslation).filter(
            and_(
                ShippingMethodTranslation.shipping_method_id == method.id,
                ShippingMethodTranslation.language_code == language_code
            )
        ).first()

        return translation.name if translation else method.name

    def _get_translated_company_name(self, method: ShippingMethod, language_code: str) -> str:
        """获取翻译后的快递公司名称"""
        translation = self.db.query(ShippingMethodTranslation).filter(
            and_(
                ShippingMethodTranslation.shipping_method_id == method.id,
                ShippingMethodTranslation.language_code == language_code
            )
        ).first()

        return translation.company_name if translation and translation.company_name else method.company_name

    def _get_translated_method_description(self, method: ShippingMethod, language_code: str) -> Optional[str]:
        """获取翻译后的快递方式描述"""
        translation = self.db.query(ShippingMethodTranslation).filter(
            and_(
                ShippingMethodTranslation.shipping_method_id == method.id,
                ShippingMethodTranslation.language_code == language_code
            )
        ).first()

        if translation and translation.description:
            return translation.description
        return method.description

    def _format_delivery_time(self, method: ShippingMethod, language_code: str) -> Optional[str]:
        """格式化配送时间文本"""
        if not method.min_delivery_days:
            return None

        min_days = method.min_delivery_days
        max_days = method.max_delivery_days

        if language_code.startswith('zh'):
            if max_days and max_days != min_days:
                return f"{min_days}-{max_days} 个工作日"
            else:
                return f"{min_days} 个工作日"
        else:
            if max_days and max_days != min_days:
                return f"{min_days}-{max_days} business days"
            else:
                return f"{min_days} business days" 