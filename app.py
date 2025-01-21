import os
import pandas as pd
from httpx import Client
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.exceptions import UnexpectedModelBehavior
from model import GEMINI_MODEL

# providing a schema for pydantic
class Product(BaseModel):
    brand_name: str = Field(title="Brand Name", description="The brand name of the product")
    product_name: str = Field(title="Product Name", description="The name of the product")
    price: str | None = Field(title="Price", description="The price of the product")
    rating_count: int | None = Field(title="Rating Count", description="The ratings for the product")
    
class Results(BaseModel):
    dataset: list[Product] = Field(title="Dataset", description="The list of products")