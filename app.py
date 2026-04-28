from extract.scraper import run
from clean.clean_data import process_ads


def run():

    data = [
        {
            "title": "Appartement test",
            "price": 500000,
            "city": "Casablanca",
            "link": "test-link"
        }
    ]

    return data