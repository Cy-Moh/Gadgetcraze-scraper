from bs4 import BeautifulSoup     
import pandas as pd
import requests
import schedule
import time

# --- Configuration settings ---
BASE_URL = "https://www.gadgetcraze.ug"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'     # Mimics a real browser
}
OUTPUT_FILE = "gadgetcraze_all_products.xlsx"   # Excel output file name


# --- Step 1: Get all category links from the main /shop page ----
def get_all_category_links():
    url = f"{BASE_URL}/shop"
    print(f"🌐 Fetching all categories from {url}")

    # Send HTTP request
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    category_links = {}

    # Find all anchor tags pointing to category pages
    for a in soup.select("a[href*='/shop/category/']"):
        href = a.get("href")
        name = a.get_text(strip=True)

        # Ensure valid category URL and name
        if href.startswith("/shop/category/") and name:
            full_url = BASE_URL + href
            category_links[name] = full_url
            
    print(f"✅ Found {len(category_links)} categories.")
    return category_links

# --- Step 2: Get all product links in a given category (with pagination support) ---
def get_product_links(category_url):
    product_links = []
    page = 1

    # Loop through all paginated pages
    while True:
        url = f"{category_url}?page={page}"
        print(f"   📄 Fetching page {page}: {url}")
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            page_links = []

            # Extract product links (not category links)
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith('/shop/') and '/shop/category/' not in href:
                    full_url = BASE_URL + href
                    if full_url not in product_links:
                        page_links.append(full_url)

            # If no product links found on this page, stop paginating
            if not page_links:
                print(f"   ⛔ No more products on page {page}.")
                break

            product_links.extend(page_links)
            page += 1

        except Exception as e:
            print(f'❌ Error on page {page} of {category_url}: {e}')
            break

    print(f"   ✅ Found {len(product_links)} total product links.")
    return list(set(product_links))  # Remove duplicates

# --- Step 3: Scrape data from an individual product page ---
def scrape_product_page(product_url, category_name):
    try:
        response = requests.get(product_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product title and price
        title_tag = soup.find('h1')
        price_tag = soup.find('span', class_='oe_currency_value')

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        price_text = price_tag.get_text(strip=True).replace(
            ",", "") if price_tag else "0"
        
        # Convert price to integer if possible
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

# --- Step 4: Main scraping function that puts it all together ---
def scrape_all():
    print("🚀 Starting full scrape...")
    all_products = []

    # Step 4.1: Get all category links
    category_links = get_all_category_links()

    # Step 4.2: Loop through each category
    for cat_name, cat_url in category_links.items():
        print(f"🔎 Scraping category: {cat_name}")

        # Step 4.3: Get product links this category
        product_links = get_product_links(cat_url)

        # Step 4.4: Visit and scrape each product page
        for link in product_links:
            product = scrape_product_page(link, cat_name)
            if product:
                all_products.append(product)

    # Step 4.5: Save scraped data to Excel
    df = pd.DataFrame(all_products)
    df.drop_duplicates(inplace=True)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ Scraping complete. Data saved to {OUTPUT_FILE}")

# --- Step 5: Scheduled automation ---

# Define the job that runs on a schedule
def job():
    print("🔁 Scheduled job started...")
    scrape_all()


# Run once immediately on startup
scrape_all()

# Schedule the job to run every Monday at 10:00 AM
schedule.every().monday.at("10:00").do(job)

print("⏰ Scheduler is running. Waiting for next run...")

while True:
    schedule.run_pending()
    time.sleep(60)

# You must leave the script running(in a terminal or hosted server) for scheduling to work
