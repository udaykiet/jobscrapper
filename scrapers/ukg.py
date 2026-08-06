import requests


class UKGScraper:


    def __init__(self):

        self.url = (
            "https://apply.ukg.com/api/pcsx/search"
        )



    def fetch_jobs(self):

        jobs = []


        start = 0

        page_size = 10



        headers = {

            "Accept": "application/json",

            "User-Agent":
            "Mozilla/5.0"

        }



        while True:


            print(
                "Fetching UKG page start:",
                start
            )


            params = {


                "domain":
                "ukg.com",


                "query":
                "java",


                "location":
                "Noida, UP, India",


                "start":
                start,


                "sort_by":
                "relevance",


                "filter_distance":
                160,


                "filter_include_remote":
                1,


                "filter_include_relocation":
                0

            }



            response = requests.get(

                self.url,

                params=params,

                headers=headers,

                timeout=30

            )



            response.raise_for_status()



            data = response.json()



            positions = (

                data
                .get("data", {})
                .get("positions", [])

            )



            print(
                "Jobs received:",
                len(positions)
            )



            if not positions:

                print(
                    "No more jobs"
                )

                break



            for job in positions:



                position_url = job.get(
                    "positionUrl",
                    ""
                )



                apply_url = ""

                if position_url:

                    apply_url = (
                        "https://apply.ukg.com"
                        + position_url
                    )



                jobs.append(

                    {

                        "job_id":
                        job.get(
                            "displayJobId",
                            ""
                        ),


                        "title":
                        job.get(
                            "name",
                            ""
                        ),


                        "location":
                        ", ".join(
                            job.get(
                                "locations",
                                []
                            )
                        ),


                        "department":
                        job.get(
                            "department",
                            ""
                        ),


                        "work_type":
                        job.get(
                            "workLocationOption",
                            ""
                        ),


                        "url":
                        apply_url

                    }

                )



            print(
                "Total collected:",
                len(jobs)
            )



            #
            # Next page
            #

            if len(positions) < page_size:

                print(
                    "Last page reached"
                )

                break



            start += 10



        print(
            "Final UKG jobs count:",
            len(jobs)
        )


        return jobs