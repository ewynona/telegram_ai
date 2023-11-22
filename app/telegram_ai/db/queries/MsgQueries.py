from db import CharacterMsg, session_factory


class MsgQueries:
    @staticmethod
    def insert_msg(user_id, character_id, user_msg, bot_msg):
        with session_factory() as session:
            msg = CharacterMsg(
                user_id=user_id,
                character_id=character_id,
                user_msg=user_msg,
                bot_msg=bot_msg
            )
            session.add(msg)
            session.commit()

    @staticmethod
    def get_msg(user_id, character_id):
        with (session_factory() as session):
            msg = session.query(CharacterMsg).filter(
                CharacterMsg.user_id == user_id,
                CharacterMsg.character_id == character_id
            ).all()
        return msg
