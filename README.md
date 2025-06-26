# 📦 GadgetCraze Product Scraper

Hi there! 👋

This is a Python-based web scraper I built to extract product names and prices from [GadgetCraze Uganda](https://www.gadgetcraze.ug) and export the data into an Excel spreadsheet. The script uses `BeautifulSoup`, `pandas`, and `requests`, and also includes automated **weekly scheduling** using the `schedule` module.

---

## 🚀 Why I Built This

I needed a way to track products and their price changes on GadgetCraze. Unfortunately, when I first attempted to run the scraper in Jupyter Notebook on Anaconda Navigator, the environment failed to execute code properly — no output, no errors, just a dead kernel. So I switched to **VS Code**, and from there, everything worked smoothly.

This project was also a great opportunity to practice modular scraping, pagination handling, and task scheduling in Python — all using a clean and editable structure.

---

## 🧰 What This Project Does

- Extracts product **names** and **prices (in UGX)** from specified GadgetCraze categories
- Handles **pagination** automatically
- Eliminates **duplicates**
- Saves results into a neat **Excel file**
- Runs **every Monday at 10:00 AM** via a background scheduler

---

## 🗂️ Tools and Libraries Used

- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) – For HTML parsing
- [pandas](https://pypi.org/project/pandas/) – For tabular data manipulation and Excel export
- [requests](https://pypi.org/project/requests/) – For sending HTTP requests
- [schedule](https://pypi.org/project/schedule/) – For weekly automation
- [openpyxl](https://pypi.org/project/openpyxl/) – For writing Excel files

---

## 📥 Installation Guide

1. Open VS Code (I switched here after Jupyter failed)
2. Make sure you have Python 3.7+
3. In your terminal, install the dependencies:

```bash
py -m pip install beautifulsoup4 pandas requests schedule openpyxl
```

4. Clone or copy the script into a file, e.g. `gadgetcraze_scraper.py`

---

## 🔨 How to Run the Script

Run it directly in the terminal:

```bash
py gadgetcraze_scraper.py
```

What happens:
- The script immediately scrapes the site
- It saves the result to `gadgetcraze_all_products.xlsx`
- Then it enters a background loop that waits for the next Monday 10:00 AM run

---

## 📊 Categories Being Scraped

In the beginning I was interested in just these three categories:

| Category       | URL                                                                  |
|----------------|----------------------------------------------------------------------|
| iPhones        | https://www.gadgetcraze.ug/shop/category/mobile-phones-iphone-211    |
| iPads          | https://www.gadgetcraze.ug/shop/category/tablets-apple-242           |
| Apple Watches  | https://www.gadgetcraze.ug/shop/category/smart-watches-apple-238     |

For some reason in the end, I ended up scraping the entire website.
The scraper automatically fetches all categories from the main shop page with the function `def get_all_category_links():`

---

## ⚙️ Project Structure

```
gadgetcraze_scraper.py     # Main scraper script
gadgetcraze_products.xlsx  # Output Excel file (auto-generated)
README.md                  # This file
```

---

## 🧠 What I Learned

- The importance of a reliable execution environment — Jupyter sometimes just doesn’t cooperate
- How to structure a scraper that can scale to multiple pages and categories
- How to use `schedule` to run tasks at specific times without relying on cron jobs
- How to export well-formatted Excel tables using `pandas`

---

## ⏰ Scheduling Details

The script runs automatically every **Monday at 10:00 AM** (based on your system time). This is done using the `schedule` module — no need for cron or Task Scheduler!

If you want to change the timing, just modify this line:

```python
schedule.every().monday.at("10:00").do(scrape_all)
```

---

## 📌 Future Improvements

- Notifications when new products appear
- Integrate email notifications with scraped results
- Export to Google Sheets
- Filters for price range(s) and keywords
- Dockerize for deployment


---

## 💬 Questions or Feedback?

If you’d like to collaborate or improve this scraper, feel free to reach out. I built this as a personal learning and utility tool, but I’m happy to build on it.

Cheers!  
**Simon 'CyMoh' Bbaale**

