from typing import Any, Callable, Iterable
from scraper.scraper import Scraper
from validate import validate


class SequentialScraper(Scraper):
    def __init__(
        self,
        url: str | Iterable[str],
        request_func: Callable[[str], str],
        scrape_func: Callable[[str], str],
    ) -> None:
        """
        Sequential scraper.

        Will scrape urls sequentially. Meaning it will request the first url, scrape it, then request the second url, scrape it, and so on.

        Args:
            url (str | Iterable[str]): url or urls to scrape.
            request_func (Callable[[str], str]): function to request html from a url. Expects single str argument and returns str.
            scrape_func (Callable[[str], str]): function to scrape html. Expects single str argument and returns Any.
        """

        super().__init__(url, request_func, scrape_func)

    def run(self, callback: Callable[[int, str], Any] = None) -> list[Any]:
        """
        Run the sequential scraper.

        Args:
            callback (Callable[[int, str], Any], optional): Called at the start of every sequential parse iteration.
                It is called with the current url iteration number and the url. Defaults to None.

        Returns:
            list[Any]: List of results.
        """

        # validate that callback is a callable
        validate(callback, Callable)

        # create a list to store the results
        results: list[Any] = []

        # loop through the urls
        for i, url in enumerate(self.urls):
            # if a callback is provided, call it
            if callback is not None:
                callback(i, url)

            # request the url and scrape the response
            response = self.request_func(url)
            scraped: Any = self.scrape_func(response)

            print(scraped)

            results.append(scraped)

        # return the results
        return results
