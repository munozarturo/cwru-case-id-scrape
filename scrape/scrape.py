from pathlib import Path
from typing import Any
from validate import validate_iterable, validate, is_callable
from validate.vval import validate_option

from urllib.parse import quote
from urllib.request import urlopen

import re


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class RequestError(Error):
    """Base class for request exceptions."""
    pass


def scrape_info_regex(url: str) -> list[str]:
    """
    Scrape email addresses from a Case Western Reserve University directory query url.

    Args:
        url (str): URL to scrape.

    Returns:
        list[str]: list of @case.edu email addresses.
    """
    
    validate(url, str)
    
    # request content
    request = urlopen(url)
    
    # check for errors
    if request.getcode() == 500:
        raise RequestError("Server Error")
    
    html: str = request.read().decode("utf-8")
    # find all email addresses that match the pattern email@case.edu
    matches: list[str] = list(re.findall('[\w\.-]+@case.edu+', html))
    
    """These dont' work properly."""
    # too many matches
    if re.match(r'Your search returned more than 10 matches.', html):
        raise RequestError("Too many matches")
    
    # no matches
    if re.match(r'Sorry, there are no results for your search.', html):
        raise RequestError("No matches")
    
    # convert to set and then back to list to remove duplicates
    return list(set(matches))