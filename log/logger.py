from pathlib import Path
from types import NoneType
from typing import Any
from validate.vval import validate


class Logger:
    @property
    def log_num(self) -> int:
        return self.__log_num

    @log_num.setter
    def log_num(self, log_num: int) -> None:
        raise AttributeError("Cannot set log_num.")

    @log_num.deleter
    def log_num(self) -> None:
        raise AttributeError("Cannot delete log_num.")

    @property
    def file_path(self) -> Path | NoneType:
        return self.__path

    @file_path.setter
    def file_path(self, file_path: str | Path | NoneType | Any) -> None:
        try:
            self.__path = file_path if isinstance(file_path, Path) else Path(file_path)
        except:
            raise TypeError("`file_path` must be pathlike.")

    @file_path.deleter
    def file_path(self) -> None:
        self.__path = None

    @property
    def print(self) -> bool:
        return self.__print

    @print.setter
    def print(self, print_: bool) -> None:
        validate(print_, bool)

        self.__print = print_

    @print.deleter
    def print(self) -> None:
        raise AttributeError("Cannot delete print.")

    @property
    def file_(self) -> bool:
        return self.__file_

    @file_.setter
    def file_(self, file_: bool) -> None:
        validate(file_, bool)

        self.__file_ = file_

    def __init__(
        self, file_path: str | Path | NoneType | Any, print_: bool = True, file_: bool = True
    ) -> None:
        self.__log_num: int = 0
        self.__print: bool = True
        self.__file_: bool = True
        self.__path: Path | NoneType = None

        self.print = print_
        self.file_ = file_
        self.file_path = file_path

    def log(
        self, msg: str, indent_level: int = 0, source: str | NoneType = None
    ) -> None:
        """
        Print `msg` to console and write it to `log.txt`.

        Args:
            msg (str): Message to be logged.
            indent_level (int, optional): Indentation level. Defaults to 0.
        """

        validate(msg, str)
        validate(indent_level, int)
        validate(source, (str, NoneType))

        indent: str = "    " * indent_level

        if source is not None:
            _msg: str = f"{str(self.log_num).rjust(7)}  {indent} {source}: {msg}"
        else:
            _msg: str = f"{str(self.log_num).rjust(7)}  {indent} {msg}"

        if self.print:
            print(_msg)

        if self.file_:
            with open(self.file_path, "a") as file:
                file.write(_msg + "\n")

        self.__log_num += 1
