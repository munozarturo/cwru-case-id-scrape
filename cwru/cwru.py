from validate import validate
from validate.vval import validate_option

from urllib.parse import quote


def generate_query_url(seach_text: str    = "",
                       surname: str       = "",
                       given_name: str    = "",
                       category: str      = "all",
                       search_method: str = "regular") -> str:
    """
    Generate a query url for the Case Western Reserve University directory.
    
    Search Tips:
    1) Using the "*" wildcard symbol will help you further narrow your search (especially with common names). For example, if you are looking for Barbara Johnson and you are unsure of how to spell Barbara, you can type in "Barb* Johnson" or even "B* Johnson" in the search box and you will get better results than if you were to simply type in "Johnson".
    2) If you are unsure of how a name is spelled, you can use the Phonetic search method. Just type out the name the way it sounds and select the "Phonetic Search" button.
    3) The "*" wildcard symbol does not work with the phonetic search feature.
    4) This directory only performs searches based only on names, e-mail addresses, and phone numbers.
    5) This directory only returns exact matches for 2 character search criteria; a minimum of 3 characters is required for all other searches.

    ***
        Department and Location searches are only supported if logged in with a case email.

    Args:
        seach_text (str, optional): Query text. Defaults to "".
        surname (str, optional): Surname. Defaults to "".
        given_name (str, optional): Given Name. Defaults to "".
        category (str, optional): Search category, one of 'all', 'faculty', 'stagg', 'student', 'emeriti'. Defaults to "all".
        search_method (str, optional): Search method, one of 'regular', 'phonetic'. Defaults to "regular".

    Returns:
        str: Query url.
    """
    
    # validate arguments
    validate(seach_text, str)
    
    validate(surname, str)
    
    validate(given_name, str)
    
    categories: list[str] = ["all", "faculty", "staff", "student", "emeriti"]
    validate_option(category, categories)
    
    search_methods: list[str] = ["regular", "phonetic"]
    validate_option(search_method, search_methods)
    
    # url encode special characters
    seach_text = quote(seach_text)
    surname    = quote(surname)
    given_name = quote(given_name)
    
    return "https://webapps.case.edu/directory/lookup?" + \
            f"search_text={seach_text}&surname={surname}&givenname={given_name}" + \
            f"&department=&location=&category={category}" + \
            f"&search_method={search_method}"