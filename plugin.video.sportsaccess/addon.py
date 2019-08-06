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
import gui
import xbmc
import json
from strings import PROC_FILE, ADDON
from service import verify_login, login_popup


def get_kodi_version():
    # retrieve current installed version
    jsonQuery = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    jsonQuery = unicode(jsonQuery, 'utf-8', errors='ignore')
    jsonQuery = json.loads(jsonQuery)
    version = []
    if jsonQuery.has_key('result') and jsonQuery['result'].has_key('version'):
        version = jsonQuery['result']['version']
    return version['major']


if __name__ == '__main__':
    ok = True
    user = ADDON.getSetting('skyusername')
    passw = ADDON.getSetting('skypassword')
    if user == '' or passw == '':
        ok = login_popup()
    else:
        ok = verify_login(user, passw)

    if ok:
        # Apply Workaround for Kodi v17 on Android
        if xbmc.getCondVisibility('system.platform.android') and int(get_kodi_version()) == 17:
            ADDON.setSetting('background.stream', 'false')

        # After a restart the proc file should be wiped!
        f = open(PROC_FILE, 'w')
        f.write('')
        f.close()

        try:
            w = gui.TVGuide()
            w.doModal()
            del w

        except:
            import sys
            import traceback as tb
            (etype, value, traceback) = sys.exc_info()
            tb.print_exception(etype, value, traceback)