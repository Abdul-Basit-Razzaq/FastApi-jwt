# # from pydantic import BaseModel, EmailStr
# # from typing import Optional
# # # Users
# # class UserBase(BaseModel):
# #     username: str
# #     email: EmailStr
# #     fullname: str
# #     disabled: Optional[bool] = False
# #
# # class UserCreate(UserBase):
# #     password: str
# #
# # class User(UserBase):
# #     id: int
# #     class Config:
# #         orm_mode = True
# #
# # #Product
# # class ProductBase(BaseModel):
# #     name: str
# #     description: Optional[str] = None
# #     price: float
# #
# # class ProductCreate(ProductBase):
# #     pass
# #
# #
# # class Product(ProductBase):
# #     id: int
# #     owner_id: int
# #
# #     class Config:
# #         orm_mode = True
# # # OtP
# # class OTPRequest(BaseModel):
# #     email: EmailStr
# #
# # class OTPVerify(BaseModel):
# #     email: EmailStr
# #     otp: str
# from pydantic import BaseModel, EmailStr
# from typing import Optional
#
# # Users
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     fullname: str
#     disabled: Optional[bool] = False
#
# class UserCreate(UserBase):
#     password: str
#
# class User(UserBase):
#     id: int
#
#     class Config:
#         from_attributes = True  # ✅ Updated for Pydantic v2
#
#
# # =========================
# # Products
# # =========================
# class ProductBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#
# class ProductCreate(ProductBase):
#     pass
#
# class Product(ProductBase):
#     id: int
#     owner_id: int
#
#     class Config:
#         from_attributes = True  # ✅ Updated for Pydantic v2
#
# # OTP
# class OTPRequest(BaseModel):
#     email: EmailStr
#
# class OTPVerify(BaseModel):
#     email: EmailStr
#     otp: str

from pydantic import BaseModel, EmailStr
from typing import Optional

# ---------------- User Schemas ----------------
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
        from_attributes = True  # Updated for Pydantic v2

# ---------------- Product Schemas ----------------
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
        from_attributes = True

# ---------------- OTP Schemas ----------------
class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str
