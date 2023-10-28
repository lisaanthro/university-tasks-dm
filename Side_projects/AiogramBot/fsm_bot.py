from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, PhotoSize)

from keys import TOKEN

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(storage=storage)

user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillFrom(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    upload_photo = State()
    fill_education = State()
    fill_wish_news = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот демонстрирует работу FSM.\n'
             'Для перехода к заполнению анкеты отправьте команду /fillform'
    )