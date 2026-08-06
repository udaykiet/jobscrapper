import requests
import json


class CoforgeScraper:


    def __init__(self):

        self.url = (
            "https://public.zwayam.com/jobs/search"
        )



    def fetch_jobs(self):

        jobs = []


        headers = {

            "Accept":
            "application/json, text/plain, */*",

            "User-Agent":
            "Mozilla/5.0",

            "Origin":
            "https://careers.coforge.com",

            "Referer":
            "https://careers.coforge.com/"

        }



        pagination_start = 0



        while True:


            print(
                "Fetching Coforge page:",
                pagination_start
            )



            filter_cri = {

                "paginationStartNo":
                pagination_start,

                "selectedCall":
                "sort",

                "sortCriteria":
                {
                    "name":
                    "modifiedDate",

                    "isAscending":
                    False
                },

                "anyOfTheseWords":
                ""

            }



            data = {

                "filterCri":
                json.dumps(filter_cri),

                "domain":
                "careers.coforge.com",

                "companyId":
                "MTUxNzM="

            }



            response = requests.post(

                self.url,

                data=data,

                headers=headers,

                timeout=30

            )



            print(
                "Status:",
                response.status_code
            )



            response.raise_for_status()



            result = response.json()



            job_list = (

                result
                .get("data", {})
                .get("data", [])

            )



            print(
                "Jobs received:",
                len(job_list)
            )



            if not job_list:

                print(
                    "No more Coforge jobs"
                )

                break




            for item in job_list:


                source = item.get(
                    "_source",
                    {}
                )



                locations = source.get(
                    "jobLocationRecord",
                    []
                )



                location = ""

                country = ""



                if locations:

                    location = locations[0].get(
                        "formattedLocation",
                        ""
                    )


                    country = locations[0].get(
                        "country",
                        ""
                    )



                #
                # India filter
                #

                if country != "India":

                    continue




                jobs.append(

    {

        "title":
        source.get(
            "jobTitle",
            ""
        ),


        "job_id":
        source.get(
            "referenceNumber",
            ""
        ),


        "designation":
        source.get(
            "designation",
            ""
        ),


        "location":
        location,


        "experience":
        source.get(
            "yrsOfExperience",
            ""
        ),


        "skills":
        source.get(
            "skillSet",
            ""
        ),


        "posted_date":
        source.get(
            "createDate",
            ""
        ),


        "url":
        (
            "https://careers.coforge.com/job/"
            +
            source.get(
                "jobUrl",
                ""
            )
        )

    }

)



            print(
                "Total collected:",
                len(jobs)
            )



            pagination_start += len(job_list)




        print(
            "Final Coforge jobs count:",
            len(jobs)
        )


        return jobs