from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    sms_provider: Optional[str] = "africastalking"
    languages: List[str] = ["am", "om", "en"]  # Amharic, Oromo, English
    chapa_secret: Optional[str] = None
    telebirr_public: Optional[str] = None
    telebirr_secret: Optional[str] = None

    class Config:
        env_file = ".env"
        env_ignore_empty = True


settings = Settings()
