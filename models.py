from typing import TYPE_CHECKING, Union, Text
from uuid import UUID

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from litestar.contrib.sqlalchemy.base import UUIDAuditBase, UUIDBase


from pydantic import BaseModel as _BaseModel
from pydantic import parse_obj_as


class BaseModel(_BaseModel):
    class Config:
        orm_mode = True


class ProjectModel(UUIDBase):
    name: Mapped[str]


class TodoItemModel(UUIDAuditBase):
    jira_key: Mapped[str]
    jira_url: Mapped[str]
    issue_description: Mapped[Text]
    # project: Union[str,None] = None
    status: Mapped[str]
    done: Mapped[int]


class Project(BaseModel):
    name: str


class TodoItem(BaseModel):
    jira_key: str
    jira_url: str
    issue_description: Text
    status: str
    done: int
