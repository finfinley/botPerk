from lxml import html
# This file collects the Soup from the page of a tweet and writes to file
import requests
from bs4 import BeautifulSoup

url = 'https://twitter.com/realDonaldTrump/status/1265774767493148672/likes'
html_text = requests.get(url).text

soup = BeautifulSoup(html_text, 'html.parser')
html = soup.prettify("utf-8")
with open("soup2.txt", "wb") as file:
    file.write(html)

