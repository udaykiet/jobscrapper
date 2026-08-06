from playwright.sync_api import sync_playwright


class ServiceNowScraper:

    def __init__(self):

        self.base_url = (
            "https://careers.servicenow.com/jobs/"
            "?orderby=0"
            "&pagesize=20"
            "&page=1"
            "&radius=100"
            "&country=India"
        )


    def fetch_jobs(self):

        jobs = []


        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )


            page = browser.new_page()


            print(
                "Opening ServiceNow careers page..."
            )


            page.goto(
                self.base_url,
                wait_until="domcontentloaded",
                timeout=60000
            )


            print(
                "Page loaded"
            )


            page_number = 1


            while True:


                print(
                    f"Scraping page {page_number}"
                )


                # wait for job cards

                page.wait_for_selector(
                    "a.js-view-job",
                    timeout=30000
                )


                job_links = page.locator(
                    "a.js-view-job"
                )


                print(
                    "Jobs on page:",
                    job_links.count()
                )


                current_page_jobs = []


                for i in range(
                    job_links.count()
                ):

                    link = job_links.nth(i)


                    title = link.inner_text().strip()


                    href = link.get_attribute(
                        "href"
                    )


                    if not href:
                        continue


                    job_url = (
                        "https://careers.servicenow.com"
                        + href
                    )


                    # Find location from parent card

                    card = link.locator(
                        "xpath=ancestor::div[contains(@class,'card-body')]"
                    )


                    location = ""


                    if card.count() > 0:

                        location_element = card.locator(
                            "li.list-inline-item"
                        ).first


                        if location_element.count() > 0:

                            location = (
                                location_element
                                .inner_text()
                                .strip()
                            )


                    current_page_jobs.append(
                        {
                            "title": title,
                            "location": location,
                            "url": job_url
                        }
                    )


                jobs.extend(
                    current_page_jobs
                )


                print(
                    "Total collected:",
                    len(jobs)
                )


                #
                # PAGINATION
                #

                next_button = page.locator(
                    "a[aria-label='Next page']"
                ).first


                if next_button.count() == 0:

                    print(
                        "No next page found"
                    )

                    break



                next_url = next_button.get_attribute(
                    "href"
                )


                if not next_url:

                    print(
                        "Next URL missing"
                    )

                    break



                print(
                    "Going to next page:",
                    next_url
                )


                page.goto(
                    next_url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )


                page_number += 1



            browser.close()



        print(
            "Final jobs count:",
            len(jobs)
        )


        return jobs