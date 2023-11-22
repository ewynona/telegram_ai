from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from chatbot import GptCharacter
from db.queries import UserQueries, MsgQueries, CharacterQueries


# Checks whether the user is registered and has a character selected for communication
async def user_check(event) -> bool:
    get_user = UserQueries.get_user(event.from_user.id)
    if get_user is None and event.text != '/start':
        await event.answer(
            'Вы не зарегестрированы. Введите команду /start и выберите персонажа с которым будете общаться.')
    elif get_user is None and event.text == '/start':
        UserQueries.insert_user(user_id=event.from_user.id,
                                username=event.from_user.username,
                                name=event.from_user.first_name,
                                second_name=event.from_user.last_name)
        return True
    elif get_user.current_character is None and event.text != '/start' and event.web_app_data is None:
        await event.answer('Выберите персонажа с которым будете общаться. Для выбора введите команду /start')
    else:
        return True
    return False


# !!!!! Remake it by configure character caching for each user !!!!!
class CounterMiddleware(BaseMiddleware):
    def __init__(self):
        self.character = None
        self.character_id = None

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        if await user_check(event) is False:
            return

        # Checking for character change or launch after bot restart
        if event.content_type == 'web_app_data' or self.character is None and event.text != '/start':
            user_id = event.from_user.id

            if event.content_type == 'web_app_data':
                character = event.web_app_data.data
                character_id = CharacterQueries.get_character_id(character)

                if character_id is None:
                    CharacterQueries.insert_character(character)
                    character_id = CharacterQueries.get_character_id(character)
                UserQueries.update_user_character(user_id, character_id)

            self.character = GptCharacter(UserQueries.get_current_character(user_id))
            self.character_id = UserQueries.select_user(user_id).current_character
        # Saving the dialogue history from the database to maintain the context of the dialogue
        elif event.content_type == 'text':
            messages = MsgQueries.get_msg(event.from_user.id, self.character_id)
            for msg in messages:
                self.character.set_message(msg.user_msg)
                self.character.set_bot_message(msg.bot_msg)

        data['character'] = self.character
        data['character_id'] = self.character_id

        return await handler(event, data)
