class NaukriExtractor:


    def extract_jobs(self, page):

        print("Extracting jobs...")


        jobs = []


        job_cards = page.locator(
            "div.cust-job-tuple"
        )


        print(
            "Jobs found:",
            job_cards.count()
        )


        for i in range(job_cards.count()):


            card = job_cards.nth(i)


            title = ""
            url = ""


            title_element = card.locator(
                "h2 a.title"
            )


            if title_element.count():

                title = (
                    title_element
                    .inner_text()
                    .strip()
                )

                url = (
                    title_element
                    .get_attribute("href")
                )



            company = ""

            company_element = card.locator(
                ".comp-name"
            )


            if company_element.count():

                company = (
                    company_element
                    .inner_text()
                    .strip()
                )



            salary = ""

            salary_element = card.locator(
                ".sal-wrap span[title]"
            )


            if salary_element.count():

                salary = (
                    salary_element
                    .get_attribute("title")
                )



            location = ""

            location_element = card.locator(
                ".loc-wrap span[title]"
            )


            if location_element.count():

                location = (
                    location_element
                    .get_attribute("title")
                )



            description = ""

            desc_element = card.locator(
                ".job-desc"
            )


            if desc_element.count():

                description = (
                    desc_element
                    .inner_text()
                    .strip()
                )



            skills = []

            skill_elements = card.locator(
                ".tags-gt li"
            )


            for j in range(
                skill_elements.count()
            ):

                skills.append(
                    skill_elements
                    .nth(j)
                    .inner_text()
                    .strip()
                )



            posted_date = ""

            posted_element = card.locator(
                ".job-post-day"
            )


            if posted_element.count():

                posted_date = (
                    posted_element
                    .inner_text()
                    .strip()
                )



            jobs.append(
                {
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "description": description,
                    "skills": ", ".join(skills),
                    "posted_date": posted_date,
                    "url": url
                }
            )



        print(
            "Extraction completed:",
            len(jobs)
        )


        return jobs