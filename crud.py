from sqlalchemy.orm import Session
import models, schemas
from utils import get_password_hash
from datetime import datetime, timedelta
OTP_EXPIRY_MINUTES = 2

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        fullname=user.fullname,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        disabled=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_product(db: Session, product: schemas.ProductCreate, user_id: int):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        owner_id=user_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_otp(db: Session, email: str, otp: str):
    db.query(models.OTP).filter(models.OTP.email == email).delete()
    db.commit()

    db_otp = models.OTP(
        email=email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=2)
    )
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp

def verify_otp(db: Session, email: str, otp: str):
    # delete expired OTPs first
    db.query(models.OTP).filter(models.OTP.expires_at < datetime.utcnow()).delete()
    db.commit()

    db_otp = db.query(models.OTP).filter(
        models.OTP.email == email,
        models.OTP.otp == otp,
        models.OTP.expires_at >= datetime.utcnow()
    ).first()

    return db_otp is not None

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


