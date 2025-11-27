from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from .. import crud, schemas
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..schemas import User, Order
from ..config import settings
import asyncio

router = APIRouter()


class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    method: str  # "chapa", "telebirr", "cod"


class PaymentResponse(BaseModel):
    transaction_id: str
    status: str  # "pending", "success", "failed"
    message: str


@router.post("/initiate", response_model=PaymentResponse)
async def initiate_payment(
    request: PaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    if current_user.role != schemas.UserRole.CONSUMER:
        raise HTTPException(status_code=403, detail="Consumer only")

    order = db.query(Order).filter(Order.id == request.order_id,
                                   Order.consumer_id == current_user.id).first()
    if not order or order.status != "pending":
        raise HTTPException(status_code=404, detail="Invalid order")

    if request.method == "cod":
        # Instant "success"
        order.payment_status = "paid"
        order.status = "shipped"
        db.commit()
        return PaymentResponse(transaction_id="COD-123", status="success", message="Cash on delivery confirmed!")

    elif request.method == "chapa":
        mock_tx = f"CHAPA-{asyncio.get_event_loop().time()}"

        async def mock_process():
            await asyncio.sleep(2)
            verify_mock = {
                "status": "success" if "test" in current_user.email else "failed"}
            order.payment_status = verify_mock["status"]
            order.status = "shipped" if verify_mock["status"] == "success" else "failed"
            db.commit()
        background_tasks.add_task(mock_process)
        return PaymentResponse(transaction_id=mock_tx, status="pending", message="Redirecting to Chapa...")

    elif request.method == "telebirr":
        mock_tx = f"TELE-{asyncio.get_event_loop().time()}"

        async def mock_process():
            await asyncio.sleep(1.5)
            verify_mock = {
                "status": "success" if request.amount < 100 else "failed"}
            order.payment_status = verify_mock["status"]
            order.status = "shipped" if verify_mock["status"] == "success" else "failed"
            db.commit()
        background_tasks.add_task(mock_process)
        return PaymentResponse(transaction_id=mock_tx, status="pending", message="Redirecting to Telebirr...")

    raise HTTPException(status_code=400, detail="Invalid method")


@router.get("/status/{tx_id}", response_model=PaymentResponse)
async def check_status(tx_id: str, db: Session = Depends(get_db)):
    await asyncio.sleep(1)
    return PaymentResponse(transaction_id=tx_id, status="success", message="Payment confirmed!")
