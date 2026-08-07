from playwright.sync_api import sync_playwright


class NaukriScraper:

    def __init__(self):

        self.profile_path = "./naukri_profile"



    def open_browser(self):

        print("Starting Chrome profile...")


        self.playwright = sync_playwright().start()


        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_path,
            channel="chrome",
            headless=False
        )


        self.page = (
            self.context.pages[0]
            if self.context.pages
            else self.context.new_page()
        )


        print("Chrome started")



    def open_naukri(self):

        print("Opening Naukri...")


        self.page.goto(
            "https://www.naukri.com",
            wait_until="domcontentloaded",
            timeout=60000
        )


        print("Naukri opened")



    def wait_for_login(self):

        input(
            "Login using OTP manually. After reaching homepage press ENTER..."
        )


        print(
            "Login session stored in Chrome profile"
        )



    def search_jobs(self, keyword, experience):

        print(
            "Opening search bar..."
        )


        self.page.locator(
            "button.nI-gNb-sb__expand"
        ).click()


        self.page.wait_for_timeout(
            2000
        )


        print(
            f"Searching for {keyword}"
        )


        keyword_input = self.page.locator(
            "input[placeholder='Enter keyword / designation / companies']"
        )


        keyword_input.fill(
            keyword
        )


        print(
            "Selecting experience..."
        )


        exp_input = self.page.locator(
            "#experienceDD"
        )


        exp_input.click()


        self.page.wait_for_timeout(
            2000
        )


        self.page.get_by_text(
            experience,
            exact=True
        ).click()


        print(
            f"Experience selected: {experience}"
        )



        print(
            "Clicking search button..."
        )


        self.page.locator(
            "button.nI-gNb-sb__icon-wrapper"
        ).click()


        print(
            "Search completed"
        )


        self.page.wait_for_timeout(
            10000
        )



    def apply_filters(self):

        print(
            "Applying freshness filter..."
        )


        freshness_button = self.page.locator(
            "#filter-freshness"
        )


        if freshness_button.count() == 0:

            print(
                "Freshness filter not found"
            )

            return



        freshness_button.click()


        self.page.wait_for_timeout(
            1000
        )


        print(
            "Selecting Last 1 day..."
        )


        last_day = self.page.locator(
            "a[data-id='filter-freshness-1']"
        )


        if last_day.count():

            last_day.click()


            print(
                "Freshness selected: Last 1 day"
            )


        else:

            print(
                "Last 1 day option not found"
            )


        self.page.wait_for_timeout(
            5000
        )


        print(
            "Freshness filter applied"
        )



    def get_page(self):

        return self.page



    def go_to_next_page(self):

        print(
            "Checking next page..."
        )


        next_buttons = self.page.locator(
            "div.styles_pagination__oIvXh a.styles_btn-secondary__2AsIP"
        )


        next_button = None


        for i in range(next_buttons.count()):

            button = next_buttons.nth(i)


            text = (
                button
                .inner_text()
                .strip()
            )


            if text.startswith("Next"):

                next_button = button
                break



        if next_button is None:

            print(
                "Next button not found"
            )

            return False



        disabled = next_button.get_attribute(
            "disabled"
        )


        if disabled is not None:

            print(
                "Reached last page"
            )

            return False



        next_url = next_button.get_attribute(
            "href"
        )


        if not next_url:

            print(
                "Next URL missing"
            )

            return False



        print(
            "Moving to:",
            next_url
        )



        self.page.goto(
            "https://www.naukri.com" + next_url,
            wait_until="domcontentloaded",
            timeout=60000
        )


        self.page.wait_for_timeout(
            5000
        )


        print(
            "Next page loaded"
        )


        return True



    def close(self):

        print(
            "Closing browser..."
        )


        self.context.close()

        self.playwright.stop()