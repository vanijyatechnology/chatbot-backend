import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        texts = [p.get_text() for p in soup.find_all(["p", "h1", "h2", "li"])]
        return "\n".join(texts).strip()
    except Exception as e:
        return f"Error scraping URL: {e}"
