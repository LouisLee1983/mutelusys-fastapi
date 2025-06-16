# -*- coding: utf-8 -*-
"""
DeepSeek翻译服务
提供基于DeepSeek AI的商品信息自动翻译功能
"""
try:
    # 尝试新版本的openai导入方式
    from openai import OpenAI
    NEW_OPENAI = True
except ImportError:
    # 回退到旧版本
    import openai
    NEW_OPENAI = False

import json
from typing import Dict, Any, Optional
from fastapi import HTTPException
import logging

# 配置日志
logger = logging.getLogger(__name__)

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-57cc0b100c2f46029a01a8f3f9aa09c5"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# 语言映射
LANGUAGE_MAPPING = {
    "zh-cn": "简体中文",
    "zh-tw": "繁体中文", 
    "en-us": "英语",
    "en-gb": "英语",
    "ja-jp": "日语",
    "ko-kr": "韩语",
    "ms-my": "马来语",
    "th-th": "泰语",
    "vi-vn": "越南语",
    "id-id": "印尼语",
    "tl-ph": "菲律宾语",
    "es-es": "西班牙语",
    "fr-fr": "法语",
    "de-de": "德语",
    "it-it": "意大利语",
    "pt-pt": "葡萄牙语",
    "ru-ru": "俄语",
    "ar-sa": "阿拉伯语",
    "hi-in": "印地语",
    "ta-in": "泰米尔语"
}

class DeepSeekTranslationService:
    """DeepSeek翻译服务类"""
    
    def __init__(self):
        """初始化DeepSeek客户端"""
        if NEW_OPENAI:
            self.client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_BASE_URL
            )
        else:
            openai.api_key = DEEPSEEK_API_KEY
            openai.api_base = DEEPSEEK_BASE_URL
            self.client = None
    
    def get_language_name(self, language_code: str) -> str:
        """获取语言名称（大小写不敏感）"""
        # 转换为小写进行匹配
        code_lower = language_code.lower()
        
        # 扩展的语言映射，包含更多变体
        extended_mapping = {
            "zh-cn": "简体中文",
            "zh-tw": "繁体中文", 
            "en": "英语",
            "en-us": "英语",
            "en-gb": "英语",
            "ja": "日语",
            "ja-jp": "日语",
            "ko": "韩语",
            "ko-kr": "韩语",
            "ms-my": "马来语",
            "th": "泰语",
            "th-th": "泰语",
            "vi": "越南语",
            "vi-vn": "越南语",
            "id-id": "印尼语",
            "tl-ph": "菲律宾语",
            "es": "西班牙语",
            "es-es": "西班牙语",
            "fr": "法语",
            "fr-fr": "法语",
            "de": "德语",
            "de-de": "德语",
            "it": "意大利语",
            "it-it": "意大利语",
            "pt": "葡萄牙语",
            "pt-pt": "葡萄牙语",
            "ru": "俄语",
            "ru-ru": "俄语",
            "ar": "阿拉伯语",
            "ar-sa": "阿拉伯语",
            "hi-in": "印地语",
            "ta-in": "泰米尔语"
        }
        
        return extended_mapping.get(code_lower, language_code)
    
    def create_translation_prompt(self, source_data: Dict[str, Any], target_language: str) -> str:
        """创建翻译提示词"""
        language_name = self.get_language_name(target_language)
        
        prompt = f"""
请将以下商品信息翻译成{language_name}，保持专业性和准确性。请严格按照JSON格式返回翻译结果：

原始商品信息（中文）：
- 商品名称：{source_data.get('name', '')}
- 简短描述：{source_data.get('short_description', '')}
- 详细描述：{source_data.get('description', '')}
- 商品规格：{source_data.get('specifications', '')}
- 商品优势：{source_data.get('benefits', '')}
- 使用说明：{source_data.get('instructions', '')}

SEO信息：
- SEO标题：{source_data.get('seo_title', '')}
- SEO描述：{source_data.get('seo_description', '')}
- SEO关键词：{source_data.get('seo_keywords', '')}

请翻译成{language_name}，并以以下JSON格式返回（只返回JSON，不要其他内容）：
{{
    "name": "翻译后的商品名称",
    "short_description": "翻译后的简短描述",
    "description": "翻译后的详细描述", 
    "specifications": "翻译后的商品规格",
    "benefits": "翻译后的商品优势",
    "instructions": "翻译后的使用说明",
    "seo_title": "翻译后的SEO标题",
    "seo_description": "翻译后的SEO描述",
    "seo_keywords": "翻译后的SEO关键词"
}}

注意：
1. 保持原有的格式和结构
2. 确保翻译的专业性和准确性
3. SEO关键词用逗号分隔
4. 如果原文为空，翻译结果也应为空字符串
5. 确保返回的是有效的JSON格式
"""
        return prompt

    async def translate_product_info(
        self, 
        source_data: Dict[str, Any], 
        target_language: str
    ) -> Dict[str, Any]:
        """
        使用DeepSeek翻译商品信息
        
        Args:
            source_data: 源语言商品信息
            target_language: 目标语言代码
            
        Returns:
            翻译后的商品信息字典
        """
        try:
            # 创建翻译提示词
            prompt = self.create_translation_prompt(source_data, target_language)
            
            # 调用DeepSeek API (兼容新旧版本)
            if NEW_OPENAI and self.client:
                # 新版本API调用
                response = self.client.chat.completions.create(
                    model="deepseek-chat",  # DeepSeek的聊天模型
                    messages=[
                        {
                            "role": "system", 
                            "content": "你是一个专业的商品信息翻译专家，擅长将商品信息准确翻译成各种语言，保持商业性和吸引力。请严格按照JSON格式返回翻译结果。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,  # 较低的温度确保翻译准确性
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                translated_content = response.choices[0].message.content.strip()
            else:
                # 旧版本API调用
                response = openai.ChatCompletion.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system", 
                            "content": "你是一个专业的商品信息翻译专家，擅长将商品信息准确翻译成各种语言，保持商业性和吸引力。请严格按照JSON格式返回翻译结果。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,  # 较低的温度确保翻译准确性
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                translated_content = response.choices[0].message.content.strip()
            
            # 尝试解析JSON
            try:
                # 移除可能的代码块标记
                if translated_content.startswith('```json'):
                    translated_content = translated_content[7:]
                if translated_content.endswith('```'):
                    translated_content = translated_content[:-3]
                
                translated_data = json.loads(translated_content)
                
                # 验证返回的数据结构
                required_fields = ['name', 'short_description', 'description', 'specifications', 'benefits', 'instructions', 'seo_title', 'seo_description', 'seo_keywords']
                for field in required_fields:
                    if field not in translated_data:
                        translated_data[field] = ""
                
                return translated_data
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {e}, 内容: {translated_content}")
                raise HTTPException(status_code=500, detail="翻译结果格式解析失败")
                
        except Exception as e:
            if "openai" in str(type(e)).lower() or "api" in str(e).lower():
                logger.error(f"DeepSeek API调用失败: {e}")
                raise HTTPException(status_code=500, detail=f"翻译服务调用失败: {str(e)}")
            else:
                logger.error(f"翻译过程中发生未知错误: {e}")
                raise HTTPException(status_code=500, detail=f"翻译失败: {str(e)}")

    async def batch_translate_product_info(
        self,
        source_data: Dict[str, Any],
        target_languages: list
    ) -> Dict[str, Dict[str, Any]]:
        """
        批量翻译商品信息到多种语言
        
        Args:
            source_data: 源语言商品信息
            target_languages: 目标语言列表
            
        Returns:
            包含所有翻译结果的字典，键为语言代码
        """
        results = {}
        failed_languages = []
        
        for language_code in target_languages:
            try:
                translated_data = await self.translate_product_info(source_data, language_code)
                results[language_code] = translated_data
            except Exception as e:
                logger.error(f"翻译到 {language_code} 失败: {e}")
                failed_languages.append(language_code)
                
        if failed_languages:
            logger.warning(f"以下语言翻译失败: {failed_languages}")
            
        return results

    async def translate_policy_content(
        self,
        content: str,
        source_language: str,
        target_language: str,
        policy_type: str
    ) -> str:
        """
        使用DeepSeek翻译政策文档内容
        
        Args:
            content: 原始文档内容（Markdown格式）
            source_language: 源语言代码
            target_language: 目标语言代码
            policy_type: 政策类型（shipping/refund/about）
            
        Returns:
            翻译后的文档内容
        """
        try:
            # 记录输入参数
            logger.info(f"开始翻译政策文档: type={policy_type}, source={source_language}, target={target_language}")
            
            source_lang_name = self.get_language_name(source_language)
            target_lang_name = self.get_language_name(target_language)
            
            logger.info(f"语言名称映射: {source_language} -> {source_lang_name}, {target_language} -> {target_lang_name}")
            
            # 根据政策类型创建更精准的系统提示
            policy_context = {
                "shipping": "运输政策和物流相关",
                "refund": "退款退货政策",
                "about": "公司介绍和品牌故事"
            }
            
            context_desc = policy_context.get(policy_type, "政策文档")
            
            prompt = f"""
请将以下{context_desc}内容从{source_lang_name}翻译成{target_lang_name}。

要求：
1. 保持原有的Markdown格式
2. 保持专业性和准确性
3. 保留所有的格式标记（如#、##、###、-、*等）
4. 保留所有的表格格式
5. 邮箱地址、网址、数字等不需要翻译
6. 品牌名称MUTELU保持不变
7. 对于专业术语，使用目标语言中最常用的表达方式

原始内容：
{content}

请直接返回翻译后的内容，不要包含任何额外的说明。
"""
            
            # 调用DeepSeek API
            if NEW_OPENAI and self.client:
                logger.info("使用新版OpenAI客户端调用DeepSeek API")
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": f"你是一个专业的{context_desc}翻译专家，擅长将文档准确翻译成各种语言，保持格式和专业性。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=4000,  # 政策文档可能比较长
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                translated_content = response.choices[0].message.content.strip()
            else:
                logger.info("使用旧版OpenAI API调用DeepSeek")
                response = openai.ChatCompletion.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": f"你是一个专业的{context_desc}翻译专家，擅长将文档准确翻译成各种语言，保持格式和专业性。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=4000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                translated_content = response.choices[0].message.content.strip()
            
            logger.info(f"翻译成功，返回内容长度: {len(translated_content)}")
            return translated_content
            
        except Exception as e:
            logger.error(f"政策文档翻译失败: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"翻译失败: {str(e)}")

# 创建全局翻译服务实例
deepseek_translation_service = DeepSeekTranslationService() 