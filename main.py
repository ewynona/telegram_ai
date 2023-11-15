import asyncio
from bot.handlers.handlers import router
from aiogram import Bot, Dispatcher


async def main():
    bot = Bot(token='6428118499:AAFqX8KTYXHBAhpjSwJ_r-4UjdhcvhcZpyI')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print("Exit")


