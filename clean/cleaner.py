import time
import random
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre"

COLUMNS = [
    "titre",
    "prix",
    "ville",
    "quartier",
    "surface_m2",
    "chambres",
    "sdb",
    "etage",
    "annee_construction",
    "lien"
]

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=options)

def parse_text(text):

    titre = text.split("\n")[0] if text else None

    prix = None
    m = re.search(r"(\d[\d\s]*)\s?(dh|dhs|mad)", text.lower())
    if m:
        prix = m.group(1)

    ville = None
    quartier = None

    # surface / rooms
    surface = None
    chambres = None
    sdb = None

    m = re.search(r"(\d+)\s?m²", text)
    if m:
        surface = int(m.group(1))

    m = re.search(r"(\d+)\s?ch", text)
    if m:
        chambres = int(m.group(1))

    m = re.search(r"(\d+)\s?sdb", text)
    if m:
        sdb = int(m.group(1))

    return titre, prix, ville, quartier, surface, chambres, sdb

def run():

    driver = init_driver()
    driver.get(URL)
    print(driver.current_url)
    print(driver.title)
    open("debug.html", "w", encoding="utf-8").write(driver.page_source)

    time.sleep(6)

    for _ in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 3))

    # 🔥 IMPORTANT FIX
    cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/fr/']")

    print("Cards found:", len(cards))

    data = []
    seen = set()

    for card in cards:
        try:
            link = card.get_attribute("href")

            if not link or link in seen:
                continue

            seen.add(link)

            text = card.text.strip()

            titre, prix, ville, quartier, surface, chambres, sdb = parse_text(text)

            if not titre:
                continue

            data.append({
                "titre": titre,
                "prix": prix,
                "ville": ville,
                "quartier": quartier,
                "surface_m2": surface,
                "chambres": chambres,
                "sdb": sdb,
                "etage": None,
                "annee_construction": None,
                "lien": link
            })

        except:
            continue

    driver.quit()

    df = pd.DataFrame(data, columns=COLUMNS)

    print("Extracted rows:", len(df))

    df.to_csv("immo_avito.csv", index=False, encoding="utf-8")

    print("✅ DONE SAVED")

if __name__ == "__main__":
    run()






from utils.logger import log


def sanitize(ad):

    # حذف أي بيانات حساسة إذا كانت موجودة
    ad.pop("phone", None)
    ad.pop("email", None)
    ad.pop("seller_name", None)

    return ad


def process_ads(raw_ads):

    cleaned = []

    for ad in raw_ads:

        ad = sanitize(ad)

        log("Ad cleaned")

        cleaned.append(ad)

    return cleaned