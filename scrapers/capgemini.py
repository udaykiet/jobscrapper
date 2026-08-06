import requests


class CapgeminiScraper:

    def __init__(self):

        self.base_url = (
            "https://cg-jobstream-api.azurewebsites.net/api/job-search"
        )

        self.page_size = 50

        self.search = "java"

        self.country = "in-en"



    def fetch_jobs(self):

        jobs = []


        page = 1


        while True:


            print(
                f"Fetching Capgemini page {page}"
            )


            params = {
                "page": page,
                "size": self.page_size,
                "search": self.search,
                "country_code": self.country
            }


            response = requests.get(
                self.base_url,
                params=params,
                timeout=30
            )


            if response.status_code != 200:

                print(
                    "API failed:",
                    response.status_code
                )

                break



            data = response.json()



            job_list = data.get(
                "data",
                []
            )


            print(
                "Jobs received:",
                len(job_list)
            )



            if not job_list:

                break



            for job in job_list:


                jobs.append(
                    {
                        "title": job.get(
                            "title",
                            ""
                        ),

                        "location": job.get(
                            "location",
                            ""
                        ),

                        "company": job.get(
                            "brand",
                            ""
                        ),

                        "contract_type": job.get(
                            "contract_type",
                            ""
                        ),

                        "experience_level": job.get(
                            "experience_level",
                            ""
                        ),

                        "url": job.get(
                            "apply_job_url",
                            ""
                        ),

                        "description": job.get(
                            "description_stripped",
                            ""
                        )
                    }
                )



            #
            # Pagination
            #

            total = data.get(
                "count",
                0
            )


            if len(jobs) >= total:

                break


            page += 1



        print(
            "Total Capgemini jobs:",
            len(jobs)
        )


        return jobs