# -*- coding: utf-8 -*-
"""
Geting odds 
"""
import re
from bs4 import BeautifulSoup


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__data__ = '08.09.2021'


def check_pattern(td):
    patterns = ['1.5', '2.5']
    team_tb = {}
    for pattern in patterns:
        try:
            team_tb[pattern] = td.find('div', text=re.compile(
                pattern)).find_next_sibling().find('span').text
            return team_tb
        except Exception:
            pass


def get_totals(html):
    """Geting total odds"""
    soup = BeautifulSoup(html, 'lxml')

    kefOver = []
    kefUnder= []
    divs = soup.find_all('div', text=re.compile(
        '(?<!Asian)\s* Total Goals \(\w+\s*(\&\s)?\w*\s*\w*\)\s*(?!.)'))
    for div in divs:
        itemsOver = {}
        itemsUnder = {}
        trs = div.find_parent('table').find_next_sibling().find_all('tr')[1:]
        for tr in trs:
            tds = tr.find_all('td')
            try:
                itemsOver = {**itemsOver, **check_pattern(tds[1])}
            except TypeError:
                pass
            except IndexError:
                pass
            try:
                itemsUnder = {**itemsUnder, **check_pattern(tds[0])}
            except TypeError:
                pass
            except IndexError:
                pass
        kefOver.append(itemsOver)
        kefUnder.append(itemsUnder)
    return kefOver, kefUnder


def get_CS(html):
    """Geting clean sheets odds"""
    soup = BeautifulSoup(html, 'lxml')

    csHome_yes, csHome_no, csAway_yes, csAway_no = ['', '', '', '']
    try:
        trs = soup.find('div', text=re.compile(
            'Goal Markets$')).find_parent('table').find_next_sibling().find_all(
            'tr')[2:10]
        for tr in trs:
            tds = tr.find_all('td')
            try:
                csAway_yes = tds[2].find('span', attrs={
                    'data-selection-key': re.compile(
                        'First_Team_To_Score.no')}).text
            except Exception:
                pass
            try:
                csAway_no = tds[1].find('span', attrs={
                    'data-selection-key': re.compile(
                        'First_Team_To_Score.yes')}).text
            except Exception:
                pass
            try:
                csHome_yes = tds[2].find('span', attrs={
                    'data-selection-key': re.compile(
                        'Second_Team_To_Score.no')}).text
            except Exception:
                pass
            try:
                csHome_no = tds[1].find('span', attrs={
                    'data-selection-key': re.compile(
                        'Second_Team_To_Score.yes')}).text
            except Exception:
                pass
    except AttributeError:
        pass
    return csHome_yes, csHome_no, csAway_yes, csAway_no
