from pathlib import Path
from typing import Any, Callable, Iterable
from scraper.scraper import Scraper


class BatchScraper(Scraper):
    @property
    def path(self) -> Path:
        return self.__path

    @path.setter
    def path(self, path: str | Path | Any) -> None:
        _path: Path = Path(path) if not isinstance(path, Path) else path

        if not _path.exists():
            _path.mkdir(parents=True)

        self.__path = _path

    @path.deleter
    def path(self) -> None:
        raise AttributeError("Cannot delete `path`.")

    def __init__(
        self,
        url: str | Iterable[str],
        request_func: Callable[[str], str],
        scrape_func: Callable[[str], str],
        path: str | Path | Any,
    ) -> None:
        """
        Batch scraper.

        Will scrape urls in parts. Will first request and store all urls, then scrape and delete all urls.

        Args:
            url (str | Iterable[str]): url or urls to scrape.
            request_func (Callable[[str], str]): function to request html from a url. Expects single str argument and returns str.
            scrape_func (Callable[[str], str]): function to scrape html. Expects single str argument and returns Any.
            path (str | Path | Any, optional): path to store requested html.
        """
        super().__init__(url, request_func, scrape_func)

        self.__path: Path = None
        self.path = path

    def run(
        self,
        request_callback: Callable[[int, str], Any] = None,
        scrape_callback: Callable[[int, str], Any] = None,
    ) -> list[Any]:
        """
        Run the batch scraper.

        Args:
            request_callback (Callable[[int, str], Any], optional): Called at the start of every sequential request iteration.
                It is called with the current url iteration number and the url. Defaults to None.
            scrape_callback (Callable[[int, str], Any], optional): Called at the start of every sequential scrape iteration.
                It is called with the current url iteration number and the url. Defaults to None.

        Returns:
            list[Any]: List of results.
        """

        for i, url in enumerate(self.urls):
            if request_callback is not None:
                request_callback(i, url)

            response = self.request_func(url)

            file_path: Path = Path(f"{self.path}/{i}.html")
            file_path.write_text(response)

        results: list[Any] = []

        for i, url in enumerate(self.urls):
            if scrape_callback is not None:
                scrape_callback(i, url)

            file_path: Path = Path(f"{self.path}/{i}.html")
            response: str = file_path.read_text()
            results.append(self.scrape_func(response))
            file_path.unlink()

        return results
