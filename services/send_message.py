from aiogram import Bot

import asyncio

# from services.page import get_page
from database.database import DataBase
from lexicon.lexicon import hubs
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    "User-Agent": ua.random
}

db = DataBase("database/db2.db")

async def send_message(bot: Bot, period: str):
    users_id = db.get_users()
    pages = await parse_habr(period)

    for user_id in users_id:
        if period == "Daily":
            await bot.send_message(user_id[0], "ТОП СТАТЬИ ЭТОГО ДНЯ")
        else:
            await bot.send_message(user_id[0], "ТОП СТАТЬИ ЭТОЙ НЕДЕЛИ")
        subscriptions = db.get_subscribtions(user_id[0])
        for subscription in subscriptions:
            if pages[subscription[0]]:
                articles_str = '\n'.join(map(str, pages[subscription[0]]))
                await bot.send_message(user_id[0], f'Хаб <b>{subscription[0]}</b>:\n\n{articles_str}')
                await asyncio.sleep(5)

async def parse_habr(period: str) -> dict:
    pages = {hub: set() for hub in hubs}
    for hub in pages:
        page = await get_page(hub, period)
        if page:
            pages[hub].add(page)
    return pages

# async def parse_habr_daily() -> dict:
#     pages = {hub: set() for hub in hubs}
#     for hub in pages:
#         page = await get_page(hub, "daily")
#         if page:
#             pages[hub].add(page)
#     return pages
#
# async def parse_habr_weekly() -> dict:
#     pages = {hub: set() for hub in hubs}
#     for hub in pages:
#         page = await get_page(hub, "weekly")
#         if page:
#             pages[hub].add(page)
#     return pages

async def get_page(hub: str, period: str) -> str | None:
    url = f"https://habr.com/ru/hub/{hub}/top/{period}/"
    try:
        response = requests.get(url, headers=headers, timeout=5).text
        soup = BeautifulSoup(response, features="html.parser")
        h2_element = soup.find("h2")
        if h2_element:
            link = h2_element.find("a")
            if link:
                page = link.get("href")
                return "https://habr.com" + page
        return None
    except Exception as E:
        print(f"error - {E}")
        return None
