from aiogram import Bot, Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from random import randint
import json
import asyncio

from aiogram import F

from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
storage = MemoryStorage()


class FSMMovieOfTheDay(StatesGroup):
    get_movie_of_the_day = State()


class FSMMovieByGenre(StatesGroup):
    genre_choice = State()
    get_movies_by_genre = State()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text='Фильм дня')],
        [types.KeyboardButton(text='Рекомендация по жанру')],
        [types.KeyboardButton(text='Случайный фильм')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Привет, выбери одно: ', reply_markup=keyboard)


@dp.message(Command('cancel'), ~StateFilter(default_state))
async def process_cancel_state(message: types.Message, state: FSMContext):
    await message.answer(text='Возвращаемся в начало.')
    await state.clear()


def get_movies(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


@dp.message(F.text == 'Фильм дня', StateFilter(default_state))
async def movie_of_the_day(message: types.Message, state: FSMContext):
    movies_json = get_movies('random_movie.json')
    print(movies_json)
    movie_id = randint(0, len(movies_json))
    movie = movies_json.get(str(movie_id), 'Фильм дня недоступен')
    await message.answer(movie)


@dp.message(F.text == 'Рекомендация по жанру', StateFilter(default_state))
async def genre_choice(message: types.Message, state: FSMContext):
    genres_json = get_movies('movie_by_genre.json')
    kb = [[types.KeyboardButton(text=x)] for x in genres_json.keys()]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    await message.answer('Выберите жанр:', reply_markup=markup)
    await state.set_state(FSMMovieByGenre.get_movies_by_genre)


@dp.message(StateFilter(FSMMovieByGenre.get_movies_by_genre))
async def movie_by_genre(message: types.Message, state: FSMContext):
    await message.answer('Ну тут я еще не доделала')



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
