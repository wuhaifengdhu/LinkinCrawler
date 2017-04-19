#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import requests
import urlparse
import time
# import random
from bs4 import BeautifulSoup
from urllib import urlencode
# from dict_helper import DictHelper
from store_helper import StoreHelper
# from fake_useragent import UserAgent
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

# user_agent = UserAgent()
# failed_agent = {}
# current_agent = None
# change_agent = True
# req_proxy = RequestProxy(sustain=True)


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
        try:
            return meta['content']
        except Exception:
            return None

    @staticmethod
    def get_travel_url(web_source, home_url="https://www.linkedin.com"):
        next_urls = re.findall('{"pageNumber":1,"pageUrl":"([^"]*)",', web_source)
        return urlparse.urljoin(home_url, next_urls[0]) if len(next_urls) > 0 else None

    @staticmethod
    def get_web_source(web_url):
        # time.sleep(random.choice([3, 5, 3, 5, 15, 3, 3, 5, 3]))
        # global change_agent
        # if change_agent:
        #     while True:
        #         global current_agent
        #         global failed_agent
        #         current_agent = user_agent.random
        #         if current_agent not in failed_agent or failed_agent[current_agent] < 3:
        #             print ("use agent: %s" % current_agent)
        #             break
        #         else:
        #             print ("agent can not use: %s" % current_agent)
        #     change_agent = False
        #
        # global req_proxy
        # response = req_proxy.generate_proxied_request(web_url, headers={'User-Agent': current_agent})
        # response = req_proxy.generate_proxied_request(web_url)
        # response = requests.get(web_url, proxies={'http': 'http://138.68.132.206:3128'}, headers={'User-Agent': current_agent})
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        response = requests.get(web_url)
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
        id_list = StoreHelper.load_data(ids_file, [])
        total_count = len(id_list)
        current = 0
        continue_not_found = 0

        # Recover if already has post
        post_list = CrawlHelper.recover_from_file(save_file)
        if len(post_list) > 0:
            current = sum([len(_value) for _value in post_list.values()])
            id_list = id_list[current:]
            print ("recover crawl from post job %i" % current)
        last_save_account = current
        failed_id_list = []

        total_crawled = 0
        retry = 3
        while retry > 0:
            for ids in id_list:
                id_url = urlparse.urljoin("https://www.linkedin.com/jobs/view/", ids)
                print("Working on url: %s" % id_url)
                current += 1
                print("progress report: %i in %i for %s" % (current, total_count, ids_file))
                # if current % 9 == 0:
                #     time.sleep(90)

                # Save checkpoint if get about 10 records
                if current > last_save_account + 10:
                    CrawlHelper.save_checkpoint(post_list, save_file)
                    last_save_account = current

                web_source = CrawlHelper.get_web_source(id_url)
                company = CrawlHelper.get_company_name(web_source)
                post_content = CrawlHelper.get_post_information(web_source)

                if post_content is None:
                    failed_id_list.append(ids)
                    print ("No skills found for %s! Continue times %i" % (id_url, continue_not_found))
                    continue_not_found += 1
                    if continue_not_found >= 1:
                        retry = 0
                        break
                    # global current_agent
                    # global failed_agent
                    # global change_agent
                    # global req_proxy
                    # req_proxy.randomize_proxy()
                    # change_agent = True
                    # if current_agent in failed_agent:
                    #     failed_agent[current_agent] += 1
                    # else:
                    #     failed_agent[current_agent] = 1
                    # print ("agent %s failed %i times" % (current_agent, failed_agent[current_agent]))
                else:
                    total_crawled += 1
                    continue_not_found = 0
                    if company in post_list.keys():
                        post_list[company].append((company, id_url, post_content))
                    else:
                        post_list[company] = [(company, id_url, post_content)]

            # retry for failed id list
            if len(failed_id_list) == 0:
                break
            print ("retry times %i for failed %i job posts" % (4 - retry, len(failed_id_list)))
            id_list = failed_id_list
            failed_id_list = []
            retry -= 1
        StoreHelper.store_data(post_list, save_file)
        if len(failed_id_list) > 0:
            StoreHelper.store_data(failed_id_list, "%s.failed" % save_file)

        if current >= total_count -1:
            return -1  # means succeed
        return total_crawled

    @staticmethod
    def save_checkpoint(job_post, save_file):
        # Save current loaded data into file
        print ("Save crawled data to db!")
        StoreHelper.store_data(job_post, save_file)

    @staticmethod
    def recover_from_file(file_name):
        return StoreHelper.load_data(file_name, {})

    @staticmethod
    def run_crawl(us_geography):
        for key, value in us_geography.items():
            crawled_count = CrawlHelper.crawl_post_information("../data/%s.ids.dat" % key.encode('utf-8'),
                                                        "../data/post/%s.dat" % key.encode('utf-8'))
            if crawled_count != -1:
                return crawled_count
        return -1   # Finished all crawl job

if __name__ == '__main__':
    wu_dict = {u'na.us.mo': u'Missouri', u'na.us.il': u'Illinois', u'na.us.ma': u'Massachusetts',
               u'na.us.in': u'Indiana', u'na.us.md': u'Maryland', u'na.us.me': u'Maine', u'na.us.wv': u'West Virginia',
               u'na.us.ut': u'Utah', u'na.us.az': u'Arizona', u'na.us.de': u'Delaware', u'na.us.ok': u'Oklahoma',
               u'na.us.co': u'Colorado', u'na.us.fl': u'Florida', u'na.us.wa': u'Washington',
               u'na.us.dc': u'District Of Columbia', u'na.us.wi': u'Wisconsin'}

    # raw_dict = DictHelper.load_dict_from_excel("../resource/linkedin_geography.xlsx")
    # us_geography = DictHelper.generate_geography_dic(raw_dict, 'na.us', 1)
    # print(us_geography)
    detector_delay = 60
    min_delay = 0
    while True:
        last_crawled = CrawlHelper.run_crawl(wu_dict)
        if last_crawled == -1: # all job finished
            break
        elif last_crawled <= 5:
            min_delay = detector_delay
            print ("Min delay set to %i due to 0 records crawled!" % min_delay)
            detector_delay *= 2
        else:
            if last_crawled > 15:
                detector_delay -= 1 if detector_delay > min_delay else detector_delay
            print ("Delay %i crawl %i record" % (detector_delay, last_crawled))
        print ("Sleep for time %i seconds" % detector_delay)
        time.sleep(detector_delay)
    print ("All data crawled for this dict!")



