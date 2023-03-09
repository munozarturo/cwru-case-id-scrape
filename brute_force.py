from itertools import product
import re
from urllib.request import urlopen
from cwru.cwru import generate_query_url
from log import Logger
from scraper import SequentialScraper

"""
This module mainly tries to collect all student emails from the university
by using every possible 3 letter combination of the alphabet and a wildcard to
match all possible names.

There are a few limitations to this:
- Using the requests library without some form of university authetication limits the
  search results to 10 per query.
  - If some way to authenticate with a unversity account is found, this would remove
    this limitation, and allow for up to 250 results per page which would exponentially
    speed up the scraping process (around 600 queries instead of 17576).

General Notes
- This approach is not particularly fast -- could be due to a bottleneck or just
  its brute force nature.
- This approach of brute forcing names will not match all possible names, but it
  gets close enough to be useful.
  - Some names that will not be matched: R'Ay, etc.

"""

logger: Logger = Logger(print_=True, file_=True, file_path="log.txt")

urls: list[str] = [generate_query_url(seach_text=query, category="student") for query in
    [f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=3)]]

scraper: SequentialScraper = SequentialScraper(
    url=urls,
    request_func=lambda url: urlopen(url).read().decode("utf-8"),
    scrape_func=lambda html: list(set(re.findall('[\w\.-]+@case.edu+', html))),
)

results: list[list[str]] = scraper.run(
    callback=lambda i, url: Logger.log(f"Scraping {i} of {len(urls)}: {url}")
)