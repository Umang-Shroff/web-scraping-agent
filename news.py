# import streamlit as st
# import subprocess
# import os
# import feedparser
# import pandas as pd
# from datetime import datetime

# RSS_FEED_URL = "https://feeds.bbci.co.uk/news/technology/rss.xml"

# def fetch_latest_news() -> pd.DataFrame:
#     feed = feedparser.parse(RSS_FEED_URL)
#     articles = []
#     for entry in feed.entries:
#         article = {
#             'title': entry.title,
#             'link': entry.link,
#             'published': datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d %H:%M:%S'),
#             'summary': entry.summary,
#         }
#         articles.append(article)
#     df = pd.DataFrame(articles)
#     return df

# def display_news_in_cards(df: pd.DataFrame):
#     for index, row in df.iterrows():
#         st.markdown(
#             f"""
#             <div style="background-color: #f7f7f7; border-radius: 10px; padding: 15px; margin-bottom: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
#                 <h3 style="color: #333333;">{row['title']}</h3>
#                 <p style="color: #777777; font-size: 14px;">Published on: {row['published']}</p>
#                 <p style="color: #555555; font-size: 16px; margin-top: 10px;">{row['summary']}</p>
#                 <a href="{row['link']}" target="_blank" style="color: #1e90ff; font-size: 16px; text-decoration: none; font-weight: bold;">Read more...</a>
#             </div>
#             """, unsafe_allow_html=True
#         )

# def main():
#     st.title('News and E-commerce Scraper')
#     st.markdown("### Choose an option:")
    
#     if st.button('Scrape E-commerce Website'):
#         url = st.text_input("Enter the URL of the e-commerce website you want to scrape:")

#         if url:
#             st.write(f"Fetching data from {url}...")
#             try:
#                 # Call app.py using subprocess and pass the URL to it
#                 subprocess.run(["python", "app.py", url], check=True)
#                 st.write("E-commerce data scraped successfully!")
#                 # Here you can handle displaying the output
#                 # Example: you can call a method to show the scraped products
#                 # display_product_data()
#             except subprocess.CalledProcessError as e:
#                 st.write(f"Error occurred while scraping the e-commerce site: {e}")

#     if st.button('Daily News'):
#         st.write("Fetching the latest news...")
#         df = fetch_latest_news()
#         st.write("Latest News:")
#         display_news_in_cards(df)

# if __name__ == '__main__':
#     main()
