from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    FARMER = "farmer"
    CONSUMER = "consumer"
    DEVELOPER = "developer"
    ADMIN = "admin"
    AGENT = "agent"


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    language: str = "en"


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.CONSUMER


class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None
    images: Optional[List[str]] = []


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    farmer_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    product_id: int
    quantity: int
    payment_method: Optional[str] = "cod"


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    consumer_id: int
    status: str
    payment_status: str
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    method: str  # "chapa", "telebirr", "cod"


class PaymentResponse(BaseModel):
    transaction_id: str
    status: str  # "pending", "success", "failed"
    message: str
