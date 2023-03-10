from itertools import product
import os
from cwru.cwru import generate_query_url
from log import Logger
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from scraper import BatchScraper
import re
import dotenv
from selenium.webdriver.common.by import By

"""
To use this module you must have a .env file in the root directory with the following variables:
CWRU_USERNAME and CWRU_PASSWORD.

The file should look something like this:
```
CWRU_USERNAME=your_username
CWRU_PASSWORD=your_password
```

Additionally you must have the chromedriver.exe file in the web_drivers directory.
It is possible to download the chromedriver.exe file from here: https://chromedriver.chromium.org/downloads.
Check the version of your chrome browser and download the appropriate chromedriver.exe file and then move it to this directory.

***
This module follows a very similar approach to the brute_force.py module, but with a few key differences:
- It queries the University's website by finding a way to provide authentication.
    - By providing valid authentication, the university's website allows for up to 250 results per page.
    - Unly uses 2 letter combinations which reduces the number of queries (about 600 instead of 17576).
- The scraping function remains the same.

Working with the selenium library has provided an insight on authentication:
* It might be done through a cookie, but I'm not sure.
    * Investing time into this would be a good idea. Since it would speed up the process of requesting.
    
Additionally, I have noticed that the query results website has no ids, which makes parsing harder so
I stuck to the regex parser for this example.
"""

dotenv.load_dotenv()

logger: Logger = Logger(print_=True, file_=True, file_path="auth_request_log.rlog")


def request_func(url: str) -> None:
    """
    HTML request function using Selenium chromedriver.
    This is a very slow process, and is definitely not the most elegant way of providing authentication.
    But it is A WAY of providing authentication.

    Args:
        url (str): URL to request.

    Returns:
        str: HTML source.
    """

    # set up chrome driver
    service: Service = Service(executable_path="web_drivers/chromedriver.exe")
    driver: webdriver.Chrome = webdriver.Chrome(service=service)

    # open url
    driver.get(url)

    try:
        # find the login prompt
        driver.find_element(By.PARTIAL_LINK_TEXT, "log in").click()
        
        # enter credentials
        driver.find_element(By.ID, "username").send_keys(os.getenv("CWRU_USERNAME"))
        driver.find_element(By.ID, "password").send_keys(os.getenv("CWRU_PASSWORD"))
        driver.find_element(By.ID, "login-submit").click()
    except:
        """
        ignore the exception, because presumable the login prompt has not been found, which means that there are no results.
        or less than 10 results.
        in the case that there are no results this is ingored
        in the case that there are less than 10 results, the data is still scraped.
        """ 
        pass

    # get html source
    html: str = driver.page_source

    # return html source
    return html


# create a list of urls to scrape
urls: list[str] = [
    generate_query_url(seach_text=query, category="student")
    for query in [
        f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=2)
    ]
]

# create a scraper
scraper: BatchScraper = BatchScraper(
    url=urls,
    request_func=request_func,
    scrape_func=lambda html: list(set(re.findall("[\w\.-]+@case.edu+", html))),
    path="dump",
)

# run the scraper
results: list[list[str]] = scraper.run(
    request_callback=lambda i, url: logger.log(f"Requesting {i} of {len(urls)}: {url}"),
    scrape_callback=lambda i, url: logger.log(f"Scraping {i} of {len(urls)}: {url}"),
    delete_after_use=False
)

# flatten the results
results: list[str] = [r for r in results for r in r]

# write the results to a file
with open("auth_request_results.dump", "w") as f:
    f.write("\n".join(results))