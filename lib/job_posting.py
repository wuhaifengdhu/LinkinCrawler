#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.store_helper import StoreHelper


class JobPost(object):
    def __init__(self, job_type, location_id, skills_dic):
        self.job_type = job_type
        self.location_id = location_id
        self.skills_dic = skills_dic
        self.dic_file = "%s_%s.dic" % (job_type, location_id)
        self.job_post_skills = {}

    def add_job_post(self, job_url, post_content):
        self.job_post_skills[job_url] = self.__extract_skills_from_post(post_content)

    def __extract_skills_from_post(self, post_content):
        return [key for key, value in self.skills_dic.items() if key in post_content]

    def save(self):
        StoreHelper.store_data(self, self.dic_file)





