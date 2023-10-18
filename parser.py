# This is a parser with which you can get an ordered list of key skills for the position you are looking for

import requests
from bs4 import BeautifulSoup
import os
import random


position = "junior devops"
position = "+".join(position.split())


def get_html():
    url = f"https://hh.ru/search/vacancy?text={position}&search_period=7&schedule=remote"

    useragents = open("user-agents.txt").read().strip().split("\n")
    headers = {"User-Agent": random.choice(useragents)}

    r = requests.get(url, headers=headers)
    text = r.text
    with open("page.html", "w") as f:
        f.write(text)


def main():
    proxies = open("proxy.txt").read().strip().split("\n")

    proxy = {"https": "https://" + random.choice(proxies)}

    get_html()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

