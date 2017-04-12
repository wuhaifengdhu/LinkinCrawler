#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.linkedin_crawler import LinkedInCrawler
from lib.dict_helper import DictHelper
from lib.store_helper import StoreHelper
from lib import job_posting
import sys


class Main(object):
    @staticmethod
    def run():
        crawler = LinkedInCrawler("https://www.linkedin.com/jobs/search", "wulinkedinmem@gmail.com", "Linkedin0405",
                                  "../data/skills.dic")
        raw_dict = DictHelper.load_dict_from_excel("./resource/linkedin_geography.xlsx")
        us_geography = DictHelper.generate_geography_dic(raw_dict, "na.us", 1)
        print us_geography
        # crawler.craw_job("Data Scientist", "Charleston, South Carolina Area", 1, "../data/carolina.dat")

    @staticmethod
    def view_data(data_list):
        if len(data_list) == 0:
            print "No data file in data_list"
            return
        merged_result = StoreHelper.load_data("./data/%s" % data_list[0])
        Main.merge_result(merged_result, [StoreHelper.load_data("./data/%s" % data_file) for data_file in data_list[1:]])
        output = open("./data/company_statistics.txt", "wb")
        total_post = 0
        for company in merged_result.job_post_skills.keys():
            cnt = len(merged_result.job_post_skills[company])
            total_post += cnt
            output.write(str(cnt) + " " + company.encode('utf-8'))
        print "Total job for us: %i" % total_post

    @staticmethod
    def merge_result(job_posting_merged, job_posting_list):
        for job_post in job_posting_list:
            for company in job_post.job_post_skills.keys():
                if company in job_posting_merged.job_post_skills.keys():
                    job_posting_merged.job_post_skills[company].append(job_post.job_post_skills[company])
                else:
                    job_posting_merged.job_post_skills[company] = job_post.job_post_skills[company]


if __name__ == '__main__':
    sys.modules['job_posting'] = job_posting
    data_list = ["na.us.ak.dat", "na.us.al.dat", "na.us.ar.dat", "na.us.az.dat", "na.us.ca.dat", "na.us.co.dat",
                 "na.us.ct.dat", "na.us.dc.dat", "na.us.de.dat", "na.us.fl.dat", "na.us.ga.dat", "na.us.hi.dat",
                 "na.us.ia.dat", "na.us.id.dat", "na.us.il.dat", "na.us.in.dat", "na.us.ks.dat", "na.us.ky.dat",
                 "na.us.la.dat", "na.us.ma.dat", "na.us.md.dat", "na.us.me.dat", "na.us.mi.dat", "na.us.mn.dat",
                 "na.us.mo.dat", "na.us.ms.dat", "na.us.mt.dat", "na.us.nc.dat", "na.us.nd.dat", "na.us.ne.dat",
                 "na.us.nh.dat", "na.us.nj.dat", "na.us.nm.dat", "na.us.nv.dat", "na.us.ny.dat", "na.us.oh.dat",
                 "na.us.ok.dat", "na.us.or.dat", "na.us.pa.dat", "na.us.ri.dat", "na.us.sc.dat", "na.us.sd.dat",
                 "na.us.tn.dat", "na.us.tx.dat", "na.us.ut.dat", "na.us.va.dat", "na.us.vt.dat", "na.us.wa.dat",
                 "na.us.wi.dat", "na.us.wv.dat", "na.us.wy.dat"]
    Main.view_data(data_list)
