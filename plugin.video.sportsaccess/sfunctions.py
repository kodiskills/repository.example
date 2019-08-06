# -*- coding: utf-8 -*-
#
#      Copyright (C) 2016 SportsAccess.se
#

import datetime
def timestampToDate(timestamp):
    return datetime.datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d')