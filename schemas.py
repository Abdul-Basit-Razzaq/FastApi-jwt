from pydantic import BaseModel, EmailStr
from typing import Optional
# Users
class UserBase(BaseModel):
    username: str
    email: EmailStr
    fullname: str
    disabled: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

#Product
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
# OtP
class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str