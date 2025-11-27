from pydantic import BaseModel


class MockResponse(BaseModel):
    status: str
    message: str


async def initiate_chapa_payment(amount: float, email: str, tx_ref: str) -> MockResponse:
    return MockResponse(status="pending", message=f"Mock Chapa init for {amount} ETB")


async def verify_chapa_tx(tx_ref: str) -> MockResponse:
    return MockResponse(status="success", message="Mock verification passed")
