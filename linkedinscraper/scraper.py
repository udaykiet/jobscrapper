from playwright.sync_api import sync_playwright



class LinkedInScraper:


    def __init__(self):

        self.profile_path = "./linkedin_profile"

        self.base_url = (
            "https://www.linkedin.com/jobs/search-results/"
        )



    def open_browser(self):

        print(
            "Starting Chrome profile..."
        )


        self.playwright = sync_playwright().start()


        self.context = (
            self.playwright
            .chromium
            .launch_persistent_context(
                user_data_dir=self.profile_path,
                channel="chrome",
                headless=False
            )
        )


        self.page = (
            self.context.pages[0]
            if self.context.pages
            else self.context.new_page()
        )


        print(
            "Chrome started"
        )



    def open_linkedin(self):

        print(
            "Opening LinkedIn..."
        )


        self.page.goto(
            "https://www.linkedin.com",
            wait_until="domcontentloaded",
            timeout=60000
        )


        print(
            "LinkedIn opened"
        )



    def wait_for_login(self):

        input(
            "Login manually then press ENTER..."
        )


        print(
            "LinkedIn session saved"
        )



    def open_jobs_url(
            self,
            keyword="java"
    ):


        url = (
            self.base_url
            +
            f"?keywords={keyword}"
            +
            "&f_TPR=r86400"
        )


        print(
            "Opening:",
            url
        )


        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )


        self.page.wait_for_timeout(
            8000
        )


        print(
            "Jobs page loaded"
        )



    def go_to_next_page(
            self,
            page_number,
            keyword="java"
    ):


        start = page_number * 25


        url = (
            self.base_url
            +
            f"?keywords={keyword}"
            +
            "&f_TPR=r86400"
            +
            f"&start={start}"
        )


        print(
            "Opening next page:",
            url
        )


        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )


        self.page.wait_for_timeout(
            8000
        )



        # New LinkedIn job card selector

        jobs = self.page.locator(
            "div[componentkey^='job-card-component-ref-']"
        )


        count = jobs.count()


        print(
            "Jobs found on page:",
            count
        )


        if count == 0:

            print(
                "No more jobs available"
            )

            return False



        return True



    def get_job_cards(self):


        return self.page.locator(
            "div[componentkey^='job-card-component-ref-']"
        )



    def get_page(self):

        return self.page



    def close(self):

        print(
            "Closing browser..."
        )


        self.context.close()

        self.playwright.stop()