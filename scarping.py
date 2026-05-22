import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://en.wikipedia.org"

start_pages = [
    "/wiki/Python_(programming_language)",
    "/wiki/LangChain"
]

visited = set()
all_data = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

MAX_PAGES = 20   

def get_page_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, []

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text

    paragraphs = soup.find_all("p")
    content = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])

    links = []
    for a in soup.select("a[href^='/wiki/']"):
        href = a.get("href")

        # Skip unwanted pages
        if ":" in href:
            continue

        full_url = urljoin(BASE_URL, href)
        links.append(full_url)

    return {
        "title": title,
        "url": url,
        "content": content
    }, links

queue = [urljoin(BASE_URL, p) for p in start_pages]

while queue and len(all_data) < MAX_PAGES:
    url = queue.pop(0)

    if url in visited:
        continue

    print(f"Scraping: {url}")
    visited.add(url)

    try:
        data, links = get_page_data(url)

        if data and len(data["content"]) > 500:
            all_data.append(data)
            print(f"Saved: {data['title']}")

        # Add new links to queue
        for link in links[:10]:  # limit links per page
            if link not in visited:
                queue.append(link)

        time.sleep(1)  # be respectful

    except Exception as e:
        print(f"Error: {e}")


with open("wikipedia_big_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

print(f"\n Done! Total pages scraped: {len(all_data)}")
