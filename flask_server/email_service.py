import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def send_verification_email(recipient_email, name, verify_link):
    """
    Send verification email with multiple fallback options
    """
    try:
        # Try Gmail SMTP first
        return send_gmail_smtp(recipient_email, name, verify_link)
    except Exception as gmail_error:
        logging.warning(f"Gmail SMTP failed: {gmail_error}")
        try:
            # Fallback to alternative SMTP (if configured)
            return send_alternative_smtp(recipient_email, name, verify_link)
        except Exception as alt_error:
            logging.error(f"All email services failed: Gmail={gmail_error}, Alt={alt_error}")
            return False, f"Email services unavailable: {str(gmail_error)}"

def send_gmail_smtp(recipient_email, name, verify_link):
    """Send email via Gmail SMTP"""
    smtp_server = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    email_user = os.getenv('SMTP_EMAIL')
    email_pass = os.getenv('SMTP_PASSWORD')
    from_name = os.getenv('FROM_NAME', 'FinTrack')
    
    if not email_user or not email_pass:
        raise Exception("Gmail credentials not configured")
    
    print(f"📧 Email Config - User: {email_user}, Server: {smtp_server}:{smtp_port}")
    print(f"📧 Sending email to: {recipient_email}")
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{from_name} <{email_user}>"
    msg['To'] = recipient_email
    msg['Subject'] = f"Verify your email - {from_name}"
    
    # Plain text version
    text_body = f"""
    Welcome to FinTrack, {name}!
    
    Please click the link below to verify your email address:
    {verify_link}
    
    This link is valid for 1 hour.
    
    If you didn't create this account, please ignore this email.
    
    Best regards,
    FinTrack Team
    """
    
    # HTML version with styled verification page
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify Your Email - FinTrack</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Arial', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
        <table width="100%" cellpadding="0" cellspacing="0" style="min-height: 100vh;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                        <tr>
                            <td style="padding: 50px 40px; text-align: center;">
                                <!-- Icon -->
                                <div style="font-size: 64px; margin-bottom: 20px;">📧</div>
                                
                                <!-- Logo/Title -->
                                <h1 style="color: #7c3aed; font-size: 32px; font-weight: 800; margin: 0 0 10px 0; letter-spacing: 1px;">FinTrack</h1>
                                
                                <!-- Heading -->
                                <h2 style="color: #333; font-size: 24px; margin: 20px 0; font-weight: 600;">Verify Your Email</h2>
                                
                                <!-- Welcome Message -->
                                <p style="color: #666; font-size: 16px; line-height: 1.6; margin: 20px 0;">
                                    Registration successful! Welcome to FinTrack, <strong>{name}</strong>!
                                </p>
                                
                                <p style="color: #666; font-size: 16px; line-height: 1.6; margin: 20px 0;">
                                    Please verify your email address by clicking the button below to activate your account and start managing your finances.
                                </p>
                                
                                <!-- Verify Button -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <a href="{verify_link}" style="display: inline-block; background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%); color: white; padding: 18px 40px; border-radius: 12px; text-decoration: none; font-size: 18px; font-weight: 600; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);">
                                                Verify Email Now
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Alternative Link -->
                                <div style="background: rgba(124, 58, 237, 0.1); padding: 20px; border-radius: 8px; margin: 30px 0;">
                                    <p style="font-size: 14px; color: #666; margin: 0 0 10px 0;">
                                        Or copy and paste this link in your browser:
                                    </p>
                                    <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; font-size: 13px; word-break: break-all; color: #495057; border: 1px solid #dee2e6;">
                                        {verify_link}
                                    </div>
                                </div>
                                
                                <!-- Expiry Notice -->
                                <p style="color: #999; font-size: 14px; margin: 20px 0;">
                                    ⏰ This verification link is valid for <strong>1 hour</strong>.
                                </p>
                                
                                <!-- Already Verified Link -->
                                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                                    <p style="font-size: 14px; color: #666; margin-bottom: 10px;">
                                        Already verified?
                                    </p>
                                    <a href="{verify_link.rsplit('/', 2)[0]}/login" style="color: #7c3aed; text-decoration: underline; font-weight: 600; font-size: 14px;">
                                        Go to Login
                                    </a>
                                </div>
                                
                                <!-- Footer -->
                                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                                    <p style="color: #999; font-size: 13px; line-height: 1.5; margin: 0;">
                                        If you didn't create this account, please ignore this email.
                                    </p>
                                    <p style="color: #666; font-size: 14px; margin: 15px 0 0 0; font-weight: 600;">
                                        Best regards,<br>
                                        <span style="color: #7c3aed;">FinTrack Team</span>
                                    </p>
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    # Attach both versions
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    # Send email with timeout
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            print("📧 Connecting to SMTP server...")
            server.starttls()
            print("📧 Starting TLS...")
            server.login(email_user, email_pass)
            print("📧 Login successful...")
            server.send_message(msg)
            print("✅ Email sent successfully!")
        
        return True, "Email sent successfully"
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        raise e

def send_alternative_smtp(recipient_email, name, verify_link):
    """Alternative SMTP service using SendGrid"""
    import requests
    
    # SendGrid API (Free: 100 emails/day)
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        raise Exception("SendGrid API key not configured")
    
    from_email = os.getenv('FROM_EMAIL', 'kushalpathave53@gmail.com')
    from_name = os.getenv('FROM_NAME', 'FinTrack')
    
    print(f"📧 SendGrid Config - API Key: {sendgrid_api_key[:10]}...")
    print(f"📧 From: {from_name} <{from_email}>")
    
    # SendGrid API call
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "personalizations": [{
            "to": [{"email": recipient_email}],
            "subject": f"✅ Verify your email - {from_name}"
        }],
        "from": {"email": from_email, "name": from_name},
        "reply_to": {"email": from_email, "name": from_name},
        "categories": ["email-verification"],
        "custom_args": {
            "type": "verification",
            "app": "fintrack"
        },
        "content": [{
            "type": "text/html",
            "value": f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Verify Your Email - {from_name}</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 600;">
                            Welcome to {from_name}! 🎉
                        </h1>
                        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">
                            Hi {name}, let's verify your email address
                        </p>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 40px 30px;">
                        <p style="color: #374151; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                            Thank you for signing up! To complete your registration and start using {from_name}, please verify your email address by clicking the button below:
                        </p>
                        
                        <!-- CTA Button -->
                        <div style="text-align: center; margin: 40px 0;">
                            <a href="{verify_link}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); transition: all 0.3s ease;">
                                ✅ Verify My Email
                            </a>
                        </div>
                        
                        <!-- Alternative Link -->
                        <div style="background-color: #f9fafb; border-radius: 8px; padding: 20px; margin: 30px 0;">
                            <p style="color: #6b7280; font-size: 14px; margin: 0 0 10px 0;">
                                If the button doesn't work, copy and paste this link in your browser:
                            </p>
                            <p style="word-break: break-all; color: #3b82f6; font-size: 14px; margin: 0;">
                                {verify_link}
                            </p>
                        </div>
                        
                        <!-- Security Note -->
                        <div style="border-left: 4px solid #fbbf24; background-color: #fffbeb; padding: 16px; margin: 30px 0; border-radius: 0 8px 8px 0;">
                            <p style="color: #92400e; font-size: 14px; margin: 0; font-weight: 500;">
                                🔒 Security Note: This verification link expires in 1 hour for your security.
                            </p>
                        </div>
                        
                        <!-- Help -->
                        <p style="color: #6b7280; font-size: 14px; line-height: 1.5; margin: 30px 0 0 0;">
                            Need help? Contact our support team or visit our help center.<br>
                            This email was sent to you because you signed up for {from_name}.
                        </p>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                        <p style="color: #6b7280; font-size: 14px; margin: 0;">
                            © 2024 {from_name}. All rights reserved.
                        </p>
                        <p style="color: #9ca3af; font-size: 12px; margin: 10px 0 0 0;">
                            Financial Analytics Dashboard - Secure & Reliable
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
        }]
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 202:
        return True, "Email sent via SendGrid"
    else:
        raise Exception(f"SendGrid failed: {response.status_code} - {response.text}")
