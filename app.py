from typing import TYPE_CHECKING

from litestar import Litestar
from litestar.contrib.sqlalchemy.base import UUIDBase

# from models import TodoItem, Project
from controllers import TodoItemController

from settings import (
    openapi_config,
    template_config,
    sqlalchemy_config,
    sqlalchemy_plugin,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


async def on_startup() -> None:
    async with sqlalchemy_config.create_engine().begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)


app = Litestar(
    route_handlers=[TodoItemController],
    on_startup=[on_startup],
    plugins=[sqlalchemy_plugin],
    template_config=template_config,
    openapi_config=openapi_config,
)
