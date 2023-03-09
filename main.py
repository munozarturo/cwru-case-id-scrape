from itertools import product
from pathlib import Path
from scrape import RequestError, generate_query_url, scrape_info

from log import log

# output file
output_to: Path = Path("results.txt")
dump_on_exit: Path = Path("dump.txt")

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
    total_scraped: int = 0
    while given_names:
        # get query url
        current_name: str = given_names[0]
        query_url: str = generate_query_url(given_name=given_names.pop(0), category="student")
        
        if i > 26**3 - 6970:    
            # print progress
            log(f"Scraping {current_name}...")
            log(f"{i+1}/{len(given_names)} ({round((i+1)/len(given_names)*100, 2)}%) {len(given_names)} remaining...", indent_level=1)
            
            # get results
            try:
                # scrape
                results: list[str] = scrape_info(query_url)
                
                # update total scraped
                total_scraped += len(results)
                
                # print results
                log(f"Found {len(results)} results.", indent_level=1, source=current_name)
                log(f"Total scraped: {total_scraped}", indent_level=1)

                # write results to file
                for result in results:
                    with open(output_to, "a") as file:
                        file.write(result + "\n")
            except RequestError as e:
                # if there is an error, add the query url to the list
                log(f"Error scraping {current_name}...", indent_level=1, source=current_name)
                log(f"Added to query_urls list.", indent_level=2, source=current_name)
                
                given_names.append(current_name)
                
        i += 1
except Exception as e:
    log(f"Error: {e}")
except KeyboardInterrupt:
    log("Exiting...")
    log(f"Results saved to '{output_to}'.", indent_level=1)
    log(f"Dumping remaining query urls to '{dump_on_exit}'.", indent_level=1)
    
    with open(dump_on_exit, "w") as file:
        for name in given_names:
            file.write(name + "\n")
    
    exit(0)