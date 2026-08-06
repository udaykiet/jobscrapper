import requests
import re


class VirtusaScraper:


    def __init__(self):

        self.url = (
            "https://prod.agenticweb-marketing.com/careers/graphql"
        )



    def fetch_jobs(self):

        jobs = []


        headers = {

            "Content-Type": "application/json",

            "Accept": "application/json",

            "User-Agent": "Mozilla/5.0"

        }



        payload = {

            "query": """

            query {

                jobListResults(isList:"true") {

                    results {

                        title

                        careerCtaLink

                        descriptionInternalHTML

                        country

                        city

                        jobField

                        skill

                        yearsOfExperience

                    }

                }

            }

            """

        }



        print(
            "Fetching Virtusa jobs..."
        )



        response = requests.post(

            self.url,

            json=payload,

            headers=headers,

            timeout=60

        )



        print(
            "Status:",
            response.status_code
        )



        response.raise_for_status()



        data = response.json()



        #
        # GraphQL error handling
        #

        if "errors" in data:

            print(
                "GraphQL Error:",
                data["errors"]
            )

            return []



        job_results = (

            data
            .get("data", {})
            .get("jobListResults", {})
            .get("results", [])

        )



        print(
            "Total received:",
            len(job_results)
        )



        for job in job_results:



            #
            # Only India jobs
            #

            if job.get("country") != "India":

                continue



            description = job.get(
                "descriptionInternalHTML",
                ""
            )



            experience = self.extract_experience(
                description
            )



            apply_id = (

                job
                .get(
                    "careerCtaLink",
                    ""
                )
                .split("/")
                [-1]

            )



            jobs.append(

                {


                    "title":
                    job.get(
                        "title",
                        ""
                    ),



                    "role":
                    job.get(
                        "jobField",
                        ""
                    ),



                    "location":
                    (
                        job.get(
                            "city",
                            ""
                        )
                        + ", India"
                    ),



                    "experience":
                    experience,



                    "skills":
                    job.get(
                        "skill",
                        ""
                    ),



                    "apply_id":
                    apply_id

                }

            )



        print(
            "Total Virtusa India jobs:",
            len(jobs)
        )



        return jobs




    def extract_experience(self, text):


        if not text:

            return ""



        pattern = (

            r"Years of Experience\s*"
            r"([0-9]+\s*-\s*[0-9]+\s*Years?)"

        )



        match = re.search(

            pattern,

            text,

            re.IGNORECASE

        )



        if match:

            return (

                match
                .group(1)
                .strip()

            )



        #
        # fallback from yearsOfExperience field
        #

        return ""




    def run(self):

        print(
            "Running VirtusaScraper"
        )

        return self.fetch_jobs()