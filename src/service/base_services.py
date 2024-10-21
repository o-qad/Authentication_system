from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controller.database.database import get_db

class BaseService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

    def rollback(self):
        self.db.rollback()
    # Helper function to send OTP via email
def send_otp_via_email(to_email: str, otp_code: str):
    smtp_server = "smtp-mail.outlook.com"
    port = 587
    sender_email = "omar.api12@hotmail.com"
    password = "omar_API123"

    message = MIMEMultipart(f"alternative")
    message["Subject"] = "OTP Code"
    message["From"] = sender_email
    message["To"] = to_email

    # Plain text content
    text_content = f"Your one-time password (OTP) for verification is: {otp_code}\nThis code is valid for 5 minutes."
    
    # HTML content with OTP code inserted
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OTP Verification</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 50px auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding: 20px;
                background-color: #4285f4;
                color: #ffffff;
                border-radius: 10px 10px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
                text-align: center;
            }}
            .otp {{
                font-size: 28px;
                font-weight: bold;
                color: #333;
                padding: 20px;
                background-color: #f1f1f1;
                display: inline-block;
                border-radius: 5px;
                letter-spacing: 2px;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 12px;
                color: #999999;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your OTP Code</h1>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>Your one-time password (OTP) for verification is:</p>
                <div class="otp">{otp_code}</div>
                <p>This code is valid for 5 minutes. Please do not share this code with anyone.</p>
            </div>
            <div class="footer">
                <p>If you didn't request this, you can safely ignore this email.</p>
                <p>Thank you for using our service!</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Attach both plain text and HTML content
    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())    
