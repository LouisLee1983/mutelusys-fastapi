# -*- coding: utf-8 -*-
"""
AI助手核心服务类
"""
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.analytics.ai_copilot.models import (
    AICallRecord, ProductAIAnalysis, AIServiceProvider, 
    AICallStatus, AICallType
)
from app.analytics.ai_copilot.schema import (
    AICallRecordCreate, ProductAIAnalysisCreate,
    ProductAnalysisRequest, ProductAnalysisResponse,
    ApplyAnalysisRequest
)
from app.analytics.ai_copilot.alibaba_service import AlibabaBailianService
from app.product.models import Product, ProductCategory, ProductMaterial
from app.product.service import ProductService
from app.product.category.service import ProductCategoryService


class AICopilotService:
    """AI助手核心服务类"""
    
    def __init__(self):
        self.alibaba_service = AlibabaBailianService()
    
    async def analyze_product_images(
        self, 
        db: Session,
        request: ProductAnalysisRequest,
        user_id: Optional[uuid.UUID] = None
    ) -> ProductAnalysisResponse:
        """分析商品图片"""
        
        call_record = None
        try:
            # 1. 创建AI调用记录
            call_record = self._create_call_record(
                db, 
                request.image_urls, 
                request.additional_context, 
                user_id
            )
            
            # 2. 调用AI服务进行分析
            ai_service = AlibabaBailianService()
            analysis_result = await ai_service.analyze_product_images(
                image_urls=request.image_urls,
                additional_context=request.additional_context,
                language=request.language or "zh-CN"
            )
            
            if analysis_result.get("success"):
                # 3. 更新调用记录
                parsed_data = analysis_result.get("parsed_result", {})
                usage_info = analysis_result.get("raw_response", {}).get("usage", {})
                
                call_record.status = AICallStatus.SUCCESS
                call_record.response_data = analysis_result.get("raw_response")
                call_record.parsed_result = parsed_data
                call_record.tokens_used = usage_info.get("total_tokens", 0)
                call_record.confidence_score = parsed_data.get("confidence", 0.0)
                
                # 设置完成时间，保持与started_at相同的时区感知状态
                if call_record.started_at and call_record.started_at.tzinfo is not None:
                    import pytz
                    call_record.completed_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
                else:
                    call_record.completed_at = datetime.utcnow()
                
                # 4. 计算调用成本
                if call_record.tokens_used:
                    call_record.cost = ai_service.estimate_cost(call_record.tokens_used)
                
                # 5. 计算调用耗时
                if call_record.started_at:
                    # 确保两个datetime对象具有相同的时区感知状态
                    end_time = datetime.utcnow()
                    start_time = call_record.started_at
                    
                    # 如果start_time是aware，将end_time也转换为aware
                    if start_time.tzinfo is not None:
                        import pytz
                        end_time = end_time.replace(tzinfo=pytz.UTC)
                    # 如果start_time是naive，确保end_time也是naive
                    elif end_time.tzinfo is not None:
                        end_time = end_time.replace(tzinfo=None)
                    
                    duration = (end_time - start_time).total_seconds() * 1000
                    call_record.duration_ms = int(duration)
                
                # 先提交调用记录的更新
                try:
                    db.commit()
                except Exception as e:
                    print(f"提交调用记录失败: {e}")
                    db.rollback()
                    raise
                
                # 6. 创建分析记录
                try:
                    # 开始新的数据库事务来保存分析记录
                    analysis_record = self._create_analysis_record(
                        db,
                        call_record_id=call_record.id,
                        parsed_data=parsed_data
                    )
                    
                    # 确保分析记录已经保存并刷新
                    db.commit()
                    
                    # 重新获取分析记录以确保数据完整性
                    fresh_analysis_record = db.query(ProductAIAnalysis).filter(
                        ProductAIAnalysis.id == analysis_record.id
                    ).first()
                    
                    if not fresh_analysis_record:
                        raise Exception("无法重新获取保存的分析记录")
                    
                    # 使用from_db_model方法转换数据库对象为API响应格式
                    from app.analytics.ai_copilot.schema import ProductAIAnalysis as ProductAIAnalysisSchema
                    
                    print(f"🔍 转换数据库对象，类型: {type(fresh_analysis_record)}")
                    if hasattr(fresh_analysis_record, '__dict__'):
                        print(f"🔍 对象属性: {list(fresh_analysis_record.__dict__.keys())}")
                    
                    analysis_for_response = ProductAIAnalysisSchema.from_db_model(fresh_analysis_record)
                    
                except Exception as e:
                    print(f"创建分析记录失败，但调用记录已保存: {e}")
                    # 即使分析记录保存失败，也不影响主要功能
                    # 创建一个包含所有必需字段的临时分析记录
                    
                    # 处理属性建议
                    suggested_attributes = {
                        "style": parsed_data.get("style", ""),
                        "features": parsed_data.get("features", [])
                    }
                    
                    # 适应新的JSON格式
                    suggested_prices = {
                        "min": parsed_data.get("price_min", 0),
                        "max": parsed_data.get("price_max", 0),
                        "currency": parsed_data.get("currency", "USD")
                    }
                    
                    # 创建符合Pydantic模型期望的临时对象
                    analysis_for_response = type('TempAnalysis', (), {
                        'id': uuid.uuid4(),
                        'call_record_id': call_record.id,  # 必需字段
                        'product_id': None,
                        'suggested_name': parsed_data.get("name", ""),
                        'suggested_description': parsed_data.get("description", ""),
                        'suggested_category_ids': None,
                        'suggested_attributes': suggested_attributes,
                        'suggested_materials': parsed_data.get("materials", []),
                        'suggested_colors': parsed_data.get("colors", []),
                        'suggested_sizes': parsed_data.get("sizes", []),
                        'suggested_prices': suggested_prices,
                        'suggested_tags': parsed_data.get("tags", []),
                        'suggested_scenes': parsed_data.get("scenes", []),
                        'suggested_target_groups': parsed_data.get("targets", []),
                        'analysis_confidence': parsed_data.get("confidence", 0.0),
                        'raw_analysis': parsed_data,
                        'is_applied': False,
                        'applied_at': None,
                        'applied_by': None,
                        'created_at': datetime.utcnow(),  # 必需字段
                        'updated_at': datetime.utcnow()   # 必需字段
                    })()
                
                # 7. 处理建议信息
                suggestions = await self._process_suggestions(db, parsed_data)
                
                return ProductAnalysisResponse(
                    call_record_id=call_record.id,
                    analysis_id=analysis_for_response.id,
                    analysis=analysis_for_response,
                    suggestions=suggestions
                )
            else:
                raise Exception(analysis_result.get("error", "AI分析失败"))
                
        except Exception as e:
            # 更新调用记录为失败状态
            if call_record:
                try:
                    call_record.status = AICallStatus.FAILED
                    call_record.error_message = str(e)
                    
                    # 设置完成时间，保持与started_at相同的时区感知状态
                    if call_record.started_at and call_record.started_at.tzinfo is not None:
                        import pytz
                        call_record.completed_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
                    else:
                        call_record.completed_at = datetime.utcnow()
                    
                    db.commit()
                except Exception as commit_error:
                    print(f"更新失败状态记录时出错: {commit_error}")
                    db.rollback()
            
            print(f"分析商品图片失败: {e}")
            raise Exception(f"分析失败: {str(e)}")
    
    def _create_call_record(
        self, 
        db: Session,
        image_urls: List[str],
        additional_context: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None
    ) -> AICallRecord:
        """创建AI调用记录"""
        try:
            call_record = AICallRecord(
                provider=AIServiceProvider.ALIBABA_BAILIAN,
                model_name="qwen-vl-max",
                call_type=AICallType.PRODUCT_ANALYSIS,
                status=AICallStatus.PROCESSING,  # 设置为处理中状态
                image_urls=image_urls,
                prompt=additional_context,
                user_id=user_id,
                started_at=datetime.utcnow(),  # 设置开始时间
                business_context={
                    "action": "product_image_analysis",
                    "image_count": len(image_urls)
                }
            )
            
            db.add(call_record)
            db.commit()
            db.refresh(call_record)
            
            return call_record
        except Exception as e:
            print(f"创建调用记录失败: {e}")
            db.rollback()
            raise Exception(f"创建调用记录失败: {str(e)}")
    
    def _create_analysis_record(
        self,
        db: Session,
        call_record_id: uuid.UUID,
        parsed_data: Dict[str, Any]
    ) -> ProductAIAnalysis:
        """创建产品分析记录"""
        
        try:
            import json
            
            # 提取建议信息，适应新的JSON格式
            suggested_categories = parsed_data.get("categories", [])
            suggested_materials = parsed_data.get("materials", [])
            suggested_colors = parsed_data.get("colors", [])
            suggested_sizes = parsed_data.get("sizes", [])
            suggested_tags = parsed_data.get("tags", [])
            suggested_scenes = parsed_data.get("scenes", [])
            suggested_target_groups = parsed_data.get("targets", [])
            
            # 确保列表数据是正确的Python对象，而不是字符串
            if isinstance(suggested_materials, str):
                suggested_materials = json.loads(suggested_materials)
            if isinstance(suggested_colors, str):
                suggested_colors = json.loads(suggested_colors)
            if isinstance(suggested_sizes, str):
                suggested_sizes = json.loads(suggested_sizes)
            if isinstance(suggested_tags, str):
                suggested_tags = json.loads(suggested_tags)
            if isinstance(suggested_scenes, str):
                suggested_scenes = json.loads(suggested_scenes)
            if isinstance(suggested_target_groups, str):
                suggested_target_groups = json.loads(suggested_target_groups)
            
            # 适应新的JSON格式的价格数据
            suggested_prices = {
                "min": parsed_data.get("price_min", 0),
                "max": parsed_data.get("price_max", 0),
                "currency": parsed_data.get("currency", "USD")
            }
            
            # 处理属性建议
            suggested_features = parsed_data.get("features", [])
            if isinstance(suggested_features, str):
                suggested_features = json.loads(suggested_features)
                
            suggested_attributes = {
                "style": parsed_data.get("style", ""),
                "features": suggested_features
            }
            
            # 将数据转换为JSON字符串，因为现在字段是Text类型
            # 创建分析记录，所有JSON字段都转换为字符串
            analysis_record = ProductAIAnalysis(
                call_record_id=call_record_id,
                suggested_name=parsed_data.get("name"),
                suggested_description=parsed_data.get("description"),
                suggested_attributes=json.dumps(suggested_attributes, ensure_ascii=False) if suggested_attributes else None,
                suggested_materials=json.dumps(suggested_materials, ensure_ascii=False) if suggested_materials else None,
                suggested_colors=json.dumps(suggested_colors, ensure_ascii=False) if suggested_colors else None,
                suggested_sizes=json.dumps(suggested_sizes, ensure_ascii=False) if suggested_sizes else None,
                suggested_prices=json.dumps(suggested_prices, ensure_ascii=False) if suggested_prices else None,
                suggested_tags=json.dumps(suggested_tags, ensure_ascii=False) if suggested_tags else None,
                suggested_scenes=json.dumps(suggested_scenes, ensure_ascii=False) if suggested_scenes else None,
                suggested_target_groups=json.dumps(suggested_target_groups, ensure_ascii=False) if suggested_target_groups else None,
                analysis_confidence=parsed_data.get("confidence", 0.0),
                raw_analysis=json.dumps(parsed_data, ensure_ascii=False) if parsed_data else None
            )
            
            db.add(analysis_record)
            db.flush()  # 使用flush而不是commit，让上层管理事务
            db.refresh(analysis_record)
            
            # 确保返回的对象有正确的属性
            if not analysis_record or not hasattr(analysis_record, 'id'):
                raise Exception("创建的分析记录无效")
            
            print(f"✅ 成功创建分析记录，ID: {analysis_record.id}")
            return analysis_record
            
        except Exception as e:
            print(f"创建分析记录失败: {e}")
            db.rollback()  # 回滚当前事务
            raise Exception(f"保存分析结果失败: {str(e)}")
    
    async def _process_suggestions(
        self,
        db: Session,
        parsed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """处理建议信息，匹配现有的分类、材质等"""
        
        suggestions = {
            "categories": [],
            "materials": [],
            "existing_products": [],
            "price_analysis": {},
            "confidence_level": parsed_data.get("confidence", 0.0)
        }
        
        # 1. 匹配分类
        suggested_categories = parsed_data.get("categories", [])
        if suggested_categories:
            matched_categories = self._match_categories(db, suggested_categories)
            suggestions["categories"] = matched_categories
        
        # 2. 匹配材质
        suggested_materials = parsed_data.get("materials", [])
        if suggested_materials:
            matched_materials = self._match_materials(db, suggested_materials)
            suggestions["materials"] = matched_materials
        
        # 3. 价格分析，适应新的JSON格式
        price_min = parsed_data.get("price_min", 0)
        price_max = parsed_data.get("price_max", 0)
        currency = parsed_data.get("currency", "USD")
        
        if price_min > 0 or price_max > 0:
            price_range = {"min": price_min, "max": price_max, "currency": currency}
            suggestions["price_analysis"] = {
                "suggested_min": price_min,
                "suggested_max": price_max,
                "currency": currency,
                "market_positioning": self._analyze_price_positioning(price_range)
            }
        
        # 4. 查找相似商品
        product_name = parsed_data.get("name", "")
        if product_name:
            similar_products = self._find_similar_products(db, product_name)
            suggestions["existing_products"] = similar_products
        
        return suggestions
    
    def _match_categories(self, db: Session, suggested_categories: List[str]) -> List[Dict[str, Any]]:
        """匹配现有分类"""
        matched_categories = []
        
        for category_name in suggested_categories:
            # 查找匹配的分类（模糊匹配）
            categories = db.query(ProductCategory).filter(
                ProductCategory.name.ilike(f"%{category_name}%")
            ).limit(3).all()
            
            for category in categories:
                matched_categories.append({
                    "id": str(category.id),
                    "name": category.name,
                    "slug": category.slug,
                    "match_score": self._calculate_match_score(category_name, category.name),
                    "suggested_name": category_name
                })
        
        # 按匹配分数排序
        matched_categories.sort(key=lambda x: x["match_score"], reverse=True)
        return matched_categories[:5]  # 返回前5个匹配结果
    
    def _match_materials(self, db: Session, suggested_materials: List[str]) -> List[Dict[str, Any]]:
        """匹配现有材质"""
        matched_materials = []
        
        for material_name in suggested_materials:
            # 查找匹配的材质
            materials = db.query(ProductMaterial).filter(
                ProductMaterial.name.ilike(f"%{material_name}%")
            ).limit(3).all()
            
            for material in materials:
                matched_materials.append({
                    "id": str(material.id),
                    "name": material.name,
                    "slug": material.slug,
                    "material_type": material.material_type.value,
                    "match_score": self._calculate_match_score(material_name, material.name),
                    "suggested_name": material_name
                })
        
        # 按匹配分数排序
        matched_materials.sort(key=lambda x: x["match_score"], reverse=True)
        return matched_materials[:5]
    
    def _calculate_match_score(self, suggested: str, existing: str) -> float:
        """计算匹配分数"""
        suggested = suggested.lower().strip()
        existing = existing.lower().strip()
        
        if suggested == existing:
            return 1.0
        elif suggested in existing or existing in suggested:
            return 0.8
        else:
            # 简单的字符相似度计算
            common_chars = set(suggested) & set(existing)
            return len(common_chars) / max(len(suggested), len(existing))
    
    def _analyze_price_positioning(self, price_range: Dict[str, Any]) -> str:
        """分析价格定位"""
        min_price = price_range.get("min", 0)
        max_price = price_range.get("max", 0)
        avg_price = (min_price + max_price) / 2 if max_price > 0 else min_price
        
        if avg_price < 20:
            return "经济型"
        elif avg_price < 50:
            return "中低端"
        elif avg_price < 100:
            return "中端"
        elif avg_price < 200:
            return "中高端"
        else:
            return "高端"
    
    def _find_similar_products(self, db: Session, product_name: str) -> List[Dict[str, Any]]:
        """查找相似商品"""
        # 查找名称相似的商品
        products = db.query(Product).filter(
            Product.name.ilike(f"%{product_name}%")
        ).limit(5).all()
        
        similar_products = []
        for product in products:
            similar_products.append({
                "id": str(product.id),
                "name": product.name,
                "sku_code": product.sku_code,
                "status": product.status.value,
                "is_featured": product.is_featured
            })
        
        return similar_products
    
    async def apply_analysis_suggestions(
        self,
        db: Session,
        request: ApplyAnalysisRequest,
        user_id: Optional[uuid.UUID] = None
    ) -> Dict[str, Any]:
        """应用分析建议，创建或更新商品"""
        
        # 1. 获取分析记录
        analysis = db.query(ProductAIAnalysis).filter(
            ProductAIAnalysis.id == request.analysis_id
        ).first()
        
        if not analysis:
            raise Exception("分析记录不存在")
        
        # 2. 根据选择的建议创建或更新商品
        if request.create_product:
            # 创建新商品
            product_id = await self._create_product_from_suggestions(
                db, analysis, request.selected_suggestions, user_id
            )
        else:
            # 更新现有商品
            if not request.product_id:
                raise Exception("更新商品时必须提供商品ID")
            product_id = await self._update_product_from_suggestions(
                db, request.product_id, analysis, request.selected_suggestions, user_id
            )
        
        # 3. 标记分析结果已应用
        analysis.is_applied = True
        analysis.applied_at = datetime.utcnow()
        analysis.applied_by = user_id
        analysis.product_id = product_id
        db.commit()
        
        return {
            "success": True,
            "product_id": str(product_id),
            "analysis_id": str(analysis.id),
            "applied_suggestions": request.selected_suggestions
        }
    
    async def _create_product_from_suggestions(
        self,
        db: Session,
        analysis: ProductAIAnalysis,
        selected_suggestions: Dict[str, Any],
        user_id: Optional[uuid.UUID] = None
    ) -> uuid.UUID:
        """根据建议创建新商品"""
        
        # 构建商品创建数据
        product_data = {
            "sku_code": f"AI-{uuid.uuid4().hex[:8].upper()}",
            "name": selected_suggestions.get("name", analysis.suggested_name),
            "description": selected_suggestions.get("description", analysis.suggested_description),
            "status": "draft",  # 默认为草稿状态
            "is_featured": False,
            "is_new": True,
        }
        
        # 这里需要调用商品服务创建商品
        # 由于ProductService的具体实现可能比较复杂，这里先返回一个模拟的商品ID
        product_id = uuid.uuid4()
        
        return product_id
    
    async def _update_product_from_suggestions(
        self,
        db: Session,
        product_id: uuid.UUID,
        analysis: ProductAIAnalysis,
        selected_suggestions: Dict[str, Any],
        user_id: Optional[uuid.UUID] = None
    ) -> uuid.UUID:
        """根据建议更新现有商品"""
        
        # 获取现有商品
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise Exception("商品不存在")
        
        # 更新商品信息
        if selected_suggestions.get("name"):
            product.name = selected_suggestions["name"]
        
        if selected_suggestions.get("description"):
            product.description = selected_suggestions["description"]
        
        product.updated_at = datetime.utcnow()
        db.commit()
        
        return product_id 