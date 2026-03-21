# Kemmler Shop Price Scraper 🛠️

A professional Python-based tool designed to automate price extraction from the Kemmler Shop website using SKU (Stock Keeping Unit) identifiers. This project demonstrates web scraping best practices, data processing with Pandas, and ethical automation.

## 🚀 Features

- **SKU-Based Search**: Direct item lookup using unique catalog numbers.
- **Clean Data Extraction**: Pulls precise price values from HTML `<meta>` tags (Schema.org compliant).
- **Excel Integration**: Automatically generates `.xlsx` reports for easy business analysis.
- **Ethical Scraping**: Built-in rate limiting (`time.sleep`) to respect server resources.
- **Robust Error Handling**: Manages connection timeouts and missing data gracefully.

## 🛠️ Tech Stack

- **Python 3.x**
- **Requests**: For handling HTTP protocols.
- **BeautifulSoup4**: For parsing HTML content.
- **Pandas & Openpyxl**: For professional Excel report generation.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USER_NAME/kemmler-shop-scraper.git](https://github.com/YOUR_USER_NAME/kemmler-shop-scraper.git)
   cd kemmler-shop-scraper

2. Instal dependencies:

    ```
    pip install -r requirements.txt

📋 Usage
1. Prepare your SKU list in the main.py file (or provide an input file).

2. Run the scraper:

    ```
    python main.py
3. Check the generated kemmler_prices.xlsx file for results

⚖️ Legal & Ethics (Compliance)

This project was developed with respect for the website's robots.txt and terms of service:

    Robots.txt: Adheres to the Content-Signal: search=yes permission.

    Rate Limiting: Random delays between requests are implemented to prevent server strain.

    User-Agent: Identification headers are used to mimic standard browser behavior.

    Educational Purpose: This tool is intended for demonstration and portfolio purposes only.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.