#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from store_helper import StoreHelper
import pandas


class ExcelHelper(object):
    @staticmethod
    def generate_skills_dict(excel_file, sheet_index=0):
        raw_data = pandas.read_excel(excel_file, sheet_index).values
        row, column = raw_data.shape
        print("Get %i row %i column from excel file %s" % (row, column, excel_file))
        return {raw_data[i][0]: raw_data[i][1] for i in range(row)}


if __name__ == '__main__':
    my_dict = ExcelHelper.generate_skills_dict("../resource/UserSkillUS.xlsx", 1)
    print (len(my_dict.keys()))
    StoreHelper.store_data(my_dict, "../data/skills.dic")

