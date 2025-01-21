# Web Scraping Agent using Pydantic AI

This project implements a surface level web scraping agent powered by Pydantic AI that extracts product information from an e-commerce website. The data is parsed from the HTML content and returned as structured data, including product details like brand name, product name, price, and rating count.

## Features

- **Web Scraping**: Scrapes data from an e-commerce website using custom logic.
- **Structured Data**: Extracted data is structured in a user-friendly format, displaying product details like `brand_name`, `product_name`, `price`, and `rating_count`.
- **Pydantic AI**: Uses Pydantic AI to handle the scraping logic and data formatting.
- **Customizable**: You can easily change the scraping logic and URL.

## Prerequisites

- Python 3.7 or higher
- An API key for Pydantic AI's Gemini model (you will need to sign up and get your API key from Pydantic AI).
- `.env` file for storing sensitive environment variables (like the API key).

