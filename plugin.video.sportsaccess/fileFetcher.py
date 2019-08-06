# -*- coding: utf-8 -*-
#
# FTV Guide
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
#
#      Modified for use with SportsAccess
#      09/2016 SportsAccess.se
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import urllib

import xbmc
import xbmcvfs
import xbmcgui
import os
import urllib2
import datetime
import zlib

from strings import ADDON

MAIN_URL = 'http://37.187.77.87/api/'


class FileFetcher(object):
    INTERVAL_ALWAYS = 0
    INTERVAL_2 = 2
    INTERVAL_6 = 6
    INTERVAL_12 = 12
    INTERVAL_24 = 24
    INTERVAL_48 = 48

    FETCH_ERROR = -1
    FETCH_NOT_NEEDED = 0
    FETCH_OK = 1

    TYPE_DEFAULT = 1
    TYPE_REMOTE = 2

    base_path = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    file_path = ''
    file_url = ''
    addon = None
    file_type = TYPE_DEFAULT

    def __init__(self, file_name, addon, show_popup=True, interval=None):
        self.addon = addon
        self.show_popup = show_popup
        if interval is None:
            interval = self.INTERVAL_2
        self.interval = interval

        if file_name.startswith("http://") or file_name.startswith("sftp://") or file_name.startswith(
                "ftp://") or \
                file_name.startswith("https://") or file_name.startswith(
            "ftps://") or file_name.startswith("smb://") or \
                file_name.startswith("nfs://"):
            self.file_type = self.TYPE_REMOTE
            self.file_url = file_name
            self.file_path = os.path.join(self.base_path, file_name.split('/')[-1])
        else:
            self.file_type = self.TYPE_DEFAULT
            user = addon.getSetting('skyusername')
            passw = addon.getSetting('skypassword')
            data = {'username': user, 'password': passw, 'type': file_name}
            data = urllib.urlencode(data)
            self.file_url = MAIN_URL + '?' + data
            self.file_path = os.path.join(self.base_path, file_name)

        # make sure the folder is actually there already!
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def fetch_file(self):
        ret_val = self.FETCH_NOT_NEEDED
        fetch = False
        if not os.path.exists(self.file_path):  # always fetch if file doesn't exist!
            fetch = True
        else:
            interval = self.interval  # int(self.addon.getSetting('xmltv.interval'))
            if interval != self.INTERVAL_ALWAYS:
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.file_path))
                td = datetime.datetime.now() - mod_time
                # need to do it this way cause Android doesn't support .total_seconds() :(
                diff = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6
                if ((interval == self.INTERVAL_2 and diff >= 7200) or
                        (interval == self.INTERVAL_6 and diff >= 21600) or
                        (interval == self.INTERVAL_12 and diff >= 43200) or
                        (interval == self.INTERVAL_24 and diff >= 86400) or
                        (interval == self.INTERVAL_48 and diff >= 172800)):
                    fetch = True
            else:
                fetch = True

        if fetch:
            tmp_file = os.path.join(self.base_path, 'tmp')
            if self.file_type == self.TYPE_REMOTE:
                xbmc.log('[plugin.video.sportsaccess] file is in remote location: %s' % self.file_url,
                         xbmc.LOGDEBUG)
                if not xbmcvfs.copy(self.file_url, tmp_file):
                    xbmc.log(
                        '[plugin.video.sportsaccess] Remote file couldn\'t be copied: %s' % self.file_url,
                        xbmc.LOGERROR)
            else:
                f = open(tmp_file, 'wb')
                xbmc.log('[plugin.video.sportsaccess] file is on the internet', xbmc.LOGDEBUG)
                try:
                    tmp_data = urllib2.urlopen(self.file_url)
                    data = tmp_data.read()
                    if tmp_data.info().get('content-encoding') == 'gzip':
                        data = zlib.decompress(data, zlib.MAX_WBITS + 16)
                    f.write(data)
                except urllib2.URLError as e:
                    xbmc.log('[plugin.video.sportsaccess] Error downloading file: %s' % str(e), xbmc.LOGERROR)
                    if self.show_popup:
                        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'),
                                            '[COLOR red]Error downloading Guide Data![/COLOR]', str(e))
                    return self.FETCH_ERROR
                f.close()
            if os.path.getsize(tmp_file) > 256:
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)
                os.rename(tmp_file, self.file_path)
                ret_val = self.FETCH_OK
                xbmc.log('[plugin.video.sportsaccess] file %s was downloaded' % self.file_path, xbmc.LOGDEBUG)
            else:
                ret_val = self.FETCH_ERROR
        return ret_val


def fetch_extra_files(show_popup=True):
    fetcher = FileFetcher("4", ADDON, show_popup, interval=FileFetcher.INTERVAL_2)
    result = fetcher.fetch_file()
    if result == fetcher.FETCH_OK:
        xbmc.log("[plugin.video.sportsaccess] Messages downloaded", xbmc.LOGDEBUG)
    elif result == fetcher.FETCH_ERROR:
        xbmc.log("[plugin.video.sportsaccess] Error downloading Messages", xbmc.LOGERROR)
        return False

    fetcher = FileFetcher("5", ADDON, show_popup, interval=FileFetcher.INTERVAL_2)
    result = fetcher.fetch_file()
    if result == fetcher.FETCH_OK:
        xbmc.log("[plugin.video.sportsaccess] Team-Map downloaded", xbmc.LOGDEBUG)
    elif result == fetcher.FETCH_ERROR:
        xbmc.log("[plugin.video.sportsaccess] Error downloading Team-Map", xbmc.LOGERROR)
        return False

    return True
