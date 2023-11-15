from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text


class Base(DeclarativeBase):
    pass


engine = create_engine(
    url="postgresql+psycopg://bikbulat:bikbulat@localhost:5432/character_ai",
    echo=False,
    pool_size=5,
    max_overflow=10
)

session_factory = sessionmaker(engine)
