from aiogram import Router, F
from aiogram.types import Message
from chatbot import GptCharacter
from db.queries import MsgQueries
from .keyboards import web_app_markup, remove_markup
from .middleware import CounterMiddleware


router = Router()
router.message.middleware(CounterMiddleware())


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать', reply_markup=web_app_markup)


@router.message(F.content_type == 'web_app_data')
async def cmd_web_data(message: Message):
    await message.answer(
        f"Вы выбрали персонажа {message.web_app_data.data}. Для того, чтобы сменить персонажа, введите команду /start",
        reply_markup=remove_markup
    )


# Generates and sends a response from chatgpt
@router.message(F.text)
async def cmd_text(message: Message, character: GptCharacter, character_id: int):
    character.set_message(message.text)
    # bot_msg = character.get_reply()
    bot_msg = 'test'
    MsgQueries.insert_msg(message.from_user.id, character_id, message.text, bot_msg)
    await message.answer(f"{bot_msg}")
