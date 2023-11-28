from db import CharacterMsg, session_factory, Characters


class MsgQueries:
    @staticmethod
    def insert_msg(user_id, character_name, user_msg, bot_msg):
        with session_factory() as session:
            character_id = session.query(Characters).filter(Characters.character == character_name).first().character_id
            msg = CharacterMsg(
                user_id=user_id,
                character_id=character_id,
                user_msg=user_msg,
                bot_msg=bot_msg
            )
            session.add(msg)
            session.commit()

    @staticmethod
    def get_msg(user_id, character_name: str):
        with (session_factory() as session):
            character = MsgQueries.get_character_id(character_name)
            msg = session.query(CharacterMsg).filter(
                CharacterMsg.user_id == user_id,
                CharacterMsg.character_id == character.character_id
            ).all()
        return msg

    @staticmethod
    def get_character_id(character_name: str):
        with session_factory() as session:
            character = session.query(Characters).filter(Characters.character == character_name).first()
        return character
