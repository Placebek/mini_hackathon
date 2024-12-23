import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    def reload_env(self):
        load_dotenv(override=True)

    @property
    def DATABASE_URL_asyncpg(self):
        self.reload_env()
        return f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    TOKEN_SECRET_KEY: str

settings = Settings()