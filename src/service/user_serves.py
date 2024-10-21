from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.queries.user_queries import get_user_by_email, update_user_password, delete_user_by_email
from src.service.auth_serves import hash_password, verify_password, decode_jwt_token

# Function to update user password
def update_password(old_password: str, new_password: str, token: str, db: Session):
    # Decode the token to get the user's email
    email = decode_jwt_token(token)

    # Get the user by email
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify old password
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Hash the new password and update it in the database
    new_hashed_password = hash_password(new_password)
    update_user_password(db, email, new_hashed_password)

    return {"message": "Password updated successfully"}

# Function to delete user account
def delete_user(full_name: str, token: str, db: Session):
    # Decode the token to get the user's email
    email = decode_jwt_token(token)

    # Get the user by email
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate full name
    if user.first_name + " " + user.last_name != full_name:
        raise HTTPException(status_code=400, detail="Full name does not match")

    # Delete the user from the database
    delete_user_by_email(db, email)

    return {"message": "Account deleted successfully"}

# Function to get user information (excluding password)
def get_user_info(token: str, db: Session):
    # Decode the token to get the user's email
    email = decode_jwt_token(token)

    # Get the user by email
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return user information excluding sensitive fields like password
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "is_active": user.is_active
    }
