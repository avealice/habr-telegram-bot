from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start",
                   description="Start"),
        BotCommand(command="/help",
                   description="О боте"),
    ]

    await bot.set_my_commands(main_menu_commands)