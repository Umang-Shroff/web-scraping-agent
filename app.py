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

# Providing a schema for pydantic
class Product(BaseModel):
    brand_name: str = Field(title="Brand Name", description="The brand name of the product")
    product_name: str = Field(title="Product Name", description="The name of the product")
    price: str | None = Field(title="Price", description="The price of the product")
    rating_count: int | None = Field(title="Rating Count", description="The ratings for the product")

class Results(BaseModel):
    dataset: list[Product] = Field(title="Dataset", description="The list of products")

# Defining agent
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

# Define custom function to fetch HTML text
@web_scraping_agent.tool_plain(retries=1)
def fetch_html_text(url: str) -> str:
    """
    Fetches the HTML text from a given URL
    """
    print('Calling URL: ', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    with Client(headers=headers) as client:
        try:
            response = client.get(url, timeout=20)
            print(f"HTTP Response Code: {response.status_code}")
            if response.status_code != 200:
                return f"Failed to fetch the HTML text from {url}. Status code: {response.status_code}"

            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text().replace('\n', '').replace('\r', '')
        except Exception as e:
            print(f"Error occurred while fetching HTML: {e}")
            return f"Error occurred: {e}"

# Main function
def main() -> None:
    # Input website URL
    prompt = 'https://www.ikea.com/us/en/cat/best-sellers/'

    try:
        print("Running web scraping agent...") 
        response = web_scraping_agent.run_sync(prompt)
        print("Response from agent:", response)
        
        if response.data is None:
            raise UnexpectedModelBehavior("The model did not return any data.")
        
        print('-' * 50)
        print('Input_tokens: ', response.usage().request_tokens)
        print('Output_tokens: ', response.usage().response_tokens)
        print('Total tokens: ', response.usage().total_tokens)
         
        lst = []
        for item in response.data.dataset:
            lst.append(item.model_dump())
         
        df = pd.DataFrame(lst)
         
        print("\nExtracted Product Data:")
        print(df.to_string(index=False)) 
        
    except UnexpectedModelBehavior as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
