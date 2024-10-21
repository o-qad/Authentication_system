from datetime import date
from pydantic import BaseModel, EmailStr

class RegisterUserSchema(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    password: str

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    otp_code: str
