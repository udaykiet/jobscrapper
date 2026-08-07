from scraper import NaukriScraper
from extractor import NaukriExtractor
from csv_writer import CSVWriter



def main():

    scraper = NaukriScraper()
    extractor = NaukriExtractor()


    try:

        # Start browser
        scraper.open_browser()


        # Open Naukri
        scraper.open_naukri()



        input(
            "If login is required complete it manually then press ENTER..."
        )



        # Search jobs
        scraper.search_jobs(
            keyword="java",
            experience="2 years"
        )



        # Apply filters
        scraper.apply_filters()



        all_jobs = []



        while True:


            print(
                "Extracting current page..."
            )


            jobs = extractor.extract_jobs(
                scraper.get_page()
            )


            all_jobs.extend(
                jobs
            )


            print(
                f"Total jobs collected: {len(all_jobs)}"
            )



            # Move to next page

            next_page = scraper.go_to_next_page()



            if not next_page:


                print(
                    "No more pages available"
                )

                break



        print(
            f"Final jobs extracted: {len(all_jobs)}"
        )



        # Save CSV

        csv_writer = CSVWriter(
            filename="java_jobs_filtered.csv"
        )


        csv_writer.save_jobs(
            all_jobs
        )



        print(
            "CSV created successfully"
        )



        input(
            "Press ENTER to close browser..."
        )



    finally:


        scraper.close()



if __name__ == "__main__":

    main()