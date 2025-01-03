from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from bot_config import database

opros_router = Router()


# fsm = finite state machine - конечный автомат
class Opros(StatesGroup):
    name = State()
    age = State()
    gender = State()
    genre = State()


@opros_router.message(Command("stop"))
@opros_router.message(F.text == "стоп")
async def stop_opros(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос остановлен")


@opros_router.message(Command("opros"), default_state)
async def start_opros(message: types.Message, state: FSMContext):
    await state.set_state(Opros.name)
    await message.answer("Как вас зовут?")


@opros_router.message(Opros.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Opros.age)
    await message.answer("Напишите ваш возраст:")


@opros_router.message(Opros.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Вводите только цифры!")
        return
    age = int(age)
    if age < 12 or age > 90:
        await message.answer("Вводите возраст от 12 до 90")
        return
    
    await state.update_data(age=message.text)
    await state.set_state(Opros.gender)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="мужской"),
                types.KeyboardButton(text="женский")
            ]
        ]
    )
    await message.answer("Напишите ваш пол", reply_markup=kb)

# lst = [1, 2, 3]
# x = 12
# if x in lst:
#     ...

@opros_router.message(Opros.gender)
async def process_gender(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.update_data(gender=message.text)
    await state.set_state(Opros.genre)
    await message.answer("Какой у вас любимый литературный жанр", reply_markup=kb)


# @opros_router.message(Opros.gender, F.text == "мужской"))
# async def process_gender(message: types.Message, state: FSMContext):
#     await state.update_data(gender=message.text)
#     await state.set_state(Opros.genre)
#     await message.answer("Какой у вас любимый литературный жанр")

# @opros_router.message(Opros.gender, F.text == "женский"))
# async def process_gender(message: types.Message, state: FSMContext):
#     await state.update_data(gender=message.text)
#     await state.set_state(Opros.genre)
#     await message.answer("Какой у вас любимый литературный жанр")


@opros_router.message(Opros.genre)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("Спасибо за пройденный опрос")
    data = await state.get_data()
    print(data) # {"name": "igor", "age": 32, "gender": "мужской", "genre": "horror"}

    database.execute(
        query="""
        INSERT INTO survey_results (name, age, gender, genre)
        VALUES (?, ?, ?, ?)
        """,
        params=(data["name"], data["age"], data["gender"], data["genre"])
    )

    # так делать не надо:
    # database.execute(
    #     query=f"INSERT INTO survey_results (name, age, gender, genre) VALUES ({data['name']},  {data["age"]}, {data["gender"]}, {data["genre"]})",
    #     params=tuple()
    # )
    
    await state.clear()
