import requests


class OracleScraper:


    def __init__(self):

        self.url = (
            "https://eeho.fa.us2.oraclecloud.com/"
            "hcmRestApi/resources/latest/recruitingCEJobRequisitions"
        )



    def fetch_jobs(self):

        headers = {

            "User-Agent": "Mozilla/5.0",

            "Accept": "application/json"

        }



        limit = 20
        offset = 0

        jobs = []

        total_jobs = None



        while True:


            params = {


                "onlyData": "true",


                "expand": (
                    "requisitionList.workLocation,"
                    "requisitionList.otherWorkLocations,"
                    "requisitionList.secondaryLocations,"
                    "flexFieldsFacet.values,"
                    "requisitionList.requisitionFlexFields"
                ),


                "finder": (
                    "findReqs;"
                    "siteNumber=CX_45001,"
                    "facetsList=LOCATIONS;WORK_LOCATIONS;"
                    "WORKPLACE_TYPES;TITLES;CATEGORIES;"
                    "ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,"
                    f"limit={limit},"
                    f"offset={offset},"
                    "locationId=300000000106947,"
                    "sortBy=POSTING_DATES_DESC"
                )

            }



            response = requests.get(

                self.url,

                params=params,

                headers=headers,

                timeout=30

            )


            response.raise_for_status()



            data = response.json()



            item = data["items"][0]



            if total_jobs is None:


                total_jobs = item["TotalJobsCount"]


                print(
                    f"Total Oracle Jobs Found: {total_jobs}"
                )



            requisitions = item["requisitionList"]



            if not requisitions:

                break



            print(
                f"Fetched {len(requisitions)} jobs "
                f"(offset={offset})"
            )



            for job in requisitions:


                jobs.append(

                    {


                        "title":
                        job.get(
                            "Title",
                            ""
                        ),



                        "role":
                        job.get(
                            "Title",
                            ""
                        ),



                        "location":
                        job.get(
                            "PrimaryLocation",
                            ""
                        ),



                        "experience":
                        "",



                        "skills":
                        "",



                        "apply_id":
                        job.get(
                            "Id",
                            ""
                        )

                    }

                )



            offset += limit



            if len(jobs) >= total_jobs:

                break




        print(
            "Total Oracle jobs:",
            len(jobs)
        )


        return jobs



    def run(self):

        print(
            "Fetching Oracle jobs...\n"
        )

        return self.fetch_jobs()