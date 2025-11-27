from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..schemas import User
from ..models import Product

router = APIRouter()


@router.post("/orders", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != schemas.UserRole.CONSUMER:
        raise HTTPException(status_code=403, detail="Not a consumer")
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.create_order(db, order, current_user.id, product.price)


@router.get("/orders", response_model=list[schemas.Order])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != schemas.UserRole.CONSUMER:
        raise HTTPException(status_code=403, detail="Not a consumer")
    return crud.get_orders_by_consumer(db, current_user.id)
