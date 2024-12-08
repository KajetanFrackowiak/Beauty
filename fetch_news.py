import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY environment variable is not set.")

def fetch_beauty_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f"beauty",
        "language": "en",
        "apiKey": NEWS_API_KEY,
        "sortBy": "popularity",
    }
    response = requests.get(url, params=params)
    news_data = response.json()
    if "articles" not in news_data:
        print("The key 'articles' is not present in the response.")
        print("Response received:", news_data)
        return []

    articles = [
        {"title": article["title"], "content": article["content"], "url": article["url"]}
        for article in news_data["articles"]
    ]
    return articles

articles = fetch_beauty_news()
print(articles)