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
    with open('marathonbet.csv', 'a', encoding='utf-8') as file:
        order = [
            'nowDate', 'nowTime',
            'matchDate', 'matchTime',
            'teamHome', 'teamAway',
            'kefWin', 'kefDraw', 'kefLose',
            'csHome', 'csAway',
            'team1_over25', 'team2_over25',
            'team1_over15', 'team2_over15', ]
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def run_once(f):
    def wrapper(*args, **kwargs):
        wrapper.has_run = os.path.isfile('marathonbet.csv')
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def print_headline():
    """Insert table header"""
    data_headline = {'nowDate': 'parsingDate', 'nowTime': 'parsingTime',
                     'matchDate': 'Date', 'matchTime': 'Time',
                     'teamHome': 'Home', 'teamAway': 'Away',
                     'kefWin': '1', 'kefDraw': 'X', 'kefLose': '2',
                     'csHome': 'CS1', 'csAway': 'CS2',
                     'team1_over25': '1 > 2.5', 'team2_over25': '2 > 2.5',
                     'team1_over15': '1 > 1.5', 'team2_over15': '2 > 1.5', }
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
    matchDate_full = matchDate_full + timedelta(hours=2)
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

    teams_over = []
    divs = soup.find_all('div', text=re.compile(
        'Total Goals \(\w+\s*(\&\s)?\w*\s*\w*\)\s*(?!.)'))
    for div in divs:
        tb_team = {}
        trs = div.find_parent('table').find_next_sibling().find_all('tr')[1:]
        for tr in trs:
            tds = tr.find_all('td')
            try:
                tb_team = {**tb_team, **check_pattern(tds[1])}
            except TypeError:
                pass
            except IndexError:
                pass
        teams_over.append(tb_team)
    return teams_over


def get_CS(html):
    """Getting clean sheets odds"""
    soup = BeautifulSoup(html, 'lxml')

    csHome, csAway = ['', '']
    try:
        trs = soup.find('div', text=re.compile(
            'Goal Markets')).find_parent('table').find_next_sibling().find_all(
            'tr')[2:10]
        for tr in trs:
            tds = tr.find_all('td')
            try:
                csAway = tds[2].find('span', attrs={
                    'data-selection-key': re.compile(
                        'First_Team_To_Score.no')}).text
            except Exception:
                pass
            try:
                csHome = tds[2].find('span', attrs={
                    'data-selection-key': re.compile(
                        'Second_Team_To_Score.no')}).text
            except Exception:
                pass
    except AttributeError:
        pass
    return csHome, csAway


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
        teams_over = get_totals(html_dop)
        csHome, csAway = get_CS(html_dop)

        data = {'nowDate': nowDate, 'nowTime': nowTime,
                'matchDate': matchDate, 'matchTime': matchTime,
                'teamHome': teamHome, 'teamAway': teamAway,
                'kefWin': kefWin, 'kefDraw': kefDraw, 'kefLose': kefLose,
                'csHome': csHome, 'csAway': csAway, }

        try:
            data.update({'team1_over15': teams_over[0]['1.5']})
        except LookupError:
            data.update({'team1_over15': ''})
        try:
            data.update({'team1_over25': teams_over[0]['2.5']})
        except LookupError:
            data.update({'team1_over25': ''})
        try:
            data.update({'team2_over15': teams_over[1]['1.5']})
        except LookupError:
            data.update({'team2_over15': ''})
        try:
            data.update({'team2_over25': teams_over[1]['2.5']})
        except LookupError:
            data.update({'team2_over25': ''})

        write_csv(data)


def main():
    urls = TOURNAMENTS_URL.split(', ')
    for url in urls:
        tournament = Parser(url)
        get_pageData(tournament.parserResult())


if __name__ == '__main__':
    main()
