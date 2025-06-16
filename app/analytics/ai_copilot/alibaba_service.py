# -*- coding: utf-8 -*-
"""
阿里云百炼平台服务类
"""
import json
import time
import asyncio
import base64
import os
from typing import List, Dict, Any, Optional
import aiohttp
from datetime import datetime

from app.core.config import settings


class AlibabaBailianService:
    """阿里云百炼平台服务类"""
    
    def __init__(self):
        self.api_key = "sk-7be51a35e4ea4ee9bc3e0d2584e0a33a"
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        self.vision_model = "qwen-vl-max"  # 图像分析模型
        self.text_model = "qwen-plus"  # 文本翻译模型
    
    async def translate_text(
        self,
        source_text: str,
        target_language: str,
        source_language: str = "zh-CN",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        翻译文本到目标语言
        
        Args:
            source_text: 需要翻译的源文本
            target_language: 目标语言代码 (如 en-US, th-TH)
            source_language: 源语言代码 (默认 zh-CN)
            context: 翻译上下文，帮助提供更准确的翻译
        
        Returns:
            翻译结果字典
        """
        try:
            # 构建翻译提示词
            content = self._build_translation_prompt(
                source_text, target_language, source_language, context
            )
            
            # 调用阿里云API
            response = await self._call_translation_api(content)
            
            # 解析翻译结果
            translated_text = self._parse_translation_response(response)
            
            return {
                "success": True,
                "original_text": source_text,
                "translated_text": translated_text,
                "source_language": source_language,
                "target_language": target_language,
                "model_name": self.text_model,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),  
                "original_text": source_text,
                "source_language": source_language,
                "target_language": target_language,
                "model_name": self.text_model,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _build_translation_prompt(
        self,
        source_text: str,
        target_language: str,
        source_language: str,
        context: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """构建翻译提示词"""
        
        language_names = {
            "zh-CN": "中文",
            "en-US": "英文",
            "th-TH": "泰文"
        }
        
        source_lang_name = language_names.get(source_language, source_language)
        target_lang_name = language_names.get(target_language, target_language)
        
        system_prompt = f"""你是一个专业的翻译专家，擅长{source_lang_name}到{target_lang_name}的翻译。

翻译要求：
1. 准确传达原文的含义和语调
2. 保持自然流畅的{target_lang_name}表达
3. 考虑文化背景和语言习惯
4. 对于专业术语要准确翻译
5. 保持原文的情感色彩和语言风格

请直接返回翻译结果，不要包含解释或其他内容。"""

        if context:
            system_prompt += f"\n\n翻译上下文：{context}"

        user_prompt = f"请将以下{source_lang_name}文本翻译成{target_lang_name}：\n\n{source_text}"

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    async def _call_translation_api(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """调用阿里云百炼翻译API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 使用阿里云百炼的标准格式
        payload = {
            "model": self.text_model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message",
                "temperature": 0.1,  # 翻译任务使用较低的温度以获得更稳定结果
                "top_p": 0.8,
                "max_tokens": 2000,
                "enable_search": False,
                "incremental_output": False
            }
        }
        
        # 使用正确的阿里云百炼文本生成API端点
        api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"API调用失败: {response.status}, {error_text}")
    
    def _parse_translation_response(self, response: Dict[str, Any]) -> str:
        """解析翻译API响应"""
        try:
            # 检查响应状态
            if response.get("code"):
                raise Exception(f"API返回错误: {response.get('message', '未知错误')}")
            
            # 提取输出内容（阿里云百炼格式）
            output = response.get("output", {})
            
            # 处理文本生成的响应格式
            if "text" in output:
                return output["text"].strip()
            elif "choices" in output and len(output["choices"]) > 0:
                choice = output["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"].strip()
            
            raise Exception(f"响应格式不正确: {response}")
            
        except Exception as e:
            raise Exception(f"解析翻译结果失败: {str(e)}")

    async def analyze_product_images(
        self, 
        image_urls: List[str], 
        additional_context: Optional[str] = None,
        language: str = "zh-CN"
    ) -> Dict[str, Any]:
        """
        分析商品图片并提取商品信息
        
        Args:
            image_urls: 图片URL列表（可以是本地路径或完整URL）
            additional_context: 额外上下文信息
            language: 分析语言
        
        Returns:
            分析结果字典
        """
        try:
            # 处理图片数据（转换为base64）
            image_data_list = await self._process_images(image_urls)
            
            # 构建消息内容
            content = self._build_analysis_prompt(image_data_list, additional_context, language)
            
            # 调用阿里云API
            response = await self._call_api(content)
            
            # 解析响应结果
            parsed_result = self._parse_analysis_response(response)
            
            return {
                "success": True,
                "raw_response": response,
                "parsed_result": parsed_result,
                "model_name": self.vision_model,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_name": self.vision_model,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _process_images(self, image_urls: List[str]) -> List[str]:
        """处理图片，转换为base64格式"""
        image_data_list = []
        
        for image_url in image_urls:
            try:
                if image_url.startswith('data:image'):
                    # 已经是base64格式
                    image_data_list.append(image_url)
                elif image_url.startswith('http'):
                    # 网络图片，下载并转换
                    base64_data = await self._download_and_encode_image(image_url)
                    image_data_list.append(base64_data)
                else:
                    # 本地文件路径，读取并转换
                    base64_data = self._encode_local_image(image_url)
                    image_data_list.append(base64_data)
            except Exception as e:
                print(f"处理图片失败 {image_url}: {e}")
                continue
        
        return image_data_list
    
    def _encode_local_image(self, image_path: str) -> str:
        """将本地图片编码为base64格式，符合阿里云百炼API要求"""
        # 处理相对路径，转换为绝对路径
        full_path = None
        
        if image_path.startswith('/static/uploads/'):
            # FastAPI static目录映射：/static/uploads/ -> static/uploads/
            relative_path = image_path[1:]  # 移除开头的 '/'
            full_path = os.path.join(os.getcwd(), relative_path)
        elif image_path.startswith('static/uploads/'):
            # 直接的相对路径
            full_path = os.path.join(os.getcwd(), image_path)
        elif image_path.startswith('/uploads/'):
            # 另一种可能的路径格式
            relative_path = 'static' + image_path  # /uploads/ -> static/uploads/
            full_path = os.path.join(os.getcwd(), relative_path)
        elif os.path.isabs(image_path):
            # 绝对路径
            full_path = image_path
        else:
            # 其他情况，尝试在static/uploads目录中查找
            full_path = os.path.join(os.getcwd(), 'static', 'uploads', os.path.basename(image_path))
        
        print(f"尝试读取图片文件: {full_path}")  # 调试信息
        
        if not os.path.exists(full_path):
            # 如果文件不存在，尝试在几个可能的位置查找
            possible_paths = [
                os.path.join(os.getcwd(), 'static', 'uploads', os.path.basename(image_path)),
                os.path.join(os.getcwd(), 'static', 'uploads', 'product-images', os.path.basename(image_path)),
                os.path.join(os.getcwd(), 'uploads', os.path.basename(image_path)),
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'uploads', os.path.basename(image_path))
            ]
            
            for possible_path in possible_paths:
                normalized_path = os.path.normpath(possible_path)
                if os.path.exists(normalized_path):
                    full_path = normalized_path
                    print(f"在备选路径找到文件: {full_path}")
                    break
            else:
                raise FileNotFoundError(f"图片文件不存在: {image_path}，尝试过的路径: {[full_path] + possible_paths}")
        
        try:
            # 读取图片文件
            with open(full_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # 根据阿里云百炼API文档，检查文件大小限制（通常不超过20MB）
            max_size = 20 * 1024 * 1024  # 20MB
            if len(image_data) > max_size:
                raise Exception(f"图片文件过大: {len(image_data)} bytes，超过限制 {max_size} bytes")
            
            # 编码为base64
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            
            # 根据文件扩展名确定MIME类型
            file_extension = os.path.splitext(full_path)[1].lower()
            mime_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
                '.bmp': 'image/bmp'
            }
            mime_type = mime_type_map.get(file_extension, 'image/jpeg')
            
            print(f"成功编码图片: {full_path}, 大小: {len(image_data)} bytes, MIME: {mime_type}")
            
            # 根据阿里云百炼API文档，返回标准的data URL格式
            return f"data:{mime_type};base64,{base64_encoded}"
            
        except Exception as e:
            raise Exception(f"读取图片文件失败 {full_path}: {str(e)}")
    
    async def _download_and_encode_image(self, image_url: str) -> str:
        """下载网络图片并编码为base64格式"""
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    base64_encoded = base64.b64encode(image_data).decode('utf-8')
                    
                    # 从Content-Type获取MIME类型
                    content_type = response.headers.get('content-type', 'image/jpeg')
                    
                    return f"data:{content_type};base64,{base64_encoded}"
                else:
                    raise Exception(f"下载图片失败: {response.status}")
    
    def _build_analysis_prompt(
        self, 
        image_data_list: List[str], 
        additional_context: Optional[str] = None,
        language: str = "zh-CN"
    ) -> List[Dict[str, Any]]:
        """构建分析提示词，符合阿里云百炼API格式要求"""
        
        # 基础分析指令 - 优化为标准JSON格式，禁止Unicode转义
        base_instruction = """
你是一个专业的电商商品分析师。请仔细分析这些商品图片，并提供详细的商品信息。

CRITICAL REQUIREMENTS（重要要求）：
1. 必须返回严格的标准JSON格式
2. 所有中文字符必须使用原生UTF-8编码，绝对禁止Unicode转义（如\\u7d2b）
3. 所有属性名必须用双引号包围
4. 所有字符串值必须用双引号包围
5. 数组和对象使用标准JSON语法
6. 不要添加任何注释或额外文字
7. 不要使用markdown代码块
8. 直接返回JSON，不要任何前缀或后缀

正确示例（必须像这样）：
{
    "name": "紫水晶手链",
    "description": "精美的紫水晶手链，适合日常佩戴",
    "materials": ["紫水晶", "金属链"],
    "colors": ["紫色", "金色"],
    "sizes": ["标准尺寸"],
    "style": "简约时尚",
    "targets": ["女性", "年轻人"],
    "scenes": ["日常佩戴", "礼品"],
    "features": ["天然水晶", "精致工艺"],
    "tags": ["首饰", "手链", "水晶"],
    "categories": ["珠宝", "手链"],
    "price_min": 50,
    "price_max": 150,
    "currency": "USD",
    "confidence": 0.95
}

错误示例（绝对禁止）：
{
    "name": "\\u7d2b\\u6c34\\u6676\\u624b\\u94fe",
    "materials": ["\\u7d2b\\u6c34\\u6676", "\\u91d1\\u5c5e"]
}

严格按照以下JSON结构返回，所有中文必须是原生字符：
{
    "name": "产品名称（中文原生字符）",
    "description": "详细产品描述（中文原生字符）",
    "materials": ["材质1", "材质2"],
    "colors": ["颜色1", "颜色2"],
    "sizes": ["尺寸1", "尺寸2"],
    "style": "设计风格",
    "targets": ["目标群体1", "目标群体2"],
    "scenes": ["使用场景1", "使用场景2"],
    "features": ["特点1", "特点2"],
    "tags": ["标签1", "标签2"],
    "categories": ["分类1", "分类2"],
    "price_min": 50,
    "price_max": 150,
    "currency": "USD",
    "confidence": 0.95
}

分析要点：
1. 个性化首饰产品，重点分析材质、工艺、设计风格
2. 识别文化符号、宗教元素、民族特色
3. 分析适用场合（日常、礼品、仪式等）
4. 判断目标客户群体（年龄、性别、文化背景）
5. 评估商品的工艺复杂度和价值定位

重要提醒：
- 绝对不要使用\\u开头的Unicode转义序列
- 直接使用中文字符：紫水晶、金色、女性等
- 确保返回的JSON可以被标准JSON解析器正确解析
- 字符编码必须是UTF-8原生格式

只返回一个有效的JSON对象，不要添加任何其他内容。
        """
        
        if language == "en":
            base_instruction = """
You are a professional e-commerce product analyst. Please carefully analyze these product images and provide detailed product information.

CRITICAL REQUIREMENTS:
1. Must return strict standard JSON format
2. All property names must be enclosed in double quotes
3. All string values must be enclosed in double quotes
4. Use standard JSON syntax for arrays and objects
5. Do not add any comments or extra text
6. Do not use markdown code blocks
7. Return JSON directly without any prefix or suffix
8. Do not use Unicode escape sequences

Correct example:
{
    "name": "Crystal Bracelet",
    "description": "Beautiful crystal bracelet for daily wear",
    "materials": ["crystal", "metal chain"],
    "colors": ["purple", "gold"],
    "sizes": ["standard"],
    "style": "elegant",
    "targets": ["women", "young adults"],
    "scenes": ["daily wear", "gifts"],
    "features": ["natural crystal", "fine craftsmanship"],
    "tags": ["jewelry", "bracelet", "crystal"],
    "categories": ["jewelry", "bracelet"],
    "price_min": 50,
    "price_max": 150,
    "currency": "USD",
    "confidence": 0.95
}

Strictly follow this JSON format:
{
    "name": "Product Name",
    "description": "Detailed product description",
    "materials": ["material1", "material2"],
    "colors": ["color1", "color2"],
    "sizes": ["size1", "size2"],
    "style": "Design style",
    "targets": ["target group1", "target group2"],
    "scenes": ["usage scene1", "usage scene2"],
    "features": ["feature1", "feature2"],
    "tags": ["tag1", "tag2"],
    "categories": ["category1", "category2"],
    "price_min": 50,
    "price_max": 150,
    "currency": "USD",
    "confidence": 0.95
}

Analysis focus:
1. Personalized jewelry product, focus on materials, craftsmanship, and design style
2. Identify cultural symbols, religious elements, ethnic characteristics
3. Analyze applicable occasions (daily, gifts, ceremonies, etc.)
4. Determine target customer groups (age, gender, cultural background)
5. Evaluate craftsmanship complexity and value positioning

Important: Return only a valid JSON object, no additional content.
            """
        
        # 添加额外上下文
        if additional_context:
            base_instruction += f"\n\n额外信息：{additional_context}"
        
        # 根据阿里云百炼API文档构建消息内容
        content = [
            {
                "type": "text",
                "text": base_instruction
            }
        ]
        
        # 添加图片 - 严格按照阿里云百炼API文档格式
        for image_data in image_data_list:
            content.append({
                "type": "image",
                "image": image_data  # 已经是data:image/jpeg;base64,xxx格式
            })
        
        return [{
            "role": "user",
            "content": content
        }]
    
    async def _call_api(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """调用阿里云百炼API，严格按照官方文档格式"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # 根据文档，移除异步调用头，使用同步调用
        }
        
        # 根据阿里云百炼API文档构建请求体
        payload = {
            "model": self.vision_model,  # qwen-vl-max
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message",  # 确保返回message格式
                "temperature": 0.1,  # 降低温度以获得更稳定的结果
                "max_tokens": 2000,  # 最大输出token数
                "top_p": 0.8,
                "enable_search": False,  # 禁用搜索功能
                "incremental_output": False  # 禁用流式输出
            }
        }
        
        # 使用DashScope标准API endpoint
        api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
        
        print(f"准备调用阿里云百炼API: {api_url}")
        print(f"模型: {self.vision_model}")
        print(f"图片数量: {len(messages[0]['content']) - 1}")  # 减去text部分
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as session:
            async with session.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=120
            ) as response:
                
                print(f"API响应状态码: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"API调用成功，返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    return result
                else:
                    error_text = await response.text()
                    print(f"API调用失败: {response.status} - {error_text}")
                    raise Exception(f"API调用失败: {response.status} - {error_text}")
    
    def _parse_analysis_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析阿里云百炼API响应"""
        try:
            # 检查响应状态
            if response.get("code"):
                raise Exception(f"API返回错误: {response.get('message', '未知错误')}")
            
            # 提取输出内容
            output = response.get("output", {})
            choices = output.get("choices", [])
            
            if not choices:
                raise Exception("API响应中没有找到有效的选择项")
            
            # 获取第一个选择的内容
            first_choice = choices[0]
            message = first_choice.get("message", {})
            content_array = message.get("content", [])
            
            # 处理content数组格式
            content = ""
            if isinstance(content_array, list) and len(content_array) > 0:
                # 阿里云百炼API返回的content是数组格式
                for item in content_array:
                    if isinstance(item, dict) and "text" in item:
                        content += item["text"]
            elif isinstance(content_array, str):
                # 兼容其他可能的字符串格式
                content = content_array
            
            if not content:
                raise Exception("API响应内容为空")
            
            # 尝试解析JSON内容，优化解析策略
            try:
                json_content = ""
                
                # 策略1：检查是否包含markdown代码块
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    json_content = content[json_start:json_end].strip()
                
                # 策略2：查找大括号包围的内容
                elif "{" in content and "}" in content:
                    json_start = content.find("{")
                    json_end = content.rfind("}") + 1
                    json_content = content[json_start:json_end].strip()
                
                # 策略3：整个内容就是JSON（去除首尾空白）
                else:
                    json_content = content.strip()
                
                # 预处理：修复常见的非标准JSON格式
                if json_content:
                    # 处理缺少引号的属性名（例如：name: "value" -> "name": "value"）
                    import re
                    
                    # 修复属性名没有引号的问题
                    json_content = re.sub(r'(\s*)(\w+)(\s*:\s*)', r'\1"\2"\3', json_content)
                    
                    # 修复数组中元素没有引号的问题（仅处理简单情况）
                    json_content = re.sub(r'\[([^\]]+)\]', self._fix_array_quotes, json_content)
                
                if not json_content:
                    # 如果没有找到有效JSON，创建基础结构
                    json_content = '{"name": "' + content[:100].replace('"', '') + '", "description": "' + content.replace('"', '') + '", "confidence": 0.8}'
                
                parsed_data = json.loads(json_content)
                
                # 适应新的JSON格式，确保包含必要字段
                default_fields = {
                    "name": "未识别商品",
                    "description": content,
                    "categories": [],
                    "materials": [],
                    "colors": [],
                    "sizes": [],
                    "tags": [],
                    "scenes": [],
                    "targets": [],
                    "features": [],
                    "price_min": 0,
                    "price_max": 0,
                    "currency": "USD",
                    "confidence": 0.8
                }
                
                # 兼容旧格式字段映射
                if "product_name" in parsed_data:
                    parsed_data["name"] = parsed_data.get("product_name")
                if "usage_scenes" in parsed_data:
                    parsed_data["scenes"] = parsed_data.get("usage_scenes")
                if "target_groups" in parsed_data:
                    parsed_data["targets"] = parsed_data.get("target_groups")
                if "suggested_price_range" in parsed_data:
                    price_range = parsed_data.get("suggested_price_range", {})
                    parsed_data["price_min"] = price_range.get("min", 0)
                    parsed_data["price_max"] = price_range.get("max", 0)
                    parsed_data["currency"] = price_range.get("currency", "USD")
                
                # 合并默认字段和解析结果
                for key, default_value in default_fields.items():
                    if key not in parsed_data:
                        parsed_data[key] = default_value
                
                # 添加原始响应信息
                parsed_data["raw_content"] = content
                parsed_data["usage"] = output.get("usage", {})
                
                return parsed_data
                
            except json.JSONDecodeError as e:
                # JSON解析失败，返回基础结构
                return {
                    "product_name": "AI分析结果",
                    "description": content,
                    "categories": [],
                    "materials": [],
                    "colors": [],
                    "tags": [],
                    "confidence": 0.5,
                    "raw_content": content,
                    "parse_error": str(e)
                }
                
        except Exception as e:
            raise Exception(f"解析响应失败: {str(e)}")
    
    def _fix_array_quotes(self, match):
        """修复数组中元素缺少引号的问题"""
        array_content = match.group(1)
        
        # 分割数组元素
        elements = [elem.strip() for elem in array_content.split(',')]
        fixed_elements = []
        
        for elem in elements:
            # 如果元素没有被引号包围且不是数字，添加引号
            if not (elem.startswith('"') and elem.endswith('"')):
                try:
                    # 尝试转换为数字，如果成功则不加引号
                    float(elem)
                    fixed_elements.append(elem)
                except ValueError:
                    # 不是数字，添加引号
                    elem_clean = elem.strip('"').strip("'")  # 移除现有的引号
                    fixed_elements.append(f'"{elem_clean}"')
            else:
                fixed_elements.append(elem)
        
        return f"[{', '.join(fixed_elements)}]"
    
    def estimate_cost(self, tokens_used: int) -> float:
        """估算调用成本"""
        # 阿里云百炼qwen-vl-max模型的大概定价
        # 这里使用估算值，实际成本以阿里云账单为准
        cost_per_1k_tokens = 0.02  # 每1000个token约0.02元
        return (tokens_used / 1000) * cost_per_1k_tokens 