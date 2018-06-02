#coding:utf-8

from HTMLParser import HTMLParser
from flask_restful import fields


class HTMLField(fields.Raw):

    def format(self, value):
        return strip_tags(str(value))


class HTMLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed =[]

    def handle_data(self, data_object):
        self.fed.append(data_object)

    def get_data(self):
        return ''.join(self.fed)



def strip_tags(html):

    stripper = HTMLStripper()
    stripper.feed(html)

    return stripper.get_data()