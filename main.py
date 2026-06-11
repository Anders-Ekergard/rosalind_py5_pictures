import py5
import os
from typing import Dict, List, Any, Callable
import requests

# ============================================================================
# API och nyckelord (från whale.py)
# ============================================================================
api_key = os.getenv("api_key") or os.getenv("API_KEY")
THE_NEWS_API_URL = "https://api.thenewsapi.com/v1/news/all"

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

# ============================================================================
# Valkonfiguration
# ============================================================================
global drawing_mode
drawing_mode = None
global sentiments_data
sentiments_data = None

# ============================================================================
# Hval-ritfunktioner (från whalefig.py och whale.py)
# ============================================================================
def draw_whale(x: float, y: float, scale: float = 1.0):
    """Rita ett hval med angiven skalning."""
    py5.push_matrix()
    py5.translate(x, y)
    py5.scale(scale)
    
    # --- färger ---
    top_blue = py5.color(40, 90, 160)
    bottom_blue = py5.color(120, 170, 220)

    # --- kropp (bezier-form) ---
    py5.fill(top_blue)
    py5.begin_shape()
    py5.vertex(-250, 0)
    py5.bezier_vertex(-150, -120, 100, -120, 220, -10)
    py5.bezier_vertex(260, 20, 260, 80, 200, 110)
    py5.bezier_vertex(50, 160, -150, 140, -250, 40)
    py5.end_shape(py5.CLOSE)

    # --- undersida ---
    py5.fill(bottom_blue)
    py5.begin_shape()
    py5.vertex(-250, 40)
    py5.bezier_vertex(-150, 120, 50, 140, 200, 110)
    py5.bezier_vertex(150, 80, -50, 60, -250, 0)
    py5.end_shape(py5.CLOSE)

    # --- stjärtfena ---
    py5.fill(top_blue)
    py5.begin_shape()
    py5.vertex(220, -10)
    py5.bezier_vertex(260, -40, 310, -20, 330, -60)
    py5.bezier_vertex(300, -40, 260, -20, 220, 10)
    py5.end_shape(py5.CLOSE)

    # --- fena ---
    py5.begin_shape()
    py5.vertex(-50, 40)
    py5.bezier_vertex(-20, 20, 40, 40, 20, 90)
    py5.bezier_vertex(0, 70, -20, 60, -50, 40)
    py5.end_shape(py5.CLOSE)

    # --- öga ---
    py5.fill(0)
    py5.circle(-150, -10, 12)

    # --- prickar på ryggen ---
    py5.fill(255, 255, 255, 120)
    for x_offset in range(-200, 150, 40):
        py5.circle(x_offset, -40 - (x_offset % 30), 6)
    
    py5.pop_matrix()

def draw_circle(x: float, y: float, radius: float = 10):
    """Rita en cirkel."""
    py5.fill(100, 150, 200, 150)
    py5.circle(x, y, radius)

# ============================================================================
# Ritfunktioner för olika lägen
# ============================================================================
def draw_whale_grid(scale_func: Callable):
    """Rita ett rutnät av hvalar (från whalefig.py-logik)."""
    py5.background(230, 245, 255)
    
    m = 10  # Marginal
    scale = scale_func()  # Lista med 0..8 värden
    
    for i in range(8):
        for j in range(8):
            # Välj rätt skalvärde
            if j % 2 == 0:
                s = scale[i]
            else:
                s = scale[7 - i]

            x = m + j * py5.width / 8
            y = m + i * py5.height / 8
            
            draw_whale(x, y, s * 0.15)

def draw_sentiment_grid(sentiments: List[float]):
    """Rita ett rutnät baserat på sentimentanalys (från whale.py)."""
    py5.background(255)
    
    m = 40
    scale = sentiments
    
    for i in range(8):
        for j in range(8):
            # Välj rätt skalvärde
            if j % 2 == 0:
                s = 1 * (scale[i] if i < len(scale) else 0)
            else:
                s = 1 * (scale[7 - i] if 7 - i < len(scale) else 0)

            x = m + j * py5.width / 8
            y = m + i * py5.height / 8

            # Skicka bara talet vidare
            if j == 2 and i == 2:
                draw_whale(x, y, s * 0.25)
            else:
                draw_circle(x, y, s * 35)

# ============================================================================
# Setup och Draw för py5
# ============================================================================
def setup():
    py5.size(800, 500)
    py5.smooth()
    py5.background(255)
    
    print("\n" + "="*60)
    print("VÄLJ RITLÄGE:")
    print("="*60)
    print("1. Rita rutnät av hvalar (single whale grid)")
    print("2. Rita sentimentanalys av hvaldata från API")
    print("="*60)
    print("\nOm du väljer 2, väntar programmet på API-anropet...")

def draw():
    global drawing_mode, sentiments_data
    
    if drawing_mode is None:
        return
    
    if drawing_mode == 1:
        # Rutnät av hvalar med skalvärden 0-8
        def get_scale():
            return [i for i in range(8)]
        draw_whale_grid(get_scale)
    
    elif drawing_mode == 2:
        if sentiments_data is not None:
            draw_sentiment_grid(sentiments_data)
        else:
            py5.background(255)
            py5.fill(0)
            py5.text_size(20)
            py5.text("Laddar sentimentdata från API...", 50, py5.height // 2)

def key_pressed():
    global drawing_mode, sentiments_data
    
    if py5.key == "1":
        drawing_mode = 1
        print("\n✓ Rutnät av hvalar valt!")
    
    elif py5.key == "2":
        drawing_mode = 2
        print("\n✓ Sentimentanalys valt - laddar data från API...")
        try:
            keywords = {
                'positive': ['growing population', 'healthy', 'protected', 'recovery', 'success', 'ökande population', 'skyddad'],
                'negative': ['endangered', 'declining', 'threatened', 'extinct', 'danger', 'utrotningshotad', 'minskande', 'hotad'],
                'neutral': ['study', 'observation', 'research', 'studie', 'observation', 'forskning']
            }
            whale = 'blue whale'
            years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017]
            sentiments_data = get_yearly_sentiment(keywords, whale, years)
            print(f"✓ Sentimentdata laddad: {sentiments_data}")
        except Exception as e:
            print(f"✗ Fel vid API-anrop: {e}")
            drawing_mode = None
    
    else:
        print("Tryck på 1 eller 2 för att välja ritläge")

if __name__ == "__main__":
    py5.run_sketch()
