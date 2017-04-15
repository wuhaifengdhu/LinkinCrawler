#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from store_helper import StoreHelper
import pandas


class DictHelper(object):
    @staticmethod
    def load_dict_from_excel(excel_file, sheet_index=0):
        raw_data = pandas.read_excel(excel_file, sheet_index).values
        row, column = raw_data.shape
        print("Get %i row %i column from excel file %s" % (row, column, excel_file))
        return {raw_data[i][0]: raw_data[i][1] for i in range(row)}

    @staticmethod
    def load_dict_from_dic(dict_file):
        return StoreHelper.load_data(dict_file, {})

    @staticmethod
    def save_dict(dic_data, dic_file):
        StoreHelper.store_data(dic_data, dic_file)

    @staticmethod
    def generate_geography_dic(raw_dict, prefix, deep=1):
        return {key: value for key, value in raw_dict.items() if DictHelper.__key_meet_requirement(key, prefix, deep)}

    @staticmethod
    def __key_meet_requirement(key, prefix, deep):
        if deep == 0:
            return key == prefix
        else:
            return prefix in key and key[len(prefix):].count('.') == deep

if __name__ == '__main__':
    # my_dict = DictHelper.generate_skills_dict("../resource/UserSkillUS.xlsx", 1)
    # print (len(my_dict.keys()))
    # StoreHelper.store_data(my_dict, "../data/skills.dic")
    # print (len(DictHelper.load_dict_from_dic("../data/skills.dic")))
    raw_dict = DictHelper.load_dict_from_excel("../resource/linkedin_geography.xlsx")
    print (DictHelper.generate_geography_dic(raw_dict, 'na.us', 1))
