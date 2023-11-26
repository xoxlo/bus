import requests
import pandas as pd
import pprint
from bs4 import BeautifulSoup

url = requests.get("https://its.sc.go.kr:8443/internet/bisExploreSearch.view?lang=ko")

url