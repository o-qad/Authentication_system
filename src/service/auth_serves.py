import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError , jwt
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret_key"

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SENDER_EMAIL = "email"
SENDER_PASSWORD = "password"  # Generate this from your Gmail account

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify hashed password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_jwt_token(email: str):
    expiration = datetime.utcnow() + timedelta(minutes=15)
    token = jwt.encode({"exp": expiration, "email": email}, SECRET_KEY)
    return token

# Decode JWT token
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("email")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Send OTP via email using Gmail SMTP
def send_otp(email: str, otp_code: str):
    try:
        # Validate email
        validate_email(email)

        # Set up the MIME message
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = email
        message["Subject"] = "Your OTP Code"

        # HTML content with OTP code
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
                    <p>This code is valid for 15 minutes. Please do not share this code with anyone.</p>
                </div>
                <div class="footer">
                    <p>If you didn't request this, you can safely ignore this email.</p>
                    <p>Thank you for using our service!</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        message.attach(MIMEText(html_content, "html"))

        # Create SMTP session and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, message.as_string())

        print(f"OTP sent to {email}")
    except EmailNotValidError as e:
        print(f"Invalid email address: {e}")
        raise HTTPException(status_code=400, detail="Invalid email address")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP")
