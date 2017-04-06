#!/usr/bin/python
# -*- coding: utf-8 -*-
import urlparse
from urllib import urlencode
import requests


class LinkedInCrawler(object):
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.user = username
        self.password = password

    def crawl(self, job_name, location_id="sg", start=0):
        job_search_url = self._build_search_url(job_name, location_id, start)
        print job_search_url
        job_urls = self._get_job_urls(job_search_url)
        output = open("web.html", "w")
        output.write(job_urls)
        output.close()

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
