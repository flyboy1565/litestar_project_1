from typing import TYPE_CHECKING

from litestar.di import Provide
from litestar.controller import Controller
from litestar.pagination import OffsetPagination
from litestar.handlers import get, put, post, patch, delete
from litestar.contrib.repository.filters import LimitOffset
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import parse_obj_as

from models import TodoItem, TodoItemModel
from db import TodoItems


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class TodoItemRepository(SQLAlchemyAsyncRepository[TodoItemModel]):
    model_type = TodoItemModel


async def provide_todos_repo(db_session: "AsyncSession") -> TodoItemRepository:
    return TodoItemRepository(session=db_session)


async def provide_todo_details_repo(db_session: "AsyncSession") -> TodoItemRepository:
    return TodoItemRepository(statement=select(TodoItemModel), session=db_session)


class TodoItemController(Controller):
    dependencies = {"todos_repo": Provide(provide_todos_repo)}

    @get(path="/api")
    async def get_all(
        self, todos_repo: TodoItemRepository, limit_offset: LimitOffset
    ) -> OffsetPagination[TodoItem]:
        results, total = await todos_repo.list_and_count(limit_offset)
        return OffsetPagination[TodoItem](
            items=parse_obj_as(list[TodoItem], results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get(path="/api/{jira_key:str}")
    async def get_todo(self, jira_key: str, todos_repo: TodoItemRepository) -> TodoItem:
        result = await todos_repo.get_one(jira_key)
        return result

    @post(path="/api")
    async def create_todo(
        self, todos_repo: TodoItemRepository, data: TodoItem
    ) -> TodoItem:
        obj = await todos_repo.add(
            TodoItemModel(
                **data.dict(exclude_unset=True, by_alias=False, exclude_none=True)
            )
        )
        await todos_repo.session.commit()
        return TodoItem.from_orm(obj)
