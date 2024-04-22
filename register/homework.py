import asyncio
import logging
import os
import sys
import json
import pandas as pd
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, BotCommand, \
    InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from dotenv import load_dotenv
from email_send import send_emails
from send_xlsx import send_xlsx_gmail

load_dotenv('.env')
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
to_email = ["rvkamronbek@gmail.com", "rvkamronbek@gmail.com"]


class Form(StatesGroup):
    ism = State()
    familya = State()
    age = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await add_user_db(message)
    await state.set_state(Form.ism)
    text = ('<b>Xush kelibsiz!</b>\n'
            '<em>Ismingizni kiriting👇🏻</em>')
    await message.answer(text)


# @dp.message(Command(commands='stop'))
# async def on_shutdown(message: Message) ->None:
#     await dp.stop_polling()

@dp.message(Form.ism)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(ism=message.text)
    await state.set_state(Form.familya)
    await message.answer('<em>Familiyangizni kiriting👇🏻</em>')


@dp.message(Form.familya)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(familya=message.text)
    await state.set_state(Form.age)
    await message.answer('<em>Yoshingizni kiriting</em>')


@dp.message(Form.age)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    data = await state.get_data()
    text = f'''
<em>Ma'lumotlaringniz to'grimi</em>:
<em>Ism</em>: {data["ism"]}
<em>Familya</em>: {data["familya"]}
<em>Age</em>: {data["age"]}
'''
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text='Xa ✅', callback_data='confirm'),
        InlineKeyboardButton(text='Yoq ❌', callback_data='cancel'),
    )

    await message.answer(text, reply_markup=ikb.as_markup())


@dp.callback_query()
async def confirm_callback_handler(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.data == 'confirm':
        data = await state.get_data()
        await state.clear()
        text = f'''
<b>Malumotlaringniz👇🏻</b>
<em>Ism</em>: {data.get("ism")}
<em>Familya</em>: {data.get("familya")}
<em>Age</em>: {data.get("age")}
'''
        await bot.edit_message_text(text, callback.from_user.id, callback.message.message_id)
        rkb = ReplyKeyboardBuilder()
        rkb.add(KeyboardButton(text="Telefon raqam jo'natish 👈🏻", request_contact=True))
        await callback.message.answer('<em>Telefon raqamingizni yuboring👇🏻</em>',
                                      reply_markup=rkb.as_markup(resize_keyboard=True))
        database[callback.from_user.id].update(data)
    else:
        await callback.message.delete()
        await callback.answer("Malumotlaringiz o'chirildi✅", show_alert=True)


database = {}


async def add_user_db(msg: Message):
    database[msg.from_user.id] = {
        'first_name': msg.from_user.first_name,
        'last_name': msg.from_user.last_name,
        'username': msg.from_user.username,
    }


async def add_user_phone_db(msg: Message):
    user = database[msg.from_user.id]
    user['phone'] = msg.contact.phone_number
    database[msg.from_user.id] = user


@dp.message(F.content_type == ContentType.CONTACT)
async def contact_handler(message: Message) -> None:
    await add_user_phone_db(message)
    await message.answer("Raqamingiz ro'yxatga olindi ✅", parse_mode=ParseMode.HTML.MARKDOWN_V2)
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="Joylashgan O'rningizni jo'natish📍", request_location=True))
    await message.answer("Joylashgan o'rningizni yuboring👇🏻", reply_markup=rkb.as_markup(resize_keyboard=True))


def write_json(data: dict) -> None:
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=2)

    with open('users.json', 'r') as file:
        json_data = json.load(file)

    rv = pd.DataFrame.from_dict(json_data, orient='index')

    rv.to_excel('rv.xlsx', index_label='User ID')



@dp.message(F.content_type == ContentType.LOCATION)
async def location_handler(message: Message) -> None:
    user = database[message.from_user.id]
    user['location'] = f'{message.location.latitude} {message.location.longitude}'
    database[message.from_user.id] = user
    rkb = ReplyKeyboardRemove()
    await message.answer(text="||Joylashgan o'rningiz ro'yxatga saqlandi✅||", reply_markup=rkb,
                         parse_mode=ParseMode.HTML.MARKDOWN_V2)
    write_json(database)
    send_emails(to_email)
    send_xlsx_gmail(to_email)


async def on_startup(bot: Bot) -> None:
    command_list = [
        BotCommand(command='/start', description='Botni ishga tushirish'),
        BotCommand(command='/stop', description="Bo'tni to'xtatish")
    ]
    await bot.set_my_commands(command_list)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

'''

1. easy
# /start
# database ga userlarni qoshish kk
# 
# 
# telegram_id, first_name, last_name, username, phone(button), ism, familya, yoshi, manzili(button)
# database ga saqlandi


/email  (faqat admin uchun)
adminlarni ozini pochtasiga userlarni json file ni yuborsin


2. medium
xlsx


3. hard
google sheet ga userlarni yuklash kk


docker, redis                              

blockchain                                           
TON                                                  


python                                               
backend                                              

devops                                               
blockchain                                           
AI                                                   


'''
