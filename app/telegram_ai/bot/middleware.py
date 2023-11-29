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


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        self.cache = {}
        self.current_character = {}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        if await user_check(event) is False:
            return

        user_id = event.from_user.id

        # Checking for character change or launch after bot restart

        if event.content_type == 'web_app_data' or user_id not in self.cache and event.text != '/start':

            if event.content_type == 'web_app_data':
                character = event.web_app_data.data
                if CharacterQueries.get_character_id(character) is None:
                    CharacterQueries.insert_character(character)
                UserQueries.update_user_character(user_id, character)
            else:
                character = UserQueries.get_current_character(user_id)

            self.current_character[user_id] = character

            if user_id not in self.cache:
                self.cache[user_id] = {}
            if character not in self.cache[user_id]:
                self.cache[user_id][character] = GptCharacter(character)
                messages = MsgQueries.get_msg(user_id, character)
                for msg in messages:
                    self.cache[user_id][character].set_message(msg.user_msg)
                    self.cache[user_id][character].set_bot_message(msg.bot_msg)

        if event.content_type == 'text' and event.text != '/start':
            character = self.current_character[user_id]
            data['character'] = self.cache[user_id][character]

        response = await handler(event, data)
        return response
