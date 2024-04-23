import os
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


class Video_from(StatesGroup):
    link = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.add_user_db(message.from_user.id)
    text = 'Salom hush kelibsiz bizning botimizga!!!'
    await message.answer(text)


@dp.message(Video_from.link)
async def video_from(message: Message):
    ...