from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
import asyncio
from datetime import datetime

from aiogram import F

from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp['start_time'] = datetime.now()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Hello, <b>{message.from_user.full_name}</b>',
                         parse_mode=ParseMode.HTML)


@dp.message(Command('keyboard'))
async def keyboard_buttons(message: types.Message):
    kb = [
        [types.KeyboardButton(text='yes')],
        [types.KeyboardButton(text='no')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f'Hello, choose one', reply_markup=keyboard)


async def message_reply(message: types.Message):
    await message.reply('reply haha')


dp.message.register(message_reply, Command('test'))


@dp.message(Command('time'))
async def bot_start_time(message: types.Message, start_time: str):
    await message.answer(str(dp['start_time']))
    await message.answer(f'Bot started at {start_time}')


@dp.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
