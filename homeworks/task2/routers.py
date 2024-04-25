from aiogram import Router
from handlers import main_router
from config import config_router
start_router = Router()

start_router.include_routers(
    main_router,
    config_router
)