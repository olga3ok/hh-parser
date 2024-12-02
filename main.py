from parser import HTMLParser


def main():
    position = input("Введите ключевое слово для поиска: ").strip()
    search_period = input("Введите период для поиска вакансий (количество дней): ").strip()
    choice_schedule = int(input("Какой график работы? (0 - удаленная, 1 - полный день): ").strip())
    schedule = ["remote", "fullDay"][choice_schedule]
    position = "+".join(position.split())

    # Инициализация и запуск парсера
    parser = HTMLParser(position, search_period, schedule)
    parser.fetch_content()
    parser.parse_load_content()

    # Поиск ссылок по CSS-классу
    links = parser.find_links_by_class()
    print(f"Найдено {len(links)} ссылок.")

    # Извлечение данных с дочерних страниц
    parser.fetch_data_from_links(links)

    # Сохранение данных в CSV
    parser.save_to_csv()


if __name__ == '__main__':
    main()
