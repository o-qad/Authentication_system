from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.queries.user_queries import get_user_by_email, update_user_password, delete_user_by_email
from src.schemas.user_schema import ChangePasswordSchema
from src.service.auth_serves import verify_password, hash_password
from src.controller.database.database import get_db
from src.service.auth_serves import decode_jwt_token

router = APIRouter()

@router.get("/user-info")
def get_user_info(token: str, db: Session = Depends(get_db)):
    # Decode the token and fetch user info
    email = decode_jwt_token(token)
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth":user.date_of_birth,
        "password":user.password,
        "token_type": "bearer",
        "is_active":user.is_active
    }

@router.post("/change-password")
def change_password(data: ChangePasswordSchema, db: Session = Depends(get_db)):
    email = decode_jwt_token(data.token)
    user = get_user_by_email(db, email)
    
    # Verify old password and update to new password
    if not verify_password(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    new_hashed_password = hash_password(data.new_password)
    update_user_password(db, email, new_hashed_password)
    return {"message": "Password updated successfully"}

@router.delete("/delete-account")
def delete_account(full_name: str, token: str, db: Session = Depends(get_db)):
    email = decode_jwt_token(token)
    user = get_user_by_email(db, email)
    
    if not user or user.first_name + " " + user.last_name != full_name:
        raise HTTPException(status_code=400, detail="User identity mismatch")
    
    delete_user_by_email(db, email)
    return {"message": "Account deleted successfully"}
