#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import os


class StoreHelper(object):
    @staticmethod
    def store_data(data, store_file):
        file_handler = open(store_file, 'wb')
        pickle.dump(data, file_handler)
        file_handler.close()

    @staticmethod
    def load_data(store_file):
        file_handler = open(store_file, 'rb')
        data = pickle.load(file_handler)
        file_handler.close()
        return data

