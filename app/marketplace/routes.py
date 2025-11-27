from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product
from ..schemas import Product
from ..common.utils import send_sms

router = APIRouter()


@router.get("/products", response_model=list[Product])
def list_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.post("/alerts")
def send_price_alert(product_name: str, phone: str, db: Session = Depends(get_db)):
    # Stub: Mock avg price
    avg_price = 25.0
    message = f"{product_name} price: {avg_price} ETB/kg"
    send_sms(phone, message)
    return {"status": "Alert sent"}
