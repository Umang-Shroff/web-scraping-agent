# Web Scraping Agent using Pydantic AI

This project implements a surface level web scraping agent powered by Pydantic AI that extracts product information from an e-commerce website. The data is parsed from the HTML content and returned as structured data, including product details like brand name, product name, price, and rating count.

## Features

- **Web Scraping**: Scrapes data from an e-commerce website using custom logic.
- **Structured Data**: Extracted data is structured in a user-friendly format, displaying product details like `brand_name`, `product_name`, `price`, and `rating_count`.
- **Pydantic AI**: Uses Pydantic AI to handle the scraping logic and data formatting.
- **Customizable**: You can easily change the scraping logic and URL.
- **Streamlit Interface**: The app provides a user-friendly interface to interact with the web scraper and fetch daily news or scrape e-commerce websites.

## Deployed Application

You can try out the application live by visiting the following link:

[Web Scrape Agent on Streamlit](https://web-scrape-agent.streamlit.app/)

## Prerequisites

- Python 3.7 or higher
- An API key for Pydantic AI's Gemini model (you will need to sign up and get your API key from Pydantic AI).
- `.env` file for storing sensitive environment variables (like the API key) when running locally.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your **GEMINI_API_KEY**:
    ```
    GEMINI_API_KEY=your_pydantic_ai_api_key_here
    ```

4. Run the app locally:
    ```bash
    streamlit run app.py
    ```

## How to Use

- **Daily News**: The app fetches the latest tech news and displays it in an easy-to-read card format.
- **Scrape E-commerce Website**: You can provide a URL to an e-commerce website to extract product details such as brand, product name, price, and rating count.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
