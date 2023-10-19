# This is a parser with which you can get an ordered list of key skills for the position you are looking for

import requests
from bs4 import BeautifulSoup
import os
import random
import csv


position = "junior devops" # position
position = "+".join(position.split())

vacancies = []
key_skills = {}

useragents = open("user-agents.txt").read().strip().split("\n")
headers = {"User-Agent": random.choice(useragents)}

os.mkdir("vacancies/")

def get_html():
    url = f"https://hh.ru/search/vacancy?text={position}&search_period=7&schedule=remote"

    r = requests.get(url, headers=headers)
    src = r.text
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(src)


def get_skills(title):
    with open(f"vacancies/{title}.html", encoding="utf-8") as f:
        src = f.read()
        soup = BeautifulSoup(src, "lxml")
        skills = soup.find_all("span", class_="bloko-tag__section bloko-tag__section_text")
        for s in skills:
            skill = s.text
            if skill in key_skills:
                key_skills[skill] += 1
            else:
                key_skills[skill] = 1


def get_data():
    with open("page.html", encoding="utf-8") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    links_to_vacancies = soup.find_all("a", class_="serp-item__title")

    for l in links_to_vacancies:
        link = l.get("href")
        r = requests.get(link, headers=headers)
        src = r.text
        soup = BeautifulSoup(src, "lxml")
        title = soup.find("h1").text

        list_of_files = os.listdir(path="vacancies/")
        if title in list_of_files:
            title = title + "_" + str(len(list_of_files))

        for ch in title:
            if ch in "\\:|\"*?<>/":
                title = title.replace(ch, "")

        vacancies.append(title)
        with open(f"vacancies/{title}.html", "w", encoding="utf-8") as f:
            f.write(src)

        get_skills(title)


def data_to_csv():
    sorted_key_skills = sorted(key_skills.items(), key=lambda item:item[1], reverse=True)

    with open(f"key_skills_for_{position}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Skill", "Count of repetitions"])

    for skill in sorted_key_skills:
        with open(f"key_skills_for_{position}.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(skill)


def main():
    # proxies = open("proxy.txt").read().strip().split("\n")
    # proxy = {"https": "https://" + random.choice(proxies)}

    get_html()
    get_data()
    data_to_csv()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

