import requests


class AmexScraper:

    def __init__(self):

        self.url = (
            "https://egug.fa.us2.oraclecloud.com/"
            "hcmRestApi/resources/latest/recruitingCEJobRequisitions"
        )


    def fetch_jobs(self):

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        limit = 10
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
                    "siteNumber=CX_1,"
                    "facetsList=LOCATIONS;WORK_LOCATIONS;WORKPLACE_TYPES;"
                    "TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,"
                    f"limit={limit},"
                    f"offset={offset},"
                    "locationId=300000000228786,"
                    "sortBy=POSTING_DATES_DESC"
                )
            }

            response = requests.get(
                self.url,
                params=params,
                headers=headers
            )

            response.raise_for_status()

            data = response.json()

            item = data["items"][0]

            if total_jobs is None:

                total_jobs = item["TotalJobsCount"]

                print(
                    f"Total Amex Jobs Found: {total_jobs}"
                )

            requisitions = item["requisitionList"]

            if not requisitions:
                break

            print(
                f"Fetched {len(requisitions)} jobs "
                f"(offset={offset})"
            )

            for job in requisitions:

                # Extract relevant job information
                job_data = {
                    "Id": job.get("Id"),
                    "Title": job.get("Title"),
                    "PostedDate": job.get("PostedDate"),
                    "PrimaryLocation": job.get("PrimaryLocation"),
                    "WorkplaceType": job.get("WorkplaceType"),
                    "HotJobFlag": job.get("HotJobFlag"),
                    "TrendingFlag": job.get("TrendingFlag"),
                    "BeFirstToApplyFlag": job.get("BeFirstToApplyFlag"),
                    "Relevancy": job.get("Relevancy"),
                    "PrimaryLocationCountry": job.get("PrimaryLocationCountry"),
                    "Language": job.get("Language")
                }

                # Extract work location details if available
                if job.get("workLocation") and len(job["workLocation"]) > 0:
                    work_location = job["workLocation"][0]
                    job_data["WorkLocationName"] = work_location.get("LocationName")
                    job_data["WorkLocationAddress"] = work_location.get("AddressLine1")
                    job_data["WorkLocationCity"] = work_location.get("TownOrCity")
                    job_data["WorkLocationPostalCode"] = work_location.get("PostalCode")
                else:
                    job_data["WorkLocationName"] = None
                    job_data["WorkLocationAddress"] = None
                    job_data["WorkLocationCity"] = None
                    job_data["WorkLocationPostalCode"] = None

                jobs.append(job_data)

            offset += limit

            if len(jobs) >= total_jobs:
                break

        print(
            f"Fetched {len(jobs)} jobs from Amex"
        )

        return jobs
