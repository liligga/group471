import asyncio
import logging

from bot_config import bot, dp, database
from handlers.opros_dialog import opros_router
from handlers.other_messages import echo_router
from handlers.picture import picture_router
from handlers.start import start_router
from handlers.admin_book import admin_book_router
from handlers.shop import shop_router

async def on_startup(bot):
    database.create_tables()
    # await bot.send_message(chat_id=12321312,text="я онлан")


async def main():
    dp.include_router(start_router)
    dp.include_router(picture_router)
    dp.include_router(opros_router)
    dp.include_router(admin_book_router)
    dp.include_router(shop_router)
    
    # в самом конце
    dp.include_router(echo_router)

    dp.startup.register(on_startup)
    # запуск бота:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # подключаем логи
    asyncio.run(main())
