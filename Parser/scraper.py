# -*- coding: utf-8 -*-
"""
Quotes API Scraper
==================

Сайт quotes.toscrape.com/scroll втайне берёт данные с адреса
/api/quotes?page=N, который отдаёт готовый JSON. Мы обращаемся прямо туда —
это самый быстрый и надёжный способ, и тут даже не нужен BeautifulSoup.

Как найти такой "скрытый API" самому:
  1) открой сайт, нажми F12 -> вкладка Network -> фильтр Fetch/XHR;
  2) обнови страницу и смотри запросы, которые возвращают JSON;
  3) если в ответе твои данные — это и есть нужный адрес.

Запуск:
    pip install requests
    python scraper.py
"""

import csv
import json
import time

import requests

# Адрес "кухонного окошка". {} — место, куда подставим номер страницы.
API_URL = "https://quotes.toscrape.com/api/quotes?page={}"


def parse_quotes(data: dict) -> list[dict]:
    """Берёт JSON одной страницы и достаёт из него нужные поля."""
    quotes = []
    for q in data["quotes"]:           # в JSON есть список "quotes"
        quotes.append({
            "text": q["text"],
            "author": q["author"]["name"],   # автор лежит во вложенном объекте
            "tags": "; ".join(q["tags"]),    # список тегов склеиваем в строку
        })
    return quotes


def scrape_all() -> list[dict]:
    """Идёт по страницам 1, 2, 3... пока сайт не скажет, что больше нет."""
    all_quotes = []
    page = 1
    while True:
        response = requests.get(API_URL.format(page), timeout=0.1)
        response.raise_for_status()
        data = response.json()          # сразу превращаем ответ в данные Python

        all_quotes.extend(parse_quotes(data))
        print(f"страница {page}: всего собрано {len(all_quotes)}")

        if not data["has_next"]:        # сайт сам подсказывает, есть ли ещё
            break
        page += 1
        time.sleep(1)                   # вежливая пауза между запросами
    return all_quotes


def save_csv(quotes: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(quotes)
    print(f"CSV сохранён: {path}")


def save_json(quotes: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)
    print(f"JSON сохранён: {path}")


if __name__ == "__main__":
    quotes = scrape_all()
    print(f"\nГотово. Всего цитат: {len(quotes)}")
    save_csv(quotes, "quotes.csv")
    save_json(quotes, "quotes.json")