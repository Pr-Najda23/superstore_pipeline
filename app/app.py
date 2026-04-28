from extract.scraper import run
from clean.clean_data import process_ads


def main():

    raw_data = run()

    clean_data = process_ads(raw_data)

    print(clean_data)


if __name__ == "__main__":
    main()