import os
import pandas as pd
from httpx import Client
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.exceptions import UnexpectedModelBehavior
from model import GEMINI_MODEL
import datetime

# providing a schema for pydantic
class Product(BaseModel):
    brand_name: str = Field(title="Brand Name", description="The brand name of the product")
    product_name: str = Field(title="Product Name", description="The name of the product")
    price: str | None = Field(title="Price", description="The price of the product")
    rating_count: int | None = Field(title="Rating Count", description="The ratings for the product")
    
class Results(BaseModel):
    dataset: list[Product] = Field(title="Dataset", description="The list of products")
    
    
# defining agent
web_scraping_agent = Agent(
    name="Web Scraping Agent",
    model=GEMINI_MODEL,
    system_prompt=("""
        Your task is to extract relevant product information from the provided HTML content 
        and return it as a list of dictionaries. Each dictionary should contain the following 
        fields if they are present: 'brand_name', 'product_name', 'price', and 'rating_count'.

        Step 1: Use the `fetch_html_text(url)` function to fetch the HTML content from the provided URL. 
        Step 2: Parse and extract the required fields from the HTML. 
        Step 3: Clean the data by removing unnecessary HTML tags, scripts, and any irrelevant content.
        Step 4: Return the extracted data as a list of dictionaries with the following format:
          [
            {"brand_name": "BrandA", "product_name": "Product 1", "price": "$100", "rating_count": 120},
            ...
          ]      
    """),
    retries=3,
    result_type=Results,
    model_settings=ModelSettings(
        max_tokens=8000,
        temperature=0.1
    )
)

# define custom function
@web_scraping_agent.tool_plain(retries=1)
def fetch_html_text(url: str) -> str:
    """
    Fetches the HTML text from a given URL

    Args:
        url: str - The page's URL to fetch the HTML text from

    Returns:
        str: The HTML text from the given URL
    """
    print('Calling URL: ',url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    with Client(headers=headers) as client:
        response = client.get(url, timeout=20)
        if response.status_code != 200:
            return f'Failed to fetch the HTML text from {url}. Status code: {response.status_code}'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        with open('soup.txt', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print('Soup file saved')
        return soup.get_text().replace('\n', '').replace('\r', '')
    

# main function
def main() -> None:
    prompt = ''
    
    try:
        response = web_scraping_agent.run_sync(prompt)
        
        if response.data is None:
            raise UnexpectedModelBehavior("The model did not return any data.")
        
        print('-' * 50)
        print('Input_tokens: ', response.usage().request_tokens)
        print('Output_tokens: ', response.usage().response_tokens)
        print('Total tokens: ', response.usage().total_tokens)
        
        lst = []
        for item in response.data.dataset:
            lst.append(item.model_dump())
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        df = pd.DataFrame(lst)
        df.to_csv(f'scrapped_{timestamp}.csv', index=False)
    
    except UnexpectedModelBehavior as e:
        print(f"Error: {e}")
