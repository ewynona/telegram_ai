from db import session_factory, UserInfo, Characters
from db.queries import CharacterQueries
from sqlalchemy import delete


class UserQueries:
    @staticmethod
    def insert_user(user_id, username, name, second_name=None):
        with session_factory() as session:
            user = UserInfo(user_id=user_id, username=username, name=name, second_name=second_name)
            session.add(user)
            session.commit()

    @staticmethod
    def get_user(user_id):
        with session_factory() as session:
            user = session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
        return user

    @staticmethod
    def del_user(user_id: int):
        with session_factory() as session:
            query = delete(UserInfo).filter(UserInfo.user_id == user_id)
            session.execute(query)
            session.commit()

    @staticmethod
    def select_user(user_id: int):
        with session_factory() as session:
            user = session.query(UserInfo).filter(UserInfo.user_id == user_id).first()

        return user

    @staticmethod
    def update_user_character(user_id: int, character_name: str):
        with session_factory() as session:
            character_id = CharacterQueries.get_character_id(character_name)
            user = session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
            user.current_character = character_id
            session.commit()

    @staticmethod
    def get_current_character(user_id: int):
        with session_factory() as session:
            query = session.query(UserInfo, Characters).join(
                Characters,
                UserInfo.current_character == Characters.character_id
            ).filter(UserInfo.user_id == user_id).all()
        return query[0][1].character
