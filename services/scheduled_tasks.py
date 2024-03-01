import schedule
import asyncio
from aiogram import Bot
from datetime import datetime, timedelta
from services.send_message import send_message

async def scheduled_messages(bot: Bot):
    schedule.every().day.at("19:00").do(lambda: asyncio.create_task(send_message(bot, "daily")))
    schedule.every().sunday.at("15:00").do(lambda: asyncio.create_task(send_message(bot, "weekly")))

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

