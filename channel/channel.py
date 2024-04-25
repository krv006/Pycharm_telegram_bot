import asyncio
import logging
from redis_dict import RedisDict
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, BotCommand, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from middleware import UserAddMiddleware
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

ADMIN_IDS = 1305675046

TOKEN = '6839903315:AAEAThMFk2rFE3ja229EKrxfT-cANlS02e0'

# CHANNEL_IDS = [-1002124192341, -1002084653626, -1002045673840, -1002025286923]
CHANNEL_IDS = {-1002124192341: {'name': 'Prosta', 'url': 'https://t.me/kanal_1_obuna'},
               -1002045673840: {'name': 'Prosta2', 'url': 'https://t.me/kanal_2_obuna'},
               -1002025286923: {'name': 'Prosta3', 'url': 'https://t.me/kanal_3_obuna'},
               -1002025286923: {'name': 'RV', 'url': 'https://t.me/rv_006'}}

redis_dict = RedisDict()
# redis_dict.clear()
print(redis_dict)
dp = Dispatcher()
ADMINS = [1305675046]


class Addchannel(StatesGroup):
    id_ = State()


# async def inline_keyboards(message: Message):
#     ikb = InlineKeyboardBuilder()
#     ikb.row(InlineKeyboardButton(text='1 - Kanal', url='https://t.me/kanal_1_obuna'))
#     ikb.row(InlineKeyboardButton(text='2 - Kanal', url='https://t.me/kanal_2_obuna'))
#     ikb.row(InlineKeyboardButton(text='3 - Kanal', url='https://t.me/kanal_3_obuna'))
#     ikb.row(InlineKeyboardButton(text='4 - Kanal', url='https://t.me/rv_006'))
#     ikb.row(InlineKeyboardButton(text='Tasdiqlash', callback_data='tasdiqlash'))
#     await message.answer('Kanallarag obuna boling', reply_markup=ikb.as_markup())


@dp.message(Command(commands='id'))  # /id
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if str(message.chat.id) in str(ADMINS):
        ikb = InlineKeyboardBuilder()
        ikb.add(InlineKeyboardButton(text="ADMIN", callback_data="admin"),
                InlineKeyboardButton(text="TABRIKLAYMAN", callback_data="tabrik")),
        await message.answer('SIZ ADMINSIZ', reply_markup=ikb.as_markup())
    else:
        rkb = ReplyKeyboardBuilder()
        rkb.add(KeyboardButton(text="Siz admin emassiz"), KeyboardButton(text="ADMINbolishingiz kerak"))
        await message.answer(text='SIZ ADMIN BOLISHGA XARKAT QILING', reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(Command(commands='add'))
async def add_chanel_id(message: Message, state: FSMContext) -> None:
    if str(message.chat.id) in str(ADMINS):
        await message.answer(text="Kanal id sini kiriting!!!")
        await state.set_state(Addchannel.id_)
    else:
        await message.answer(text='Siz admin emassiz bu funksiya faqat admin uchun')


@dp.message(Addchannel.id_)
async def command_id(message: Message) -> None:
    try:
        if int(message.text) in CHANNEL_IDS:
            await message.answer("Bunday id li kanal bizning bazamizda bor !!!")
        elif int(message.text) not in CHANNEL_IDS:
            redis_dict[message.text] = True
            await message.answer(text="Kanaldi bazaga saqlab oldik")
        else:
            await message.answer("id da xatolik bor")
    except ValueError:
        await message.answer("INT tipida xato bor")


@dp.message(Command(commands='channels'))
async def add_chanel_id(message: Message) -> None:
    if str(message.chat.id) in str(ADMINS):
        ikb = InlineKeyboardBuilder()
        ikb.row(InlineKeyboardButton(text="Nomi", callback_data="nomi"),
                InlineKeyboardButton(text='id', callback_data="id"),
                InlineKeyboardButton(text="url", callback_data="url"),
                InlineKeyboardButton(text="Bekor qilish", callback_data="change-iks")
                )
        ikb.row(InlineKeyboardButton(text="Prosta", callback_data="nomi"),
                InlineKeyboardButton(text='-1002124192341', callback_data="id"),
                InlineKeyboardButton(text="url", url='https://t.me/kanal_1_obuna'),
                InlineKeyboardButton(text="❌", callback_data="change-iks")
                )
        ikb.row(InlineKeyboardButton(text="Prosta2", callback_data="nomi"),
                InlineKeyboardButton(text='-1002084653626', callback_data="id"),
                InlineKeyboardButton(text="url", url='https://t.me/kanal_2_obuna'),
                InlineKeyboardButton(text="❌", callback_data="change-iks")
                )
        ikb.row(InlineKeyboardButton(text="Prosta3", callback_data="nomi"),
                InlineKeyboardButton(text='-1002045673840', callback_data="id"),
                InlineKeyboardButton(text="url", url='https://t.me/kanal_3_obuna'),
                InlineKeyboardButton(text="❌", callback_data="change-iks")
                )
        ikb.row(InlineKeyboardButton(text="rv", callback_data="rv"),
                InlineKeyboardButton(text='-1002025286923', callback_data="id"),
                InlineKeyboardButton(text="url", url='https://t.me/rv_006'),
                InlineKeyboardButton(text="❌", callback_data="change-iks")
                )
        await message.answer('Kanallarag obuna boling', reply_markup=ikb.as_markup())
    else:
        await message.answer(text='Siz admin emassiz bu funksiya faqat admin uchun')


@dp.callback_query(F.data.startswith('change'))
async def iks(callback_data: CallbackQuery):
    ...


async def on_startup(bot: Bot) -> None:
    print('Bot started!')
    command_list = [
        BotCommand(command='/start', description="Botni boshlash"),
        BotCommand(command='/id', description="O'zimizni id ko'rish"),
        BotCommand(command='/add', description="Admin uchun command"),
        BotCommand(command='/channels', description="Admin uchun command"),

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
