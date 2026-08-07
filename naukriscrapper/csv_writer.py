import csv


class CSVWriter:


    def __init__(self, filename="jobs.csv"):

        self.filename = filename



    def save_jobs(self, jobs):

        if not jobs:
            print("No jobs to save")
            return


        print("Saving jobs to CSV...")


        with open(
            self.filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:


            writer = csv.DictWriter(
                file,
                fieldnames=jobs[0].keys()
            )


            writer.writeheader()


            writer.writerows(jobs)



        print(
            f"Saved {len(jobs)} jobs into {self.filename}"
        )