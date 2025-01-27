import os

from pydantic_settings import BaseSettings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    app_name: str = 'Spimex app v0.1'
    debug: bool = False
    database_url: str = ''

    class Config:
        env_file = BASE_DIR + '/.env'


settings = Settings()
