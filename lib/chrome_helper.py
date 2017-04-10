#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class Chrome(object):
    def __init__(self):
        self.home_folder = os.getcwd()
        self.driver = self._get_driver()
        self.base_url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&locationId=sg%3A0"

    def _get_driver(self):
        driver_path = os.path.join(self.home_folder, 'chromedriver')
        os.environ["webdriver.chrome.driver"] = driver_path
        return webdriver.Chrome(driver_path)


    def _pre_login(self):
        login_url = "https://www.linkedin.com/uas/login-cap"
        self.driver.get(login_url)
        self.driver.find_element_by_id('session_key-login').send_keys("wulinkedinmem@gmail.com")
        self.driver.find_element_by_id('session_password-login').send_keys("Linkedin0405")
        self.driver.find_element_by_id("btn-primary").click()
        time.sleep(2)

    def _generate_job_detail_url(self):
        url_list = []
        pass

    @staticmethod
    def _find_job_id(self, web_source):
        job_id = list(set(re.findall('SearchJobJserp":{"jobPosting":"urn:li:fs_normalized_jobPosting:(\d*)"',
                                     web_source)))
        return job_id

    def open_url(self, url):
        self.driver.get(url)
        delay = 3  # seconds
        try:
            WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.ID, 'clientPageInstance')))
            print "Page is ready!"
            html_doc = self.driver.page_source.encode("utf-8")
            self._find_job_id(html_doc)
        except TimeoutException:
            print "Loading took too much time!"

    def base_login(self):
        self.driver.find_element_by_id('jobs-tab-icon').click()
        # login_url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&locationId=sg%3A0"
        # self.driver.get(login_url)
        # self.driver.find_element_by_class_name("ember-text-field ember-view").send_keys("Data Scientist")
        # self.driver.find_element_by_id("submit-button button-primary-large").click()


if __name__ == "__main__":
    chrome = Chrome()
    chrome.pre_login()
    chrome.open_url("https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&locationId=sg%3A0&start=25")
