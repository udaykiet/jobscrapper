from scrapers.ey import EYScraper
from scrapers.oracle import OracleScraper
from scrapers.bricknbolt import BricknBoltScraper
from scrapers.amex import AmexScraper
from storage.csv_writer import CSVWriter
from scrapers.servicenow import ServiceNowScraper
from scrapers.capgemini import CapgeminiScraper
from scrapers.cognizant import CognizantScraper
from scrapers.infosys import InfosysScraper
from scrapers.cgi import CGIScraper
from scrapers.ukg import UKGScraper
from scrapers.publicis_sapient import PublicisSapientScraper
from scrapers.salesforce import SalesforceScraper
from scrapers.algoworks import AlgoworksScraper
from scrapers.virtusa import VirtusaScraper
from scrapers.coforge import CoforgeScraper
from scrapers.delta import DeltaScraper

def run_scraper(scraper, filename):

    print(f"\nRunning {scraper.__class__.__name__}")

    jobs = scraper.fetch_jobs()

    writer = CSVWriter(filename)

    writer.write(jobs)

    print("Completed\n")



scrapers = [
#     (
#         OracleScraper(),
#         "oracle_jobs.csv"
#     ),
#     (
#         BricknBoltScraper(),
#         "bricknbolt_jobs.csv"
#     ),
#     (
#         AlgoworksScraper(),
#         "algoworks_jobs.csv"
#     ),
#     (
#         AmexScraper(),
#         "amex_jobs.csv"
#     ),
#    (
#        EYScraper(),
#        "ey_jobs.csv"
#    ),
#    (
#         ServiceNowScraper(),
#         "servicenow_jobs.csv"
#    ),
#    (
#     CapgeminiScraper(),
#     "capgemini_jobs.csv"
# ),
# (
#     CognizantScraper(),
#     "cognizant_jobs.csv"
# ),
# (
#     InfosysScraper(),
#     "infosys_jobs.csv"
# ),
#     (
#         CGIScraper(),
#         "cgi_jobs.csv"
#     ),
    (
    UKGScraper(),
    "ukg_jobs.csv"
),
# (
#     PublicisSapientScraper(),
#     "publicis_sapient_jobs.csv"
# ),
# (
#     SalesforceScraper(),
#     "salesforce_jobs.csv"
# ),
# (
#             AlgoworksScraper(),
#             "algoworks_jobs.csv"
#         ),
#         (
#     VirtusaScraper(),
#     "virtusa_jobs.csv"
# ),
# (
#     CoforgeScraper(),
#     "coforge_jobs.csv"
# ),
(
    DeltaScraper(),
    "delta_jobs.csv"
),

]



for scraper, filename in scrapers:

    run_scraper(
        scraper,
        filename
    )