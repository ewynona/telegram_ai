from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_web_app = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton
        (
            text="Hello",
            callback_data="123"
        )
    ]

])

