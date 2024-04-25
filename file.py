



async def send_to_admins(msg: Message, text: str, bot: Bot):
    for admin in ADMINS:
        await bot.send_message(admin, f'{text} ({msg.from_user.id} - {msg.from_user.first_name})')


# @dp.message((F.text == '/start') & (F.chat.type == ChatType.PRIVATE))
@dp.message(Command(commands='id'))  # /id
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))


@dp.message(F.content_type.in_({ContentType.CONTACT, ContentType.LOCATION}))
async def command_start_handler(message: Message, bot: Bot) -> None:
    if message.content_type == ContentType.CONTACT:  # contact
        await send_to_admins(message, message.contact.phone_number, bot)
    else:  # location
        text = f'{message.location.latitude} {message.location.longitude}'
        await send_to_admins(message, text, bot)


async def on_startup(bot: Bot) -> None:
    print('Bot started!')
    command_list = [
        BotCommand(command='/start', description="Botni boshlash"),
        BotCommand(command='/id', description="O'zimizni id ko'rish"),
    ]
    await bot.set_my_commands(command_list)


async def on_shutdown(bot: Bot) -> None:
    print('Bot stopped!')

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)