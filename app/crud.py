# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, auth

# --- Users ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # también crea perfil vacío
    db_profile = models.Profile(user_id=db_user.id)
    db.add(db_profile)
    db.commit()
    return db_user

# --- Profiles ---
def get_profile(db: Session, user_id: int):
    return db.query(models.Profile).filter(models.Profile.user_id == user_id).first()

def update_profile(db: Session, user_id: int, profile: schemas.ProfileCreate):
    db_profile = get_profile(db, user_id)
    for field, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, field, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile
