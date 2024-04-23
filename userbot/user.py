import json
import logging
import os
import sys
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv("BOT_TOKEN")
ADMIN = os.getenv("ADMIN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer('Ismingizni kiriting: ')


@dp.message(F.text == '/count')
async def admin_handler(message: Message):
    if message.from_user.id == ADMIN:
        with open('users.json') as f2:
            user_data = json.load(f2)
        await message.answer(f"O'quvchilar soni {len(user_data)}")


@dp.message()
async def command_start(message: Message):
    await message.answer(message.text)
    with open('users.json') as f1:
        d = json.load(f1)
        d[str(message.from_user.id)] = message.text
    with open('users.json', 'w') as f:
        json.dump(d, f, indent=3)


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
