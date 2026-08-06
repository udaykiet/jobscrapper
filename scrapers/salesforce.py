import requests



class SalesforceScraper:


    def __init__(self):

        self.url = (
            "https://a.sfdcstatic.com/"
            "digital/xsf/careers/prod/jobs_1.json"
        )



    def fetch_jobs(self):

        jobs = []


        print(
            "Fetching Salesforce jobs..."
        )



        headers = {

            "Accept":
            "application/json",

            "User-Agent":
            "Mozilla/5.0"

        }



        response = requests.get(

            self.url,

            headers=headers,

            timeout=60

        )


        response.raise_for_status()



        data = response.json()



        all_jobs = data.get(
            "Report_Entry",
            []
        )



        print(
            "Total jobs received:",
            len(all_jobs)
        )



        for job in all_jobs:



            countries = job.get(
                "Countries",
                []
            )



            #
            # Only India jobs
            #

            if "India" not in countries:

                continue



            external_url = job.get(
                "External_Job_Posting_Site",
                ""
            )



            jobs.append(

                {


                    "job_id":
                    job.get(
                        "Job_Requisition_Ref_ID",
                        ""
                    ),



                    "title":
                    job.get(
                        "Job_Posting_Title",
                        ""
                    ),



                    "location":
                    job.get(
                        "Job_Requisition_Primary_Location",
                        ""
                    ),



                    "country":
                    ", ".join(
                        countries
                    ),



                    "job_family":
                    job.get(
                        "Job_Family_Group",
                        ""
                    ),



                    "employment_type":
                    job.get(
                        "Time_Type",
                        ""
                    ),



                    "employee_type":
                    job.get(
                        "Employee_Type",
                        ""
                    ),



                    "url":
                    external_url

                }

            )



        print(
            "India Salesforce jobs:",
            len(jobs)
        )



        return jobs