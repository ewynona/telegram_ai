import datetime
from typing import Annotated
from sqlalchemy import String, ForeignKey, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from db import Base, engine

int_pk = Annotated[int, mapped_column(primary_key=True)]


class UserInfo(Base):
    __tablename__ = 'user_info'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(64))
    second_name: Mapped[str | None] = mapped_column(String(64))
    reg_time: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    current_character: Mapped[int | None] = mapped_column(ForeignKey("characters.character_id", ondelete="SET NULL"))


class Characters(Base):
    __tablename__ = 'characters'

    character_id: Mapped[int_pk]
    character: Mapped[str]


class CharacterMsg(Base):
    __tablename__ = 'character_msg'

    msg_id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('user_info.user_id', ondelete='CASCADE'))
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.character_id', ondelete='CASCADE'))
    user_msg: Mapped[str]
    bot_msg: Mapped[str | None]
    msg_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
