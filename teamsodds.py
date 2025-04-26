# -*- coding: utf-8 -*-
"""
Geting odds on marathonbet
"""
import addpath
from simple_settings import settings

from common_modules.csv_w import write_csv
from common_modules.txt_r import read_txt
from common_modules.headline import print_headline
from common_modules.parser import Parser
from common_modules.my_remove import remove_file
from function.format import refine_date, renameTeams, make_team, make_abbr
from function.odds import get_CS, get_totals
from function.addreq import add_html

import re
from bs4 import BeautifulSoup


__author__ = 'Vadim Arsenev'
__version__ = '1.1.0'
__data__ = '26.04.2025'


ORDER = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS).split('\n')))


def get_pageData(html):
    """The main module for performing all operations of a request
       and writing to a file"""
    print_headline(settings.RESULT_FILE[0], settings.COLUMNS, ORDER)
    if settings.TEAM_NAMES == 'abbr':
        make_abbr()
    else:
        make_team()

    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find_all('div', class_='bg coupon-row')
    for tr in trs:
        tds = tr.find_all('span', class_='member')
        teamHome = renameTeams(tds[0].find('span').text.strip())
        teamAway = renameTeams(tds[1].find('span').find_next('span').text.strip())
        matchDate_str = tr.find('div', class_='score-and-time').find('span').text.strip()
        nowDate, nowTime, matchDate, matchTime = refine_date(
            matchDate_str)

        print(f'{matchDate}: {teamHome} - {teamAway}')
        tds = tr.find_all('td', colspan='2')
        try:
            kefWin = float(tds[0].find('span', class_='right-simple').text.strip())
            kefDraw = float(tds[1].find('span', class_='right-simple').text.strip())
            kefLose = float(tds[2].find('span', class_='right-simple').text.strip())
        except ValueError:
            kefWin = float(tds[1].find('span', class_='right-simple').text.strip())
            kefDraw = float(tds[2].find('span', class_='right-simple').text.strip())
            kefLose = float(tds[3].find('span', class_='right-simple').text.strip())
        try:
            treeid = tr.find_all(
                'td', class_='member-area-button')[0].get('treeid')
        except IndexError:
            continue

        html_dop = add_html(treeid)
        kefOver, kefUnder = get_totals(html_dop)
        csHome_yes, csHome_no, csAway_yes, csAway_no = get_CS(html_dop)

        dataHome = {'team': teamHome,
                    'kefWin': kefWin,
                    'kefDraw': kefDraw,
                    'cs_yes': csHome_yes,
                    'cs_no': csHome_no, 
                    'matchDate': matchDate, }

        try:
            dataHome.update({'over15': kefOver[0]['1.5']})
        except LookupError:
            dataHome.update({'over15': ''})
        try:
            dataHome.update({'over25': kefOver[0]['2.5']})
        except LookupError:
            dataHome.update({'over25': ''})
        try:
            dataHome.update({'under15': kefUnder[0]['1.5']})
        except LookupError:
            dataHome.update({'under15': ''})
        try:
            dataHome.update({'under25': kefUnder[0]['2.5']})
        except LookupError:
            dataHome.update({'under25': ''})

        write_csv(settings.RESULT_FILE[0], dataHome, ORDER)

        dataAway = {'team': teamAway,
                    'kefWin': kefLose,
                    'kefDraw': '',
                    'cs_yes': csAway_yes,
                    'cs_no': csAway_no, 
                    'matchDate': matchDate, }

        try:
            dataAway.update({'over15': kefOver[1]['1.5']})
        except LookupError:
            dataAway.update({'over15': ''})
        try:
            dataAway.update({'over25': kefOver[1]['2.5']})
        except LookupError:
            dataAway.update({'over25': ''})
        try:
            dataAway.update({'under15': kefUnder[1]['1.5']})
        except LookupError:
            dataAway.update({'under15': ''})
        try:
            dataAway.update({'under25': kefUnder[1]['2.5']})
        except LookupError:
            dataAway.update({'under25': ''})

        write_csv(settings.RESULT_FILE[0], dataAway, ORDER)


def main():
    tournament = Parser(settings.TOURNAMENTS_URL)
    get_pageData(tournament.parser_resultHtml())



if __name__ == '__main__':
    remove_file(settings.RESULT_FILE[0])
    main()
    remove_file('./data/teams.json')
