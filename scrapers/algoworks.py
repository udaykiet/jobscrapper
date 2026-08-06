import requests
import re
from bs4 import BeautifulSoup


class AlgoworksScraper:


    def __init__(self):

        self.url = (
            "https://algoworks.keka.com/careers/api/embedjobs/default/active/"
            "c1623220-7738-4bff-ba91-5a9f0bbe01fc"
        )



    def extract_field(self, text, field):

        pattern = (
            rf"{field}:\s*(.*)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )


        if match:

            return match.group(1).strip()


        return ""



    def extract_skills(self, text):

        skills = []


        keywords = [

            "Java",
            "Spring",
            "Spring Boot",
            "Microservices",
            "AWS",
            "Azure",
            "Docker",
            "Kubernetes",
            "Salesforce",
            "React",
            "Angular",
            "Python",
            "AI",
            "Machine Learning",
            "SQL",
            "DevOps"

        ]


        for skill in keywords:

            if skill.lower() in text.lower():

                skills.append(skill)



        return ", ".join(skills)




    def clean_html(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )


        return soup.get_text(
            " ",
            strip=True
        )



    def fetch_jobs(self):

        jobs = []


        print(
            "Fetching Algoworks jobs..."
        )


        response = requests.get(
            self.url,
            timeout=30
        )


        response.raise_for_status()


        data = response.json()



        for job in data:


            description = self.clean_html(
                job.get(
                    "description",
                    ""
                )
            )



            location = self.extract_field(
                description,
                "Location"
            )


            experience = self.extract_field(
                description,
                "Experience"
            )



            skills = self.extract_skills(
                description
            )



            jobs.append(

                {

                    "title":
                    job.get(
                        "title",
                        ""
                    ),


                    "role":
                    job.get(
                        "title",
                        ""
                    ),


                    "location":
                    location,


                    "experience":
                    experience,


                    "skills":
                    skills,


                    "apply_id":
                    job.get(
                        "id",
                        ""
                    )

                }

            )



        print(
            "Total Algoworks jobs:",
            len(jobs)
        )


        return jobs