#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import requests
import urlparse
import time
from bs4 import BeautifulSoup
from urllib import urlencode
from dict_helper import DictHelper
from store_helper import StoreHelper


class CrawlHelper(object):
    @staticmethod
    def extract_job_id_list(web_source):
        job_list = list(set(re.findall('{"jobPosting":"urn:li:jobPosting:(\d*)"', web_source)))
        print "Get %i job ids from web source" % len(job_list)
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
        if meta is None or 'content' not in meta:
            return "No description found!"
        return meta['content']

    @staticmethod
    def get_travel_url(web_source, home_url="https://www.linkedin.com"):
        next_urls = re.findall('{"pageNumber":1,"pageUrl":"([^"]*)",', web_source)
        return urlparse.urljoin(home_url, next_urls[0]) if len(next_urls) > 0 else None

    @staticmethod
    def get_web_source(web_url):
        time.sleep(3)
        response = requests.get(web_url, auth=("kindlebookshare@163.com", "Linkedin0405"))
        print "Get web source from %s" % web_url
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
        print "Now working on page %i" % page_number
        url_parts = list(urlparse.urlparse(travel_url))
        para_dict = dict(urlparse.parse_qsl(url_parts[4]))
        para_dict['count'] = page_count
        para_dict['trk'] = "jobs_jserp_pagination_%i" % page_number
        para_dict['start'] = (page_number - 1) * page_count
        url_parts[4] = urlencode(para_dict)
        return urlparse.urlunparse(url_parts)


if __name__ == '__main__':
    # step 1, load location dict from excel
    raw_dict = DictHelper.load_dict_from_excel("../resource/linkedin_geography.xlsx")
    us_geography = DictHelper.generate_geography_dic(raw_dict, "na.us", 1)
    _position = "Data Scientist"
    _job_view_url = "https://www.linkedin.com/jobs/view/"
    _page_count = 25

    # step 2, get all job id list
    for key, value in us_geography.items():
        _search_url = CrawlHelper.build_job_search_url(_position, unicode(value).encode('utf-8'))
        _web_source = CrawlHelper.get_web_source(_search_url)
        _job_id_list = CrawlHelper.extract_job_id_list(_web_source)
        _total_items = int(CrawlHelper.get_total_items(_web_source))

        if _total_items != -1:
            print "total has items %i" % _total_items
            _travel_url = CrawlHelper.get_travel_url(_web_source)
            print "travel url is %s" % _travel_url
            if _travel_url is None:
                print "No further page found for %s" % _search_url
            else:
                _total_page = _total_items / _page_count
                for i in range(_total_page):
                    _next_url = CrawlHelper.get_page_url(_travel_url, i + 2, _page_count)
                    _job_id_list.extend(CrawlHelper.extract_job_id_list(CrawlHelper.get_web_source(_next_url)))

        StoreHelper.store_data(_job_id_list, "%s.job_ids.dic" % unicode(key).encode('utf-8'))
        break







