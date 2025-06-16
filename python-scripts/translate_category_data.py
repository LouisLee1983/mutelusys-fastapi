# -*- coding: utf-8 -*-
"""
商品分类多语言翻译数据迁移脚本

功能：
1. 读取所有现有的 zh-CN 分类翻译记录
2. 使用阿里云百炼 API 翻译成 en-US 和 th-TH
3. 创建新的翻译记录入库
4. 避免重复翻译（检查已存在的记录）
5. 记录翻译日志和错误

使用方法：
python python-scripts/translate_category_data.py
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import List, Dict, Any
import logging

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.core.config import settings
from app.db.session import SessionLocal
from app.product.models import ProductCategoryTranslation
from app.analytics.ai_copilot.alibaba_service import AlibabaBailianService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('category_translation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CategoryTranslationMigrator:
    """分类翻译数据迁移器"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.alibaba_service = AlibabaBailianService()
        self.target_languages = ["en-US", "th-TH"]
        self.source_language = "zh-CN"
        
        # 统计信息
        self.stats = {
            "total_found": 0,
            "total_processed": 0,
            "total_created": 0,
            "total_skipped": 0,
            "total_errors": 0,
            "translations_by_language": {}
        }
    
    async def run_migration(self):
        """执行迁移任务"""
        try:
            logger.info("开始分类翻译数据迁移...")
            
            # 获取所有中文分类翻译记录
            zh_translations = self.get_chinese_translations()
            self.stats["total_found"] = len(zh_translations)
            
            logger.info(f"找到 {len(zh_translations)} 个中文分类翻译记录")
            
            if not zh_translations:
                logger.warning("没有找到中文分类翻译记录，退出迁移")
                return
            
            # 为每种目标语言执行翻译
            for target_lang in self.target_languages:
                logger.info(f"开始翻译到 {target_lang}...")
                await self.translate_to_language(zh_translations, target_lang)
                logger.info(f"完成 {target_lang} 翻译")
            
            # 提交所有更改
            self.db.commit()
            
            # 输出统计结果
            self.print_statistics()
            
        except Exception as e:
            logger.error(f"迁移过程发生错误: {str(e)}")
            self.db.rollback()
            raise
        finally:
            self.db.close()
    
    def get_chinese_translations(self) -> List[ProductCategoryTranslation]:
        """获取所有中文分类翻译记录"""
        try:
            translations = (
                self.db.query(ProductCategoryTranslation)
                .filter(ProductCategoryTranslation.language_code == self.source_language)
                .all()
            )
            return translations
        except Exception as e:
            logger.error(f"获取中文翻译记录失败: {str(e)}")
            return []
    
    def check_translation_exists(self, category_id: str, language_code: str) -> bool:
        """检查翻译记录是否已存在"""
        try:
            exists = (
                self.db.query(ProductCategoryTranslation)
                .filter(
                    ProductCategoryTranslation.category_id == category_id,
                    ProductCategoryTranslation.language_code == language_code
                )
                .first()
            )
            return exists is not None
        except Exception as e:
            logger.error(f"检查翻译记录存在性失败: {str(e)}")
            return True  # 出错时假设存在，避免重复创建
    
    async def translate_to_language(self, zh_translations: List[ProductCategoryTranslation], target_language: str):
        """将中文记录翻译到指定语言"""
        self.stats["translations_by_language"][target_language] = {
            "processed": 0,
            "created": 0,
            "skipped": 0,
            "errors": 0
        }
        
        lang_stats = self.stats["translations_by_language"][target_language]
        
        for zh_translation in zh_translations:
            try:
                self.stats["total_processed"] += 1
                lang_stats["processed"] += 1
                
                # 检查是否已存在该语言的翻译
                if self.check_translation_exists(zh_translation.category_id, target_language):
                    logger.info(f"分类 {zh_translation.category_id} 的 {target_language} 翻译已存在，跳过")
                    self.stats["total_skipped"] += 1
                    lang_stats["skipped"] += 1
                    continue
                
                # 执行翻译
                logger.info(f"正在翻译分类 '{zh_translation.name}' 到 {target_language}...")
                translation_result = await zh_translation.translate_to(
                    target_language=target_language,
                    context="这是电商平台的商品分类翻译"
                )
                
                # 创建新的翻译记录
                new_translation = ProductCategoryTranslation(
                    category_id=translation_result["category_id"],
                    language_code=translation_result["language_code"],
                    name=translation_result["name"],
                    description=translation_result["description"],
                    seo_title=translation_result["seo_title"],
                    seo_description=translation_result["seo_description"],
                    seo_keywords=translation_result["seo_keywords"]
                )
                
                self.db.add(new_translation)
                
                self.stats["total_created"] += 1
                lang_stats["created"] += 1
                
                logger.info(f"成功创建 {target_language} 翻译: {translation_result['name']}")
                
                # 每处理10条记录提交一次，避免长事务
                if lang_stats["processed"] % 10 == 0:
                    self.db.commit()
                    logger.info(f"已处理 {lang_stats['processed']} 条 {target_language} 记录")
                
                # 添加延迟避免API频率限制
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"翻译分类 {zh_translation.name} 到 {target_language} 失败: {str(e)}")
                self.stats["total_errors"] += 1
                lang_stats["errors"] += 1
                
                # 回滚当前记录的更改，继续处理下一条
                self.db.rollback()
                continue
        
        # 最终提交该语言的所有更改
        try:
            self.db.commit()
            logger.info(f"{target_language} 语言翻译完成并已提交")
        except Exception as e:
            logger.error(f"提交 {target_language} 翻译失败: {str(e)}")
            self.db.rollback()
    
    def print_statistics(self):
        """输出统计信息"""
        logger.info("=" * 60)
        logger.info("翻译迁移统计结果:")
        logger.info(f"发现中文记录数: {self.stats['total_found']}")
        logger.info(f"总处理记录数: {self.stats['total_processed']}")
        logger.info(f"总创建记录数: {self.stats['total_created']}")
        logger.info(f"总跳过记录数: {self.stats['total_skipped']}")
        logger.info(f"总错误记录数: {self.stats['total_errors']}")
        
        logger.info("\n各语言详细统计:")
        for lang, stats in self.stats["translations_by_language"].items():
            logger.info(f"{lang}:")
            logger.info(f"  处理: {stats['processed']}")
            logger.info(f"  创建: {stats['created']}")
            logger.info(f"  跳过: {stats['skipped']}")
            logger.info(f"  错误: {stats['errors']}")
        
        logger.info("=" * 60)


async def main():
    """主函数"""
    try:
        logger.info("分类翻译数据迁移脚本启动")
        
        migrator = CategoryTranslationMigrator()
        await migrator.run_migration()
        
        logger.info("分类翻译数据迁移完成")
        
    except KeyboardInterrupt:
        logger.info("用户中断执行")
    except Exception as e:
        logger.error(f"脚本执行失败: {str(e)}")
        raise


if __name__ == "__main__":
    # 设置事件循环策略（Windows环境）
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # 运行异步主函数
    asyncio.run(main())