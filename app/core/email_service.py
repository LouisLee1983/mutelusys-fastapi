"""
改进的邮件发送服务
支持多种邮件服务器配置和SSL处理
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.core.config import settings


class EmailService:
    """邮件发送服务类"""
    
    @staticmethod
    def create_ssl_context(verify_cert: bool = False) -> ssl.SSLContext:
        """创建SSL上下文"""
        context = ssl.create_default_context()
        if not verify_cert:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        return context
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> bool:
        """
        发送邮件的主方法
        
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            html_content: HTML内容
            text_content: 纯文本内容（可选）
            from_email: 发件人邮箱（可选，默认使用配置）
            from_name: 发件人名称（可选）
        
        Returns:
            bool: 发送是否成功
        """
        try:
            # 构建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['To'] = to_email
            
            # 设置From字段（避免重复设置）
            if from_name:
                msg['From'] = f"{from_name} <{from_email or settings.SMTP_USER}>"
            else:
                msg['From'] = from_email or settings.SMTP_USER
            
            # 添加纯文本内容
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)
            
            # 添加HTML内容
            if html_content:
                html_part = MIMEText(html_content, 'html', 'utf-8')
                msg.attach(html_part)
            
            # 尝试不同的发送方式
            success = False
            last_error = None
            
            # 方式1: SMTP_SSL (推荐用于163邮箱)
            if settings.SMTP_SSL and not success:
                try:
                    success = EmailService._send_via_smtp_ssl(msg)
                    if success:
                        print(f"邮件发送成功 (SMTP_SSL): {to_email}")
                        return True
                except Exception as e:
                    last_error = e
                    print(f"SMTP_SSL方式失败: {e}")
            
            # 方式2: STARTTLS
            if settings.SMTP_TLS and not success:
                try:
                    success = EmailService._send_via_starttls(msg)
                    if success:
                        print(f"邮件发送成功 (STARTTLS): {to_email}")
                        return True
                except Exception as e:
                    last_error = e
                    print(f"STARTTLS方式失败: {e}")
            
            # 方式3: 普通SMTP (最后尝试)
            if not success:
                try:
                    success = EmailService._send_via_smtp(msg)
                    if success:
                        print(f"邮件发送成功 (SMTP): {to_email}")
                        return True
                except Exception as e:
                    last_error = e
                    print(f"普通SMTP方式失败: {e}")
            
            if not success and last_error:
                raise last_error
                
            return success
            
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False
    
    @staticmethod
    def _send_via_smtp_ssl(msg: MIMEMultipart) -> bool:
        """通过SMTP_SSL发送邮件"""
        if settings.SMTP_USE_SSL_CONTEXT:
            context = EmailService.create_ssl_context(verify_cert=False)
            with smtplib.SMTP_SSL(
                settings.SMTP_HOST, 
                settings.SMTP_PORT, 
                context=context,
                timeout=settings.SMTP_TIMEOUT
            ) as server:
                if settings.SMTP_DEBUG:
                    server.set_debuglevel(1)
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(
                settings.SMTP_HOST, 
                settings.SMTP_PORT,
                timeout=settings.SMTP_TIMEOUT
            ) as server:
                if settings.SMTP_DEBUG:
                    server.set_debuglevel(1)
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        return True
    
    @staticmethod
    def _send_via_starttls(msg: MIMEMultipart) -> bool:
        """通过STARTTLS发送邮件"""
        # 尝试不同的端口
        ports_to_try = [587, 25, 2525]
        
        for port in ports_to_try:
            try:
                context = EmailService.create_ssl_context(verify_cert=False)
                with smtplib.SMTP(
                    settings.SMTP_HOST, 
                    port,
                    timeout=settings.SMTP_TIMEOUT
                ) as server:
                    if settings.SMTP_DEBUG:
                        server.set_debuglevel(1)
                    server.starttls(context=context)
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)
                    return True
            except Exception as e:
                print(f"端口 {port} 尝试失败: {e}")
                continue
        return False
    
    @staticmethod
    def _send_via_smtp(msg: MIMEMultipart) -> bool:
        """通过普通SMTP发送邮件"""
        # 尝试不同的端口
        ports_to_try = [25, 587, 2525]
        
        for port in ports_to_try:
            try:
                with smtplib.SMTP(
                    settings.SMTP_HOST, 
                    port,
                    timeout=settings.SMTP_TIMEOUT
                ) as server:
                    if settings.SMTP_DEBUG:
                        server.set_debuglevel(1)
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)
                    return True
            except Exception as e:
                print(f"普通SMTP端口 {port} 尝试失败: {e}")
                continue
        return False
    
    @staticmethod
    def send_verification_code_email(
        email: str, 
        verification_code: str, 
        purpose: str = "register"
    ) -> bool:
        """
        发送验证码邮件
        
        Args:
            email: 收件人邮箱
            verification_code: 验证码
            purpose: 验证码用途
        
        Returns:
            bool: 发送是否成功
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
                <p><strong>注意：</strong></p>
                <ul>
                    <li>验证码有效期为10分钟</li>
                    <li>请勿将验证码告诉他人</li>
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
        
        # 纯文本版本
        text_content = f"""
        {desc}
        
        您的验证码是：{verification_code}
        
        注意：
        - 验证码有效期为10分钟
        - 请勿将验证码告诉他人
        - 如非本人操作，请忽略此邮件
        
        这是一封系统自动发送的邮件，请勿回复。
        如有疑问，请联系客服。
        """
        
        return EmailService.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            from_name=settings.PROJECT_NAME
        ) 