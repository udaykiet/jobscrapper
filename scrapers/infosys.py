import requests


class InfosysScraper:


    def __init__(self):

        self.url = (
            "https://intapgateway.infosysapps.com/"
            "careersci/search/intapjbsrch/"
            "getCareerSearchJobs"
        )


    def fetch_jobs(self):

        jobs = []


        params = {
            "sourceId": "1,21",
            "searchText": "ALL"
        }


        print("Calling Infosys API...")


        response = requests.get(
            self.url,
            params=params,
            timeout=30
        )


        response.raise_for_status()


        data = response.json()


        print(
            "Total jobs received:",
            len(data)
        )


        blocked_keywords = [
            "senior",
            "sr ",
            "sr.",
            "principal",
            "lead",
            "manager",
            "director",
            "architect",
            "specialist"
        ]



        for job in data:


            role = (
                job.get(
                    "roleDesignation",
                    ""
                )
                .lower()
            )


            experience = job.get(
                "minExperienceLevel",
                999
            )


            #
            # Experience filter
            #

            if experience >= 5:

                continue



            #
            # Senior role filter
            #

            if any(
                keyword in role
                for keyword in blocked_keywords
            ):

                continue



            jobs.append(

                {
                    "title":
                        job.get(
                            "postingTitle",
                            ""
                        ),


                    "role":
                        job.get(
                            "roleDesignation",
                            ""
                        ),


                    "location":
                        job.get(
                            "location",
                            ""
                        ),


                    "experience":
                        experience,


                    "skills":
                        job.get(
                            "preferredSkills",
                            ""
                        ),


                    "apply_id":
                        job.get(
                            "postingId",
                            ""
                        )
                }

            )



        print(
            "Filtered Infosys jobs:",
            len(jobs)
        )


        return jobs