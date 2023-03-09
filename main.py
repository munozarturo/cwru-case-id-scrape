from itertools import product
from pathlib import Path
from scrape import RequestError, generate_query_url, scrape_info

# output file
output_to: Path = Path("results.txt")

"""
List of possible pseudo given names.
Generated with the cartesian product of the lowercase alphabet ^ 3.
"""
given_names: list[str] = [f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=3)]

# quick check that every possible combination has been generated
assert len(given_names) == 26**3

# generate a list of query urls
query_urls: list[str] = [generate_query_url(given_name=given_name, category="student") for given_name in given_names]

# scrape all query urls
i: int = 0
while query_urls:
    query_url: str = query_urls.pop(0)
    
    # print progress
    print(f"Scraping {i+1}/{len(query_urls)} ({round((i+1)/len(query_urls)*100, 2)}%)")
    
    # get results
    try:
        results: list[str] = scrape_info(query_url)
        
        # print results
        print(f"Found {len(results)} results")

        # write results to file
        for result in results:
            with open(output_to, "a") as file:
                file.write(result + "\n")
    except RequestError as e:
        # if there is an error, add the query url to the list
        print(f"Error scraping {query_url}...")
        print(f"\tAdded to query_urls list.")
        
        query_urls.append(query_url)