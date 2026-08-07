import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



class DeltaScraper:


    def __init__(self):

        self.base_url = (
            "https://dth.avature.net"
        )

        self.search_url = (
            "https://dth.avature.net/en_US/careers/SearchJobs/"
        )



    def fetch_jobs(self):

        jobs = []

        offset = 0


        headers = {

            "User-Agent":
            "Mozilla/5.0"

        }



        while True:


            print(
                "Fetching Delta page offset:",
                offset
            )


            params = {

                "jobOffset":
                offset

            }



            response = requests.get(

                self.search_url,

                params=params,

                headers=headers,

                timeout=30

            )


            response.raise_for_status()



            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )



            job_items = soup.select(

                "ul.list--jobs li.list__item"

            )



            print(

                "Jobs found:",
                len(job_items)

            )



            if not job_items:

                break



            for item in job_items:


                #
                # title + job url
                #

                title_element = item.select_one(

                    ".list__item__text__title a"

                )


                if not title_element:

                    continue



                title = (

                    title_element
                    .get_text(strip=True)

                )


                job_url = title_element.get(
                    "href"
                )



                #
                # location + ref
                #

                subtitle = item.select(

                    ".list__item__text__subtitle span"

                )


                location = ""

                job_id = ""



                if len(subtitle) >= 1:

                    location = (

                        subtitle[0]
                        .get_text(strip=True)

                    )


                if len(subtitle) >= 2:

                    ref_text = (

                        subtitle[1]
                        .get_text(strip=True)

                    )


                    job_id = (

                        ref_text
                        .replace(
                            "Ref #",
                            ""
                        )
                        .strip()

                    )



                #
                # apply link
                #

                apply_element = item.select_one(

                    ".list__item__actions a.button--link"

                )


                apply_url = ""


                if apply_element:

                    apply_url = apply_element.get(
                        "href"
                    )



                if job_url:

                    job_url = urljoin(

                        self.base_url,

                        job_url

                    )



                if apply_url:

                    apply_url = urljoin(

                        self.base_url,

                        apply_url

                    )



                jobs.append(

                    {

                        "title":
                        title,


                        "job_id":
                        job_id,


                        "location":
                        location,


                        "url":
                        job_url,


                        "apply_url":
                        apply_url

                    }

                )




            #
            # Pagination
            #

            next_page = soup.select_one(

                "a.paginationNextLink"

            )


            if not next_page:

                print(
                    "No more pages"
                )

                break



            offset += 10




        print(

            "Total Delta jobs:",
            len(jobs)

        )


        return jobs