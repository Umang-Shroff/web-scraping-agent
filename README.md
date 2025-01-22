# Web Scraping Agent using Pydantic AI

This project implements a versatile web scraping agent powered by **Pydantic AI** to extract and display both **e-commerce product details** and **latest technology news**. The application allows users to scrape data from e-commerce websites and fetch the latest technology news from an RSS feed, all within a clean, modern UI built with **Streamlit**.

## Features

- **Web Scraping for E-Commerce**: Scrapes product data from an e-commerce website, extracting key details such as `brand_name`, `product_name`, `price`, and `rating_count`.
  
- **Latest Technology News**: Fetches and displays the latest news related to technology from a publicly available RSS feed (e.g., BBC Tech News).

- **Structured Data**: The scraped data is returned in a structured format using **Pydantic models**, making it easy to work with and display in a user-friendly way.

- **Streamlit UI**: Interactive and visually appealing user interface with dark mode and customizable background, featuring:
  - Option to scrape e-commerce data.
  - Display of the latest news articles as stylish, dark-mode cards.

- **Pydantic AI**: Utilizes **Pydantic AI's Gemini model** to handle the web scraping and data extraction, ensuring efficient and accurate results.

- **Asynchronous Data Fetching**: Scrapes e-commerce websites asynchronously to provide fast data retrieval without blocking the UI.

- **Customizable**: Easily modify the scraping logic and update the RSS feed URL to customize the sources of data.

## Prerequisites

Before running the project, ensure you have the following:

- **Python 3.7 or higher**.
- **API Key** for Pydantic AI's Gemini model (sign up and get your API key from Pydantic AI).
- **Streamlit** for running the UI.
- **.env File**: Store your sensitive environment variables, such as the API key for Pydantic AI.

### Install Dependencies

To install the necessary dependencies, create a virtual environment and install the required packages:

```bash
pip install -r requirements.txt
