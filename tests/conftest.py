import os

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import Config

# from sqlalchemy import inspect, select, text
# from sqlalchemy.ext.asyncio import (
#     AsyncConnection,
#     AsyncEngine,
#     async_sessionmaker,
# )
# from app.admin.models import AdminModel
from app.store import Database, Store
from app.web.app import Application, setup_app


@pytest.fixture(scope="session")
def application() -> Application:
    app = setup_app(
        config_path=os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "../.env"
        )
    )
    app.database = Database(app)

    return app

# @pytest.fixture(scope="session")
# def application() -> Application:
#     app = setup_app(
#         config_path=os.path.join(
#             os.path.abspath(os.path.dirname(__file__)), "config.yml"
#         )
#     )
#     app.on_startup.clear()
#     app.on_shutdown.clear()
#     app.on_cleanup.clear()

#     app.database = Database(app)
#     app.on_startup.append(app.database.connect)
#     app.on_startup.append(app.store.admins.connect)

#     app.on_shutdown.append(app.database.disconnect)
#     app.on_shutdown.append(app.store.admins.disconnect)
#     return app


@pytest.fixture
def store(application: Application) -> Store:
    return application.store


# @pytest.fixture
# def db_sessionmaker(
#     application: Application,
# ) -> async_sessionmaker[AsyncSession]:
#     print("session: ", application.database.session)
#     return application.database.session


# @pytest.fixture
# def db_engine(application: Application) -> AsyncEngine:
#     print("engine: ", application.database.engine)
#     return application.database.engine


# @pytest.fixture
# async def inspect_list_tables(db_engine: AsyncEngine) -> list[str]:
#     def use_inspector(connection: AsyncConnection) -> list[str]:
#         inspector = inspect(connection)
#         return inspector.get_table_names()

#     async with db_engine.begin() as conn:
#         return await conn.run_sync(use_inspector)


# @pytest.fixture(autouse=True)
# async def clear_db(application: Application) -> Iterator[None]:
#     try:
#         yield
#     except Exception as err:
#         logging.warning(err)
#     finally:
#         session = AsyncSession(application.database.engine)
#         connection = session.connection()
#         for table in application.database._db.metadata.tables:
#             await session.execute(text(f"TRUNCATE {table} CASCADE"))
#             await session.execute(
#                 text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1")
#             )

#         await session.commit()
#         connection.close()


@pytest.fixture
def config(application: Application) -> Config:
    return application.config


@pytest.fixture(autouse=True)
def cli(application: Application) -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=application),
        base_url="http://test"
    )


# @pytest.fixture
# async def auth_cli(cli: TestClient, config: Config) -> TestClient:
#     await cli.post(
#         path="/admin.login",
#         json={
#             "email": config.admin.email,
#             "password": config.admin.password,
#         },
#     )
#     return cli


# @pytest.fixture
# async def admin(cli, db_sessionmaker, config: Config) -> AdminModel:
#     new_admin = AdminModel(
#         email=config.admin.email,
#         password=sha256(config.admin.password.encode()).hexdigest(),
#     )

#     async with db_sessionmaker.begin() as session:
#         existed_admin = await session.scalar(
#             select(AdminModel).where(AdminModel.email == config.admin.email)
#         )
#         if existed_admin:
#             return AdminModel(id=existed_admin.id, email=existed_admin.email)

#         session.add(new_admin)
#         await session.commit()

#     return AdminModel(id=new_admin.id, email=new_admin.email)
