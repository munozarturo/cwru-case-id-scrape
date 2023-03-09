from validate import validate, validate_iterable, validate_option
from typing import Any, Callable, Iterable

class Scraper:
    @property
    def urls(self) -> Iterable[str]:
        return self.__urls
    
    @urls.setter
    def urls(self, urls: str | Iterable[str]) -> None:
        if isinstance(urls, str):
            self.__urls = [urls]
        else:
            validate_iterable(urls, str)
            
            self.__urls = urls
        
    @urls.deleter
    def urls(self) -> None:
        self.__urls = []
        
    @property
    def request_func(self) -> Callable[[str], str]:
        return self.__request_func
    
    @request_func.setter
    def request_func(self, request_func: Callable[[str], str]) -> None:
        validate(request_func, Callable)
        
        self.__request_func = request_func
        
    @request_func.deleter
    def request_func(self) -> None:
        raise AttributeError("Cannot delete `request_func`.")
    
    @property
    def scrape_func(self) -> Callable[[str], str]:
        return self.__scraper_func
    
    @scrape_func.setter
    def scrape_func(self, scrape_func: Callable[[str], str]) -> None:
        validate(scrape_func, Callable)
        
        self.__scraper_func = scrape_func
        
    @scrape_func.deleter
    def scrape_func(self) -> None:
        raise AttributeError("Cannot delete `scrape_func`.")
    
    def __init__(self, 
                 url: str | Iterable[str], 
                 request_func: Callable[[str], str], 
                 scrape_func: Callable[[str], str]) -> None:
        
        self.__urls: Iterable[str] = []
        self.__request_func: Callable[[str], str] = None
        self.__scraper_func: Callable[[str], Any] = None
        
        self.urls = url
        self.request_func = request_func
        self.scrape_func = scrape_func
        
    def run(self) -> Any:
        raise NotImplementedError("`run()` must be implemented.")