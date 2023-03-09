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
    def outpath(self) -> Path | NoneType:
        return self.__outpath
    
    @outpath.setter
    def outpath(self, outpath: str | Path | NoneType | Any) -> None:
        try:
            self.__outpath = outpath if isinstance(outpath, Path) else Path(outpath)
        except :
            raise TypeError("`outpath` must be pathlike.")
        
    @outpath.deleter
    def outpath(self) -> None:
        self.__outpath = None
    
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
    def do_log(self) -> bool:
        return self.__do_log
    
    @do_log.setter
    def do_log(self, do_log: bool) -> None:
        validate(do_log, bool)
        
        self.__do_log = do_log
    
    def __init__(self, outpath: str | Path | NoneType | Any, print_: bool = True, do_log: bool = True) -> None:
        self.__log_num: int = 0
        self.__print: bool = True
        self.__do_log: bool = True
        self.__outpath: Path | NoneType = None
        
        self.print = print_
        self.do_log = do_log
        self.outpath = outpath
        
    def log(self, msg: str, indent_level: int = 0, source: str | NoneType = None) -> None:
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
        
        if self.do_log:
            with open(self.outpath, "a") as file:
                file.write(_msg + "\n")
        
        self.__log_num += 1