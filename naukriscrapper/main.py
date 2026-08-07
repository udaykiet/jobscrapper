from scraper import NaukriScraper


def main():

    scraper = NaukriScraper()


    scraper.open_browser()


    scraper.open_naukri()


    scraper.wait_for_login()


    scraper.close()



if __name__ == "__main__":
    main()