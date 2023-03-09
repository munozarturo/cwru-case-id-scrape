from itertools import product
from pathlib import Path
from scrape import RequestError, generate_query_url, scrape_info

# output file
output_to: Path = Path("results2.txt")
dump_on_exit: Path = Path("dump2.txt")

"""
List of possible pseudo given names.
Generated with the cartesian product of the lowercase alphabet ^ 3.
"""
given_names: list[str] = [f"{''.join(c)}*" for c in product("abcdefghijklmnopqrstuvwxyz", repeat=3)]

# quick check that every possible combination has been generated
assert len(given_names) == 26**3

try:
    # scrape all query urls
    i: int = 0
    while given_names:
        # get query url
        current_name: str = given_names[0]
        query_url: str = generate_query_url(given_name=given_names.pop(0), category="student")
        
        # print progress
        log(f"Scraping {current_name}... {i+1}/{len(given_names)} ({round((i+1)/len(given_names)*100, 2)}%) {len(given_names)} remaining...")
        
        # get results
        try:
            results: list[str] = scrape_info(query_url)
            
            # print results
            log(f"  Found {len(results)} results")

            # write results to file
            for result in results:
                with open(output_to, "a") as file:
                    file.write(result + "\n")
        except RequestError as e:
            # if there is an error, add the query url to the list
            log(f"Error scraping {current_name}...")
            log(f"\tAdded to query_urls list.")
            
            given_names.append(current_name)
            
        i += 1
except Exception as e:
    log(f"Error: {e}")
except KeyboardInterrupt:
    log("Exiting...")
    log(f"Results saved to '{output_to}'.")
    log(f"Dumping remaining query urls to '{dump_on_exit}'.")
    
    with open(dump_on_exit, "w") as file:
        for name in given_names:
            file.write(name + "\n")
    
    exit(0)