# # from sqlalchemy.orm import Session
# # import models, schemas
# # from utils import get_password_hash
# # from datetime import datetime, timedelta
# # OTP_EXPIRY_MINUTES = 2
# #
# # def get_user_by_username(db: Session, username: str):
# #     return db.query(models.User).filter(models.User.username == username).first()
# #
# # def create_user(db: Session, user: schemas.UserCreate):
# #     db_user = models.User(
# #         username=user.username,
# #         fullname=user.fullname,
# #         email=user.email,
# #         hashed_password=get_password_hash(user.password),
# #         disabled=False,
# #     )
# #     db.add(db_user)
# #     db.commit()
# #     db.refresh(db_user)
# #     return db_user
# #
# # def create_product(db: Session, product: schemas.ProductCreate, user_id: int):
# #     db_product = models.Product(
# #         name=product.name,
# #         description=product.description,
# #         price=product.price,
# #         owner_id=user_id
# #     )
# #     db.add(db_product)
# #     db.commit()
# #     db.refresh(db_product)
# #     return db_product
# #
# # def get_products(db: Session, skip: int = 0, limit: int = 10):
# #     return db.query(models.Product).offset(skip).limit(limit).all()
# #
# # def create_otp(db: Session, email: str, otp: str):
# #     db.query(models.OTP).filter(models.OTP.email == email).delete()
# #     db.commit()
# #
# #     db_otp = models.OTP(
# #         email=email,
# #         otp=otp,
# #         expires_at=datetime.utcnow() + timedelta(minutes=2)
# #     )
# #     db.add(db_otp)
# #     db.commit()
# #     db.refresh(db_otp)
# #     return db_otp
# #
# # def verify_otp(db: Session, email: str, otp: str):
# #     # delete expired OTPs first
# #     db.query(models.OTP).filter(models.OTP.expires_at < datetime.utcnow()).delete()
# #     db.commit()
# #
# #     db_otp = db.query(models.OTP).filter(
# #         models.OTP.email == email,
# #         models.OTP.otp == otp,
# #         models.OTP.expires_at >= datetime.utcnow()
# #     ).first()
# #
# #     return db_otp is not None
# #
# # def get_user_by_email(db: Session, email: str):
# #     return db.query(models.User).filter(models.User.email == email).first()
# #
# #
#
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# import models, schemas
# from utils import get_password_hash
#
# # ---------------- OTP Operations ----------------
# def create_otp(db: Session, email: str, otp: str):
#     expires_at = datetime.utcnow() + timedelta(minutes=2)
#     db_otp = models.OTP(email=email, otp=otp, expires_at=expires_at)
#     db.add(db_otp)
#     db.commit()
#     db.refresh(db_otp)
#     return db_otp
#
# def verify_otp(db: Session, email: str, otp: str) -> bool:
#     record = db.query(models.OTP).filter(models.OTP.email == email).order_by(models.OTP.id.desc()).first()
#     if record and record.otp == otp and record.expires_at > datetime.utcnow():
#         return True
#     return False
#
# def is_email_verified(db: Session, email: str) -> bool:
#     """Check if OTP was successfully verified before account creation."""
#     record = db.query(models.OTP).filter(models.OTP.email == email).order_by(models.OTP.id.desc()).first()
#     return record is not None and record.expires_at > datetime.utcnow()
#
# # ---------------- User Operations ----------------
# def create_user(db: Session, user: schemas.UserCreate):
#     hashed_password = get_password_hash(user.password)
#     db_user = models.User(
#         username=user.username,
#         fullname=user.fullname,
#         email=user.email,
#         hashed_password=hashed_password
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
# def get_user_by_username(db: Session, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
# # ---------------- Product Operations ----------------
# def create_product(db: Session, product: schemas.ProductCreate, user_id: int):
#     db_product = models.Product(**product.dict(), owner_id=user_id)
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product
#
# def get_products(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(models.Product).offset(skip).limit(limit).all()

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models, schemas
from utils import get_password_hash

# ---------------- OTP Operations ----------------
def create_otp(db: Session, email: str, otp: str):
    """Create a new OTP with a 2-minute expiry."""
    expires_at = datetime.utcnow() + timedelta(minutes=2)
    db_otp = models.OTP(email=email, otp=otp, expires_at=expires_at)
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)

    # Clean up expired OTPs immediately after generating a new one
    delete_expired_otps(db)

    return db_otp

def verify_otp(db: Session, email: str, otp: str) -> bool:
    """Verify the OTP and ensure it's not expired."""
    record = db.query(models.OTP).filter(models.OTP.email == email).order_by(models.OTP.id.desc()).first()
    if record and record.otp == otp and record.expires_at > datetime.utcnow():
        return True
    return False

# def is_email_verified(db: Session, email: str) -> bool:
#     """
#     Check if OTP was successfully verified before account creation.
#     User has ONLY 1 MINUTE to complete signup after OTP verification.
#     """
#     record = db.query(models.OTP).filter(models.OTP.email == email).order_by(models.OTP.id.desc()).first()
#     if not record:
#         return False
#
#     # Only 1 minute extra after OTP expiry
#     return record.expires_at + timedelta(minutes=1) > datetime.utcnow()

def delete_expired_otps(db: Session):
    """Delete all OTP records that are past their expiry time."""
    db.query(models.OTP).filter(models.OTP.expires_at < datetime.utcnow()).delete()
    db.commit()

# ---------------- User Operations ----------------
def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user after verifying OTP."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        fullname=user.fullname,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# ---------------- Product Operations ----------------
def create_product(db: Session, product: schemas.ProductCreate, user_id: int):
    db_product = models.Product(**product.dict(), owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()
