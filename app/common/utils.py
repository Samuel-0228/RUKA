import httpx
from ..config import settings


async def send_sms(phone: str, message: str):
    if not settings.sms_provider:
        print(f"SMS stub: {message} to {phone}")
        return
    # Africa's Talking stub
    url = "https://api.africastalking.com/version1/messaging"
    payload = {"to": phone, "message": message}
    headers = {
        "apikey": settings.sms_api_key,  # Assume added to config if needed
        "Content-Type": "application/x-www-form-urlencoded"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)
    return response.json()


def translate_to_lang(text: str, lang: str) -> str:
    # Stub
    translations = {"am": {"Tomato": "ቶማት"}, "en": {"Tomato": "Tomato"}}
    return translations.get(lang, {}).get(text, text)
