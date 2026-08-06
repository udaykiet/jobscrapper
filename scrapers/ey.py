from playwright.sync_api import sync_playwright, TimeoutError


class EYScraper:

    def __init__(self):
        self.url = "https://careers.ey.com/ey/search/"


    def fetch_jobs(self):

        jobs = []


        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )


            page = browser.new_page()


            print("Opening EY careers page...")


            page.goto(
                self.url,
                wait_until="domcontentloaded",
                timeout=60000
            )


            print("Page loaded")


            # -----------------------------
            # Find search box
            # -----------------------------

            search_box = page.get_by_role(
                "textbox",
                name="Search by keyword and/or location"
            )


            search_box.wait_for(
                state="visible",
                timeout=30000
            )


            print("Search box found")


            search_box.fill(
                "india"
            )


            print("Entered india")


            # -----------------------------
            # Click search
            # -----------------------------

            search_button = page.locator(
                "input.keywordsearch-button"
            )


            search_button.wait_for(
                state="visible",
                timeout=30000
            )


            search_button.click()


            print("Search clicked")


            # -----------------------------
            # Wait for results
            # -----------------------------

            page.wait_for_load_state(
                "domcontentloaded"
            )


            print(
                "URL:",
                page.url
            )


            try:

                page.wait_for_selector(
                    "a.jobTitle-link",
                    timeout=60000
                )


                print(
                    "Job elements loaded"
                )


            except TimeoutError:


                print(
                    "Job selector not found, debugging..."
                )


                print(
                    "jobTitle-link count:",
                    page.locator(
                        "a.jobTitle-link"
                    ).count()
                )


                print(
                    "jobLocation count:",
                    page.locator(
                        "span.jobLocation"
                    ).count()
                )


                # save page for inspection

                with open(
                    "ey_debug.html",
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(
                        page.content()
                    )


                browser.close()

                return jobs



            # -----------------------------
            # Extract jobs
            # -----------------------------

            job_links = page.locator(
                "a.jobTitle-link"
            )


            print(
                "Jobs found:",
                job_links.count()
            )


            for i in range(
                job_links.count()
            ):


                job = job_links.nth(i)


                title = (
                    job
                    .inner_text()
                    .strip()
                )


                href = job.get_attribute(
                    "href"
                )


                if not href:
                    continue



                # move to parent row

                row = job.locator(
                    "xpath=ancestor::tr"
                )


                location = ""


                if row.count():


                    location_element = row.locator(
                        "span.jobLocation"
                    )


                    if location_element.count():

                        location = (
                            location_element
                            .inner_text()
                            .strip()
                        )



                jobs.append(
                    {
                        "title": title,
                        "location": location,
                        "url": "https://careers.ey.com" + href
                    }
                )



            print(
                "Total jobs collected:",
                len(jobs)
            )


            browser.close()



        return jobs