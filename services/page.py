import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    "User-Agent": ua.random
}

hubs = ["programming", "popular_science", "artificial_intelligence", "history", "python", "maths", "gamedev"]


# def get_page(hub: str, period: str) -> str | None:
#     url = f"https://habr.com/ru/hub/{hub}/top/{period}/"
#     try:
#         response = requests.get(url, "html.parser", headers=headers).text
#
#         soup = BeautifulSoup(response, features="html.parser")
#         h2_element = soup.find("h2")
#         if h2_element:
#             link = h2_element.find("a");
#             if link:
#                 page = link.get("href")
#                 return "https://habr.com" + page
#         return  None
#     except Exception as E:
#         print(f"error - {E}")
#         return None


