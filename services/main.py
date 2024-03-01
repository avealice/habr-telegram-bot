from aiogram import Bot

import asyncio

# from services.page import get_page
from lexicon.lexicon import hubs
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    "User-Agent": ua.random
}


async def send_message(period: str):
    pages = await parse_habr(period)
    if period == "Daily":
        print("Топ статьи этого дня")
    else:
        print("Топ статьи этой недели")
    for hub in hubs:
        if pages[hub]:
            print(f'Хаб <b>"{hub}"</b>:\n\n{pages[hub]}')
            await asyncio.sleep(3)


async def parse_habr(period: str) -> dict:
    pages = {hub: set() for hub in hubs}
    for hub in pages:
        page = await get_page(hub, period)
        if page:
            pages[hub].add(page)
            print(f"{pages}: {page}")
    return pages


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

async def main():
    await send_message("Daily")
    await send_message("Weekly")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')