#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from lib.store_helper import StoreHelper


class JobPosting(object):
    def __init__(self, job_type, location_id, skills_dic):
        # TODO move skills dic out of instance
        self.job_type = job_type
        self.location_id = location_id
        self.skills_dic = skills_dic
        self.job_post_skills = {}

    def add_job_post(self, company, job_url, post_content):
        if company in self.job_post_skills.keys():
            self.job_post_skills[company].append((job_url, self.__extract_skills_from_post(post_content), post_content))
        else:
            self.job_post_skills[company] = [(job_url, self.__extract_skills_from_post(post_content), post_content)]

    def __extract_skills_from_post(self, post_content):
        return [key for key, value in self.skills_dic.items() if key.encode('utf-8') in post_content]

    def save(self, dict_file):
        StoreHelper.store_data(self, dict_file)

    @staticmethod
    def load_from_file(file_name):
        return StoreHelper.load_data("../data/%s" % file_name)





