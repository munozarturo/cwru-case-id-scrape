"""
This module mainly tries to collect all student emails from the university
by using every possible 3 letter combination of the alphabet and a wildcard to
match all possible names.

There are a few limitations to this:
* Using the requests library without some form of university authetication limits the
  search results to 10 per query.
    * If some way to authenticate with a unversity account is found, this would remove
      this limitation, and allow for up to 250 results per page which would exponentially
      speed up the scraping process (around 600 queries instead of 17576).

General Notes
* This approach is not particularly fast -- could be due to a bottleneck or just
  its brute force nature.
* This approach of brute forcing names will not match all possible names, but it
  gets close enough to be useful.
    * Some names that will not be matched: R'Ay, etc.

"""

from itertools import product
from pathlib import Path
from scrape import RequestError, generate_query_url, scrape_info

from log import log

def brute_force() -> None:
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
          query_url: str = generate_query_url(seach_text=given_names.pop(0), category="student")

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