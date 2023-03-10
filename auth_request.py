import os
import dotenv

dotenv.load_dotenv(".env")

from itertools import product
import urllib.request
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

# create password manager
password_manager: urllib.request.HTTPPasswordMgrWithDefaultRealm = urllib.request.HTTPPasswordMgrWithDefaultRealm()
# add username and password
password_manager.add_password(None, "https://webapps.case.edu", os.getenv("CWRU_USERNAME"), os.getenv("CWRU_PASSWORD"))

# create authentication handler
handler: urllib.request.HTTPBasicAuthHandler = urllib.request.HTTPBasicAuthHandler(password_manager)

# create a url opener
opener: urllib.request.OpenerDirector = urllib.request.build_opener(handler)
# install the opener
urllib.request.install_opener(opener)

# create a list of urls to scrape
urls: list[str] = [
    generate_query_url(seach_text=query, category="student")
    for query in [
        f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=2)
    ]
]

