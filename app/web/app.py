from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import Config, setup_config
from app.store import Store
from app.store.database.database import Database
from app.userbot.app import UserBot
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes


class Application(FastAPI):
    config: Config | None = None
    store: Store | None = None
    database: Database | None = None
    userbot: UserBot | None = None


@asynccontextmanager
async def lifespan(app: Application):
    app.database = Database(app)
    app.store = Store(app)

    await app.database.connect()

    yield

    await app.database.disconnect()


app = Application(title="Claude MCP Server", lifespan=lifespan)


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_routes(app)

    setup_middlewares(app)
    return app
