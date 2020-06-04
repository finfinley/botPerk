import time, botometer
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import html
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

url = ("https://twitter.com/realDonaldTrump/status/1265827032707072000")
driver = webdriver.Chrome(
    'Chomedriver/path/here')

# Twitter API / Bot-o-meter Info
rapidapi_key = "d8f34cfb8bmshcc45a662c421371p1ab8ddjsn33c9d9b68e66"
twitter_app_auth = {
    'consumer_key': 'CONSUMERKEYHERE',
    'consumer_secret': 'CONSUMERSECRETHERE',
    'access_token': 'ACCESSTOKENHERE',
    'access_token_secret': 'ACCESSTOKENSECRETHERE',
}
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)


def scroll_to_bottom(driver):
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
                soup = BeautifulSoup(html, features='lxml')
                usernameSoup = soup.find_all(
                "div", class_="css-901oao css-bfa6kz r-111h2gw r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0")
                list_of_usernames = [x.text for x in usernameSoup]
                # Prints current loot of usernames
                text = ', '.join(list_of_usernames)
                print("SCROLLING LOOT:", text)
                print("LEN:", len(list_of_usernames))
                # Extends master list of usernames
                FULL_LIST.extend(list_of_usernames)
                # Deletes any duplicates in FULL_LIST
                FULL_LIST = list(dict.fromkeys(FULL_LIST))
                # Sleep and Scroll
                time.sleep(5)
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
                if results['display_scores']['user'] > 3.0:
                        bots.append(results['user']['screen_name'])
                        print('Bot found.')
            except KeyError:
                pass            

        print("Total Bots: ", len(bots))
        print("Bot accounts: ", bots)
        #print("Results: ", results['display_scores']['user'])



driver.get(url)
scroll_to_bottom(driver)
#driver.quit()



