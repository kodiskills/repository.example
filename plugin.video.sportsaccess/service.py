# -*- coding: utf-8 -*-
#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
#      Modified for use with SportsAccess
#      09/2016 SportsAccess.se
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
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

import json
import os
import urllib
import urllib2

import xbmcaddon
import notification
import xbmc
import xbmcgui
import source
import fileFetcher
from strings import PROC_FILE, ADDON


class Service(object):
    def __init__(self):
        self.database = source.Database(False)
        self.database.initialize(self.onInit)
        self.pluginData = xbmc.translatePath(os.path.join('special://profile', 'addon_data', ADDON.getAddonInfo('id')))

    def onInit(self, success):
        if success:
            self.database.updateChannelAndProgramListCaches(self.onCachesUpdated)
            fileFetcher.fetch_extra_files(False)
        else:
            self.database.close()

    def onCachesUpdated(self):

        if ADDON.getSetting('notifications.enabled') == 'true':
            n = notification.Notification(self.database, ADDON.getAddonInfo('path'))
            n.scheduleNotifications()

        self.database.close(None)


def login_popup(message=None):
    dialog = xbmcgui.Dialog()
    additional = 'or register if you don have an account at sportsaccess.se'
    if message:
        additional = message
    ret = dialog.yesno('[COLOR red]SportsAccess[/COLOR]', 'Please check your SportsAccess credentials',
                       additional, '', 'Cancel', 'Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Enter Username')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            username = search
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                search = keyb.getText()
                password = search
                ADDON.setSetting('skyusername', username)
                ADDON.setSetting('skypassword', password)
                return verify_login(username, password)

    return False


def verify_login(u_name, u_pass, show_popup=True):
    login_url = 'http://sportsaccess.se/?api_check=1'
    default_timeout = 30
    data = {'username': u_name, 'password': u_pass}
    data = urllib.urlencode(data)
    opener = urllib2.build_opener()
    response = opener.open(login_url, data, default_timeout)
    json_raw = response.read()
    opener.close()
    response.close()
    if json_raw:
        json_object = json.loads(json_raw)
        if "error" in json_object:
            xbmc.log("[plugin.video.sportsaccess] Login-Error: %s" % json_object["error"],
                     xbmc.LOGWARNING)
            if show_popup:
                return login_popup("Error - " + json_object["error"])
            else:
                return False
        else:
            return True
    return False


def run_service():
    ok = True
    user = ADDON.getSetting('skyusername')
    passw = ADDON.getSetting('skypassword')
    if user == '' or passw == '':
        xbmc.log("[plugin.video.sportsaccess] No username or password configured!",
                 xbmc.LOGWARNING)
        ok = False
    else:
        ok = verify_login(user, passw, False)
    if ok:
        xbmc.log("[plugin.video.sportsaccess] Service now being triggered...", xbmc.LOGNOTICE)
        Service()
    else:
        xbmc.log("[plugin.video.sportsaccess] Service cannot be triggered", xbmc.LOGWARNING)


if __name__ == '__main__':

    # After a restart the proc file should be wiped!
    path = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    if not os.path.exists(path):
        os.mkdir(path)
    f = open(PROC_FILE, 'w')
    f.write('')
    f.close()

    try:
        ADDON = xbmcaddon.Addon('plugin.video.sportsaccess')
        if ADDON.getSetting('autostart') == "true":
            xbmc.executebuiltin("RunAddon(plugin.video.sportsaccess)")

        monitor = xbmc.Monitor()
        xbmc.log("[plugin.video.sportsaccess] Background service started...", xbmc.LOGNOTICE)
        run_service()

        interval = 1  # hard-coded to 1 hour
        if interval == 1:
            waitTime = 3600  # Default 1hr
        elif interval == 2:
            waitTime = 7200  # 2hrs
        elif interval == 6:
            waitTime = 21600  # 6hrs
        elif interval == 12:
            waitTime = 43200  # 12hrs
        elif interval == 24:
            waitTime = 86400  # 24hrs

        while not monitor.abortRequested():
            # Sleep/wait for specified time
            xbmc.log("[plugin.video.sportsaccess] Service waiting for interval %s sec." % waitTime,
                     xbmc.LOGNOTICE)
            if monitor.waitForAbort(waitTime):
                # Abort was requested while waiting. We should exit
                break
            run_service()

    except source.SourceNotConfiguredException:
        pass  # ignore
    except Exception, ex:
        xbmc.log('[plugin.video.sportsaccess] Uncaught exception in service.py: %s' % str(ex),
                 xbmc.LOGERROR)
