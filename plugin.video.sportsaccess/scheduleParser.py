# -*- coding: utf-8 -*-
#
#      Copyright (C) 2016 SportsAccess.se
#

import os
import re
import urllib2
import time
import datetime
from HTMLParser import HTMLParser
from xml.etree import ElementTree

import pytz
import xbmc
from Category import Category

schedule_url = 'http://sportsaccess.se/schedule_new/index.php'
default_timeout = 30


def parse_schedule_xmltv(s_file):
    programmes = []
    if not os.path.exists(s_file):
        return programmes

    tree = ElementTree.parse(s_file)
    root = tree.getroot()
    for elem in root.findall('programme'):
        channel = elem.get("channel").replace("'", "")
        title = elem.findtext('title')
        category = elem.findtext('category')
        start = elem.get('start')
        end = elem.get('end')
        programmes.append({'channel': channel, 'title': title, 'startDate': start, 'endDate': end,
                           'category': category})
    return programmes


def parse_schedule():
    programmes = []
    html_parser = HTMLParser()
    categories = Category.category_mappings
    for day, day_date in list_days().items():
        xbmc.log("Parsing day=" + day, xbmc.LOGDEBUG)
        request_url = schedule_url + "?js=0"
        request_url += "&timezone=America/New_York&cat=&day=" + day
        request_url = request_url.replace(" ", "%20")
        xbmc.log(request_url, xbmc.LOGDEBUG)
        schedule_html = html_no_cookies(request_url)

        list_html = schedule_html.split('id="schedule"')[1]
        list_html = list_html.split('</ul>')[0]
        list_html = list_html.split('<ul>')[1]
        list_items = re.compile('<li.+? style=\'(.*)\'>\n*(.*\n*.*\n*.*\n*.*\n*.*\n*.*)</li>').findall(list_html)
        for colour, line in list_items:
            if colour:
                colour = colour[:-1].split(':')[1]
            line = line.strip()
            item_parts = re.compile('.* (.*) \|.*\n*.*<i>#(.+)</i>.*\n*.*\|.*\n*(.+)').findall(line)
            for event_time, ch, event_name in item_parts:
                event_name = re.sub('[\t+]', '', event_name)
                is_hd = 'HD720.png' in event_name
                event_name = re.sub('<img.*>', '', event_name)
                event_name = html_parser.unescape(event_name)
                if is_hd:
                    event_name = '[B][COLOR white]HD|720[/COLOR][/B] - ' + event_name
                if isinstance(event_name, str):
                    event_name = event_name.encode("utf-8", 'ignore')

                ch = str(ch)
                t_start, t_end = prepare_times(event_time, day_date)
                utc_start = to_local_time(t_start)
                utc_end = to_local_time(t_end)

                category = ''
                for cat, cat_colour in categories.iteritems():
                    if colour == cat_colour:
                        category = cat
                        break
                programmes.append({'channel': ch, 'title': event_name, 'startDate': utc_start,
                                   'endDate': utc_end, 'category': category})
    return programmes


def prepare_times(event_time, naive_date):
    time_start, time_end = event_time.split('-')
    item_start_date = "%s-%s-%s %s:00" % (
        naive_date.year, naive_date.month, naive_date.day, time_start)
    xbmc.log(str(naive_date)+" -> "+item_start_date, xbmc.LOGDEBUG)
    hrs_start, _ = time_start.split(":")
    hrs_end, _ = time_end.split(":")
    if int(hrs_start) >= 20 and int(hrs_end) <= 5:
        naive_date = naive_date + datetime.timedelta(days=1)
    item_end_date = "%s-%s-%s %s:00" % (
        naive_date.year, naive_date.month, naive_date.day, time_end)
    try:
        t_start = datetime.datetime.strptime(item_start_date, '%Y-%m-%d %H:%M:%S')
        t_end = datetime.datetime.strptime(item_end_date, '%Y-%m-%d %H:%M:%S')
    except TypeError:
        t_start = datetime.datetime.fromtimestamp(
                        time.mktime(time.strptime(item_start_date, '%Y-%m-%d %H:%M:%S')))
        t_end = datetime.datetime.fromtimestamp(
                        time.mktime(time.strptime(item_end_date, '%Y-%m-%d %H:%M:%S')))

    return t_start, t_end


def to_local_time(dt):
    utc = pytz.utc
    local_tz = pytz.timezone('US/Eastern')
    dt_aware = local_tz.localize(dt)
    dt_utc_aware = dt_aware.astimezone(utc)
    utc_naive = dt_utc_aware.replace(tzinfo=None) - dt_utc_aware.utcoffset()
    # get the local timezone offset in seconds
    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset = - (time.altzone if is_dst else time.timezone)
    td_local = datetime.timedelta(seconds=utc_offset)
    return utc_naive + td_local


def list_days():
    dates = {}
    utc = pytz.utc
    local_tz = pytz.timezone('US/Eastern')
    html = html_no_cookies(schedule_url)
    partial = html.split('id="days"')[1]
    partial = partial.split('</div>')[0]
    matchlist = re.compile('data-day="([^"]+)".?>([^"]+)</li').findall(partial)
    for timestamp, _ in matchlist:
        day_date = datetime.datetime.fromtimestamp(float(timestamp))
        dt_aware = local_tz.localize(day_date)
        dt_utc_aware = dt_aware.astimezone(utc)
        day_date = dt_utc_aware.replace(tzinfo=None) - dt_utc_aware.utcoffset()
        dates[timestamp] = day_date.replace(hour=0, minute=0)
    return dates


def get_channels():
    channels = {}
    xbmc.log("Fetching channels...", xbmc.LOGDEBUG)
    request_url = schedule_url + "?js=0&cat=Channel%20List"
    xbmc.log(request_url, xbmc.LOGDEBUG)
    schedule_html = html_no_cookies(request_url)

    list_html = schedule_html.split('id="schedule"')[1]
    list_html = list_html.split('</ul>')[0]
    list_html = list_html.split('<ul>')[1]
    list_items = re.compile('<li.+?>\n*(.*\n*.*\n*.*\n*.*\n*.*\n*.*)</li>').findall(list_html)
    for line in list_items:
        line = line.strip()
        item_parts = re.compile('.* (.*) \|.*\n*.*<i>#(.+)</i>.*\n*.*\|.*\n*(.+)').findall(line)
        for _, ch_no, ch_name in item_parts:
            ch_name = re.sub('[\t+]', '', ch_name)
            ch_name = re.sub('<img.*>', '', ch_name)
            ch_name = ch_name.replace("&amp;", "&")
            ch_no = str(ch_no)
            xbmc.log(ch_no + ": " + ch_name + ", ", xbmc.LOGDEBUG)
            channels[ch_no] = ch_name
    return channels


def html_no_cookies(url):
    opener = urllib2.build_opener()
    response = opener.open(url, "", default_timeout)
    encoding = response.headers.getparam('charset')
    raw = response.read().decode(encoding)
    opener.close()
    response.close()
    return raw
