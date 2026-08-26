from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, delete, text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.base import Base
from app.db.models import Conversation, ConversationMessage
from app.db.session import get_db_session
from app.main import app


@pytest.fixture(scope="session")
def database_engine() -> Generator[Engine, None, None]:
    schema_name = f"app_test_{uuid4().hex}"
    database_url = get_settings().database_url
    administration_engine = create_engine(database_url, pool_pre_ping=True)

    with administration_engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema_name}"'))

    engine = create_engine(
        database_url,
        connect_args={"options": f"-csearch_path={schema_name}"},
        pool_pre_ping=True,
    )
    Base.metadata.create_all(engine)

    try:
        yield engine
    finally:
        engine.dispose()
        with administration_engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema_name}" CASCADE'))
        administration_engine.dispose()


@pytest.fixture
def db_session(database_engine: Engine) -> Generator[Session, None, None]:
    with Session(database_engine, expire_on_commit=False) as session:
        yield session
        session.rollback()

    with database_engine.begin() as connection:
        connection.execute(delete(ConversationMessage))
        connection.execute(delete(Conversation))


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_db_session() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db_session] = override_db_session
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()
