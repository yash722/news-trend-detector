import os
import pandas as pd
from newspaper import Article
from newspaper import build
from datetime import datetime
import logging
import time

logging.getLogger("newspaper.article").setLevel(logging.CRITICAL)

def scrape_articles():
    # Add your favorite news sources (more = better clusters)
    urls = [
        "https://www.bbc.com/news",
        "https://edition.cnn.com/world",
        "https://www.npr.org/sections/news/",
        "https://www.nytimes.com/section/world"
    ]

    # Output directory
    os.makedirs("data/raw", exist_ok=True)
    output_path = f"data/raw/articles_{datetime.now().strftime('%Y%m%d')}.csv"

    articles = []
    limit = 50
    for url in urls:
        paper = build(url, memoize_articles=False)
        for article in paper.articles[:limit]:
            try:
                article.download()
                article.parse()
                articles.append({
                    "title": article.title,
                    "text": article.text,
                    "url": article.url,
                    "date": datetime.now().isoformat()
                })
                time.sleep(0.5)
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")

    if not articles:
        print("No articles scraped!")
        return

    df = pd.DataFrame(articles)
    df.to_csv(output_path, index=False)
    print(f"Scraped {len(df)} articles. Saved to: {output_path}")

# if __name__ == "__main__":
#     scrape_articles()
