from dotenv import load_dotenv

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / '.env')
load_dotenv(dotenv_path=BASE_DIR / '.db.env')

# load_dotenv(dotenv_path='.env')
# load_dotenv(dotenv_path='.db.env')


class DataBaseSettings(BaseSettings):
    """Конфиги базы данных."""

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix='POSTGRES_')
    host: str
    port: str
    db: str
    user: str
    password: str
    test_db: str


class AppSettings(BaseSettings):
    """Конфиги приложения."""

    model_config = SettingsConfigDict(case_sensitive=False)

    debug: bool
    test_base_url: str

app_settings = AppSettings()
db_settings = DataBaseSettings()
