import requests
from bs4 import BeautifulSoup
import os
import random
import csv


class HTMLParser:
    def __init__(self, position: str, search_period: str, schedule: str, content_path: str ="page.html") -> None:
        """
        Инициализация парсера
        :param position: Ключевое слово (позиция) для поиска
        :param search_period: Период для поиска
        :param schedule: График работы для поиска
        """
        self.position = position
        self.search_period = search_period
        self.schedule = schedule
        self.key_skills = {}
        self.url = self.get_url()
        self.path = content_path
        self.soup = None
        self.headers = self.set_user_agent()

    def set_user_agent(self, filename: str ="user-agents.txt") -> dict:
        """
        Устанавливает пользовательский User-Agent для запросов
        :param filename: путь к файлу с useragents
        :return: словарь заголовка с рандомным User-Agent из файла, или User-Agent по умолчанию, если нет файла
        """
        try:
            with open(filename, "r") as file:
                useragents = []
                for agent in file:
                    useragents.append(agent.strip())
                headers = {"User-Agent": random.choice(useragents)}
                return headers
        except FileNotFoundError:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            return headers

    def get_url(self) -> str:
        """Формирует URL для запроса по введенным пользователем данным"""
        url = f"https://hh.ru/search/vacancy?text={self.position}&search_period={self.search_period}&schedule={self.schedule}"
        return url

    def fetch_content(self) -> None:
        """Загружает HTML-контент по указанному URL и сохраняет его в файл"""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            content = response.text
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Содержимое страницы сохранено в файл {self.path}")
        except requests.RequestException as e:
            print(f"Ошибка при загрузке контента: {e}")

    def parse_load_content(self) -> None:
        """Загружает HTML-контент из локального файла и парсит его, сохраняя soup"""
        if not os.path.exists(self.path):
            print(f"Файл {self.path} не найден.")
            return
        with open(self.path, "r", encoding="utf-8") as file:
            content = file.read()
            self.soup = BeautifulSoup(content, "lxml")
        print(f"Файл {self.path} успешно загружен и распарсен")

    def find_links_by_class(self) -> list:
        """находит ссылки по заданному CSS-классу на основной странице"""
        if self.soup is None:
            print("Контент ещё не распарсен")

        return [a['href'] for a in self.soup.find_all('a', attrs={'data-qa': 'serp-item__title'})]

    def fetch_data_from_links(self, links: list) -> None:
        """Переходит по каждой ссылке и извлекает данные по заданному классу, сохраняя названия навыков и количество их упоминания в key_skills"""
        for link in links:
            try:
                print(f"Переход по ссылке: {link}")
                response = requests.get(link, headers=self.headers)
                response.raise_for_status()
                page_soup = BeautifulSoup(response.text, "lxml")
                finded_li = page_soup.find_all('li', attrs={'data-qa': 'skills-element'})
                for li in finded_li:
                    children = list(li.children)
                    finded_skill = children[0].find("div", class_="magritte-tag__label___YHV-o_3-0-21").text
                    if finded_skill in self.key_skills:
                        self.key_skills[finded_skill] += 1
                    else:
                        self.key_skills[finded_skill] = 1
            except requests.RequestException as e:
                print(f"Ошибка при переходе по ссылке {link}: {e}")

    def save_to_csv(self) -> None:
        """Сохраняет данные в файл CSV, сортируя навыки по частоте упоминания"""
        sorted_key_skills = sorted(self.key_skills.items(), key=lambda item: item[1], reverse=True)

        with open(f"key_skills_for_{self.position}.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Skill", "Count of repetitions"])

        for skill in sorted_key_skills:
            with open(f"key_skills_for_{self.position}.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(skill)

