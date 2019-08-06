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
import datetime
import os

import sys
import threading
import time
import urllib

import xbmc
import xbmcgui
import source as src

from strings import *

ADDON_ID = 'plugin.video.sportsaccess'


class Notification(object):
    def __init__(self, database, addonPath):
        """
        @param database: source.Database
        """
        self.database = database
        self.addonPath = addonPath
        self.icon = os.path.join(self.addonPath, 'icon.png')

    def createAlarmClockName(self, programTitle, startTime):
        return 'tvguide-%s-%s' % (programTitle, startTime)

    def scheduleNotifications(self):
        xbmc.log("[plugin.video.sportsaccess] Scheduling notifications", xbmc.LOGNOTICE)
        for ch_id, channelTitle, programTitle, startTime in self.database.getNotifications():
            self._scheduleNotification(ch_id, channelTitle, programTitle, startTime)

    def _scheduleNotification(self, ch_id, channelTitle, programTitle, startTime):
        t = startTime - datetime.datetime.now()
        timeToNotification = ((t.days * 86400) + t.seconds) / 60
        if timeToNotification < 0:
            return

        name = self.createAlarmClockName(programTitle, startTime)

        description = strings(NOTIFICATION_5_MINS, channelTitle)
        xbmc.executebuiltin('AlarmClock(%s-5mins,Notification(%s,%s,10000,%s),%d,True)' %
                            (name.encode('utf-8', 'replace'),
                             programTitle.encode('utf-8', 'replace'),
                             description.encode('utf-8', 'replace'), self.icon,
                             timeToNotification - 5))

        path = xbmc.translatePath(
            os.path.join('special://home', 'addons', ADDON_ID, 'notification.py'))
        xbmc.executebuiltin('AlarmClock(%s-now,RunScript(%s, %s, %s, "%s"),%d,True)' %
                            (name.encode('utf-8', 'replace'), path, ch_id,
                             channelTitle.encode('utf-8', 'replace'),
                             programTitle.encode('utf-8', 'replace'), timeToNotification))

    def _unscheduleNotification(self, programTitle, startTime):
        name = self.createAlarmClockName(programTitle, startTime)
        xbmc.executebuiltin('CancelAlarm(%s-5mins,True)' % name.encode('utf-8', 'replace'))
        xbmc.executebuiltin('CancelAlarm(%s-now,True)' % name.encode('utf-8', 'replace'))

    def addNotification(self, program):
        self.database.addNotification(program)
        self._scheduleNotification(program.channel.id, program.channel.title, program.title,
                                   program.startDate)

    def removeNotification(self, program):
        self.database.removeNotification(program)
        self._unscheduleNotification(program.title, program.startDate)


class NotifyWindow(xbmcgui.WindowXMLDialog):
    def __new__(cls):
        return super(NotifyWindow, cls).__new__(cls, 'script-tvguide-notify.xml',
                                                ADDON.getAddonInfo('path'))

    def __init__(self):
        super(NotifyWindow, self).__init__()
        self.is_closing = False
        self.start_play = False
        self.wait_time = 20
        self.control = None
        self.label = None
        self.message = ''

    def onInit(self):
        self.control = self.getControl(2000)
        self.label = self.getControl(2001)
        self.getControl(1000).setLabel(self.message)
        thread = ProgressMessage(self.progress, self.wait_time)
        thread.start()

    def progress(self, count, abort=False):
        if abort or self.is_closing:
            self.is_closing = True
            self.close()
            return False

        self.control.setPercent(count * 100 / self.wait_time)
        self.label.setLabel("%d seconds" % (self.wait_time - count))
        return not xbmc.abortRequested and not self.is_closing

    def onClick(self, controlId):
        if controlId == 1:
            self.is_closing = True
            self.start_play = True
            self.close()
        elif controlId == 2:
            self.is_closing = True
            self.close()
        return


class ProgressMessage(threading.Thread):
    def __init__(self, callback, wait_time):
        threading.Thread.__init__(self)
        self.callback = callback
        self.wait_time = wait_time

    def run(self):
        count = 0
        while count <= self.wait_time:
            if not self.callback(count):
                break
            count += 1
            time.sleep(1)
        self.callback(self.wait_time, True)


def onNotificationsCleared():
    xbmcgui.Dialog().ok(strings(CLEAR_NOTIFICATIONS), strings(DONE))


def onInitialized(success):
    if success:
        database.clearAllNotifications()
        database.close(onNotificationsCleared)
    else:
        database.close()


if __name__ == '__main__':

    if len(sys.argv) == 4:
        _, ch_id, ch_title, prg_title = sys.argv

        notify = NotifyWindow()
        notify.message = ch_title + '[CR]' + prg_title
        notify.doModal()

        if notify.start_play:
            icon = path = xbmc.translatePath(os.path.join('special://home', 'addons', ADDON_ID, 'icon.png'))
            xbmc.executebuiltin('Notification("Loading", "Please wait...",,%s)' % icon)
            streamUrl = urllib.quote('plugin://' + ADDON_ID + '/?url=' + ch_id +
                                     '&mode=565&name=' + prg_title, safe='?&=:/')
            xbmc.executebuiltin('RunPlugin(%s)' % streamUrl)

        del notify
    else:
        database = src.Database()
        database.initialize(onInitialized)
