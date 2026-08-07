class LinkedInExtractor:


    def extract_jobs(
            self,
            page
    ):


        print(
            "Extracting jobs..."
        )


        jobs = []


        cards = page.locator(
            "div[componentkey^='job-card-component-ref-']"
        )


        count = cards.count()


        print(
            "Jobs found:",
            count
        )



        for i in range(count):


            print(
                f"Extracting job {i+1}/{count}"
            )


            try:


                card = cards.nth(i)



                # -----------------------
                # Extract card information
                # -----------------------


                paragraphs = card.locator(
                    "p"
                )


                title = ""
                company = ""
                location = ""
                posted = ""


                if paragraphs.count() >= 3:


                    title = (
                        paragraphs
                        .nth(0)
                        .inner_text()
                    )


                    company = (
                        paragraphs
                        .nth(1)
                        .inner_text()
                    )


                    location = (
                        paragraphs
                        .nth(2)
                        .inner_text()
                    )



                # Posted time

                text = card.inner_text()


                if "ago" in text:

                    posted = text.split("ago")[0].split("\n")[-1]



                # -----------------------
                # Click job card
                # -----------------------


                card.click()


                page.wait_for_timeout(
                    3000
                )



                # -----------------------
                # Extract right panel
                # -----------------------


                description = ""


                about_job = page.locator(
                    "h2:has-text('About the job')"
                )


                if about_job.count():


                    description = (
                        about_job
                        .locator("xpath=../..")
                        .inner_text()
                    )



                jobs.append(
                    {

                        "title":
                            title.strip(),


                        "company":
                            company.strip(),


                        "location":
                            location.strip(),


                        "posted":
                            posted.strip(),


                        "description":
                            description.strip()

                    }
                )



            except Exception as e:


                print(
                    "Error extracting job:",
                    e
                )



        print(
            "Extraction completed:",
            len(jobs)
        )


        return jobs