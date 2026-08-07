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

        print("Opening search bar...")


        self.page.locator(
            "button.nI-gNb-sb__expand"
        ).click()


        self.page.wait_for_timeout(2000)



        print(
            f"Searching for {keyword}"
        )


        keyword_input = self.page.locator(
            "input[placeholder='Enter keyword / designation / companies']"
        )


        keyword_input.fill(keyword)



        print(
            "Selecting experience..."
        )


        exp_input = self.page.locator(
            "#experienceDD"
        )


        exp_input.click()


        self.page.wait_for_timeout(2000)



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


        self.page.wait_for_timeout(10000)



    def get_page(self):

        return self.page



    def close(self):

        print(
            "Closing browser..."
        )


        self.context.close()

        self.playwright.stop()