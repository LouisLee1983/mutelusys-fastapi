import json
import openai
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.fortune.models import FortuneProfile, FortuneReading, ReadingType
from app.fortune.schema import (
    BaziAnalysisRequest, 
    TarotAnalysisRequest,
    AnalysisResultResponse
)
from app.core.config import settings


class ChatGPTService:
    """ChatGPT API集成服务"""
    
    def __init__(self):
        openai.api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY not configured")
    
    async def analyze_bazi(self, request: BaziAnalysisRequest) -> str:
        """八字命理分析"""
        prompt = f"""
你是一位资深的中国传统命理大师，请根据以下信息进行八字命理分析：

出生信息：
- 出生年份：{request.birth_year}年
- 出生月份：{request.birth_month}月  
- 出生日期：{request.birth_day}日
- 出生时辰：{request.birth_hour if request.birth_hour else '未知'}时
- 性别：{'男' if request.gender == 'male' else '女'}
- 出生地：{request.birth_location or '未知'}

请提供以下内容的分析：
1. 八字基本信息（天干地支）
2. 五行分析（金木水火土的强弱）
3. 性格特征分析
4. 运势趋势（事业、财运、感情、健康）
5. 今年运势重点
6. 适合佩戴的佛牌或护身符建议

请用温和、积极的语调，给出建设性的建议。字数控制在800-1000字。
"""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一位专业的命理分析师，擅长八字命理分析，为用户提供准确、积极的人生指导。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"ChatGPT API调用失败: {str(e)}")
    
    async def analyze_tarot(self, request: TarotAnalysisRequest) -> str:
        """塔罗牌分析"""
        # 简化的塔罗牌含义（实际应用中可以建立完整的数据库）
        tarot_meanings = {
            1: "魔术师 - 创造力和行动力",
            2: "女祭司 - 直觉和内在智慧", 
            3: "皇后 - 丰盛和创造",
            # ... 可以扩展到78张牌
        }
        
        selected_meanings = [tarot_meanings.get(card, f"第{card}张牌") for card in request.selected_cards]
        
        prompt = f"""
你是一位专业的塔罗牌占卜师，请根据以下信息进行今日运势分析：

占卜信息：
- 选择的塔罗牌：{', '.join(selected_meanings)}
- 问题类型：{request.question_type}
- 占卜日期：{datetime.now().strftime('%Y年%m月%d日')}

请提供以下内容：
1. 牌面解读（每张牌的含义）
2. 综合分析（牌与牌之间的关系）
3. 今日运势指导
4. 具体建议（根据问题类型给出针对性建议）
5. 注意事项
6. 推荐佩戴的护身符或佛牌

请用温暖、鼓励的语调，给出正面积极的指导。字数控制在600-800字。
"""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一位温和、智慧的塔罗牌占卜师，擅长为用户解读牌面含义，给出积极正面的人生指导。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"ChatGPT API调用失败: {str(e)}")


class FortuneService:
    """算命服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.chatgpt = ChatGPTService()
    
    def get_or_create_profile(self, customer_id: str, request: BaziAnalysisRequest) -> FortuneProfile:
        """获取或创建用户算命档案"""
        profile = self.db.query(FortuneProfile).filter(
            FortuneProfile.customer_id == customer_id
        ).first()
        
        if not profile:
            profile = FortuneProfile(
                customer_id=customer_id,
                birth_year=request.birth_year,
                birth_month=request.birth_month,
                birth_day=request.birth_day,
                birth_hour=request.birth_hour,
                gender=request.gender,
                birth_location=request.birth_location
            )
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        
        return profile
    
    def create_or_update_profile(self, customer_id: str, birth_year: int, birth_month: int, 
                               birth_day: int, birth_hour: Optional[int], gender: str, 
                               birth_location: Optional[str], timezone: Optional[str] = None) -> FortuneProfile:
        """创建或更新用户算命档案"""
        profile = self.db.query(FortuneProfile).filter(
            FortuneProfile.customer_id == customer_id
        ).first()
        
        if profile:
            # 更新现有档案
            profile.birth_year = birth_year
            profile.birth_month = birth_month
            profile.birth_day = birth_day
            profile.birth_hour = birth_hour
            profile.gender = gender
            profile.birth_location = birth_location
            profile.updated_at = datetime.utcnow()
        else:
            # 创建新档案
            profile = FortuneProfile(
                customer_id=customer_id,
                birth_year=birth_year,
                birth_month=birth_month,
                birth_day=birth_day,
                birth_hour=birth_hour,
                gender=gender,
                birth_location=birth_location
            )
            self.db.add(profile)
        
        self.db.commit()
        self.db.refresh(profile)
        return profile
    
    async def create_bazi_reading(self, customer_id: str, request: BaziAnalysisRequest) -> AnalysisResultResponse:
        """创建八字命理分析记录"""
        # 获取或创建档案
        profile = self.get_or_create_profile(customer_id, request)
        
        # 调用ChatGPT进行分析
        analysis = await self.chatgpt.analyze_bazi(request)
        
        # 创建算命记录
        reading = FortuneReading(
            customer_id=customer_id,
            profile_id=profile.id,
            reading_type=ReadingType.BAZI,
            question_type="general",  # 八字分析默认为general类型
            input_data=request.dict(),
            ai_analysis=analysis
        )
        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)
        
        return AnalysisResultResponse(
            reading_id=str(reading.id),
            analysis=analysis,
            summary=analysis[:200] + "...",
            recommendations=[],  # 可以从分析中提取关键建议
            recommended_products=None,  # 后续实现商品推荐
            created_at=reading.created_at
        )
    
    async def create_tarot_reading(self, customer_id: str, request: TarotAnalysisRequest) -> AnalysisResultResponse:
        """创建塔罗牌分析记录"""
        # 调用ChatGPT进行分析
        analysis = await self.chatgpt.analyze_tarot(request)
        
        # 创建算命记录
        reading = FortuneReading(
            customer_id=customer_id,
            reading_type=ReadingType.TAROT,
            question_type=request.question_type,  # 塔罗使用用户指定的问题类型
            input_data=request.dict(),
            ai_analysis=analysis
        )
        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)
        
        return AnalysisResultResponse(
            reading_id=str(reading.id),
            analysis=analysis,
            summary=analysis[:200] + "...",
            recommendations=[],
            recommended_products=None,
            created_at=reading.created_at
        )
    
    def get_reading_history(self, customer_id: str, limit: int = 20) -> List[FortuneReading]:
        """获取用户算命历史记录"""
        return self.db.query(FortuneReading).filter(
            FortuneReading.customer_id == customer_id
        ).order_by(desc(FortuneReading.created_at)).limit(limit).all()
    
    def get_reading_by_id(self, reading_id: str, customer_id: str) -> Optional[FortuneReading]:
        """根据ID获取算命记录"""
        return self.db.query(FortuneReading).filter(
            FortuneReading.id == reading_id,
            FortuneReading.customer_id == customer_id
        ).first()