import asyncio
import logging
from redis_dict import RedisDict
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


@dp.message(Command(commands='id'))  # /id
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))


@dp.message(F.text == '📚 Kitoblar')
async def books(message: Message) -> None:
    ikb = InlineKeyboardBuilder()
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


@dp.callback_query(F.data.endswith('ikar'))
async def callback_query(callback: CallbackQuery) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text="IKAR to'plami", callback_data="ikarlar"),
            InlineKeyboardButton(text="Savatcha", callback_data="savatcha")),
    ikb.add(InlineKeyboardButton(text="◀️Orqaga", callback_data="orqaga"))
    await callback.message.edit_text('⚡️ IKAR', reply_markup=ikb.as_markup())


@dp.callback_query(F.data.startswith("ikarlar"))
async def icar_count(callback: CallbackQuery):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="-", callback_data="change-minus"),
            InlineKeyboardButton(text="0", callback_data="ikar"),
            InlineKeyboardButton(text="+", callback_data="change-plus")
            )
    ikb.row(InlineKeyboardButton(text="◀️Orqaga", callback_data="ortga"))
    await callback.message.edit_text('⚡️ IKAR', reply_markup=ikb.as_markup())


data = RedisDict()
data["count"] = 0


# TERMINALDAN run qib qoyish kerak
# docker ps
# docker (redis/alpine) ga qarimiz xar doim
# docker start 71

@dp.callback_query(F.data.startswith("change"))
async def count_data(callback: CallbackQuery):
    if callback.data.endswith("plus"):
        data['count'] += 1
    else:
        data['count'] -= 1
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="-", callback_data="change-minus"),
            InlineKeyboardButton(text=str(data['count']), callback_data="count"),
            InlineKeyboardButton(text="+", callback_data="change-plus")
            )
    ikb.row(InlineKeyboardButton(text="◀️Orqaga", callback_data="ortga"))
    await callback.message.edit_text('⚡️ IKAR', reply_markup=ikb.as_markup())


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
