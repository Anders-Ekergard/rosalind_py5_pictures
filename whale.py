import py5
import os
from typing import Dict, List, Any
from whalef import draw_whale
from fibc import draw_circle
import requests

api_key = os.getenv("api_key") or os.getenv("API_KEY")
THE_NEWS_API_URL = "https://api.thenewsapi.com/v1/news/all"  # Kontrollera att detta är korrekt

def analyze_article_content(content: str, keywords: Dict[str, List[str]]) -> Dict[str, int]:
    """Räkna nyckelord i en artikeltext."""
    if not keywords:
        return {}
    keyword_counts = {category: 0 for category in keywords}
    content_lower = content.lower()
    for category, words in keywords.items():
        for word in words:
            if word.lower() in content_lower:
                keyword_counts[category] += 1
    return keyword_counts

def fetch_news_articles(query: str, year: int | None = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Search The News API for articles matching the query."""
    api_token = os.getenv("api_key") or os.getenv("API_KEY")
    if not api_token:
        raise RuntimeError("Missing API key. Set api_key=... in your .env file")

    params: Dict[str, Any] = {
        "api_token": api_token,
        "search": query,
        "search_fields": "title,description,keywords,main_text",
        "language": "en",
        "limit": limit,
    }
    if year is not None:
        params["published_after"] = f"{year}-01-01T00:00:00"
        params["published_before"] = f"{year}-12-31T23:59:59"

    response = requests.get(THE_NEWS_API_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", [])

def get_yearly_sentiment(
    keywords: Dict[str, List[str]],
    whale: str,
    years: List[int],
) -> List[float]:
    """Search The News API for each year and compute a simple sentiment score."""
    yearly_sentiments: List[float] = []
    for year in years:
        query = f'"{whale}"'
        search_results = fetch_news_articles(query, year=year, limit=10)

        total_counts = {category: 0 for category in keywords}
        total_articles = 0
        for result in search_results:
            article = dict(result)
            content = " ".join([
                str(article.get("title", "")),
                str(article.get("description", "")),
                str(article.get("keywords", "")),
                str(article.get("main_text", "")),
            ]).lower()
            counts = analyze_article_content(content, keywords)
            for category in counts:
                total_counts[category] += counts[category]
            total_articles += 1

        if total_articles == 0:
            yearly_sentiments.append(0.0)
            continue

        positive = total_counts.get("positive", 0)
        negative = total_counts.get("negative", 0)
        denominator = positive + negative
        if denominator == 0:
            yearly_sentiments.append(0.0)
        else:
            sentiment = (positive - negative) / denominator
            yearly_sentiments.append(sentiment)

    return yearly_sentiments
def draw(sentiments: List[float]):
    m = 40
    scale = sentiments
    for i in range(8):
        for j in range(8):

            # Välj rätt skalvärde
            if j % 2 == 0:
                s = 1*(scale[i])
            else:
                s = 1*(scale[7 - i])

        x = m + j * py5.width / 8
        y = m + i * py5.height / 8

            # Skicka bara talet vidare
        if j == 2 and i == 2:
            draw_whale(x, y, s*0.25)
        else:
                #star(x, y, x)
            draw_circle(x, y, s*35)
def main():
    keywords = {
        'positive': ['growing population', 'healthy', 'protected', 'recovery', 'success', 'ökande population', 'skyddad'],
        'negative': ['endangered', 'declining', 'threatened', 'extinct', 'danger', 'utrotningshotad', 'minskande', 'hotad'],
        'neutral': ['study', 'observation', 'research', 'studie', 'observation', 'forskning']
    }
    whale = 'blue whale'
    years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017]
    sentiments = get_yearly_sentiment(keywords, whale, years)
    draw(sentiments)
    print("Sentiment per year:", sentiments)
    print("Example articles:", fetch_news_articles('"blue whale"', limit=5)[:2])

if __name__ == "__main__":
    py5.run_sketch()
