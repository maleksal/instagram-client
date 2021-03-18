import pathlib
import pickle
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from client.profile import Profile
from client.utils.helpers import handle_cookies


class InstaClient:
    """
	InstaClient - scrapes data using GraphQL endpoints && selenium
	Attributes:
		username:		Instagram username
		password:		Instagram password
		cookie_file:	Optional file name 'where to save/retrieve cookies'

    """

    __BASE_URL = "https://www.instagram.com"
    __DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}

    def __init__(self, username, password, cookie_file='cookies.pkl'):
        """Client Class constructor."""

        self.__username = username
        self.__password = password
        self.__cookie_file = cookie_file
        self.__session = requests.session()
        self.authenticate()

    def authenticate(self):
        """
        Handles authentication with instagram, either by cookies or password.
	"""
        if cookies_data := handle_cookies(self.__cookie_file):
            for cookie in cookies_data:
                self.__session.cookies.set(cookie['name'], cookie['value'])
        else:
            # Do not use web interface
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("enable-automation")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
            driver_path: str = str(pathlib.Path(__file__).parent)
            driver = webdriver.Firefox(options=options, executable_path=f'{driver_path}/geckodriver')

            driver.get(self.__BASE_URL + '/accounts/login/?next=login&source=desktop_nav')
            driver.implicitly_wait(5)
            driver.find_element_by_name('username').send_keys(self.__username)
            driver.find_element_by_name('password').send_keys(self.__password + Keys.ENTER)
            time.sleep(6)
            # save cookies from browser
            if cookie := driver.get_cookies():
                pickle.dump(cookie, open('cookies.pkl', 'wb'))
                driver.close()
                return self.authenticate()
            raise Exception("Unable to load cookies!.")

    def get_username_profile(self, username):
        """Returns an instagram profile object refrenced by username."""
        endpoint = f'/web/search/topsearch/?context=blended&query={username}&rank_token=0.3953592318270893&count=1'
        response = self.__session.get(self.__BASE_URL + endpoint, headers=self.__DEFAULT_HEADERS)
        jsondata = response.json()
        return Profile(self.__session, username, jsondata["users"][0]["user"]["pk"])
