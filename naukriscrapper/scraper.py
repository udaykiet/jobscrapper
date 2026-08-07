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


        print("Login session stored in Chrome profile")


    def close(self):

        self.context.close()
        self.playwright.stop()