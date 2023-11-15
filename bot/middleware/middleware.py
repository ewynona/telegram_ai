from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from chatbot.message import GptCharacter
from db.queries.UserQueries import UserQueries
from db.queries.CharacterQueries import CharacterQueries
from db.queries.MsgQueries import MsgQueries


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
    elif get_user.current_character is None and event.text != '/start' and event.web_app_data is None:
        await event.answer('Выберите персонажа с которым будете общаться.')
    else:
        return True
    return False


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

        if event.content_type == 'web_app_data' or self.character is None:
            if event.content_type == 'web_app_data':
                UserQueries.update_user_character(event.from_user.id, event.web_app_data.data)
            self.character = GptCharacter(UserQueries.get_current_character(event.from_user.id))
            self.character_id = UserQueries.select_user(event.from_user.id).current_character

        if event.content_type == 'text':
            messages = MsgQueries.get_msg(event.from_user.id, self.character_id)
            for msg in messages:
                self.character.set_message(msg.user_msg)
                self.character.set_bot_message(msg.bot_msg)

        data['character'] = self.character
        data['character_id'] = self.character_id

        return await handler(event, data)