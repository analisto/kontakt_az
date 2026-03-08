"""
Kontakt.az notebook scraper
Uses DrissionPage (Cloudflare-safe) for browser + asyncio/ThreadPoolExecutor for concurrency.
Output: data/notebooks.csv
"""

import csv
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage, ChromiumOptions

BASE_URL = "https://kontakt.az"
CATEGORY_URL = f"{BASE_URL}/notbuk-ve-kompyuterler/komputerler/notbuklar"
DATA_DIR = Path(__file__).parent.parent / "data"


# ---------------------------------------------------------------------------
# Browser factory
# ---------------------------------------------------------------------------

def make_page() -> ChromiumPage:
    """
    Launch a Chromium page that bypasses Cloudflare.
    Headed mode required (headless is detected by CF).
    Window is placed off-screen so it stays invisible to the user.
    """
    opts = ChromiumOptions()
    opts.headless(False)
    opts.set_argument("--no-sandbox")
    opts.set_argument("--disable-dev-shm-usage")
    opts.set_argument("--disable-blink-features=AutomationControlled")
    opts.set_argument("--window-position=-32000,-32000")  # off-screen = invisible
    return ChromiumPage(addr_or_opts=opts)


# ---------------------------------------------------------------------------
# Listing page parsing
# ---------------------------------------------------------------------------

def parse_listing(html: str) -> tuple[list[dict], int]:
    soup = BeautifulSoup(html, "lxml")
    products: list[dict] = []

    for item in soup.select(".prodItem"):
        link = item.select_one("a.prodItem__img[href]")
        if not link or not link["href"].startswith("http"):
            continue
        rec: dict = {"url": link["href"]}
        gtm_raw = item.get("data-gtm", "")
        if gtm_raw:
            try:
                gtm = json.loads(gtm_raw)
                rec["name"]  = gtm.get("item_name", "")
                rec["brand"] = gtm.get("item_brand", "")
                rec["price"] = str(gtm.get("price", ""))
                rec["sku"]   = item.get("data-sku", "")
            except json.JSONDecodeError:
                pass
        products.append(rec)

    pages = [1]
    for a in soup.find_all("a", href=True):
        m = re.search(r"[?&]p=(\d+)", a["href"])
        if m:
            pages.append(int(m.group(1)))

    return products, max(pages)


# ---------------------------------------------------------------------------
# Product detail page parsing
# ---------------------------------------------------------------------------

def parse_product(html: str, base: dict) -> dict:
    soup = BeautifulSoup(html, "lxml")
    rec = dict(base)

    # Current (discounted) price
    price_span = soup.select_one(".price-bar strong > span")
    if price_span:
        rec["price"] = re.sub(r"[^\d.,]", "", price_span.get_text(strip=True))

    # Original price
    orig = soup.select_one(".price-bar strong em .price-wrapper")
    if orig:
        raw = orig.get("data-price-amount") or orig.get_text(strip=True)
        rec["original_price"] = re.sub(r"[^\d.,]", "", raw)

    # Specs
    for row in soup.select(".har__row"):
        title_el = row.select_one(".har__title")
        value_el = row.select_one(".har__znach")
        if title_el and value_el:
            for tip in title_el.select(".har__tooltip, [data-tooltip-content]"):
                tip.decompose()
            key = _to_key(title_el.get_text(strip=True))
            val = value_el.get_text(strip=True)
            if key and val:
                rec[key] = val

    return rec


def _to_key(text: str) -> str:
    return re.sub(r"[^\w]+", "_", text.strip().lower()).strip("_")


# ---------------------------------------------------------------------------
# Listing scrape (sequential, single browser tab)
# ---------------------------------------------------------------------------

def scrape_listings() -> list[dict]:
    page = make_page()
    all_products: list[dict] = []

    try:
        print("Fetching listing page 1…")
        page.get(CATEGORY_URL)
        page.ele(".prodItem", timeout=20)   # wait for products
        products, total = parse_listing(page.html)
        print(f"  Page 1 -> {len(products)} items  |  Total pages: {total}")
        all_products.extend(products)

        for n in range(2, total + 1):
            page.get(f"{CATEGORY_URL}?p={n}")
            page.ele(".prodItem", timeout=20)
            items, _ = parse_listing(page.html)
            print(f"  Page {n} -> {len(items)} items")
            all_products.extend(items)
    finally:
        page.quit()

    seen: set[str] = set()
    unique = [p for p in all_products if not (p["url"] in seen or seen.add(p["url"]))]
    print(f"\nTotal unique products: {len(unique)}")
    return unique


# ---------------------------------------------------------------------------
# Product scrape — single browser, sequential navigation
# ---------------------------------------------------------------------------

def scrape_products(basics: list[dict]) -> list[dict]:
    """One browser instance, navigate each product URL sequentially."""
    total = len(basics)
    results: list[dict] = []
    page = make_page()

    try:
        for i, base in enumerate(basics, 1):
            try:
                page.get(base["url"])
                page.ele(".har", timeout=20)
                rec = parse_product(page.html, base)
            except Exception as exc:
                print(f"  [ERR] {exc!s:.80} -> {base['url']}", file=sys.stderr)
                rec = base
            results.append(rec)
            print(f"  [{i}/{total}] {rec.get('name', rec['url'])[:70]}")
    finally:
        page.quit()

    return results


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

def save_csv(records: list[dict], path: Path) -> None:
    if not records:
        print("[WARN] No records to save.", file=sys.stderr)
        return
    priority = ["url", "name", "brand", "sku", "price", "original_price"]
    extra = sorted({k for r in records for k in r} - set(priority))
    fieldnames = [f for f in priority if any(f in r for r in records)] + extra
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    print(f"\nSaved {len(records)} records -> {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    basics = scrape_listings()
    if not basics:
        print("[ERR] No products found.", file=sys.stderr)
        sys.exit(1)

    print(f"\nScraping {len(basics)} product detail pages…")
    records = scrape_products(basics)
    save_csv(records, DATA_DIR / "notebooks.csv")


if __name__ == "__main__":
    main()
