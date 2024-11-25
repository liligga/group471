import asyncio
import logging

from bot_config import bot, dp, database
from handlers import private_router
from handlers.group import group_router

async def on_startup(bot):
    database.create_tables()
    # await bot.send_message(chat_id=12321312,text="я онлан")


async def main():
    dp.include_router(private_router)
    dp.include_router(group_router)

    dp.startup.register(on_startup)
    # запуск бота:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # подключаем логи
    asyncio.run(main())
