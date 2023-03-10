import os
import re
import dotenv

dotenv.load_dotenv(".env")

from itertools import product
import requests
from cwru.cwru import generate_query_url
from log import Logger
from scraper import BatchScraper

"""
This module follows a very similar approach to the brute_force.py module, but with a few key differences:
- It queries the University's website by providing authentication.
    - By providing valid authentication, the university's website allows for up to 250 results per page.
    - Unly uses 2 letter combinations which reduces the number of queries (about 600 instead of 17576).
- The scraping function aims to handle query errors better than brute_force.py by also matching error flags.
"""

logger: Logger = Logger(print_=True, file_=True, file_path="auth_request_log.rlog")

response = requests.get("https://webapps.case.edu/directory/lookup?search_text=aa*&surname=&givenname=ar*&department=&location=&category=all&search_method=regular",
             auth=(os.getenv("USERNAME"), os.getenv("PASSWORD")))

with open("dump.html", "w") as f:
    f.write(response.text)

# # create a list of urls to scrape
# urls: list[str] = [
#     generate_query_url(seach_text=query, category="student")
#     for query in [
#         f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=2)
#     ]
# ][0:5]

# scraper: BatchScraper = BatchScraper(
#     url=urls,
#     request_func=lambda url: urllib.request.urlopen(url).read().decode("utf-8"),
#     scrape_func=lambda html: list(set(re.findall("[\w\.-]+@case.edu+", html))),
#     path="dump"
# )

# scraper.run()