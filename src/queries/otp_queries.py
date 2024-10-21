from sqlalchemy.orm import Session
from src.models.model import OTP
from datetime import datetime, timedelta
import random

def generate_new_otp(db: Session, email: str):
    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expiration_time = datetime.utcnow() + timedelta(minutes=15)
    
    otp = OTP(otp_code=otp_code, email=email, expiration=expiration_time)
    db.add(otp)
    db.commit()
    
    return otp_code

def verify_otp(db: Session, email: str, otp_code: str):
    otp = db.query(OTP).filter(OTP.email == email, OTP.otp_code == otp_code).first()
    
    if otp and otp.expiration > datetime.utcnow():
        return True
    return False
