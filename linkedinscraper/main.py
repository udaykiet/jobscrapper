from scraper import LinkedInScraper
from extractor import LinkedInExtractor
from excel_writer import ExcelWriter



def main():


    scraper = LinkedInScraper()

    extractor = LinkedInExtractor()



    keyword = "java"


    all_jobs = []



    try:


        # Open browser

        scraper.open_browser()



        # Open LinkedIn

        scraper.open_linkedin()



        # Login manually

        scraper.wait_for_login()



        # Open jobs search URL

        scraper.open_jobs_url(
            keyword=keyword
        )



        page_number = 0



        while True:



            print(
                "\n=============================="
            )

            print(
                "Extracting page:",
                page_number + 1
            )

            print(
                "=============================="
            )



            jobs = extractor.extract_jobs(
                scraper.get_page()
            )



            # If no jobs found, stop

            if len(jobs) == 0:


                print(
                    "No jobs found. Stopping..."
                )

                break



            all_jobs.extend(
                jobs
            )



            print(
                f"Total jobs collected: {len(all_jobs)}"
            )



            # Move to next page

            page_number += 1



            next_page = scraper.go_to_next_page(
                page_number,
                keyword
            )



            if not next_page:


                print(
                    "No more pages available"
                )

                break




        print(
            "\nFinal jobs extracted:",
            len(all_jobs)
        )



        if len(all_jobs) > 0:


            print(
                "Creating Excel file..."
            )


            writer = ExcelWriter(
                "linkedin_java_jobs.xlsx"
            )


            writer.save_jobs(
                all_jobs
            )


            print(
                "Excel generated successfully"
            )


        else:


            print(
                "No jobs found. Excel not created."
            )



        input(
            "Press ENTER to close..."
        )



    finally:


        scraper.close()



if __name__ == "__main__":

    main()