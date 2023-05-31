from __future__ import annotations
from importlib import resources
import resource

from typing import Any

from sqlalchemy import Boolean, Column, Integer, String, Table, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class TodoItems(Base):
    __tablename__ = "todos"
    jira_key = Column("jira_key", String, unique=True, primary_key=True)
    jira_url = Column("jira_url", String)
    description = Column("issue_description", Text)
    status = Column("status", String)
    done = Column("done", Boolean)


def main():
    with resources.path("project.data", "todos.db") as sqlite_filepath:
        engine = create_engine(f"sqlite:///{sqlite_filepath}")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
