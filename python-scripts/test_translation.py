# -*- coding: utf-8 -*-
"""
测试阿里云百炼翻译功能的脚本

使用方法：
python python-scripts/test_translation.py
"""

import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.analytics.ai_copilot.alibaba_service import AlibabaBailianService


async def test_translation():
    """测试翻译功能"""
    service = AlibabaBailianService()
    
    # 测试文本（基于用户提供的真实数据）
    test_texts = {
        "name": "珠宝首饰",
        "description": "各种精美的珠宝首饰，包括项链、手链、戒指、耳环等，采用天然宝石和贵金属制作，寓意美好，适合各种场合佩戴。",
        "seo_title": "珠宝首饰 - 天然宝石饰品 - 精美手工制作",
        "seo_description": "精选珠宝首饰，天然宝石，手工制作，品质保证。包括项链、手链、戒指、耳环等多种款式，寓意吉祥，是送礼自用的理想选择。",
        "seo_keywords": "珠宝, 首饰, 项链, 手链, 戒指, 耳环, 天然宝石, 手工制作"
    }
    
    target_languages = ["en-US", "th-TH"]
    
    print("=" * 60)
    print("阿里云百炼翻译功能测试")
    print("=" * 60)
    
    for target_lang in target_languages:
        print(f"\n翻译到 {target_lang}:")
        print("-" * 40)
        
        for field_name, text in test_texts.items():
            try:
                print(f"\n测试字段: {field_name}")
                print(f"原文: {text}")
                
                result = await service.translate_text(
                    source_text=text,
                    target_language=target_lang,
                    source_language="zh-CN",
                    context="这是电商平台商品分类的翻译测试"
                )
                
                if result["success"]:
                    print(f"译文: {result['translated_text']}")
                    print("✅ 翻译成功")
                else:
                    print(f"❌ 翻译失败: {result.get('error')}")
                    
            except Exception as e:
                print(f"❌ 翻译异常: {str(e)}")
            
            print("-" * 40)
            
            # 添加延迟避免API频率限制
            await asyncio.sleep(1)
    
    print("\n测试完成!")


async def main():
    """主函数"""
    try:
        await test_translation()
    except KeyboardInterrupt:
        print("\n用户中断执行")
    except Exception as e:
        print(f"测试失败: {str(e)}")


if __name__ == "__main__":
    # 设置事件循环策略（Windows环境）
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # 运行异步主函数
    asyncio.run(main())