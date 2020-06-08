import requests, time, botometer, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import html
from twython import Twython

#!/usr/bin/python
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

url = ("https://twitter.com/realDonaldTrump/status/1268888880264155136")
driver = webdriver.Chrome(executable_path='C:/Users/alexf/OneDrive/Documents/Python Projects/chromedriver.exe')

# Bot-o-meter Info
rapidapi_key = "d8f34cfb8bmshcc45a662c421371p1ab8ddjsn33c9d9b68e66"
twitter_app_auth = {
    'consumer_key': '3YI6rE8z8naJtUZmFn3Fr1VZF',
    'consumer_secret': 'kspiJwiRaQm1ou3RnYMbXS3riTCYNm6DCEbrsqdELgCyfvKzry',
    'access_token': '1265347900449730561-BmJNnFLhyLY16su199eiw217LDU35Q',
    'access_token_secret': 'zavatHUoEbf96OXD8RgZoat416MGSFe0529vTZYgh9NZt',
}
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

#Twitter API Info
apiKey = '3YI6rE8z8naJtUZmFn3Fr1VZF'
apiSecret = 'kspiJwiRaQm1ou3RnYMbXS3riTCYNm6DCEbrsqdELgCyfvKzry'

accessToken = '1265347900449730561-BmJNnFLhyLY16su199eiw217LDU35Q'
accessTokenSecret = 'zavatHUoEbf96OXD8RgZoat416MGSFe0529vTZYgh9NZt'

api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)



def scroll_to_bottom(driver,scrolltime):
        print('Beginning hunt...')
        # Empty list for all the usernames scraped
        FULL_LIST = []
        bots = []

        old_position = 0
        new_position = None

        while new_position != old_position:
                # Get old scroll position
                old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"))

                # Scrapes usernames from current scrolls
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                usernameSoup = soup.find_all(
                "div", class_="css-901oao")

                #css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0
                list_of_usernames = [x.text for x in usernameSoup]
                matching = [s for s in list_of_usernames if '@' in s]
                justUsers = [x for x in matching if " " not in x]
                print("SCROLLING LOOT: ", justUsers)
                print("LEN:", len(justUsers))
                
                # Extends master list of usernames
                FULL_LIST.extend(justUsers)
                # Deletes any duplicates in FULL_LIST
                FULL_LIST = list(dict.fromkeys(FULL_LIST))
    
                # Sleep and Scroll
                time.sleep(scrolltime)

                driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
                # Get new position
                new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"))
                print("FULL LIST: ", len(FULL_LIST))
        # Plugs usernames into bom        
        for screen_name, results in bom.check_accounts_in(FULL_LIST):
            print('Busy hunting bots...')
            try:
                if results['display_scores']['universal'] > 3.0 :
                        bots.append(results['user']['screen_name'])
                        print('Bot found.')
            except KeyError:
                print('Error digging for account information.')
                pass

        print("Total Bots: ", len(bots))
        print("Bot accounts: ", bots)
        print("Out of {}",format(len(FULL_LIST)))

        tweetStr = url + " Total bots found: " + str(len(bots)) + " out of " + str(len(FULL_LIST))

        api.update_status(status = tweetStr)
        print("Tweet sent.")
        

driver.get(url)
scroll_to_bottom(driver, 10)
driver.get(url)
scroll_to_bottom(driver, 20)
driver.get(url)
scroll_to_bottom(driver, 30)
driver.quit()



