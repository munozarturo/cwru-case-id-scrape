

from typing import Any, Callable, Iterable

from scraper.scraper import Scraper


class SequentialScraper(Scraper):
    def __init__(self, url: str | Iterable[str], request_func: Callable[[str], str], scrape_func: Callable[[str], str]) -> None:
        super().__init__(url, request_func, scrape_func)
        
    def run(self) -> list[Any]:
        raise NotImplementedError("BatchScraper.run() is not implemented.")