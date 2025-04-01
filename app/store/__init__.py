import typing

from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.posts.accessor import PostsAccessor

        self.posts = PostsAccessor(app)
