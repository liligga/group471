from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot_config import database


admin_book_router = Router()
admin_book_router.message.filter(
    F.from_user.id == 243154734
)

class Book(StatesGroup):
    name = State()
    author = State()
    price = State()
    genre = State()


@admin_book_router.message(Command("newbook"), default_state)
async def create_newbook(message: types.Message, state: FSMContext):
    print(message.from_user.id)
    await state.set_state(Book.name)
    await message.answer("Задайте название книги:")

@admin_book_router.message(Book.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Book.author)
    await message.answer("Задайте автора книги:")
    
@admin_book_router.message(Book.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(Book.price)
    await message.answer("Задайте цену книги:")

@admin_book_router.message(Book.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)

    await state.set_state(Book.genre)
    await message.answer("Задайте жанр книги:")

@admin_book_router.message(Book.genre)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)

    data = await state.get_data()
    database.execute(
        query="""
            INSERT INTO books(name, author, price, genre)
            VALUES (?, ?, ?, ?)
        """,
        params=(
            data["name"], 
            data["author"], 
            data["price"], 
            data["genre"]
        )
    )
    await message.answer("Книга добавлена")