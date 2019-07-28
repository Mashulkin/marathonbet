# -*- coding: utf-8 -*-
import requests
import settings


__author__ = 'Vadim Arsenev'
__version__ = '1.0.1'
__data__ = '28.07.2019'


class Parser(object):

    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/67.0.3396.79 Safari/537.36', }
        self.proxies = settings.proxies

    def response(self):
        """Connection to the site. Sending Get request"""
        response = requests.get(
            self.url, headers=self.headers, proxies=self.proxies)
        response.encoding = 'utf-8'
        return response

    def get_pageHtml(self, response):
        """Getting html"""
        data = response.text
        return data

    def parserResult(self):
        return self.get_pageHtml(self.response())


class ParserPost(Parser):

    def __init__(self, treeid, url=''):
        super().__init__(url)
        self.url = settings.markets_url
        self.treeid = treeid

    def response(self):
        """Connection to the site. Sending Post request"""
        payload = {'treeId': self.treeid, 'columnSize': '8', 'siteStyle': 'SIMPLE'}
        response = requests.post(
            settings.markets_url, data=payload, proxies=self.proxies)
        response.encoding = 'utf-8'
        return response
