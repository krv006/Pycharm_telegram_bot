from aiogram import Router, html, Bot, F
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.handlers import CallbackQueryHandler
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

main_router = Router()


@main_router.message((F.text.startswith('secret ')) & (F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP})))
async def count_command(message: Message):
    text = ' '.join(message.text.split(' ')[1:])
    if message.entities[0].type == 'text_mention':
        user = message.entities[0].user
        username = user.mention_markdown(user.full_name)
        user_id = user.id
        parse_mode = ParseMode.MARKDOWN_V2
    else:
        username = message.text.split(' ')[1]
        user_id = username
        parse_mode = None

    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text='Show message', callback_data=f'secret_|--|{text}|--|{user_id}'))
    await message.answer(f'Maxsus xabar bor {username}', reply_markup=ikb.as_markup(), parse_mode=parse_mode)


@main_router.callback_query(F.data.startswith('secret_'))
async def count_command(callback: CallbackQuery):
    text = callback.data[11:]
    user_id = text.split('|--|')[-1]
    if not user_id.isdigit() and '@' + callback.from_user.username == user_id or str(callback.from_user.id) == user_id:
        text = text[len(user_id):-len(user_id) - 4]
        await callback.answer(text, show_alert=True)
    else:
        await callback.answer('Xabar sizgamas!', show_alert=True)