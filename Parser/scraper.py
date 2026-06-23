# -*- coding: utf-8 -*-
import csv
import json
import time

import requests

API_URL = "https://quotes.toscrape.com/api/quotes?page={}"


def parse_quotes(data: dict) -> list[dict]:
    quotes = []
    for q in data["quotes"]:           
        quotes.append({
            "text": q["text"],
            "author": q["author"]["name"],   
            "tags": "; ".join(q["tags"]),   
        })
    return quotes


def scrape_all() -> list[dict]:
    all_quotes = []
    page = 1
    while True:
        response = requests.get(API_URL.format(page), timeout=0.1)
        response.raise_for_status()
        data = response.json()          

        all_quotes.extend(parse_quotes(data))
        print(f"страница {page}: всего собрано {len(all_quotes)}")

        if not data["has_next"]:        
            break
        page += 1
        time.sleep(1)                  
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
