from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..schemas import User

router = APIRouter()


@router.post("/products", response_model=schemas.Product)
def add_product(
    product: schemas.ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != schemas.UserRole.FARMER:
        raise HTTPException(status_code=403, detail="Not a farmer")
    return crud.create_product(db=db, product=product, farmer_id=current_user.id)


@router.get("/products", response_model=list[schemas.Product])
def get_my_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != schemas.UserRole.FARMER:
        raise HTTPException(status_code=403, detail="Not a farmer")
    return crud.get_products_by_farmer(db, current_user.id)
