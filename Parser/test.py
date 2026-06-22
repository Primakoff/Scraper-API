# Проверяем разбор на JSON точно такой же формы, как отдаёт настоящий API
from scraper import parse_quotes, save_csv, save_json

FAKE_API_PAGE = {
    "has_next": True,
    "page": 1,
    "quotes": [
        {
            "text": "The world as we have created it is a process of our thinking.",
            "author": {"name": "Albert Einstein", "goodreads_link": "/x"},
            "tags": ["change", "deep-thoughts", "thinking"]
        },
        {
            "text": "It is our choices that show what we truly are.",
            "author": {"name": "J.K. Rowling", "goodreads_link": "/y"},
            "tags": ["abilities", "choices"]
        }
    ]
}

result = parse_quotes(FAKE_API_PAGE)
print("Разобрано цитат:", len(result))
for q in result:
    print(f'  [{q["author"]}] {q["text"]}  | теги: {q["tags"]}')

save_csv(result, "quotes.csv")
save_json(result, "quotes.json")
print("\nСодержимое quotes.json:")
print(open("quotes.json", encoding="utf-8").read())