#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class TextHelper(object):
    @staticmethod
    def store_html(web_source, file_name='web.html'):
        file_output = open(file_name, "w")
        file_output.write(web_source)
        file_output.close()

    @staticmethod
    def extract_company_skills(web_source):
        soup = BeautifulSoup(web_source.decode('utf-8'), 'html.parser')
        try:
            company_name = soup.find("a", class_="jobs-details-top-card__company-url").getText()
            print company_name.encode('utf-8')
        except AttributeError:
            company_name = 'UNKOWN'
        pretty_html = soup.prettify().encode('utf-8')
        skill_content = TextHelper.find_text_between_tag(pretty_html, '"text":', '</code>')
        file_ = open("debug.html", 'wb')
        file_.write(pretty_html)
        file_.close()
        return company_name.encode('utf-8'), skill_content

    @staticmethod
    def find_text_between_tag(content, start_tag="<!--\n", end_tag="\n-->"):
        try:
            start_index = content.index(start_tag)
        except ValueError as TAG_NOT_FOUND_ERROR:
            print("start tag: " + start_tag + " not found in content")
            return None
        content = content[start_index:]

        if len(end_tag) == 0:
            return content
        try:
            end_index = content.index(end_tag)
        except ValueError as TAG_NOT_FOUND_ERROR:
            print("end tag: " + end_tag + " not found in content")
            return None
        return content[:end_index]