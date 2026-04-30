import time, csv, re
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

# ------------------ LOGGING ------------------
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Start scraping...")
#------------------
def basic_quality_check(title, price):
    return title and price
# ------------------ CLEANING ------------------
def clean_text(text):
    if not text:
        return None
    text = text.strip()

    # remove emails
    text = re.sub(r"\S+@\S+", "", text)

    # remove phone numbers
    text = re.sub(r"\b(?:\+?\d[\d\s\-]{8,}\d)\b", "", text)

    return text


def is_valid_record(title, price):
    if not title or not price:
        return False

    if re.search(r"\d{8,}", str(title)):
        return False

    if "@" in str(title):
        return False

    return True


# ------------------ DRIVER ------------------
driver = webdriver.Chrome()
driver.get("https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre")

results = []

# ------------------ SCRAPING ------------------
for page in range(10):
    logging.info(f"Page {page+1}")

    # scroll
    for _ in range(3):
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(1)

    cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/appartements/']")

    for c in cards:
        try:
            text = c.text

            # -------- TITLE --------
            title = None
            try:
                title = c.find_element(By.CSS_SELECTOR, "p[title]").text
            except:
                pass

            # -------- PRICE (ROBUST) --------
            price = None
            price_text = None

            try:
                # method 1 (class)
                price_element = c.find_element(By.CSS_SELECTOR, "span.sc-3286ebc5-2.PuYkS")
                price_text = price_element.get_attribute("textContent")
            except:
                try:
                    # method 2 (fallback using DH)
                    price_element = c.find_element(By.XPATH, ".//span[contains(text(),'DH')]")
                    price_text = price_element.text
                except:
                    price_text = None

            if price_text:
                price_text = re.sub(r"[^\d]", "", price_text)
                if price_text:
                    price = int(price_text)
                else:
                    logging.warning("Price empty after cleaning")
            else:
                logging.warning("Price not found")

            # -------- LOCATION --------
            location = None
            if "dans" in text:
                loc_lines = [l for l in text.split("\n") if "dans" in l]
                location = loc_lines[0] if loc_lines else None

            # -------- DETAILS --------
            surface = rooms = baths = None

            for l in text.lower().split("\n"):
                if "m²" in l:
                    surface = l
                if "chambre" in l:
                    rooms = l
                if "sdb" in l or "bain" in l:
                    baths = l

            # -------- CLEAN --------
            title = clean_text(title)
            location = clean_text(location)

            # -------- VALIDATION --------
            if basic_quality_check(title, price):
                    results.append([title, price, c.get_attribute("href")])
                    logging.info(f"{title} | {price}")
            else:
                    logging.warning("bad data")

        except Exception as e:
            logging.error(f"Error extracting data: {e}")

    # -------- NEXT PAGE --------
    try:
        next_btns = driver.find_elements(By.CSS_SELECTOR, "a[href*='?o=']")
        if next_btns:
            next_btns[-1].click()
            time.sleep(2)
        else:
            break
    except Exception as e:
        logging.error(f"Pagination error: {e}")
        break

driver.quit()

# ------------------ SAVE ------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
staging_dir = os.path.join(base_dir, "..", "staging")
os.makedirs(staging_dir, exist_ok=True)

# سيف الملف
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
filename = os.path.join(staging_dir, f"raw_{timestamp}.csv")

try:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "price", "link"])
        if results:
            writer.writerows(results)
            print(f"Success! Saved {len(results)} rows to {filename}")
        else:
            logging.warning("No results found to save.")
            print("Warning: Results list is empty.")
except Exception as e:
    logging.error(f"Save error: {e}")