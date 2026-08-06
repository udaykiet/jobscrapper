from dataclasses import dataclass


@dataclass
class Job:

    id: str
    company: str
    title: str
    location: str
    posted_date: str
    url: str