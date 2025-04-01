import typing

from pyrogram import Client as PyrogramClient

if typing.TYPE_CHECKING:
    from app.web.app import Application


NAME = "Claude MCP userbot"
TEST_MODE = True


class UserBot(PyrogramClient):
    pass


def setup_userbot(app: "Application") -> UserBot:
    c = app.config.tg
    app.userbot = UserBot(
        name=NAME,
        api_id=c.api_id,
        api_hash=c.api_hash,
        phone_number=c.phone,
        password=c.password,
        hide_password=True,
        test_mode=TEST_MODE
    )
    return app.userbot
