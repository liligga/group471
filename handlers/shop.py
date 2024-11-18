from aiogram import F, Router, types
from aiogram.filters import Command

from bot_config import database
from pprint import pprint

shop_router = Router()


@shop_router.message(Command("books"))
async def show_all_books(message: types.Message):
    all_books = database.fetch(
        query="SELECT * FROM books"
    )
    pprint(all_books)
    await message.answer("Книги из нашего каталога:")
    for book in all_books:
        await message.answer(f"Название: {book['name']}\nЦена: {book['price']}")