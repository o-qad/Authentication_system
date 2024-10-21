from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.queries.user_queries import save_user, get_user_by_email
from src.queries.otp_queries import  verify_otp, generate_new_otp
from src.service.auth_serves import send_otp, create_jwt_token, verify_password, hash_password
from src.controller.database.database import get_db
from src.schemas.auth_schema import RegisterUserSchema, LoginUserSchema, VerifyOTPSchema
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register")
def register_user(user_data: RegisterUserSchema, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password and create inactive user
    hashed_password = hash_password(user_data.password)
    save_user(db, user_data, hashed_password, is_active=False)

    # Generate and send OTP
    otp_code = generate_new_otp(db, user_data.email)
    send_otp(user_data.email, otp_code)
    return {"message": "User registered. Please verify OTP sent to your email"}

@router.post("/resend-otp")
def resend_otp(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user or user.is_active:
        raise HTTPException(status_code=400, detail="User not found or already active")
    
    # Generate new OTP and send
    otp_code = generate_new_otp(db, email)
    send_otp(email, otp_code)
    return {"message": "New OTP sent to your email"}

@router.post("/verify-account")
def verify_account(otp_data: VerifyOTPSchema, db: Session = Depends(get_db)):
    # Validate OTP and activate account
    if not verify_otp(db, otp_data.email, otp_data.otp_code):
        raise HTTPException(status_code=400, detail="Invalid OTP or OTP expired")

    # Activate user and generate JWT token
    user = get_user_by_email(db, otp_data.email)
    user.is_active = True
    db.commit()

    token = create_jwt_token(user.email)
    return {"token": token,"token_type": "bearer", "message":"Account successfully verified and activated."}

@router.post("/login")
def login_user(login_data: LoginUserSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account not activated")
    
    token = create_jwt_token(user.email)
    return {"token": token,"token_type": "bearer", "message": f"Welcome back, {user.first_name}! You have successfully logged in." }
