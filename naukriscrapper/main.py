from scraper import NaukriScraper
from extractor import NaukriExtractor
from csv_writer import CSVWriter



def main():

    scraper = NaukriScraper()

    try:

        scraper.open_browser()

        scraper.open_naukri()


        input(
            "If login is required complete it manually then press ENTER..."
        )


        scraper.search_jobs(
            keyword="java",
            experience="2 years"
        )


        # Extract jobs
        extractor = NaukriExtractor()


        jobs = extractor.extract_jobs(
            scraper.get_page()
        )


        print(
            f"Total jobs extracted: {len(jobs)}"
        )


        # Save jobs into CSV
        csv_writer = CSVWriter(
            filename="java_jobs.csv"
        )


        csv_writer.save_jobs(
            jobs
        )


        input(
            "Press ENTER to close browser..."
        )


    finally:

        scraper.close()



if __name__ == "__main__":
    main()