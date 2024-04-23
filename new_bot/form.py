import types
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
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
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, BotCommand, \
    InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from dotenv import load_dotenv

class Form(StatesGroup):
    ism = State()
    familya = State()
    age = State()


form_router = Router()


@form_router.message()
async def form(message: types.Message):
    await message.answer
