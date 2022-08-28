# -*- coding: utf-8 -*-
"""
Additional requests
"""
from simple_settings import settings
from common_modules.parser import ParserPost, Parser


__author__ = 'Vadim Arsenev'
__version__ = '1.1.0'
__data__ = '04.08.2021'


def add_html(treeid):
    params = {'treeId': treeid, 'siteStyle': 'SIMPLE'}
    tournamentMarket = Parser(settings.MARKETS_URL, params=params)
    html = tournamentMarket.parser_resultHtml()

    return html


def add_html_old(treeid):
    payload = {'treeId': treeid, 'columnSize': '8', 'siteStyle': 'SIMPLE'}
    tournamentMarket = ParserPost(settings.MARKETS_URL, payload)
    html = tournamentMarket.parser_resultHtml()

    return html
