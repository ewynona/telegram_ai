from aiogram import Router, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from chatbot.message import GptCharacter
from aiogram.types.web_app_info import WebAppInfo
from bot.middleware.middleware import CounterMiddleware
from db.models import UserInfo, Characters, CharacterMsg
from db.queries.UserQueries import UserQueries
from db.queries.MsgQueries import MsgQueries

router = Router()
router.message.middleware(CounterMiddleware())


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    markup = ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[[KeyboardButton(text='Выбор персонажа', web_app=WebAppInfo(url='https://ewynona.github.io/'))]]
    )
    await message.answer('Добро пожаловать', reply_markup=markup)


@router.message(F.content_type == 'web_app_data')
async def cmd_web_data(message):
    pass


@router.message(F.text)
async def cmd_text(message: Message, character: GptCharacter, character_id: int):
    character.set_message(message.text)
    bot_msg = character.get_message()
    MsgQueries.insert_msg(message.from_user.id, character_id, message.text, bot_msg)
    print(character.get_msg())
    await message.answer(f"{bot_msg}")
