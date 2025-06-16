from typing import Dict, Any, Optional
import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.customer.models import EmailVerificationCode, Customer
from app.core.config import settings


class EmailVerificationService:
    """邮箱验证码服务类"""
    
    @staticmethod
    def generate_verification_code() -> str:
        """生成6位数字验证码"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_verification_code(
        db: Session,
        email: str,
        purpose: str = "register",
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        发送邮箱验证码
        
        Args:
            db: 数据库会话
            email: 邮箱地址
            purpose: 验证码用途 (register, login, reset_password)
            ip_address: 请求IP地址
            user_agent: 用户代理
        """
        # 检查是否存在有效的验证码（5分钟内）
        recent_code = db.query(EmailVerificationCode).filter(
            EmailVerificationCode.email == email,
            EmailVerificationCode.purpose == purpose,
            EmailVerificationCode.is_used == False,
            EmailVerificationCode.expires_at > datetime.utcnow(),
            EmailVerificationCode.created_at > datetime.utcnow() - timedelta(minutes=1)  # 1分钟内不能重复发送
        ).first()
        
        if recent_code:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="验证码发送过于频繁，请稍后再试"
            )
        
        # 处理注册场景 - 自动创建用户并生成随机密码
        random_password = None
        if purpose == "register":
            existing_customer = db.query(Customer).filter(Customer.email == email).first()
            if existing_customer:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该邮箱已注册，请直接登录或使用其他邮箱"
                )
            
            # 自动创建客户并生成随机密码
            from app.customer.service import CustomerService
            from app.customer.schema import CustomerCreate
            from app.customer.models import RegistrationSource
            
            random_password = CustomerService._generate_random_password()
            
            # 创建客户数据
            customer_data = CustomerCreate(
                email=email,
                password=random_password,
                registration_source=RegistrationSource.WEBSITE
            )
            
            # 创建客户
            customer = CustomerService.create_customer(db=db, customer_data=customer_data)
            
            # 标记为已验证（因为我们会发送邮件）
            customer.is_verified = True
            db.commit()
        
        # 检查邮箱是否存在（针对登录和重置密码场景）
        elif purpose in ["login", "reset_password"]:
            existing_customer = db.query(Customer).filter(Customer.email == email).first()
            if not existing_customer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="该邮箱尚未注册，请先注册账号"
                )
        
        # 生成验证码
        verification_code = EmailVerificationService.generate_verification_code()
        
        # 计算过期时间（10分钟）
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        # 保存验证码到数据库
        db_code = EmailVerificationCode(
            email=email,
            verification_code=verification_code,
            purpose=purpose,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(db_code)
        db.commit()
        
        # 发送邮件
        try:
            # 使用内部邮件发送方法，可以传递额外信息
            EmailVerificationService._send_email(email, verification_code, purpose, random_password)
        except Exception as e:
            # 如果发送邮件失败，删除验证码记录
            db.delete(db_code)
            # 如果是注册时创建的用户，也要删除
            if purpose == "register" and random_password:
                created_customer = db.query(Customer).filter(Customer.email == email).first()
                if created_customer:
                    db.delete(created_customer)
            db.commit()
            print(f"邮件发送失败，详细错误: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="邮件发送失败，请稍后重试"
            )
        
        return {
            "message": "验证码已发送",
            "expires_in": 600,  # 10分钟，单位秒
            "email": email
        }
    
    @staticmethod
    def verify_code(
        db: Session,
        email: str,
        verification_code: str,
        purpose: str = "register",
        auto_mark_used: bool = True
    ) -> Dict[str, Any]:
        """
        验证邮箱验证码
        
        Args:
            db: 数据库会话
            email: 邮箱地址
            verification_code: 验证码
            purpose: 验证码用途
            auto_mark_used: 是否自动标记为已使用
        """
        # 查找有效的验证码
        db_code = db.query(EmailVerificationCode).filter(
            EmailVerificationCode.email == email,
            EmailVerificationCode.purpose == purpose,
            EmailVerificationCode.is_used == False,
            EmailVerificationCode.expires_at > datetime.utcnow()
        ).order_by(EmailVerificationCode.created_at.desc()).first()
        
        if not db_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码不存在或已过期，请重新获取"
            )
        
        # 增加尝试次数
        db_code.attempts += 1
        
        # 检查尝试次数（最多5次）
        if db_code.attempts > 5:
            db_code.is_used = True
            db_code.used_at = datetime.utcnow()
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码尝试次数过多，已失效，请重新获取"
            )
        
        # 验证验证码
        if db_code.verification_code != verification_code:
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误，请重新输入"
            )
        
        # 标记为已使用
        if auto_mark_used:
            db_code.is_used = True
            db_code.used_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message": "验证码验证成功",
            "email": email,
            "verified": True
        }
    
    @staticmethod
    def _send_email(email: str, verification_code: str, purpose: str, random_password: Optional[str] = None) -> None:
        """
        发送验证码邮件
        
        Args:
            email: 收件人邮箱
            verification_code: 验证码
            purpose: 验证码用途
            random_password: 随机生成的密码（仅注册时使用）
        """
        # 根据用途设置邮件标题和内容
        purpose_texts = {
            "register": ("注册验证", "欢迎注册我们的网站"),
            "login": ("登录验证", "您正在登录我们的网站"),
            "reset_password": ("重置密码", "您正在重置密码")
        }
        
        title, desc = purpose_texts.get(purpose, ("验证码", "验证您的邮箱"))
        
        # 构建邮件内容
        subject = f"【{settings.PROJECT_NAME}】{title}验证码"
        
        # 构建密码部分内容
        password_section = ""
        if purpose == "register" and random_password:
            password_section = f"""
                <div style="background-color: #e8f5e8; border: 1px solid #4CAF50; border-radius: 5px; padding: 20px; margin: 20px 0;">
                    <h3 style="color: #2c5aa0; margin-top: 0;">您的账户已创建成功！</h3>
                    <p>您的登录密码是：</p>
                    <div style="background-color: #ffffff; padding: 15px; text-align: center; border-radius: 3px; margin: 10px 0;">
                        <span style="font-size: 20px; font-weight: bold; color: #d32f2f; font-family: 'Courier New', monospace;">{random_password}</span>
                    </div>
                    <p style="margin-bottom: 0;"><strong>现在您可以使用以下两种方式登录：</strong></p>
                    <ul style="margin: 10px 0;">
                        <li>使用验证码快速登录</li>
                        <li>使用邮箱 + 密码登录</li>
                    </ul>
                    <p style="color: #666; font-size: 14px; margin-bottom: 0;">
                        建议您登录后在个人设置中修改为自己喜欢的密码。
                    </p>
                </div>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}验证码</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c5aa0;">{desc}</h2>
                <p>您的验证码是：</p>
                <div style="background-color: #f4f4f4; padding: 20px; text-align: center; margin: 20px 0;">
                    <span style="font-size: 32px; font-weight: bold; color: #2c5aa0; letter-spacing: 8px;">{verification_code}</span>
                </div>
                {password_section}
                <p><strong>注意：</strong></p>
                <ul>
                    <li>验证码有效期为10分钟</li>
                    <li>请勿将验证码和密码告诉他人</li>
                    <li>如非本人操作，请忽略此邮件</li>
                </ul>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    这是一封系统自动发送的邮件，请勿回复。<br>
                    如有疑问，请联系客服。
                </p>
            </div>
        </body>
        </html>
        """
        
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.SMTP_USER
        msg['To'] = email
        
        # 添加HTML内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 发送邮件 - 使用163邮箱SSL连接
        try:
            # 使用context管理器处理SSL，设置更宽松的SSL选项
            import ssl
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
                server.set_debuglevel(0)  # 设置为1可以显示详细调试信息
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
                print(f"邮件发送成功: {email}")
        except Exception as e:
            print(f"邮件发送失败: {e}")
            # 尝试使用STARTTLS方式
            try:
                import ssl
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                with smtplib.SMTP(settings.SMTP_HOST, 25) as server:
                    server.starttls(context=context)
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)
                    print(f"邮件发送成功 (STARTTLS): {email}")
            except Exception as e2:
                print(f"STARTTLS方式也失败: {e2}")
                raise e
    
    @staticmethod
    def cleanup_expired_codes(db: Session) -> int:
        """
        清理过期的验证码
        
        Returns:
            int: 清理的记录数
        """
        expired_codes = db.query(EmailVerificationCode).filter(
            EmailVerificationCode.expires_at < datetime.utcnow()
        )
        count = expired_codes.count()
        expired_codes.delete()
        db.commit()
        return count 