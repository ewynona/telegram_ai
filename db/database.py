from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    url=settings.database_url_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

session_factory = sessionmaker(engine)
