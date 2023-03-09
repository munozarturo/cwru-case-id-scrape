from itertools import product
import re
from urllib.request import urlopen
from cwru.cwru import generate_query_url
from log import Logger
from scraper import SequentialScraper

logger: Logger = Logger(print_=True, file_=True, file_path="auth_request_log.rlog")
