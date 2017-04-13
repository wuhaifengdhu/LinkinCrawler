#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import re
import requests
import urlparse
import time
import random
from bs4 import BeautifulSoup
from urllib import urlencode
from dict_helper import DictHelper
from store_helper import StoreHelper


class CrawlHelper(object):
    @staticmethod
    def extract_job_id_list(web_source):
        job_list = list(set(re.findall('{"jobPosting":"urn:li:jobPosting:(\d*)"', web_source)))
        print("Get %i job ids from web source" % len(job_list))
        return job_list

    @staticmethod
    def get_total_items(web_source):
        numbers = re.findall('"total":(\d*),', web_source)
        return numbers[0] if len(numbers) > 0 else -1  # Default value for total number

    @staticmethod
    def get_company_name(web_source):
        names = re.findall('"jobPosting":{"companyName":"([^"]*)"', web_source)
        return names[0] if len(names) > 0 else "UNKNOWN"   # Default value for company name

    @staticmethod
    def get_post_information(web_source):
        # description = re.findall('property="og:description" content="([^>])>', web_source)
        # print description
        soup = BeautifulSoup(web_source, "lxml")
        meta = soup.find('meta', {"property": "og:description"})
        return meta['content']

    @staticmethod
    def get_travel_url(web_source, home_url="https://www.linkedin.com"):
        next_urls = re.findall('{"pageNumber":1,"pageUrl":"([^"]*)",', web_source)
        return urlparse.urljoin(home_url, next_urls[0]) if len(next_urls) > 0 else None

    @staticmethod
    def get_web_source(web_url):
        time.sleep(random.choice([3, 5, 3, 5, 15, 3, 3, 5, 3]))
        response = requests.get(web_url, auth=("kindlebookshare@163.com", "Linkedin0405"))
        print("Get web source from %s" % web_url)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        return soup.prettify().encode('utf-8')

    @staticmethod
    def build_job_search_url(job_type, location, base_url="https://www.linkedin.com/jobs/search"):
        url_parts = list(urlparse.urlparse(base_url))
        url_parts[4] = urlencode({'keywords': job_type, "location": location})
        return urlparse.urlunparse(url_parts)

    @staticmethod
    def get_page_url(travel_url, page_number, page_count):
        """
        url_parts = list(urlparse.urlparse("https://www.linkedin.com/jobs/search?keywords=Data+Scientist&locationId=
        STATES.us.oh&start=0&count=25&applyLogin=false&trk=jobs_jserp_pagination_1"))
        In [8]: print urlparse.parse_qs(url_parts[4])
        {'count': ['25'], 'trk': ['jobs_jserp_pagination_1'], 'start': ['0'], 'locationId': ['STATES.us.oh'], 
        'keywords': ['Data Scientist'], 'applyLogin': ['false']}"""
        print("Now working on page %i" % page_number)
        url_parts = list(urlparse.urlparse(travel_url))
        para_dict = dict(urlparse.parse_qsl(url_parts[4]))
        para_dict['count'] = page_count
        para_dict['trk'] = "jobs_jserp_pagination_%i" % page_number
        para_dict['start'] = (page_number - 1) * page_count
        url_parts[4] = urlencode(para_dict)
        return urlparse.urlunparse(url_parts)

    @staticmethod
    def crawl_post_information(ids_file, save_file):
        id_list = StoreHelper.load_data(ids_file)
        continue_not_found = 0
        post_list = {}
        total_count = len(id_list)
        current = 0
        for ids in id_list:
            id_url = urlparse.urljoin("https://www.linkedin.com/jobs/view/", ids)
            print("Working on url: %s" % id_url)
            current += 1
            print("progress report: %i in %i for %s" % (current, total_count, ids_file))

            web_source = CrawlHelper.get_web_source(id_url)
            company = CrawlHelper.get_company_name(web_source)
            post_content = CrawlHelper.get_post_information(web_source)

            if post_content is None:
                print ("No skills found for %s! Continue times %i" % (id_url, continue_not_found))
                continue_not_found += 1
                if continue_not_found > 3:
                    break
            else:
                continue_not_found = 0
                if company in post_list.keys():
                    post_list[company].append((company, id_url, post_content))
                else:
                    post_list[company] = [(company, id_url, post_content)]
        StoreHelper.store_data(post_list, save_file)
        return current >= total_count - 1


if __name__ == '__main__':
    raw_dict = DictHelper.load_dict_from_excel("../resource/linkedin_geography.xlsx")
    us_geography = DictHelper.generate_geography_dic(raw_dict, 'na.us', 1)
    print(us_geography)
    continue_failed = 0
    escape = 2
    for key, value in us_geography.items():
        if escape > 0:
            escape -= 1
            continue
        status = CrawlHelper.crawl_post_information("../data/%s.ids.dat" % key.encode('utf-8'), "../data/post/%s.dat" % key.encode('utf-8'))
        if status is False:
            continue_failed += 1
            if continue_failed >= 2:
                print("Program exit! Maybe robot identified!")
                break
        else:
            continue_failed = 0
