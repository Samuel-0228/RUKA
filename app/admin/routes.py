from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..schemas import User
from ..models import User as UserModel, Product

router = APIRouter()


@router.get("/users", response_model=list[User])
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != User.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    users = db.query(UserModel).all()
    return users


@router.get("/stats")
def get_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != User.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    total_users = db.query(UserModel).count()
    total_products = db.query(Product).count()
    return {"total_users": total_users, "total_products": total_products}
