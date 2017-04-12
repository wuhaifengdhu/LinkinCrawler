#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import urlparse
from urllib import urlencode
from chrome_helper import ChromeHelper
from dict_helper import DictHelper
from job_posting import JobPosting
from text_helper import TextHelper


class LinkedInCrawler(object):
    def __init__(self, base_url, accounts, skills_dict):
        self.base_url = base_url
        self.accounts = accounts
        self.index = 0
        self.chrome_helper = ChromeHelper()
        self.skills_dict = DictHelper.load_dict_from_dic(skills_dict)

    def __crawl(self, job_posting, job_type, location, start):
        continue_not_found = 0
        job_search_url = self.__build_search_url(job_type, location, start)
        print(job_search_url)
        job_id_list = self.chrome_helper.extract_job_id(self.chrome_helper.get_web_source(job_search_url))
        if len(job_id_list) == 0:
            print ("no available job under this area!")
            return False
        job_url_list = ["https://www.linkedin.com/jobs/view/" + id_str for id_str in job_id_list]
        for job_url in job_url_list:
            web_source = self.chrome_helper.get_web_source(job_url)
            company, skills_content = TextHelper.extract_company_skills(web_source)
            if skills_content is None:
                print ("No skills found for %s!" % job_url)
                continue_not_found += 1

            else:
                job_posting.add_job_post(company, job_url, skills_content)
        return True

    def __build_search_url(self, job_name, location, start):
        url_parts = list(urlparse.urlparse(self.base_url))
        url_parts[4] = urlencode({'keywords': job_name, "location": location, 'start': start})
        return urlparse.urlunparse(url_parts)

    def craw_job(self, job_type, location, total_page, result_file):
        job_posting = JobPosting(job_type, location, self.skills_dict)
        for i in range(total_page):
            if i % 6 == 0:
                self.chrome_helper.close()
                self.chrome_helper = ChromeHelper()
                self.chrome_helper.authenticate("https://www.linkedin.com/uas/login-cap", self.accounts[i % 18])
            if not self.__crawl(job_posting, job_type, location, i*25):
                break
        print "Total post %i" % sum([len(job_posting[company]) for company in job_posting.job_post_skills.keys()])
        job_posting.save(result_file)


if __name__ == '__main__':
    accounts = [("some.good.ww@gmail.com", "Linkedin0405"), ("paypalshanghai@163.com", "Linkedin0405"),
                ("lofter.test.01@gmail.com", "Linkedin0405")]
    crawler = LinkedInCrawler("https://www.linkedin.com/jobs/search", accounts,
                              "../data/skills.dic")
    # raw_dict = DictHelper.load_dict_from_excel("../resource/linkedin_geography.xlsx")
    # us_geography = DictHelper.generate_geography_dic(raw_dict, "na.us", 0)
    # print us_geography
    # for key, value in us_geography.items():
    crawler.craw_job("Data Scientist", "Los Angeles, California".encode('utf-8'), 10000, "../data/log_california.dat")
