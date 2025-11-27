from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.sql import func
from .database import Base
from enum import Enum


class UserRole(Enum):
    FARMER = "farmer"
    CONSUMER = "consumer"
    DEVELOPER = "developer"
    ADMIN = "admin"
    AGENT = "agent"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Hashed
    role = Column(SQLEnum(UserRole), default=UserRole.CONSUMER)
    phone = Column(String(20), nullable=True)  # For SMS
    language = Column(String(5), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)  # ETB/kg
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    images = Column(Text, nullable=True)  # JSON list of URLs
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")  # pending, paid, shipped
    payment_method = Column(String(50), default="cod")
    payment_status = Column(String(50), default="unpaid")
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
