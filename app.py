import os
import pandas as pd
import feedparser
import streamlit as st
from datetime import datetime
import asyncio
from httpx import Client
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.exceptions import UnexpectedModelBehavior
from model import GEMINI_MODEL

# RSS Feed URL for news
RSS_FEED_URL = "https://feeds.bbci.co.uk/news/technology/rss.xml"

# Define Product schema for e-commerce scraping
class Product(BaseModel):
    brand_name: str = Field(title="Brand Name", description="The brand name of the product")
    product_name: str = Field(title="Product Name", description="The name of the product")
    price: str | None = Field(title="Price", description="The price of the product")
    rating_count: int | None = Field(title="Rating Count", description="The ratings for the product")

class Results(BaseModel):
    dataset: list[Product] = Field(title="Dataset", description="The list of products")

# Defining agent for web scraping
web_scraping_agent = Agent(
    name="Web Scraping Agent",
    model=GEMINI_MODEL,
    system_prompt=("""Your task is to extract relevant product information..."""),
    retries=3,
    result_type=Results,
    model_settings=ModelSettings(
        max_tokens=8000,
        temperature=0.1
    )
)

# Function to fetch HTML text from a URL
@web_scraping_agent.tool_plain(retries=1)
def fetch_html_text(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    with Client(headers=headers) as client:
        try:
            response = client.get(url, timeout=20)
            if response.status_code != 200:
                return f"Failed to fetch the HTML text from {url}. Status code: {response.status_code}"

            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text().replace('\n', '').replace('\r', '')
        except Exception as e:
            return f"Error occurred: {e}"

# Function to fetch the latest news
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
    return pd.DataFrame(articles)

# Function to display news in cards
def display_news_in_cards(df: pd.DataFrame):
    for index, row in df.iterrows():
        st.markdown(
            f"""
            <div style="background-color: #f7f7f7; border-radius: 10px; padding: 15px; margin-bottom: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
                <h3 style="color: #333333;">{row['title']}</h3>
                <p style="color: #777777; font-size: 14px;">Published on: {row['published']}</p>
                <p style="color: #555555; font-size: 16px; margin-top: 10px;">{row['summary']}</p>
                <a href="{row['link']}" target="_blank" style="color: #1e90ff; font-size: 16px; text-decoration: none; font-weight: bold;">Read more...</a>
            </div>
            """, unsafe_allow_html=True
        )

# Function to scrape e-commerce website (runs asynchronously)
async def scrape_ecommerce_data_async(url: str):
    try:
        response = await web_scraping_agent.run(url)
        
        if response.data is None:
            raise UnexpectedModelBehavior("The model did not return any data.")
        
        lst = [item.model_dump() for item in response.data.dataset]
        df = pd.DataFrame(lst)
        return df
        
    except UnexpectedModelBehavior as e:
        return f"Error: {e}"

# Function to run the async code within Streamlit's synchronous context
def scrape_ecommerce_data(url: str):
    return asyncio.run(scrape_ecommerce_data_async(url))

# Streamlit UI
def main():
    st.title('News and E-commerce Scraper')
    st.markdown("### Choose an option:")
    
    option = st.selectbox("Select an Option", ["Daily News", "Scrape E-commerce Website"])
    
    if option == "Scrape E-commerce Website":
        url = st.text_input("Enter the URL of the e-commerce website to scrape:")
        
        if st.button("Submit"):
            if url:
                st.write(f"Fetching data from {url}...")
                df = scrape_ecommerce_data(url)
                if isinstance(df, pd.DataFrame):
                    st.write("E-commerce Products:")
                    st.dataframe(df)
                else:
                    st.write(df)  # If an error occurs, show the message
            else:
                st.write("Please enter a valid URL.")

    if option == "Daily Tech News":
        st.write("Fetching the latest tech news...")
        df = fetch_latest_news()
        st.write("Latest Tech News:")
        display_news_in_cards(df)

if __name__ == '__main__':
    main()
