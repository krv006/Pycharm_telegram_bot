import asyncio
import logging
from redis_dict import RedisDict
import sys
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from middleware import UserAddMiddleware

ADMIN_IDS = 1305675046

TOKEN = '6839903315:AAEAThMFk2rFE3ja229EKrxfT-cANlS02e0'

CHANNEL_IDS = [-1002124192341, -1002084653626, -1002045673840, -1002025286923]

redis_dict = RedisDict()

dp = Dispatcher()
ADMIN = 1305675046


@dp.message(Command(commands='id'))  # /id
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))


async def inline_keyboards(message: Message):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='1 - Kanal', url='https://t.me/kanal_1_obuna'))
    ikb.row(InlineKeyboardButton(text='2 - Kanal', url='https://t.me/kanal_2_obuna'))
    ikb.row(InlineKeyboardButton(text='3 - Kanal', url='https://t.me/kanal_3_obuna'))
    ikb.row(InlineKeyboardButton(text='4 - Kanal', url='https://t.me/rv_006'))
    ikb.row(InlineKeyboardButton(text='Tasdiqlash', callback_data='tasdiqlash'))
    await message.answer('Kanallarag obuna boling', reply_markup=ikb.as_markup())


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if str(message.chat.id) in str(ADMIN):
        ikb = InlineKeyboardBuilder()
        ikb.add(InlineKeyboardButton(text="ADMIN", callback_data="admin"),
                InlineKeyboardButton(text="TABRIKLAYMAN", callback_data="tabrik")),
        await message.answer('SIZ ADMINSIZ', reply_markup=ikb.as_markup())
    else:
        rkb = ReplyKeyboardBuilder()
        rkb.add(KeyboardButton(text="Siz admin emassiz"), KeyboardButton(text="ADMINbolishingiz kerak"))
        await message.answer(text='SIZ ADMIN BOLISHGA XARKAT QILING', reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(Command(commands='add'))
async def add_chanel_id(message: Message) -> None:
    if str(message.chat.id) in str(ADMIN):
        ...
    else:
        await message.answer(text='Siz admin emassiz')


@dp.message(Command(commands='channels'))
async def add_chanel_id(message: Message) -> None:
    if str(message.chat.id) in str(ADMIN):
        ...
    else:
        await message.answer(text='Siz admin emassiz')


async def main() -> None:
    bot = Bot(TOKEN)
    dp.update.middleware(UserAddMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
