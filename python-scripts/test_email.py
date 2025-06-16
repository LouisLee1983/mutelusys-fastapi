#!/usr/bin/env python3
"""
邮件发送测试脚本
使用方法: python test_email.py test@example.com
"""
import sys
import os

# 添加app目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.email_service import EmailService


def test_email_sending(test_email: str):
    """测试邮件发送功能"""
    print(f"开始测试发送邮件到: {test_email}")
    
    # 测试验证码邮件
    test_code = "123456"
    
    try:
        success = EmailService.send_verification_code_email(
            email=test_email,
            verification_code=test_code,
            purpose="register"
        )
        
        if success:
            print("✅ 邮件发送成功！")
            return True
        else:
            print("❌ 邮件发送失败")
            return False
            
    except Exception as e:
        print(f"❌ 邮件发送异常: {e}")
        return False


def test_ssl_connection():
    """测试SSL连接"""
    import smtplib
    import ssl
    from app.core.config import settings
    
    print("开始测试SSL连接...")
    
    try:
        # 测试1: SMTP_SSL
        print("测试SMTP_SSL连接...")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context, timeout=30) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            print("✅ SMTP_SSL连接成功")
            return True
            
    except Exception as e:
        print(f"❌ SMTP_SSL连接失败: {e}")
        
    try:
        # 测试2: STARTTLS
        print("测试STARTTLS连接...")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with smtplib.SMTP(settings.SMTP_HOST, 587, timeout=30) as server:
            server.starttls(context=context)
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            print("✅ STARTTLS连接成功")
            return True
            
    except Exception as e:
        print(f"❌ STARTTLS连接失败: {e}")
        
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python test_email.py <测试邮箱地址>")
        print("例如: python test_email.py test@example.com")
        sys.exit(1)
    
    test_email = sys.argv[1]
    
    print("=== 邮件发送测试 ===")
    print(f"测试邮箱: {test_email}")
    print()
    
    # 首先测试连接
    print("1. 测试邮件服务器连接...")
    if test_ssl_connection():
        print("邮件服务器连接正常")
        print()
        
        # 然后测试发送邮件
        print("2. 测试发送邮件...")
        if test_email_sending(test_email):
            print(f"请检查邮箱 {test_email} 是否收到验证码邮件")
        else:
            print("邮件发送失败，请检查配置")
    else:
        print("邮件服务器连接失败，请检查网络和配置") 