import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import argparse

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

headers = {
    "User-Agent": config['user_agent'],
    **config['headers']
}

# Helper function to scrape a single URL
def scrape_url(url, elements):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        data = {element: [tag.get_text() for tag in soup.select(element)] for element in elements}

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

# Function to save data in the chosen format
def save_data(data, output_format):
    if output_format == 'csv':
        pd.DataFrame(data).to_csv('scraped_data.csv', index=False)
    elif output_format == 'json':
        with open('scraped_data.json', 'w') as f:
            json.dump(data, f, indent=4)

# Main function
def main():
    parser = argparse.ArgumentParser(description='Web Scraper Tool')
    parser.add_argument('--url', help='Single URL to scrape')
    parser.add_argument('--urls', nargs='+', help='List of URLs to scrape')
    parser.add_argument('--elements', nargs='+', help='HTML elements to scrape', required=True)
    parser.add_argument('--output', choices=['csv', 'json'], default='csv', help='Output format')

    args = parser.parse_args()

    urls = [args.url] if args.url else args.urls
    all_data = []

    for url in urls:
        print(f"Scraping {url}...")
        data = scrape_url(url, args.elements)
        if data:
            all_data.append(data)
        time.sleep(config['rate_limit'])

    save_data(all_data, args.output)
    print("Scraping complete!")

if __name__ == "__main__":
    main()
