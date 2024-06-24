# Walmart Product Scraper

This Python script scrapes product information from Walmart's website using web scraping techniques with Beautiful Soup and requests library.

## Features

- Scrapes product details such as price, reviews, availability, and more.
- Handles multiple pages of search results to gather comprehensive data.
- Saves scraped data into a CSV file for easy analysis and further processing.

## Requirements

- Python 3.x
- BeautifulSoup (`beautifulsoup4`)
- requests
- pandas

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/walmart-product-scraper.git
   cd walmart-product-scraper
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Modify the `HEADERS` in the script (`scraper.py`) if necessary to mimic a real browser's headers.

2. Run the scraper script:

   ```bash
   python scraper.py
   ```

3. The script will start scraping Walmart's website for product information based on the search query and page range specified.

4. After scraping completes, the script will save the scraped data into a CSV file named `product_info.csv` in the same directory.

## Customization
- Modify the `get_productLinks` function in `scraper.py` to change the search query or adjust pagination settings.
- Extend the script to scrape additional information or handle different types of products by modifying the `extract_productInfo` function.

## Notes
- Respect Walmart's terms of service and robots.txt when using this scraper.
- Use responsibly and considerate of server load to avoid being blocked.
