import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque
from pymongo import MongoClient


class BFSScraper:
    """Breadth-first scraper that stores results in MongoDB."""

    def __init__(self, api_key, start_url, mongo_uri="mongodb://localhost:27017", db_name="scraper"):
        self.api_key = api_key
        self.start_url = start_url if start_url.startswith("http") else f"http://{start_url}"
        parsed = urlparse(self.start_url)
        self.base = f"{parsed.scheme}://{parsed.netloc}"
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.pages = self.db.pages

    def _already_scraped(self, url):
        return self.pages.count_documents({"url": url}, limit=1) != 0

    def fetch(self, url):
        response = requests.get(
            "http://api.scraperapi.com",
            params={"api_key": self.api_key, "url": url},
            timeout=30,
        )
        response.raise_for_status()
        return response.text

    def run(self):
        queue = deque([self.start_url])
        visited = set()
        while queue:
            url = queue.popleft()
            if url in visited or self._already_scraped(url):
                continue
            try:
                html = self.fetch(url)
            except Exception:
                continue
            self.pages.insert_one({"url": url, "html": html})
            visited.add(url)
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup.find_all("a", href=True):
                link = urljoin(url, tag["href"])
                if link.startswith(self.base) and link not in visited:
                    queue.append(link)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BFS domain scraper")
    parser.add_argument("api_key", help="ScraperAPI key")
    parser.add_argument("domain", help="Domain to scrape")
    parser.add_argument("--mongo", default="mongodb://localhost:27017", help="Mongo URI")
    parser.add_argument("--db", default="scraper", help="MongoDB database")
    args = parser.parse_args()

    BFSScraper(args.api_key, args.domain, args.mongo, args.db).run()
