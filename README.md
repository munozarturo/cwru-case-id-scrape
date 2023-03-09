# Case Western Reserve University - Case ID Scrape

Library to scrape information from the [Case Western University Directory](https://webapps.case.edu/directory/index.html).

## Usage

To use this library use one of the Scraper classes:

* BatchScraper
* SequentialScraper
* or create your own by extending the Scraper class.

Sample Usage:

```python3
import re
from itertools import product
from urllib.request import urlopen
from cwru.cwru import generate_query_url
from scraper import SequentialScraper

# create a list of urls to be queried
urls: list[str] = [
    # generate a query url
    generate_query_url(seach_text=query, category="student")
    for query in [
        # generate a cartesian product of all possible 3 letter combinations in the latin alphabet
        f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=3)
    ]
]

# create a scraper instance
scraper: SequentialScraper = SequentialScraper(
    # specify urls to be scraped
    url=urls,
    # specify function to fetch the url content
    request_func=lambda url: urlopen(url).read().decode("utf-8"),
    # specify the function to scrape the url content
    scrape_func=lambda html: list(set(re.findall("[\w\.-]+@case.edu+", html))),
)

# store the results of the scrape by running the scraper
results: list[list[str]] = scraper.run(
    # specify a function to be called before every scrape (specific to SequentialScraper)
    callback=lambda i, url: print(f"Scraping {i} of {len(urls)}: {url}")
)
```
