import csv
import os


class CSVWriter:


    def __init__(self, filename):

        self.filename = filename



    def write(self, jobs):

        os.makedirs(
            "output",
            exist_ok=True
        )


        path = (
            f"output/{self.filename}"
        )


        if not jobs:
            print("No jobs found")
            return



        fieldnames = jobs[0].keys()



        with open(
            path,
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
            f"Saved {len(jobs)} jobs -> {path}"
        )