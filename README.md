# Scrape

This example provides a simple Python scraper and React front‑end. The scraper
uses [ScraperAPI](https://www.scraperapi.com/) to fetch pages and traverses a
domain in breadth‑first order. Pages are stored in MongoDB so already scraped
URLs are skipped on subsequent runs.

## Python usage

```bash
pip install -r requirements.txt
python scraperapp/app.py
```

POST `/scrape` with JSON body containing `api_key` and `domain` or use the
included React UI.

## Frontend

Open `http://localhost:5000` once the Flask app is running. Enter your
ScraperAPI key and the domain to crawl, then press **Start Scraping**.
