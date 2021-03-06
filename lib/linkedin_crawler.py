#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import urlparse
from urllib import urlencode
from chrome_helper import ChromeHelper
from dict_helper import DictHelper
from job_posting import JobPosting
from text_helper import TextHelper
from store_helper import StoreHelper


class LinkedInCrawler(object):
    def __init__(self, base_url, accounts, skills_dict):
        self.base_url = base_url
        self.accounts = accounts
        self.index = 0
        self.total_review = 0
        self.chrome_helper = ChromeHelper()
        self.chrome_helper.authenticate("https://www.linkedin.com/uas/login-cap", accounts[self.index])
        self.skills_dict = DictHelper.load_dict_from_dic(skills_dict)

    def login(self):
        print("Switch account, please check old account %s" % self.accounts[self.index % len(self.accounts)])
        self.total_review = 0
        self.index = (self.index + 1) % len(self.accounts)
        self.chrome_helper.close()
        self.chrome_helper = ChromeHelper()
        self.chrome_helper.authenticate("https://www.linkedin.com/uas/login-cap", self.accounts[self.index])

    def __crawl(self, job_posting, job_type, location, start):
        continue_not_found = 0
        job_search_url = self.__build_search_url(job_type, location, start)
        print(job_search_url)
        job_id_list = self.chrome_helper.extract_job_id(self.chrome_helper.get_web_source(job_search_url))
        if len(job_id_list) == 0:
            print ("no available job under this area!")
            return False
        job_posting.extend(job_id_list)
        return True

    def __build_search_url(self, job_name, location, start):
        url_parts = list(urlparse.urlparse(self.base_url))
        url_parts[4] = urlencode({'keywords': job_name, "location": location, 'start': start})
        return urlparse.urlunparse(url_parts)

    def craw_job(self, job_type, location, total_page, result_file):
        # job_posting = JobPosting(job_type, location, self.skills_dict)
        job_id_list = []
        for i in range(total_page):
            # if i % 60 == 0:
            #     self.chrome_helper.close()
            #     self.chrome_helper = ChromeHelper()
            #     self.chrome_helper.authenticate("https://www.linkedin.com/uas/login-cap", self.accounts[i/60%2])
            if not self.__crawl(job_id_list, job_type, location, i*25):
                break
        # print "Total post %i" % sum([len(job_posting.job_post_skills[company]) for company in job_posting.job_post_skills.keys()])
        StoreHelper.store_data(job_id_list, result_file)

    def get_post_information(self, ids_file, save_file):
        id_list = StoreHelper.load_data(ids_file)
        continue_not_found = 0
        post_list = {}
        total_count = len(id_list)
        current = 0
        for ids in id_list:
            id_url = urlparse.urljoin("https://www.linkedin.com/jobs/view/", ids)
            print("Working on url: %s" % id_url)
            current += 1
            self.total_review += 1
            print("progress report: %i in %i for %s" % (current, total_count, ids_file))
            print("current account %s already reviewed %i pages!" % (self.accounts[self.index], self.total_review))
            if self.total_review > 149:
                self.login()  # Linkedin identify robot every 200 web page

            web_source = self.chrome_helper.get_web_source(id_url)
            company, skills_content = TextHelper.extract_company_skills(web_source)
            if skills_content is None:
                print ("No skills found for %s! Continue times %i" % (id_url, continue_not_found))
                continue_not_found += 1
                if continue_not_found > 3:
                    break
            else:
                continue_not_found = 0
                if company in post_list.keys():
                    post_list[company].append((company, id_url, skills_content))
                else:
                    post_list[company] = [(company, id_url, skills_content)]
        StoreHelper.store_data(post_list, save_file)
        return current >= total_count - 1

    def test_one_page(self, id_url):
        web_source = self.chrome_helper.get_web_source(id_url)
        company, skills_content = TextHelper.extract_company_skills(web_source)
        post_list = {}
        if skills_content is None:
            print ("No skills found for %s!" % id_url)
        else:
            if company in post_list.keys():
                post_list[company].append((company, id_url, skills_content))
            else:
                post_list[company] = [(company, id_url, skills_content)]


if __name__ == '__main__':
    wu_dict = {u'na.us.mo': u'Missouri', u'na.us.il': u'Illinois', u'na.us.ma': u'Massachusetts',
               u'na.us.in': u'Indiana', u'na.us.md': u'Maryland', u'na.us.me': u'Maine', u'na.us.wv': u'West Virginia',
               u'na.us.ut': u'Utah', u'na.us.az': u'Arizona', u'na.us.de': u'Delaware', u'na.us.ok': u'Oklahoma',
               u'na.us.co': u'Colorado', u'na.us.fl': u'Florida', u'na.us.wa': u'Washington',
               u'na.us.dc': u'District Of Columbia', u'na.us.wi': u'Wisconsin'}

    hu_dict = {u'na.us.ky': u'Kentucky', u'na.us.ct': u'Connecticut', u'na.us.ny': u'New York',
               u'na.us.ri': u'Rhode Island', u'na.us.pa': u'Pennsylvania', u'na.us.nc': u'North Carolina',
               u'na.us.ne': u'Nebraska', u'na.us.nd': u'North Dakota', u'na.us.nh': u'New Hampshire',
               u'na.us.la': u'Louisiana', u'na.us.nj': u'New Jersey', u'na.us.nm': u'New Mexico',
               u'na.us.vt': u'Vermont', u'na.us.hi': u'Hawaii'}

    liu_dict = {u'na.us.ga': u'Georgia', u'na.us.tx': u'Texas', u'na.us.ar': u'Arkansas', u'na.us.wy': u'Wyoming',
                u'na.us.al': u'Alabama', u'na.us.va': u'Virginia', u'na.us.ca': u'California', u'na.us.ak': u'Alaska',
                u'na.us.ks': u'Kansas', u'na.us.tn': u'Tennessee', u'na.us.sc': u'South Carolina',
                u'na.us.sd': u'South Dakota', u'na.us.or': u'Oregon', u'na.us.ms': u'Mississippi',
                u'na.us.mt': u'Montana', u'na.us.id': u'Idaho', u'na.us.mi': u'Michigan', u'na.us.ia': u'Iowa',
                u'na.us.mn': u'Minnesota'}

    # step 1, change the dict name to your part of work
    us_geography = wu_dict

    # step 2, Add your created account to the following links
    accounts = [("testlink0a@gmail.com", "share12345"), ("testlink0b@gmail.com", "share12345")]
    crawler = LinkedInCrawler("https://www.linkedin.com/jobs/search", accounts,
                              "../data/skills.dic")
    # raw_dict = DictHelper.load_dict_from_excel("../resource/linkedin_geography.xlsx")
    # us_geography = DictHelper.generate_geography_dic(raw_dict, 'na.us', 1)
    # print(us_geography)
    continue_failed = 0
    for key, value in us_geography.items():
        status = crawler.get_post_information("../data/%s.ids.dat" % key.encode('utf-8'), "../data/post/%s.dat" %
                                     key.encode('utf-8'))
        if status is False:
            continue_failed += 1
            if continue_failed >= 2:
                print("Program exit! Maybe robot identified!")
                break
        else:
            continue_failed = 0
