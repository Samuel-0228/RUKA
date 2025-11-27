from pydantic import BaseModel


class MockResponse(BaseModel):
    status: str
    message: str


async def initiate_telebirr_payment(amount: float, phone: str, order_id: str) -> MockResponse:
    return MockResponse(status="pending", message=f"Mock Telebirr init for {amount} ETB")
