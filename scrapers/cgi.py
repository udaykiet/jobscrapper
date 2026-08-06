from playwright.sync_api import sync_playwright


class CGIScraper:


    def __init__(self):

        self.base_url = "https://cgi.njoyn.com/CORP/"

        self.url = (
            "https://cgi.njoyn.com/CORP/xweb/xweb.asp?"
            "NTKN=c&clid=21001&Page=joblisting"
        )



    def fetch_jobs(self):

        jobs = []


        with sync_playwright() as p:


            browser = p.chromium.launch(

                channel="chrome",

                headless=False,

                args=[
                    "--disable-blink-features=AutomationControlled"
                ]

            )



            context = browser.new_context(

                viewport={
                    "width":1280,
                    "height":900
                },


                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151 Safari/537.36"
                )

            )



            page = context.new_page()



            #
            # Hide webdriver
            #

            page.add_init_script(
            """
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            )
            """
            )



            print(
                "Opening CGI careers page..."
            )



            page.goto(

                self.url,

                wait_until="networkidle",

                timeout=90000

            )



            print(
                "Page loaded"
            )



            #
            # Fill keyword
            #

            keyword = page.locator(
                "#Inp_Keywords"
            )


            keyword.wait_for(

                state="visible",

                timeout=30000

            )


            keyword.fill(
                "java"
            )



            print(
                "Keyword entered"
            )



            #
            # Fill city
            #

            city = page.locator(
                "#Inp_City"
            )


            city.wait_for(

                state="visible",

                timeout=30000

            )


            city.fill(
                "hyderabad"
            )



            print(
                "City entered"
            )



            #
            # Search
            #

            search_button = page.locator(
                "input[type='submit']"
            ).first



            search_button.click()



            print(
                "Search clicked"
            )



            #
            # Wait for results
            #

            page.wait_for_timeout(
                5000
            )



            page_number = 1



            while True:


                print(
                    "Scraping page:",
                    page_number
                )



                rows = page.locator(
                    "tbody tr"
                )



                print(
                    "Rows found:",
                    rows.count()
                )



                for i in range(
                    rows.count()
                ):


                    row = rows.nth(i)



                    columns = row.locator(
                        "td"
                    )



                    if columns.count() < 5:

                        continue



                    job_id = (
                        columns
                        .nth(0)
                        .inner_text()
                        .strip()
                    )



                    title = (
                        columns
                        .nth(1)
                        .inner_text()
                        .strip()
                    )



                    category = (
                        columns
                        .nth(2)
                        .inner_text()
                        .strip()
                    )



                    location = (
                        columns
                        .nth(3)
                        .inner_text()
                        .strip()
                    )



                    country = (
                        columns
                        .nth(4)
                        .inner_text()
                        .strip()
                    )



                    href = (
                        columns
                        .nth(0)
                        .locator("a")
                        .get_attribute("href")
                    )



                    job_url = ""



                    if href:


                        if href.startswith("http"):

                            job_url = href


                        else:

                            job_url = (
                                self.base_url
                                + href
                            )



                    jobs.append(

                        {
                            "job_id": job_id,

                            "title": title,

                            "category": category,

                            "location": location,

                            "country": country,

                            "url": job_url
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
                    "a:has-text('Next')"
                ).first



                if next_button.count() == 0:


                    print(
                        "No next page"
                    )

                    break



                next_href = (
                    next_button
                    .get_attribute("href")
                )



                if not next_href:


                    break



                print(
                    "Going next page:",
                    next_href
                )



                page.goto(

                    self.base_url + next_href,

                    wait_until="networkidle",

                    timeout=90000

                )



                page.wait_for_timeout(
                    3000
                )


                page_number += 1




            print(
                "Final CGI jobs:",
                len(jobs)
            )



            browser.close()



        return jobs