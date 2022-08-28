# -*- coding: utf-8 -*-
"""
Formatting on marathonbet 
"""
from simple_settings import settings
from common_modules.txt_r import read_txt
from common_modules.json_rw import json_write, json_read
from datetime import datetime, timedelta


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__data__ = '04.08.2021'


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


def make_abbr():
    teams = dict(zip(list(map(lambda x: x.split(':')[0].strip(), \
                    read_txt(settings.TEAMS).split('\n'))), \
                     list(map(lambda x: x.split(':')[1].strip(), \
                    read_txt(settings.TEAMS).split('\n')))))
    json_write('./data/teams.json', teams)


def make_team():
    teams = dict(zip(list(map(lambda x: x.split(':')[0].strip(), \
                    read_txt(settings.TEAMS).split('\n'))), \
                     list(map(lambda x: x.split(':')[0].strip(), \
                    read_txt(settings.TEAMS).split('\n')))))
    json_write('./data/teams.json', teams)


def renameTeams(team):
    """Change the name of the team to abbreviation"""
    try:
        teams = json_read('./data/teams.json')
    except FileNotFoundError:
        pass

    try:
        abbr = teams[team]
    except KeyError:
        abbr = team
    return abbr
