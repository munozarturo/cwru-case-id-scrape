from validate.vval import validate

LOG_NUM: int = 0

def log(msg: str, indent_level: int = 0, source: str = str | None) -> None:
    """
    Print `msg` to console and write it to `log.txt`.

    Args:
        msg (str): Message to be logged.
        indent_level (int, optional): Indentation level. Defaults to 0.
    """
    
    validate(msg, str)
    validate(indent_level, int)
    validate(source, [str, None])
    
    indent: str = "    " * indent_level
    
    if source is None:
        _msg: str = f"{LOG_NUM}{indent}{source}: {msg}"
    
    print(_msg)
    
    with open("log.txt", "a") as file:
        file.write(_msg + "\n")
    
    LOG_NUM += 1