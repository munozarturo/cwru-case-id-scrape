from itertools import product
from scrape import generate_query_url

"""
List of possible pseudo given names.
Generated with the cartesian product of the lowercase alphabet ^ 3.
"""
given_names: list[str] = [f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=3)]

# quick check that every possible combination has been generated
assert len(given_names) == 26**3

query_urls: list[str] = [generate_query_url(given_name=given_name, category="student") for given_name in given_names]

