from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Contact
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.contrib.sqlalchemy.plugins import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

from constants import BASE_DIR


openapi_config = OpenAPIConfig(
    title="Jira Associated Todos",
    create_examples=True,
    contact=Contact(
        name="Bob & Tom",
        email="mailto:bobandtomshow@fakestuff.com",
    ),
    version="0.1.0",
    description="API",
)

template_config = TemplateConfig(
    directory=BASE_DIR / "static" / "templates",
    engine=JinjaTemplateEngine,
)


sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite",
    session_dependency_key="db_session",
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
