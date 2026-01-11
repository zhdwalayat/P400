"""
Database connection and session management for the Task Management API.

Uses SQLModel with SQLite for persistent storage of:
- Subjects
- Topics
- Materials (generated files)
- Tasks (generation requests)
- CLOs (Course Learning Outcomes)
"""

from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

from api.config import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    connect_args={"check_same_thread": False}  # Required for SQLite
)


def create_db_and_tables() -> None:
    """
    Create all database tables.

    Should be called once at application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        SQLModel Session instance

    Usage:
        with get_session() as session:
            # do database operations
            session.commit()
    """
    with Session(engine) as session:
        yield session


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI endpoints.

    Yields:
        SQLModel Session instance

    Usage in FastAPI:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.exec(select(Item)).all()
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
