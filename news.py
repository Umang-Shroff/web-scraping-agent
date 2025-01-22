import feedparser
import pandas as pd
from datetime import datetime

# tech news rss feed
RSS_FEED_URL = "https://feeds.bbci.co.uk/news/technology/rss.xml"

def fetch_latest_news() -> pd.DataFrame:
    feed = feedparser.parse(RSS_FEED_URL)
    
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'published': datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d %H:%M:%S'),
            'summary': entry.summary,
        }
        articles.append(article)
    
    df = pd.DataFrame(articles)
    return df

def main():
    print("Fetching the latest news...")
    df = fetch_latest_news()
    print("Latest News:")
    print(df)

if __name__ == '__main__':
    main()
