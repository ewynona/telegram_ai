import asyncio
from bot.handlers import router
from aiogram import Bot, Dispatcher
from config import settings

#
async def main():
    bot = Bot(token=settings.TELEGRAM_API_KEY)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as error:
        print("Exit\n", error)


