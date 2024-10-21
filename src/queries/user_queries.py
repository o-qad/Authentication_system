from sqlalchemy.orm import Session
from src.models.model import User

def save_user(db: Session, user_data, hashed_password, is_active):
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        date_of_birth=user_data.date_of_birth,
        email=user_data.email,
        password=hashed_password,
        is_active=is_active
    )
    db.add(new_user)
    db.commit()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user_password(db: Session, email: str, new_password: str):
    user = get_user_by_email(db, email)
    user.password = new_password
    db.commit()

def delete_user_by_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    db.delete(user)
    db.commit()
