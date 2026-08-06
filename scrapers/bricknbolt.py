import csv
import os
import requests


class BricknBoltScraper:

    def __init__(self):

        self.url = (
            "https://guardian-prod.bricknbolt.com/"
            "clientWebsite/api/bnbWebsite/career/jobPosting"
        )


    def fetch_jobs(self):

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }


        response = requests.get(
            self.url,
            headers=headers
        )

        response.raise_for_status()


        data = response.json()


        jobs = []


        for job in data["responseData"]:

            # ignore expired jobs
            if job["isExpired"]:
                continue


            jobs.append(job)


        print(
            f"Fetched {len(jobs)} active jobs"
        )


        return jobs



    def save_jobs(self, jobs):

        os.makedirs(
            "output",
            exist_ok=True
        )


        file_path = (
            "output/bricknbolt_jobs.csv"
        )


        if not jobs:
            print("No jobs found")
            return


        # Take columns dynamically from API response
        fieldnames = jobs[0].keys()


        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:


            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )


            writer.writeheader()

            writer.writerows(jobs)


        print(
            f"Saved {len(jobs)} jobs to {file_path}"
        )



    def run(self):

        print(
            "Fetching Brick&Bolt jobs..."
        )


        jobs = self.fetch_jobs()


        self.save_jobs(jobs)


        print(
            "Brick&Bolt scraping completed"
        )