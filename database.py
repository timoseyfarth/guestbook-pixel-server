from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from logger import logger

DATABASE_URL = "sqlite:///./guestbook.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

def create_db_and_tables():
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session