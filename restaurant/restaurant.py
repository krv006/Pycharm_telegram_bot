# chenal chat id
# mana shunib sorash
import asyncio
import logging
import sys
# from os import getenv
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile
from middleware import UserAddMiddleware
from settings import ADMIN_IDS
from untils.generate_keyboard import get_keyboard

# from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7137936324:AAHzBJQBQ_1zSCg52-Y41ypE9LdWHzVyIgA"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

router = Router()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if str(message.chat.id) in ADMIN_IDS:
        keyboard = [
            [KeyboardButton(text="Menu"), KeyboardButton(text="Menu qo'shish")],
            [KeyboardButton(text="Biz bilan bog'lanish")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="Menu"), KeyboardButton(text="Biz bilan bog'lanish")]
        ]

    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Xush kelibsiz, {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Menu")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Taomlar"), KeyboardButton(text="Ichimliklar"),
        KeyboardButton(text="Shirinliklar"),
        KeyboardButton(text="Salatlar"),
        KeyboardButton(text="Ovqatlar menu bo'limga qaytish")
    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Qanday ovqat xoxlaysiz , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Biz bilan bog'lanish")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("woman-call-center-icon-simple-style-vector-32225284.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Telefon:</b> +998902646366\n<b>Manzil:</b> Mirzo Ulug'bek tumani",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Taomlar")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Suyuq ovqatlar"),
        KeyboardButton(text="Quyuq ovqatlar"),
        KeyboardButton(text="Dietniy ovqatlar"),
        KeyboardButton(text="Gazaklar")

    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Qanday ovqat xoxlaysiz , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Suyuq ovqatlar")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Mastava"),
        KeyboardButton(text="Sho'rva"),
        KeyboardButton(text="Chuchvara"),
        KeyboardButton(text="Bo'rsh"),
        KeyboardButton(text="Ovqatlar menu bo'limga qaytish")
    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Suyuq taomlarimizdan birini tanlang , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Sho'rva")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("maxresdefault.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Sho'rva\n<b>Narxi:</b> 26 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Mastava")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("u-7752c7090092d0f5ec425a6113489eca.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Mastava\n<b>Narxi:</b> 26 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Chuchvara")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("201_1643971179-e1643971274658-1280x640.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Chuchvara\n<b>Narxi:</b> 26 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Bo'rsh")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("66296068-76ff-11ee-82f1-6a1532868e1f_49f1b34e_470e_11ee_80e3_061d5246dd39_cover_page.avif")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Bo'rsh\n<b>Narxi:</b> 26 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Quyuq ovqatlar")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Jarkob"),
        KeyboardButton(text="Shashlik"),
        KeyboardButton(text="Dimlama"),
        KeyboardButton(text="Beshbarmoq"),
        KeyboardButton(text="Ovqatlar menu bo'limga qaytish")
    ]
    kb = get_keyboard(keyboard, message, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Quyuq taomlarimizdan birini tanlang , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Jarkob")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("c84bff5fc9522d81ae8612cb6e31c3d7.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Jarkob\n<b>Narxi:</b> 1 kg 88 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Shashlik")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("stock-photo-bbq-meat-on-wooden-skewers-on-plate-top-view-flat-lay-614450792.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Shashlik\n<b>Narxi:</b> 1 donasi - 26 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Dimlama")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("zd.webp")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Dimlama\n<b>Narxi:</b> 26 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Beshbarmoq")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("beshm-698x540.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Beshbarmoq\n<b>Narxi:</b> 88 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Ichimliklar")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Gazli va Gazsiz"),
        # KeyboardButton(text="Gazsiz"),
        KeyboardButton(text="Soklar"),

    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Qanday ichimlik xoxlaysiz , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Gazli va Gazsiz")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Kola"),
        KeyboardButton(text="Fanta"),
        KeyboardButton(text="Sprite"),
        KeyboardButton(text="Pepsi"),
        KeyboardButton(text="Ovqatlar menu bo'limga qaytish")

    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Qanday ichimlik turini hoxlaysiz , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Kola")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("kola-3000h3000-scaled.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Kola\n<b>Narxi:</b> 14 000 ",
        parse_mode="HTML")
    print(msg)


@router.message(F.text == "Fanta")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("MAT_1360544_PCE_LV.webp")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Fanta\n<b>Narxi:</b> 14 000 ",
        parse_mode="HTML")


@router.message(F.text == "Sprite")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("sprite-1000ml-1.webp")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Sprite\n<b>Narxi:</b> 14 000 ",
        parse_mode="HTML")


@router.message(F.text == "Pepsi")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("44d00abe-766c-4b92-aedb-4840c48637bb.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Pepsi\n<b>Narxi:</b> 14 000 ",
        parse_mode="HTML")


@router.message(F.text == "Suv gazsiz")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("b8a1309a-ba53-48c7-bca3-9c36aab2338a-thumb.jpg")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Suv gazsiz\n<b>Narxi:</b> 5 000 ",
        parse_mode="HTML")


@router.message(F.text == "Suv gazli")
async def echo_handler(message: types.Message) -> None:
    photo = FSInputFile("by_bon-aqua_prod_17_750x750_v1.webp")
    msg = await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption="<b>Taom nomi:</b> Suv gazli\n<b>Narxi:</b> 5 000 ",
        parse_mode="HTML")


@router.message(F.text == "Salatlar")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Maynezli salatlar"),
        KeyboardButton(text="Maynezsiz salatlar"),
        KeyboardButton(text="Achiq salatlar"),

    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Qanday salat xoxlaysiz , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Shirinliklar")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Napaleon"),
        KeyboardButton(text="Tvarojni"),
        KeyboardButton(text="Chiscake"),
        KeyboardButton(text="Kurasan")

    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Qanday shirinlik xoxlaysiz , {message.from_user.full_name}",
                           reply_markup=markup)


@router.message(F.text == "Ovqatlar menu bo'limga qaytish")
async def echo_handler(message: types.Message) -> None:
    keyboard = [
        KeyboardButton(text="Taomlar"),
        KeyboardButton(text="Ichimliklar"),
        KeyboardButton(text="Shirinliklar"),
        KeyboardButton(text="Salatlar"),
        KeyboardButton(text="Ovqatlar menu bo'limga qaytish")
    ]
    kb = get_keyboard(keyboard, 2)
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Orqaga qaytdingiz, {message.from_user.full_name}",
                           reply_markup=markup)


async def main() -> None:
    dp.include_router(router)
    dp.update.middleware(UserAddMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
