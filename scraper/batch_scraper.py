

from typing import Any, Callable, Iterable
from scraper.scraper import Scraper


class BatchScraper(Scraper):
    def __init__(self, url: str | Iterable[str], request_func: Callable[[str], str], scrape_func: Callable[[str], str]) -> None:
        super().__init__(url, request_func, scrape_func)
        
    def run(self) -> list[Any]:
        results: list[Any] = []
        
        for url in self.urls:
            response = self.request_func(url)
            results.append(self.scrape_func(response))
            
        return results