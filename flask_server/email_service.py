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
    smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('MAIL_PORT', 587))
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    
    if not email_user or not email_pass:
        raise Exception("Gmail credentials not configured")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient_email
    msg['Subject'] = "Verify your email - FinTrack"
    
    body = f"""
    Welcome to FinTrack, {name}!
    
    Please click the link below to verify your email address:
    {verify_link}
    
    This link is valid for 1 hour.
    
    If you didn't create this account, please ignore this email.
    
    Best regards,
    FinTrack Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email with timeout
    with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
    
    return True, "Email sent successfully"

def send_alternative_smtp(recipient_email, name, verify_link):
    """Alternative SMTP service (can be configured for SendGrid, Mailgun, etc.)"""
    # For now, just raise exception - can be implemented later
    raise Exception("Alternative SMTP not configured")
