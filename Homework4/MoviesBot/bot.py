from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
import datetime
import json
from random import randint

from config_reader import config
from messages import genres

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
storage = MemoryStorage()


class FSMMovieByGenre(StatesGroup):
    get_movies_by_genre = State()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text='Фильм дня')],
        [types.KeyboardButton(text='Рекомендация по жанру')],
        [types.KeyboardButton(text='Случайный фильм')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Привет, я помогаю выбирать фильмы.\nВыбери одно: ', reply_markup=keyboard)


@dp.message(Command('cancel'), ~StateFilter(default_state))
async def process_cancel_state(message: types.Message, state: FSMContext):
    await message.answer(text='Возвращаемся в начало.')
    await state.clear()


def get_movies(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}


@dp.message(F.text == 'Фильм дня', StateFilter(default_state))
async def get_movie_of_the_day(message: types.Message, state: FSMContext):
    dp['today_date'] = datetime.date.today()
    await message.answer(f'Сегодняшняя дата: {dp["today_date"]}')
    movies_json = get_movies('movie_of_the_day.json')
    movie_id = dp['today_date'].weekday() % 3
    movie = movies_json.get(str(movie_id), 'Фильм дня недоступен')
    await message.answer(movie)
    await state.clear()


@dp.message(F.text == 'Случайный фильм')
async def get_random_movie(message: types.Message, state: FSMContext):
    movies_json = get_movies('random_movie.json')
    movie_id = randint(0, len(movies_json) - 1)
    print(movie_id)
    print(movies_json)
    movie = movies_json.get(str(movie_id), 'Случайный фильм недоступен')
    await message.answer(movie)
    await state.clear()


@dp.message(F.text == 'Рекомендация по жанру', StateFilter(default_state))
async def genre_choice(message: types.Message, state: FSMContext):
    genres_json = get_movies('movie_by_genre.json')
    kb = [[types.KeyboardButton(text=x)] for x in genres_json.keys()]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    await message.answer('Выберите жанр:', reply_markup=markup)
    await state.set_state(FSMMovieByGenre.get_movies_by_genre)


@dp.message(F.text.in_(genres), StateFilter(FSMMovieByGenre.get_movies_by_genre))
async def get_movie_by_genre(message: types.Message, state: FSMContext):
    genre = message.text
    movies_json = get_movies('movie_by_genre.json')
    movie = movies_json.get(genre, 'Фильм по жанру недоступен')
    await message.answer(movie, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@dp.message(StateFilter(FSMMovieByGenre.get_movies_by_genre))
async def warning_not_genre(message: types.Message):
    await message.answer('Пожалуйста, выберите из доступных жанров')


@dp.message(StateFilter(default_state))
async def send_echo(message: types.Message):
    await message.answer('Извините, такой команды нет.\nДля возвращения в начало нажмите /start\nДля отмены нажмите /cancel')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
