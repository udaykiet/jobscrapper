from playwright.sync_api import sync_playwright


class CognizantScraper:


    def __init__(self):

        self.url = (
            "https://careers.cognizant.com/"
            "india-en/jobs/"
            "?keyword=java"
            "&location=India"
            "&radius=100"
            "&lat="
            "&lng="
            "&cname=India"
            "&ccode=IN"
            "&pagesize=10"
            "#results"
        )



    def fetch_jobs(self):

        jobs = []


        with sync_playwright() as p:


            browser = p.chromium.launch(
                headless=False
            )


            context = browser.new_context(

                viewport={
                    "width": 1280,
                    "height": 900
                },

                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/120 Safari/537.36"
                )
            )


            page = context.new_page()



            print(
                "Opening Cognizant careers page..."
            )


            page.goto(
                self.url,
                wait_until="domcontentloaded",
                timeout=90000
            )


            print(
                "Page loaded"
            )



            #
            # Handle cookie popup
            #

            try:

                accept_button = page.get_by_text(
                    "Accept All",
                    exact=True
                )


                accept_button.wait_for(
                    state="visible",
                    timeout=10000
                )


                accept_button.click()


                print(
                    "Cookie accepted"
                )


            except Exception:


                print(
                    "No cookie popup"
                )



            #
            # Wait for jobs to load
            #

            try:

                page.wait_for_selector(
                    "div.card-job",
                    timeout=60000
                )


            except Exception:


                page.screenshot(
                    path="cognizant_debug.png"
                )


                print(
                    "Job cards not found. Screenshot saved."
                )

                browser.close()

                return jobs




            page_number = 1



            while True:


                print(
                    "Scraping page:",
                    page_number
                )



                cards = page.locator(
                    "div.card-job"
                )



                print(
                    "Jobs on page:",
                    cards.count()
                )



                for i in range(cards.count()):


                    card = cards.nth(i)



                    title_element = card.locator(
                        ".card-title a"
                    )



                    if title_element.count() == 0:

                        continue



                    title = (
                        title_element
                        .inner_text()
                        .strip()
                    )



                    href = (
                        title_element
                        .get_attribute("href")
                    )



                    location = ""



                    location_element = card.locator(
                        ".job-meta li"
                    ).first



                    if location_element.count() > 0:

                        location = (
                            location_element
                            .inner_text()
                            .strip()
                        )



                    jobs.append(

                        {
                            "title": title,

                            "location": location,

                            "url":
                            "https://careers.cognizant.com"
                            + href
                        }

                    )




                print(
                    "Total collected:",
                    len(jobs)
                )



                #
                # Pagination
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
                        "Next page URL missing"
                    )

                    break




                print(
                    "Going to next page:",
                    next_url
                )



                page.goto(
                    next_url,
                    wait_until="domcontentloaded",
                    timeout=90000
                )



                try:

                    page.wait_for_selector(
                        "div.card-job",
                        timeout=60000
                    )


                except Exception:


                    print(
                        "Next page jobs not loaded"
                    )

                    break




                page_number += 1




            print(
                "Final Cognizant jobs count:",
                len(jobs)
            )



            browser.close()



        return jobs