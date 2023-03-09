from types import NoneType
from typing import Union
from validate.vval import validate

LOG_NUM: int = 0
PRINT: bool = True
LOG: bool = True

def set_print(print_: bool) -> None:
    global PRINT
    PRINT = print_
    
def set_log(log_: bool) -> None:
    global LOG
    LOG = log_


def log(msg: str, indent_level: int = 0, source: str | NoneType = None) -> None:
    """
    Print `msg` to console and write it to `log.txt`.

    Args:
        msg (str): Message to be logged.
        indent_level (int, optional): Indentation level. Defaults to 0.
    """
    
    validate(msg, str)
    validate(indent_level, int)
    validate(source, (str, NoneType))
    
    global LOG_NUM
    
    indent: str = "    " * indent_level
    
    if source is not None:
        _msg: str = f"{str(LOG_NUM).rjust(5)}  {indent}{source}: {msg}"
    else:
        _msg: str = f"{str(LOG_NUM).rjust(5)}  {indent} {msg}"
    
    global PRINT
    if PRINT:
        print(_msg)
    
    global LOG
    if LOG:
        with open("log.txt", "a") as file:
            file.write(_msg + "\n")
    
    LOG_NUM += 1