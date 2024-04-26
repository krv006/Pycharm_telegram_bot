import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis_dict import RedisDict

from middleware import UserAddMiddleware

TOKEN = '6839903315:AAEAThMFk2rFE3ja229EKrxfT-cANlS02e0'
dp = Dispatcher()
ADMINS = 1305675046,

add_channels = RedisDict()
users_in_channels = RedisDict('users_in_channels')

CHANNEL_IDS = {-1002124192341: {'name': 'Prosta', 'url': 'https://t.me/kanal_1_obuna'},
               -1002045673840: {'name': 'Prosta2', 'url': 'https://t.me/kanal_2_obuna'},
               -1002025286923: {'name': 'Prosta3', 'url': 'https://t.me/kanal_3_obuna'}}


class StateForAddChannel(StatesGroup):
    id_ = State()


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
    await message.answer('Kanallarag obuna boling  👇', reply_markup=ikb.as_markup())


@dp.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    if message.from_user.id not in users_in_channels or not await check_member_of_channels(message.from_user.id, bot):
        await bot.delete_message(message.chat.id, message.message_id)
        await inline_keyboards(message)
    else:
        await message.answer('Sizga qanday yordam bera olaman')


@dp.message(Command(commands='add'))
async def add_chanel_id(message: Message, state: FSMContext) -> None:
    if message.chat.id in ADMINS:
        await message.answer('Channel idsini kiriting!')
        await state.set_state(StateForAddChannel.id_)
    else:
        await message.answer(text='Siz admin emassiz bu funksiya faqat admin uchun')


@dp.message(Command(commands='channels'))
async def print_channels(message: Message) -> None:
    if message.chat.id in ADMINS:
        ikb = InlineKeyboardBuilder()
        ikb.row(InlineKeyboardButton(text="Name 👇", callback_data="a"),
                InlineKeyboardButton(text="ID 👇", callback_data="a"),
                InlineKeyboardButton(text="URL 👇", callback_data="a"),
                InlineKeyboardButton(text='Ochirish 👇', callback_data="o"))
        for key, value in CHANNEL_IDS.items():
            ikb.row(InlineKeyboardButton(text=value['name'], url=value['url']),
                    InlineKeyboardButton(text=str(key), callback_data=value['name']),
                    InlineKeyboardButton(text='Url', callback_data=value['name']),
                    InlineKeyboardButton(text='❌', callback_data='remove_channel'))
        await message.answer('Sizda bor kannalar', reply_markup=ikb.as_markup())
    else:
        await message.answer('Siz admin emassiz')


@dp.callback_query(F.data.startswith('tasdiqlash'))
async def check_messages(callback_query: CallbackQuery, bot: Bot):
    is_in_channel = await check_member_of_channels(callback_query.from_user.id, bot)
    if is_in_channel:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await callback_query.answer('Tasdiqlandi')
        users_in_channels[str(callback_query.from_user.id)] = True
    else:
        await callback_query.answer('Tasdiqlanmadi')


@dp.message(StateForAddChannel.id_)
async def add_id(message: Message) -> None:
    try:
        if message.text in add_channels:
            await message.answer('Bu id bazada bor')
        elif int(message.text) in CHANNEL_IDS:
            add_channels[message.text] = CHANNEL_IDS[int(message.text)]
            await message.answer('Channelni bazaga saqladik!')
        else:
            await message.answer('Id da xatolik')
    except ValueError:
        await message.answer('Channel idisi faqat raqamlardan iborat')


@dp.message()
async def messages(message: Message, bot: Bot):
    if message.from_user.id not in users_in_channels or not await check_member_of_channels(message.from_user.id, bot):
        await bot.delete_message(message.chat.id, message.message_id)
        await inline_keyboards(message)


async def on_startup(bot: Bot) -> None:
    command_list = [
        BotCommand(command='/start', description="Botni boshlash"),
        BotCommand(command='/add', description="Faqat admin uchun"),
        BotCommand(command='/channels', description="Faqat admin uchun")
    ]
    await bot.set_my_commands(command_list)


dp.startup.register(on_startup)


async def main() -> None:
    bot = Bot(TOKEN)
    dp.update.middleware(UserAddMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
