#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from bs4 import BeautifulSoup
import os
import time
import re
from text_helper import TextHelper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By


class ChromeHelper(object):
    def __init__(self):
        self.__home_folder = os.getcwd()
        self.__driver = self.__get_driver()
        self.__driver.maximize_window()
        self.__has_authentication = False

    def __get_driver(self):
        driver_path = os.path.join(self.__home_folder, 'chromedriver')
        os.environ["webdriver.chrome.driver"] = driver_path
        return webdriver.Chrome(driver_path)

    def authenticate(self, author_url, user, password):
        self.__driver.get(author_url)
        self.__driver.find_element_by_id('session_key-login').send_keys(user)
        self.__driver.find_element_by_id('session_password-login').send_keys(password)
        self.__driver.find_element_by_id("btn-primary").click()
        time.sleep(3)
        self.__has_authentication = True
        # self.__driver.close()

    @staticmethod
    def extract_job_id(web_source):
        job_id = list(set(re.findall('SearchJobJserp":{"jobPosting":"urn:li:fs_normalized_jobPosting:(\d*)"',
                                     web_source)))
        return job_id

    def get_web_source(self, url):
        if not self.__has_authentication:
            print("Error! Not have authenticate yet!")
            return None
        self.__driver.get(url)
        delay = 8  # seconds
        try:
            WebDriverWait(self.__driver, delay).until(
                EC.presence_of_element_located((By.ID, 'clientPageInstance')))
            print("Page is ready!")
            return self.__driver.page_source.encode("utf-8")
        except TimeoutException:
            print("Loading took too much time!")
            return None


if __name__ == "__main__":
    chrome = ChromeHelper()
    chrome.authenticate("https://www.linkedin.com/uas/login-cap", "wulinkedinmem@gmail.com", "Linkedin0405")
    web_content = chrome.get_web_source("https://www.linkedin.com/jobs/view/309059479")
    soup = BeautifulSoup(web_content.decode('utf-8'), 'html.parser')
    TextHelper.store_html(soup.prettify().encode('utf-8'), "309059479.html")
