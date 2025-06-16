import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, Text, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class RecommendationType(str, enum.Enum):
    PRODUCT = "product"           # 产品推荐
    BUNDLE = "bundle"             # 套装推荐
    CONTENT = "content"           # 内容推荐
    SYMBOL = "symbol"             # 符号推荐
    INTENTION = "intention"       # 意图推荐
    MATERIAL = "material"         # 材质推荐
    CATEGORY = "category"         # 分类推荐


class RecommendationAlgorithm(str, enum.Enum):
    COLLABORATIVE_FILTERING = "collaborative_filtering"  # 协同过滤
    CONTENT_BASED = "content_based"                      # 基于内容
    POPULARITY_BASED = "popularity_based"                # 基于流行度
    HYBRID = "hybrid"                                    # 混合方法
    CULTURAL_INTENTION = "cultural_intention"            # 文化意图推荐
    RULE_BASED = "rule_based"                            # 基于规则


class PersonalizedRecommendation(Base):
    """个性化推荐，基于用户文化偏好和意图偏好的智能推荐"""
    __tablename__ = "personalized_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True, comment="客户ID，可为空")
    session_id = Column(String(100), nullable=True, comment="会话ID，用于匿名用户")
    
    # 推荐信息
    recommendation_type = Column(Enum(RecommendationType), nullable=False, comment="推荐类型")
    item_id = Column(UUID(as_uuid=True), nullable=False, comment="推荐项目ID")
    item_type = Column(String(50), nullable=False, comment="项目类型：product, bundle, content等")
    algorithm = Column(Enum(RecommendationAlgorithm), default=RecommendationAlgorithm.HYBRID, nullable=False, comment="推荐算法")
    
    # 推荐上下文
    context = Column(String(50), nullable=True, comment="推荐上下文：homepage, product_detail, cart, checkout等")
    position = Column(String(50), nullable=True, comment="推荐位置：top, sidebar, bottom等")
    section = Column(String(50), nullable=True, comment="推荐区块：recently_viewed, related_items等")
    
    # 意图和文化设置
    related_intention = Column(String(100), nullable=True, comment="相关意图")
    related_cultural_element = Column(String(100), nullable=True, comment="相关文化元素")
    matching_score = Column(Float, default=0, comment="匹配分数")
    
    # 推荐原因
    reason_code = Column(String(50), nullable=True, comment="推荐原因代码")
    reason_text = Column(String(255), nullable=True, comment="推荐原因文本")
    
    # 客户行为源
    source_behavior = Column(String(50), nullable=True, comment="来源行为：view, purchase, search, wishlist等")
    source_item_id = Column(UUID(as_uuid=True), nullable=True, comment="来源项目ID")
    source_item_type = Column(String(50), nullable=True, comment="来源项目类型")
    
    # 统计信息
    was_shown = Column(Boolean, default=False, comment="是否已展示")
    was_clicked = Column(Boolean, default=False, comment="是否被点击")
    was_converted = Column(Boolean, default=False, comment="是否已转化")
    
    # 时间记录
    shown_at = Column(DateTime, nullable=True, comment="展示时间")
    clicked_at = Column(DateTime, nullable=True, comment="点击时间")
    converted_at = Column(DateTime, nullable=True, comment="转化时间")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    customer = relationship("Customer")


class RecommendationRule(Base):
    """推荐规则配置，定义产品间的关系规则"""
    __tablename__ = "recommendation_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="规则名称")
    description = Column(Text, nullable=True, comment="规则描述")
    
    # 规则类型
    rule_type = Column(String(50), nullable=False, comment="规则类型：complementary, substitute, ensemble等")
    
    # 规则源和目标
    source_type = Column(String(50), nullable=False, comment="源类型：product, category, intention等")
    source_id = Column(UUID(as_uuid=True), nullable=True, comment="源ID")
    target_type = Column(String(50), nullable=False, comment="目标类型：product, category, intention等")
    target_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True, comment="目标ID列表")
    
    # 规则设置
    strength = Column(Float, default=1.0, comment="规则强度（0-1）")
    priority = Column(Integer, default=0, comment="优先级")
    is_bidirectional = Column(Boolean, default=False, comment="是否双向规则")
    
    # 规则条件
    conditions = Column(JSON, nullable=True, comment="规则条件")
    
    # 显示设置
    reason_text = Column(String(255), nullable=True, comment="推荐原因文本")
    
    # 状态信息
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间设置
    start_date = Column(DateTime, nullable=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    creator = relationship("User")


class RecommendationModel(Base):
    """推荐模型配置，记录模型参数和性能"""
    __tablename__ = "recommendation_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="模型名称")
    description = Column(Text, nullable=True, comment="模型描述")
    
    # 模型信息
    algorithm = Column(Enum(RecommendationAlgorithm), nullable=False, comment="算法")
    version = Column(String(20), nullable=False, comment="版本")
    parameters = Column(JSON, nullable=True, comment="参数设置")
    
    # 训练信息
    training_date = Column(DateTime, nullable=True, comment="训练日期")
    training_duration = Column(Integer, nullable=True, comment="训练时长（秒）")
    training_data_size = Column(Integer, nullable=True, comment="训练数据大小")
    
    # 性能指标
    accuracy = Column(Float, nullable=True, comment="准确率")
    precision = Column(Float, nullable=True, comment="精确率")
    recall = Column(Float, nullable=True, comment="召回率")
    f1_score = Column(Float, nullable=True, comment="F1分数")
    mean_average_precision = Column(Float, nullable=True, comment="平均精度")
    
    # 模型路径
    model_path = Column(String(255), nullable=True, comment="模型路径")
    
    # 状态信息
    is_active = Column(Boolean, default=False, comment="是否激活")
    is_in_production = Column(Boolean, default=False, comment="是否在生产环境")
    
    # A/B测试
    is_in_test = Column(Boolean, default=False, comment="是否在测试中")
    test_group = Column(String(50), nullable=True, comment="测试组")
    
    # 额外信息
    meta_data = Column(JSON, nullable=True, comment="元数据")
    
    # 共有字段
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    creator = relationship("User")
