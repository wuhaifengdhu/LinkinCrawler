#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver


class Chrome(object):
    def __init__(self):
        self.home_folder = os.getcwd()
        self.driver = self._get_driver()
        self.base_url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&locationId=sg%3A0"

    def _get_driver(self):
        driver_path = os.path.join(self.home_folder, 'chromedriver')
        os.environ["webdriver.chrome.driver"] = driver_path
        return webdriver.Chrome(driver_path)

    def _store_html(self, web_source, file_name='web.html'):
        file_output = open(file_name, "w")
        file_output.write(web_source)
        file_output.close()

    def pre_login(self):
        login_url = "https://www.linkedin.com/uas/login-cap"
        self.driver.get(login_url)
        self.driver.find_element_by_id('session_key-login').send_keys("wulinkedinmem@gmail.com")
        self.driver.find_element_by_id('session_password-login').send_keys("Linkedin0405")
        self.driver.find_element_by_id("btn-primary").click()
        time.sleep(2)

    def open_url(self, url):
        self.driver.get(url)
        time.sleep(3)
        html_doc = self.driver.page_source.encode("utf-8")
        self._store_html(html_doc)

    def base_login(self):
        self.driver.find_element_by_id('jobs-tab-icon').click()
        # login_url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&locationId=sg%3A0"
        # self.driver.get(login_url)
        # self.driver.find_element_by_class_name("ember-text-field ember-view").send_keys("Data Scientist")
        # self.driver.find_element_by_id("submit-button button-primary-large").click()


if __name__ == "__main__":
    chrome = Chrome()
    chrome.pre_login()
    chrome.open_url("https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&locationId=sg%3A0&start=0")
