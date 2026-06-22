# Quotes API Scraper

A tiny, fast scraper that pulls data from a site's **hidden JSON API** instead
of parsing HTML.

`quotes.toscrape.com/scroll` loads its quotes through background calls to
`/api/quotes?page=N`, which returns clean JSON. This scraper calls that endpoint
directly — no HTML parsing, no headless browser. It's the fastest and most
reliable way to scrape, when an API is available.

## How to find a hidden API (the key skill)

1. Open the site, press **F12** → **Network** tab → filter **Fetch/XHR**
2. Reload the page and watch for requests that return JSON
3. If the response contains your data, that's the endpoint — call it directly

## Features

- Calls the JSON API page by page and follows the site's own `has_next` flag
- Polite delay between requests
- Exports to CSV and JSON
- Includes a small test for the parsing logic

## Run

```bash
pip install -r requirements.txt
python test_parse.py    # verify parsing (no network needed)
python scraper.py       # scrape all quotes -> quotes.csv + quotes.json
```

## Why it matters

When a site exposes a JSON API, hitting it directly is far faster and more stable
than rendering pages with a browser. Finding that endpoint in the Network tab is
one of the most valuable skills in web scraping.

## License

MIT