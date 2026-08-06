import requests


class PublicisSapientScraper:


    def __init__(self):

        self.url = (
            "https://careers.publicissapient.com/"
            "bin/ps-redesign/careersJobsearch"
        )



    def fetch_jobs(self):

        jobs = []


        start = 0

        page_size = 20



        headers = {

            "Accept":
            "application/json",

            "User-Agent":
            "Mozilla/5.0"

        }



        while True:


            print(
                "Fetching Publicis Sapient jobs start:",
                start
            )


            params = {


                "searchType":
                "/search",


                "lang":
                "en",


                "facetFields":
                (
                    "countryName,city,teams,"
                    "experienceLevel,remote,"
                    "typeOfEmployment"
                ),


                "q":
                "java",


                "start":
                start,


                "rows":
                page_size,


                "country":
                "India"

            }



            response = requests.get(

                self.url,

                params=params,

                headers=headers,

                timeout=30

            )



            response.raise_for_status()



            data = response.json()



            docs = (

                data
                .get("response", {})
                .get("docs", [])

            )



            print(
                "Jobs received:",
                len(docs)
            )



            if not docs:

                print(
                    "No more jobs"
                )

                break



            for job in docs:



                job_url = ""



                detail_url = job.get(
                    "jobDetailUrl",
                    ""
                )



                if detail_url:

                    job_url = (
                        "https://careers.publicissapient.com"
                        + detail_url
                    )



                jobs.append(

                    {

                        "job_id":
                        job.get(
                            "jobId",
                            ""
                        ),


                        "title":
                        job.get(
                            "name",
                            ""
                        ),


                        "location":
                        job.get(
                            "displayLocation",
                            ""
                        ),


                        "team":
                        job.get(
                            "teams",
                            ""
                        ),


                        "experience":
                        job.get(
                            "experienceLevel",
                            ""
                        ),


                        "employment_type":
                        job.get(
                            "typeOfEmployment",
                            ""
                        ),


                        "craft":
                        job.get(
                            "psCraft",
                            ""
                        ),


                        "url":
                        job_url

                    }

                )



            print(
                "Total collected:",
                len(jobs)
            )



            #
            # Pagination
            #

            if len(docs) < page_size:

                print(
                    "Last page reached"
                )

                break



            start += page_size



        print(
            "Final Publicis Sapient jobs:",
            len(jobs)
        )



        return jobs