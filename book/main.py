import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, \
    InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
ADMIN = 6126220359


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    rkb = ReplyKeyboardBuilder()
    rkb.row(KeyboardButton(text='📚 Kitoblar'))
    rkb.row(KeyboardButton(text='📃 Mening buyurtmalarim'))
    rkb.row(KeyboardButton(text='🔵 Biz ijtimoyi tarmoqlarda'), KeyboardButton(text='📞 Biz bilan bog\'lanish'))
    await message.answer(text='Assalomu alaykum! Tanlang.', reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer('''Buyruqlar: 
/start - Botni ishga tushirish
/help - Yordam''')


@dp.message(F.text == '📚 Kitoblar')
async def books(message: Message) -> None:
    ikb = InlineKeyboardBuilder()
    # ikb.add(InlineKeyboardButton(text='⚡️ IKAR', callback_data='ikar'), InlineKeyboardButton(text='📚 Factor books kitoblari'))
    # ikb.add(InlineKeyboardButton(text='💸 Biznes kitoblar'), InlineKeyboardButton(text='☪️ Diniy kitoblar'))
    # ikb.add(InlineKeyboardButton(text='📚 Boshqa kitoblar'), InlineKeyboardButton(text='🔮 Psihologik kitoblar'))
    # ikb.add(InlineKeyboardButton(text='👨‍👩‍👧‍👦 Tarbiyaviy-oilaviy kitoblar'),
    #         InlineKeyboardButton(text='🇹🇷 Turk badiy-mar\'ifiy kitoblar'))
    # ikb.add(InlineKeyboardButton(text='📚 Badiy Ramanlar'), InlineKeyboardButton(text='📚 Qissa va Romanlar'))
    # ikb.add(InlineKeyboardButton(text='📚 Badiy kitoblar va Qissalar'),
    #         InlineKeyboardButton(text='🔮 Psihologik kitoblar'))
    ikb.row(
        InlineKeyboardButton(text='⚡️IKAR', callback_data='ikar'),
        InlineKeyboardButton(text='📚Factor books kitoblar', callback_data='factor_books')
    )
    ikb.row(
        InlineKeyboardButton(text='💸Biznes kitoblar', callback_data='biznes_kitoblar'),
        InlineKeyboardButton(text='☪️Diniy kitoblar', callback_data='diniy_kitoblar')
    )
    ikb.row(
        InlineKeyboardButton(text='📚Boshqa kitoblar', callback_data='boshqa_kitoblar'),
        InlineKeyboardButton(text='🔮Psixologik kitoblar', callback_data='psixologik_kitoblar')
    )
    ikb.row(
        InlineKeyboardButton(text='👨‍👩‍👧‍👦Tarbiyavi-oilaviy kitoblar', callback_data='tarbiyavi_oilaviy_kitoblar'),
        InlineKeyboardButton(text='🇹🇷Turk badiiy-ma\'rifiy kitoblar', callback_data='turk_badiiy_ma_rifiy_kitoblar')
    )
    ikb.row(
        InlineKeyboardButton(text='📚Badiiy kitoblar', callback_data='badiiy_kitoblar'),
        InlineKeyboardButton(text='📚Qissa va Ramanlar', callback_data='qissa_va_ramanlar')
    )
    ikb.row(
        InlineKeyboardButton(text='🔍Qidirish', callback_data='inline_mode'),
    )

    await message.answer('Kategoriyalardan birini tanlang', reply_markup=ikb.as_markup())


@dp.callback_query()
async def callback_query(callback: CallbackQuery) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text="IKAR to'plami", callback_data="ikarlar"),
            InlineKeyboardButton(text='◀️Orqaga', callback_data='orqaga'))
    if callback.data == 'ikar':
        await callback.message.edit_text('⚡️ IKAR', reply_markup=ikb.as_markup())


@dp.message(Command(commands='id'))  # /id
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))


@dp.message(F.text == "IKAR to'plami")
async def ikar(message: Message):
    await message.answer()


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
