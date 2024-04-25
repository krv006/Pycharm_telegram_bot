import os

from aiogram import Bot, F, Router
from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

config_router = Router()

load_dotenv('../.env')

TOKEN='7199941527:AAH-MfUWCY7Rb3nZBC5oGhaNX1tjzuSrouE'

CHANNEL_ID = -1002084653626


async def check_member_of_channel(message: Message, bot: Bot) -> bool:
    member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
    return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)


@config_router.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def check_messages(message: Message, bot: Bot):
    if not await check_member_of_channel(message, bot) and message.text == '/hello':
        await message.delete()
        text = message.from_user.mention_markdown(message.from_user.full_name)
        chat_invite_link = await bot.create_chat_invite_link(CHANNEL_ID, creates_join_request=True)
        ikb = InlineKeyboardBuilder()
        ikb.add(InlineKeyboardButton(text=f"Kanalga a'zo bo'lish", url=chat_invite_link.invite_link))
        await message.answer(f'Kanalga azo boling {text}', reply_markup=ikb.as_markup())