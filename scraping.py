#データの取得  (requests)
from distutils.log import debug
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup  # データの抽出  (Beautiful Soup)
import re

class Scraping:
    # slackにURLが載せられた時に起動
    def __init__(self,url):
        response = requests.get(url)
        ua = UserAgent()
        header = {'user-agent': ua.chrome}
        response = requests.get(url, headers=header, timeout=3)  # ,params=param)
        self.soup = BeautifulSoup(
            response.content, "html.parser").get_text(strip=True)

    def return_text(self):
        # print(self.soup)
        # print(type(self.soup))
        return str(self.soup)
