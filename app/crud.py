from sqlalchemy.orm import Session
from . import models, schemas
from .auth.jwt import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
        language=user.language,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_product(db: Session, product: schemas.ProductCreate, farmer_id: int):
    db_product = models.Product(**product.dict(), farmer_id=farmer_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products_by_farmer(db: Session, farmer_id: int):
    return db.query(models.Product).filter(models.Product.farmer_id == farmer_id).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_order(db: Session, order: schemas.OrderCreate, consumer_id: int, product_price: float):
    total = order.quantity * product_price
    db_order = models.Order(
        **order.dict(),
        consumer_id=consumer_id,
        total_price=total
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders_by_consumer(db: Session, consumer_id: int):
    return db.query(models.Order).filter(models.Order.consumer_id == consumer_id).all()


def update_order_status(db: Session, order_id: int, status: str, payment_status: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        order.status = status
        order.payment_status = payment_status
        db.commit()
    return order
