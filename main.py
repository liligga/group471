import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    msg = f"Привет, {name}"
    await message.answer(msg)


@dp.message()
async def echo_handler(message: types.Message):
    # обработчик всех сообщений
    await message.answer(message.text)


async def main():
    # запуск бота:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
