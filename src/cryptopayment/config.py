from pydantic import BaseSettings

from myloguru.my_loguru import get_logger


class Settings(BaseSettings):
    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 8000
    DEBUG: bool = False
    ADMINS: list = []
    TELEBOT_TOKEN: str
    DB_KEY_VALIDATION: str
    MAIN_WALLET: str
    STAGE: str
    GITHUB_SECRET: str
    LOCATION: str = 'somewhere'


class Database(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    def get_db_name(self):
        return f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


ENV_PATH = '../../.env'
db = Database(_env_file=ENV_PATH, _env_file_encoding='utf-8')
settings = Settings(_env_file=ENV_PATH, _env_file_encoding='utf-8')

level = 1 if settings.DEBUG else 20
logger = get_logger(level=level)

DATABASE_CONFIG = {
    "connections": {"default": db.get_db_name()},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "models.models"
            ],
            "default_connection": "default",
        },
    },
}
