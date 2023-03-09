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


def batch_request_urls(urls: list[tuple(str, str)], dump: str | Path | Any, _sep: str = "\n"):
    """
    Batch request and download urls.

    Args:
        urls (list[tuple): List of tuples containing the name and url to download.
        dump (str | Path | Any): The location to dump the downloaded files. If a directory, the files will be dumped there. If a file, the files will be appended to the file.
        _sep (str, optional): Separator used if dumping to a single file. Defaults to "\n".

    """
    
    validate_iterable(urls, tuple)
    dump = Path(dump) if not isinstance(dump, Path) else dump
    validate(_sep, str)
    
    if not dump.is_dir():
        if not dump.exists():
            dump.mkdir(parents=True)

    for name, url in urls:
        request = urlopen(url)
        
        html: str = request.read().decode("utf-8")
        
        if dump.is_dir():
            with open(f"{dump}/{name}.html", "w") as f:
                f.write(html)
        else:
            with open(dump, "a") as f:
                f.write(_sep + html)


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