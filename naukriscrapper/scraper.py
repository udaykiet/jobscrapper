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
            "Login manually and press ENTER..."
        )



    def search_jobs(self, keyword, experience):

        print("Opening search...")


        self.page.locator(
            "button.nI-gNb-sb__expand"
        ).click()


        self.page.wait_for_timeout(2000)



        self.page.locator(
            "input[placeholder='Enter keyword / designation / companies']"
        ).fill(
            keyword
        )



        self.page.locator(
            "#experienceDD"
        ).click()


        self.page.wait_for_timeout(2000)


        self.page.get_by_text(
            experience,
            exact=True
        ).click()



        self.page.locator(
            "button.nI-gNb-sb__icon-wrapper"
        ).click()



        print(
            "Search completed"
        )


        self.page.wait_for_timeout(
            10000
        )



    def open_filtered_url(self):

        url = (
            "https://www.naukri.com/java-jobs"
            "?k=java"
            "&nignbevent_src=jobsearchDeskGNB"
            "&experience=2"
            "&jobAge=1"
            "&ctcFilter=3to6"
            "&ctcFilter=6to10"
            "&ctcFilter=10to15"
        )


        print(
            "Opening filtered URL:"
        )


        print(url)



        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )


        self.page.wait_for_timeout(
            10000
        )


        print(
            "Filtered search loaded"
        )



    def get_page(self):

        return self.page



    def go_to_next_page(self):

        print(
            "Checking next page..."
        )


        next_button = self.page.locator(
            "div.styles_pagination-cont__sWhS6 a.styles_btn-secondary__2AsIP"
        ).filter(
            has_text="Next"
        )


        if next_button.count() == 0:

            print(
                "Next page not available"
            )

            return False



        if next_button.get_attribute(
            "disabled"
        ) is not None:

            print(
                "Last page reached"
            )

            return False



        next_href = next_button.get_attribute(
            "href"
        )


        if not next_href:

            return False



        current_url = self.page.url



        query = ""


        if "?" in current_url:

            query = current_url.split("?")[1]



        next_url = (
            "https://www.naukri.com"
            +
            next_href
        )



        if query:

            next_url += (
                "?"
                +
                query
            )



        print(
            "Opening:",
            next_url
        )



        self.page.goto(
            next_url,
            wait_until="domcontentloaded",
            timeout=60000
        )


        self.page.wait_for_timeout(
            8000
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