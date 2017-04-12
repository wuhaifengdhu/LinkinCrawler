#!/usr/bin/python
# -*- coding: utf-8 -*-
import urlparse
from urllib import urlencode
import requests
from chrome_helper import ChromeHelper
from text_helper import TextHelper


class LinkedInCrawler(object):
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.user = username
        self.password = password
        self.chrome_helper = ChromeHelper()

    def crawl(self, job_name, location_id="sg", start=0):
        self.chrome_helper.authenticate("https://www.linkedin.com/uas/login-cap", self.user, self.password)
        job_search_url = self._build_search_url(job_name, location_id, start)
        print(job_search_url)
        job_id_list = self.chrome_helper.extract_job_id(self.chrome_helper.get_web_source(job_search_url))
        job_url_list = ["https://www.linkedin.com/jobs/view/" + id_str for id_str in job_id_list]
        result = []
        for job_url in job_url_list:
            print(job_url)
            result.append("=="*10)
            result.append(job_url)
            web_source = self.chrome_helper.get_web_source(job_url)
            skills = self.chrome_helper.extract_skills(web_source)
            if skills is None:
                result.append("No skills found!")
            else:
                result.append(skills)
        TextHelper.store_html('\n'.join(result), file_name="result.txt")

    def _build_search_url(self, job_name, location_id, start):
        url_parts = list(urlparse.urlparse(self.base_url))
        url_parts[4] = urlencode({'keywords': job_name, "locationId": location_id, 'start': start})
        return urlparse.urlunparse(url_parts)

    def _get_job_urls(self, job_search_url):
        response = requests.get(job_search_url, auth=(self.user, self.password))
        return response.content


if __name__ == '__main__':
    crawler = LinkedInCrawler("https://www.linkedin.com/jobs/search", "wulinkedinmem@gmail.com", "Linkedin0405")
    crawler.crawl("Data Scientist")
