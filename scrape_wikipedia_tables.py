#!/usr/bin/env python3
"""
Script to scrape electricity and energy-related tables from Wikipedia pages
and save them as CSV files.
"""

import pandas as pd
import os
from urllib.parse import urlparse, unquote
import time
import requests
from io import StringIO

# Create output directory for CSV files
OUTPUT_DIR = "wikipedia_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of Wikipedia URLs to scrape
WIKIPEDIA_URLS = [
    "https://en.wikipedia.org/wiki/List_of_countries_by_electricity_production",
    "https://en.wikipedia.org/wiki/Electricity_by_country",
    "https://en.wikipedia.org/wiki/List_of_countries_by_renewable_electricity_production",
    "https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption",
    "https://en.wikipedia.org/wiki/List_of_countries_by_energy_consumption_per_capita",
    "https://en.wikipedia.org/wiki/List_of_countries_by_energy_intensity",
    "https://en.wikipedia.org/wiki/List_of_countries_by_energy_consumption_and_production"
]


def get_page_name(url):
    """Extract a clean page name from the URL for file naming."""
    path = urlparse(url).path
    page_name = unquote(path.split('/')[-1])
    return page_name.replace('_', ' ')


def scrape_tables_from_url(url):
    """
    Scrape all tables from a Wikipedia URL and save them as CSV files.

    Args:
        url (str): The Wikipedia URL to scrape

    Returns:
        int: Number of tables scraped
    """
    page_name = get_page_name(url)
    print(f"\n{'='*80}")
    print(f"Scraping: {page_name}")
    print(f"URL: {url}")
    print(f"{'='*80}")

    try:
        # Set headers to avoid 403 Forbidden error
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Fetch the page with proper headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Read all tables from the HTML content
        tables = pd.read_html(StringIO(response.text))
        num_tables = len(tables)

        print(f"Found {num_tables} table(s) on this page")

        # Save each table as a CSV file
        for idx, table in enumerate(tables, start=1):
            # Create filename
            if num_tables == 1:
                filename = f"{page_name}.csv"
            else:
                filename = f"{page_name}_table_{idx}.csv"

            filepath = os.path.join(OUTPUT_DIR, filename)

            # Save to CSV
            table.to_csv(filepath, index=False, encoding='utf-8')
            print(f"  ✓ Saved table {idx}: {filename} ({table.shape[0]} rows × {table.shape[1]} columns)")

        return num_tables

    except Exception as e:
        print(f"  ✗ Error scraping {url}: {str(e)}")
        return 0


def main():
    """Main function to scrape all Wikipedia pages."""
    print(f"\nStarting Wikipedia table scraper")
    print(f"Output directory: {OUTPUT_DIR}/\n")

    total_tables = 0
    successful_pages = 0

    for url in WIKIPEDIA_URLS:
        num_tables = scrape_tables_from_url(url)
        total_tables += num_tables

        if num_tables > 0:
            successful_pages += 1

        # Be polite to Wikipedia servers
        time.sleep(1)

    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Pages scraped successfully: {successful_pages}/{len(WIKIPEDIA_URLS)}")
    print(f"Total tables saved: {total_tables}")
    print(f"Output directory: {OUTPUT_DIR}/")
    print(f"\nAll CSV files have been saved!")


if __name__ == "__main__":
    main()
