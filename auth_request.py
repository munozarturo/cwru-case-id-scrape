from itertools import product


def auth_request() -> None:
    
    
    query_list: list[str] = [f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=2)]
    
    