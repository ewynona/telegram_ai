from db.database import session_factory
from db.models import Characters


class CharacterQueries:
    @staticmethod
    def insert_character(character: str):
        with session_factory() as session:
            person = Characters(character=character)
            session.add(person)
            session.commit()

    @staticmethod
    def get_character_id(character: str):
        with session_factory() as session:
            character = session.query(Characters).filter(Characters.character == character).first()

        return character.character_id
