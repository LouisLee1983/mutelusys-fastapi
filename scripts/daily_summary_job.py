#!/usr/bin/env python3
"""
每日数据汇总定时任务脚本
建议在每日凌晨1点运行，生成前一天的数据汇总

使用方法：
1. 直接运行: python daily_summary_job.py
2. 指定日期: python daily_summary_job.py --date 2024-01-15  
3. crontab定时任务: 0 1 * * * /path/to/python /path/to/daily_summary_job.py
"""

import sys
import os
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from app.db.session import SessionLocal
from app.analytics.daily_summary.service import DailySummaryService


def main():
    parser = argparse.ArgumentParser(description='生成每日数据汇总')
    parser.add_argument('--date', type=str, help='指定日期 (YYYY-MM-DD)，默认为昨天')
    parser.add_argument('--force', action='store_true', help='强制重新生成已存在的数据')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细输出')
    
    args = parser.parse_args()
    
    # 确定目标日期
    if args.date:
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print(f"错误：日期格式不正确，请使用 YYYY-MM-DD 格式")
            sys.exit(1)
    else:
        # 默认生成昨天的数据
        target_date = date.today() - timedelta(days=1)
    
    print(f"开始生成 {target_date} 的数据汇总...")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        service = DailySummaryService(db)
        
        # 生成数据汇总
        start_time = datetime.now()
        result = service.generate_all_daily_summaries(target_date)
        end_time = datetime.now()
        
        # 输出结果
        print(f"✅ 数据汇总生成完成！")
        print(f"📊 生成数据：")
        print(f"   - 日期：{result['date']}")
        print(f"   - 销售汇总：✓")
        print(f"   - 用户行为汇总：✓")
        print(f"   - 商品表现记录：{result['product_performances']} 条")
        print(f"⏱️  耗时：{(end_time - start_time).total_seconds():.2f} 秒")
        
        if args.verbose:
            # 显示详细信息
            sales_summary = service.db.query(service.DailySalesSummary).filter(
                service.DailySalesSummary.report_date == target_date
            ).first()
            
            if sales_summary:
                print(f"\n📈 销售数据详情：")
                print(f"   - 总订单数：{sales_summary.total_orders}")
                print(f"   - 总销售额：{sales_summary.total_revenue}")
                print(f"   - 总客户数：{sales_summary.total_customers}")
                print(f"   - 转化率：{sales_summary.conversion_rate:.4f}")
        
    except Exception as e:
        print(f"❌ 生成数据汇总时出错：{str(e)}")
        sys.exit(1)
    
    finally:
        db.close()


if __name__ == "__main__":
    main()