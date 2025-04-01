import os
import typing
from dataclasses import dataclass

from dotenv import load_dotenv

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class TelegramConfig:
    api_id: int
    api_hash: str
    phone: str
    login: str
    password: str | None = None


@dataclass
class DataBaseConfig:
    user: str
    password: str
    host: str | None = '127.0.0.1'
    port: int | None = 5432
    db_name: str | None = 'postgre'

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass
class Config:
    tg: TelegramConfig | None = None
    db: DataBaseConfig | None = None


def setup_config(app: "Application", config_path: str):
    load_dotenv(dotenv_path=config_path, override=True)

    tg_config = TelegramConfig(
        api_id=int(os.environ["TG_API_ID"]),
        api_hash=os.environ["TG_API_HASH"],
        phone=os.environ["TG_PHONE"],
        login=os.environ["TG_LOGIN"],
        password=os.environ["TG_PASS"]
    )

    db_config = DataBaseConfig(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "5432")),
        db_name=os.environ.get("DB_NAME", "postgre")
    )

    app.config = Config(
        tg=tg_config,
        db=db_config
    )
