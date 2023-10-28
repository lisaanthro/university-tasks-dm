import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart

from keys import TOKEN

dp = Dispatcher()
bot = Bot(TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message):
    await message.answer(f'Hello {message.from_user.full_name}')


@dp.message()
async def echo_handler(message):
    await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
