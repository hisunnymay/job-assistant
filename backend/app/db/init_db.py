from sqlalchemy import text

from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_engine


def initialize_database() -> None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def main() -> None:
    initialize_database()
    print("Database initialization succeeded.")


if __name__ == "__main__":
    main()
