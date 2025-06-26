from bs4 import BeautifulSoup
import pandas as pd
import requests
import schedule
import time

# --- Configuration ---
BASE_URL = "https://www.gadgetcraze.ug"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
OUTPUT_FILE = "gadgetcraze_all_products.xlsx"


def get_all_category_links():
    url = f"{BASE_URL}/shop"
    print(f"🌐 Fetching all categories from {url}")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    category_links = {}
    for a in soup.select("a[href*='/shop/category/']"):
        href = a.get("href")
        name = a.get_text(strip=True)
        if href.startswith("/shop/category/") and name:
            full_url = BASE_URL + href
            category_links[name] = full_url
    print(f"✅ Found {len(category_links)} categories.")
    return category_links


def get_product_links(category_url):
    product_links = []
    page = 1
    while True:
        url = f"{category_url}?page={page}"
        print(f"   📄 Fetching page {page}: {url}")
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            page_links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith('/shop/') and '/shop/category/' not in href:
                    full_url = BASE_URL + href
                    if full_url not in product_links:
                        page_links.append(full_url)

            if not page_links:
                print(f"   ⛔ No more products on page {page}.")
                break

            product_links.extend(page_links)
            page += 1

        except Exception as e:
            print(f'❌ Error on page {page} of {category_url}: {e}')
            break

    print(f"   ✅ Found {len(product_links)} total product links.")
    return list(set(product_links))


def scrape_product_page(product_url, category_name):
    try:
        response = requests.get(product_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('h1')
        price_tag = soup.find('span', class_='oe_currency_value')

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        price_text = price_tag.get_text(strip=True).replace(
            ",", "") if price_tag else "0"

        try:
            price = int(price_text)
        except ValueError:
            price = None

        print(f"   🛒 {title} - UGX {price}")
        return {
            "Category": category_name,
            "Product": title,
            "Price (UGX)": price,
            "URL": product_url
        }

    except Exception as e:
        print(f"❌ Error scraping product page {product_url}: {e}")
        return None


def scrape_all():
    print("🚀 Starting full scrape...")
    all_products = []
    category_links = get_all_category_links()
    for cat_name, cat_url in category_links.items():
        print(f"🔎 Scraping category: {cat_name}")
        product_links = get_product_links(cat_url)
        for link in product_links:
            product = scrape_product_page(link, cat_name)
            if product:
                all_products.append(product)

    df = pd.DataFrame(all_products)
    df.drop_duplicates(inplace=True)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ Scraping complete. Data saved to {OUTPUT_FILE}")

# --- Scheduler setup ---


def job():
    print("🔁 Scheduled job started...")
    scrape_all()


# Run immediately once
scrape_all()

# Schedule every Monday at 9:00 AM
schedule.every().monday.at("09:00").do(job)

print("⏰ Scheduler is running. Waiting for next run...")

while True:
    schedule.run_pending()
    time.sleep(60)

# You must leave the script running(in a terminal or hosted server) for scheduling to work
