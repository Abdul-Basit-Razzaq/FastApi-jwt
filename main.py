from datetime import datetime, timedelta
from typing import Optional, List
import random
import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import models, schemas, crud
from database import Base, engine, get_db
from utils import verify_password, send_otp_email


# Create tables at startup (idempotent)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JWT + FastAPI + PostgreSQL + OTP",
    docs_url="/",         # ✅ Swagger UI will be shown at root (http://127.0.0.1:8000/)
    redoc_url=None        # Optional: Disable Redoc
)

# Load .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/signup/request")
def request_signup(data: schemas.OTPRequest, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = str(random.randint(100000, 999999))
    crud.create_otp(db, data.email, otp)

    if not send_otp_email(data.email, otp):
        raise HTTPException(status_code=500, detail="Failed to send OTP")

    return {"message": "OTP sent to your email. It expires in 2 minutes."}

@app.post("/signup/verify")
def verify_signup(data: schemas.OTPVerify, db: Session = Depends(get_db)):
    is_valid = crud.verify_otp(db, data.email, data.otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    return {"message": "OTP verified successfully. You may now create your account."}

@app.post("/signup/create", response_model=schemas.User)
def create_account(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # ✅ Check if OTP was verified for this email
    if not crud.is_email_verified(db, user.email):
        raise HTTPException(status_code=400, detail="Email not verified via OTP")

    return crud.create_user(db, user)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------- HELPERS ----------------
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = crud.get_user_by_username(db, username)
    if not user:
        raise cred_exc
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ---------------- USER ROUTES ----------------
@app.get("/user/me", response_model=schemas.User)
def read_me(current_user=Depends(get_current_active_user)):
    return current_user


# ---------------- PRODUCT ROUTES ----------------
@app.post("/products/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.create_product(db=db, product=product, user_id=current_user.id)


@app.get("/products/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 locally
    uvicorn.run("main:app", host="0.0.0.0", port=port)
<<<<<<< HEAD
=======

>>>>>>> 8858e4125c6797ee09217e14307d9e6b42a900ff
