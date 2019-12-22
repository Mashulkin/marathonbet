# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import csv
import re
import os.path
import requests
from bs4 import BeautifulSoup
from modules.parser import Parser, ParserPost
from settings import TOURNAMENTS_URL, teams


def write_csv(data):
    """Write data in csv file"""
    if not os.path.exists(os.path.dirname(FILENAME)):
        os.makedirs(os.path.dirname(FILENAME))
    with open(FILENAME, 'a', encoding='utf-8') as file:
        order = [
            'team', 'kefWin', 'kefDraw', 'cs_yes', 'cs_no', 
            'over25', 'under25', 'over15', 'under15', ]
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def run_once(f):
    def wrapper(*args, **kwargs):
        wrapper.has_run = os.path.isfile(FILENAME)
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def print_headline():
    """Insert table header"""
    data_headline = {'team': 'Team',
                     'kefWin': 'Win', 'kefDraw': 'Draw',
                     'cs_yes': 'CS_yes', 'cs_no': 'CS_no',
                     'over25': '>2.5',
                     'over15': '>1.5',
                     'under15': '<1.5',
                     'under25': '<2.5', }
    write_csv(data_headline)


def refine_date(matchDate):
    """Date formatting"""
    now = datetime.now()
    try:
        matchDate_full = datetime.strptime(
            matchDate, '%d %b %H:%M').replace(year=now.year)
    except ValueError:
        matchDate_full = datetime.strptime(
            matchDate, '%H:%M').replace(
            year=now.year, month=now.month, day=now.day)
    matchDate_full = matchDate_full + timedelta(hours=3)
    matchDate = matchDate_full.date()
    matchTime = matchDate_full.time().strftime('%H:%M')
    nowTime = datetime.strftime(now, '%H:%M')
    return now.date(), nowTime, matchDate, matchTime


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
    """Getting total odds"""
    soup = BeautifulSoup(html, 'lxml')

    kefOver = []
    kefUnder= []
    divs = soup.find_all('div', text=re.compile(
        'Total Goals \(\w+\s*(\&\s)?\w*\s*\w*\)\s*(?!.)'))
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
    """Getting clean sheets odds"""
    soup = BeautifulSoup(html, 'lxml')

    csHome_yes, csHome_no, csAway_yes, csAway_no = ['', '', '', '']
    try:
        trs = soup.find('div', text=re.compile(
            'Goal Markets')).find_parent('table').find_next_sibling().find_all(
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


def renameTeams(team):
    """Change the name of the team to abbreviation"""
    try:
        abbr = teams[team]
    except KeyError:
        abbr = team
    return abbr


def get_pageData(html):
    """The main module for performing all operations of a request
       and writing to a file"""
    print_headline()
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    trs = soup.find_all('tr', class_='sub-row')
    for tr in trs:
        # print(tr)
        tds = tr.find_all('td', class_=re.compile('name'))
        teamHome = renameTeams(tds[0].find('span').text.strip())
        teamAway = renameTeams(tds[1].find('span').text.strip())
        matchDate_str = tr.find('td', class_='date').text.strip()
        nowDate, nowTime, matchDate, matchTime = refine_date(
            matchDate_str)

        print(f'{matchDate}: {teamHome} - {teamAway}')
        tds = tr.find_all('td', colspan='2')
        kefWin = tds[0].text.strip()
        kefDraw = tds[1].text.strip()
        kefLose = tds[2].text.strip()

        treeid = tr.find_all(
            'td', class_='member-area-button')[1].get('treeid')

        tournamentMarket = ParserPost(treeid)
        html_dop = tournamentMarket.parserResult()
        kefOver, kefUnder = get_totals(html_dop)
        csHome_yes, csHome_no, csAway_yes, csAway_no = get_CS(html_dop)

        dataHome = {'team': teamHome,
                    'kefWin': kefWin,
                    'kefDraw': kefDraw,
                    'cs_yes': csHome_yes,
                    'cs_no': csHome_no, }

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

        write_csv(dataHome)

        dataAway = {'team': teamAway,
                    'kefWin': kefLose,
                    'kefDraw': '',
                    'cs_yes': csAway_yes,
                    'cs_no': csAway_no, }

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

        write_csv(dataAway)


def main():
    urls = TOURNAMENTS_URL.split(', ')
    for url in urls:
        tournament = Parser(url)
        get_pageData(tournament.parserResult())


if __name__ == '__main__':
    FILENAME = './data/marathonbet2.csv'
    main()
