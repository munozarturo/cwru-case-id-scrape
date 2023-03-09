from itertools import product
from scrape import generate_query_url, scrape_info

"""
List of possible pseudo given names.
Generated with the cartesian product of the lowercase alphabet ^ 3.
"""
given_names: list[str] = [f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=3)]

# quick check that every possible combination has been generated
assert len(given_names) == 26**3

# generate a list of query urls
query_urls: list[str] = [generate_query_url(given_name=given_name, category="student") for given_name in given_names]
    
for i, query_url in enumerate(query_urls):
    print(f"Scraping {i+1}/{len(query_urls)} ({round((i+1)/len(query_urls)*100, 2)}%)")
    
    results: list[str] = scrape_info(query_url=query_url)

    for result in results:
        with open("results.txt", "a") as file:
            file.write(result + "\n")