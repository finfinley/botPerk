# TODO: Implement selenium scrolling to engage with Twitter's endless scrolling feature to scrape more usernames

import requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import html


url = ("https://twitter.com/realDonaldTrump/status/1265827032707072000")
driver = webdriver.Chrome('INSERTDRIVERHERE')



driver.get(url)
time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, features='lxml')
usernameSoup = soup.find_all("div", class_="css-901oao css-bfa6kz r-111h2gw r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0")

list_of_usernames = [x.text for x in usernameSoup]
# If you want to print the text as a comma separated string
text = ', '.join(list_of_usernames)
print(text)
print(list_of_usernames)

#test
