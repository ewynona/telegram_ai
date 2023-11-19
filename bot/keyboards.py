from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove

web_app_markup = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[[KeyboardButton(text='Выбор персонажа', web_app=WebAppInfo(url='https://ewynona.github.io/'))]]
)

remove_markup = ReplyKeyboardRemove()
