"BOT GA KANALGA QOSHILISHINI YUBORISH AGAR JOIN BOLMASA BOT ISHLAMIDI JOIN BOLSAGINA KANAL ISHGA TUSHADI"
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis_dict import RedisDict

TOKEN = '6839903315:AAEAThMFk2rFE3ja229EKrxfT-cANlS02e0'

dp = Dispatcher()

users_in_channels = RedisDict()

CHANNEL_IDS = [-1002124192341, -1002045673840, -1002025286923]


async def check_member_of_channel(user_id, bot: Bot, CHANNEL_ID) -> bool:
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)


async def check_member_of_channels(user_id, bot: Bot) -> bool:
    is_in_channel = True
    for i in CHANNEL_IDS:
        if not await check_member_of_channel(user_id, bot, i):
            is_in_channel = False
    return is_in_channel


async def inline_keyboards(message: Message):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='1 - Kanal', url='https://t.me/kanal_1_obuna'))
    ikb.row(InlineKeyboardButton(text='2 - Kanal', url='https://t.me/kanal_2_obuna'))
    ikb.row(InlineKeyboardButton(text='3 - Kanal', url='https://t.me/kanal_3_obuna'))
    ikb.row(InlineKeyboardButton(text='Tasdiqlash', callback_data='tasdiqlash'))
    await message.answer('Kanallarag obuna boling', reply_markup=ikb.as_markup())


@dp.message(CommandStart())
async def check_messages(message: Message, bot: Bot):
    if message.from_user.id not in users_in_channels or not await check_member_of_channels(message.from_user.id, bot):
        await inline_keyboards(message)


@dp.callback_query(F.data.startswith('tasdiqlash'))
async def check_messages(callback_query: CallbackQuery, bot: Bot):
    is_in_channel = await check_member_of_channels(callback_query.from_user.id, bot)
    if is_in_channel:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await callback_query.answer('Tasdiqlandi')
        users_in_channels[str(callback_query.from_user.id)] = True
    else:
        await callback_query.answer('Tasdiqlanmadi')


@dp.message()
async def messages(message: Message, bot: Bot):
    if message.from_user.id not in users_in_channels or not await check_member_of_channels(message.from_user.id, bot):
        await inline_keyboards(message)


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
