# -*- coding: utf-8 -*-
#
#      Copyright (C) 2015 SportsAccess.se
#

import json
import os
import re
import urllib
import urllib2
from os.path import join

import sfunctions
import time
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

addon_id = 'plugin.video.sportsaccess'
AddonID = "plugin.video.sportsaccess"
artpath = xbmc.translatePath(join('special://home/addons/' + AddonID + '/resources/'))
ADDON = xbmcaddon.Addon(id='plugin.video.sportsaccess')
selfAddon = xbmcaddon.Addon(id=addon_id)
prettyName = 'SportsAccess'
fanart = xbmc.translatePath(join('special://home/addons/' + AddonID, 'fanart.jpg'))
icon = xbmc.translatePath(join('special://home/addons/' + AddonID, 'icon.jpg'))
art = xbmc.translatePath(join('special://home/addons/plugin.video.sportsaccess/resources/art', ''))
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
UpdatePath = join(datapath, 'Update')
cookiedir = join(join(datapath, 'Cookies'))
cookie_file = join(join(datapath, 'Cookies'), 'sportsaccess.cookies')
# Default settings for schedule
playConfig = {}
playConfig['defaultServerHost'] = "usa.01.cdnstreams.in"
playConfig['defaultServerPort'] = "6034"
playConfig['defaultServerName'] = "East USA"
scheduleConfig = {}
scheduleConfig['scheduleTimestamp'] = 0
scheduleConfig['scheduleCategory'] = 'All'
scheduleConfig['scheduleTimezoneValue'] = 'America/New_York'
scheduleConfig['scheduleTimezoneName'] = 'East Coast'
scheduleUrl = 'http://sportsaccess.se/schedule_new/index.php'
loginUrl = 'http://sportsaccess.se/?api_check=1'
defaultTimeout = 30

try:
    os.makedirs(UpdatePath)
except:
    pass

try:
    os.makedirs(cookiedir)
except:
    pass

if selfAddon.getSetting("server-location") == "true":
    BASE_URL = 'usplayer'
else:
    BASE_URL = 'euplayer'

user = selfAddon.getSetting('skyusername')
passw = selfAddon.getSetting('skypassword')


def OPENURL(url, mobile=False, q=False, verbose=True, timeout=10, cookie=None, data=None,
            cookiejar=False, log=True, headers=[], type='', ua=False, setCookie=[], raiseErrors=False,
            ignore_discard=True):
    import urllib2

    UserAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    if ua: UserAgent = ua
    try:
        if log:
            print "MU-Openurl = " + url
        if cookie and not cookiejar:
            import cookielib

            cookie_file = join(join(datapath, 'Cookies'), cookie + '.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try:
                    cj.load(cookie_file, ignore_discard)
                    for c in setCookie:
                        cj.set_cookie(c)
                except:
                    cj.save(cookie_file, True)
            else:
                cj.save(cookie_file, True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        elif cookiejar:
            import cookielib

            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        if mobile:
            opener.addheaders = [('User-Agent',
                                  'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')]
        else:
            opener.addheaders = [('User-Agent', UserAgent)]
        for header in headers:
            opener.addheaders.append(header)
        if data:
            if type == 'json':
                import json

                data = json.dumps(data)
                opener.addheaders.append(('Content-Type', 'application/json'))
            else:
                data = urllib.urlencode(data)
        response = opener.open(url, data, timeout)
        if cookie and not cookiejar:
            cj.save(cookie_file, ignore_discard)
        opener.close()
        link = response.read()
        response.close()
        # link = net(UserAgent).http_GET(url).content
        link = link.replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', "&").replace("&#39;", "'").replace(
            '&lt;i&gt;', '').replace("#8211;", "-").replace('&lt;/i&gt;', '').replace("&#8217;", "'").replace(
            '&amp;quot;', '"').replace('&#215;', 'x').replace('&#038;', '&').replace('&#8216;', '').replace('&#8211;',
                                                                                                            '').replace(
            '&#8220;', '').replace('&#8221;', '').replace('&#8212;', '')
        link = link.replace('%3A', ':').replace('%2F', '/')
        if q: q.put(link)
        return link
    except Exception as e:
        if raiseErrors: raise
        if verbose:
            from urlparse import urlparse

            host = urlparse(url).hostname.replace('www.', '').partition('.')[0]
            xbmc.executebuiltin("XBMC.Notification(Sorry!," + host.title() + " Website is Down,3000," + icon + ")")
        xbmc.log('***********Website Error: ' + str(e) + '**************', xbmc.LOGERROR)
        xbmc.log('***********Url: ' + url + ' **************', xbmc.LOGERROR)
        import traceback

        traceback.print_exc()
        link = 'website down'
        if q: q.put(link)
        return link


def setFile(path, content, force=False):
    if os.path.exists(path) and not force:
        return False
    else:
        try:
            open(path, 'w+').write(content)
            return True
        except:
            pass
    return False


def getNewCookie():
    user = selfAddon.getSetting('skyusername')
    passw = selfAddon.getSetting('skypassword')
    data = {'username': user, 'password': passw}
    data = urllib.urlencode(data)
    opener = urllib2.build_opener()
    response = opener.open(loginUrl, data, defaultTimeout)
    jsonRaw = response.read()
    opener.close()
    response.close()
    if jsonRaw:
        jsonObject = json.loads(jsonRaw)
        if jsonObject.has_key("error"):
            loginPopup("Error - "+jsonObject["error"])
        else:
            return jsonObject

def loginPopup(message=None):
    dialog = xbmcgui.Dialog()
    additional = 'or register if you don have an account at sportsaccess.se'
    if message:
        additional = message
    ret = dialog.yesno('[COLOR red]SportsAccess[/COLOR]', 'Please set your SportsAccess credentials',
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
                selfAddon.setSetting('skyusername', username)
                selfAddon.setSetting('skypassword', password)
                getNewCookie()
    else:
        quit()

if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try:
            os.remove(cookie_file)
        except:
            pass
    loginPopup()

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x":
            return unichr(int(text[3:-1], 16)).encode('utf-8')
        else:
            return unichr(int(text[2:-1])).encode('utf-8')

    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))


def MAINSA():
    getNewCookie()
    setDefaultDay = False
    UpdateConfig()
    requestUrl = scheduleUrl+"?js=0"
    requestUrl = requestUrl + "&timezone="+scheduleConfig['scheduleTimezoneValue']
    if scheduleConfig['scheduleCategory'] != 'All':
        requestUrl = requestUrl + "&cat="+scheduleConfig['scheduleCategory']
    if scheduleConfig['scheduleTimestamp'] != 0:
        requestUrl = requestUrl + "&day="+scheduleConfig['scheduleTimestamp']
    else:
        setDefaultDay = True
    requestUrl = requestUrl.replace(" ","%20")
    xbmc.log(str(scheduleConfig['scheduleTimestamp']))
    xbmc.log(requestUrl)
    scheduleHtml = htmlNoCookies(requestUrl)
    scheduleHtml = cleanHex(scheduleHtml)
    if setDefaultDay:
        match = re.compile('data-day="([^"]+)">Today').findall(scheduleHtml)
        timestamp = match[0]
        scheduleConfig['scheduleTimestamp'] = timestamp
    addDir('[COLOR red]Server:[/COLOR] '+playConfig['defaultServerName']+" (Click Here)", 'url', 563, artpath + 'empty.png')
    addLink2('[I][COLOR red]Refresh Links[/COLOR][/I]  (Click Here if Vidoes are not playing)', 'url', 555,
             artpath + 'empty.png', fanart)
    addDir('[COLOR orange]All Channels[/COLOR] (Click Here)', 'test', 477, artpath + 'empty.png')
    addDir('[COLOR red]Date:[/COLOR] '+sfunctions.timestampToDate(scheduleConfig['scheduleTimestamp'])+ " (Click to change)", 'f', 561, artpath + 'empty.png')
    addDir('[COLOR red]Category:[/COLOR] '+scheduleConfig['scheduleCategory']+' (Click Here)', 'f', 557, artpath + 'empty.png')
    addDir('[COLOR red]Timezone:[/COLOR] '+scheduleConfig['scheduleTimezoneName']+' (Click Here)', 'f', 559, artpath + 'empty.png')
    addLink2('[B][COLOR blue]Open EPG[/COLOR][/B] (Click Here)', 'url', 999, icon, fanart)
    listHtml = scheduleHtml.split('id="schedule"')[1]
    listHtml = listHtml.split('</ul>')[0]
    listHtml = listHtml.split('<ul>')[1]
    listItems = re.compile('<li.+?>\n*(.*\n*.*\n*.*\n*.*\n*.*\n*.*)</li>').findall(listHtml)
    for line in listItems:
        line = line.strip()
        itemParts = re.compile('.* (.*) \|.*\n*.*<i>#(.+)</i>.*\n*.*\|.*\n*(.+)').findall(line)
        for time, ch, name in itemParts:
            name = re.sub('[\t+]', '', name)
            name = re.sub('<img.*>', '', name)
            name = name.replace("&amp;","&")
            ch = str(ch)
            if scheduleConfig['scheduleCategory'] == 'PPV':
                addDir(time+" "+name + ' [COLOR orange]Channel:' + ch + '[/COLOR]', ch, 411,
                   'http://sportsaccess.se/images/' + ch + '.png')
            else:
                addLink2(time+" "+name + ' [COLOR orange]Channel:' + ch + '[/COLOR]', ch, 565,
                         'http://sportsaccess.se/images/' + ch + '.png',fanart)
    addLink('', '', '')
    addLink2('[COLOR grey][I]For support vist sportsaccess.net and submit a ticket [/I][/COLOR]', 'url', '',
             artpath + 'empty.png', fanart)


def FullChannel(murls):
    json = getNewCookie()
    keys = list(json["channel_list"].keys())
    keys.sort(key=int)
    for ch in keys:
        addLink2('Channel ' + str(ch), ch, 565,
                 'http://sportsaccess.se/images/' + ch + '.png',fanart)



def Set(id=AddonID):
    xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)


def Fresh():
    xbmc.executebuiltin("XBMC.Container.Refresh")


def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(500)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass


def clearCookies():
    dialog = xbmcgui.Dialog()
    if dialog.yesno('Mash Up', 'Are you sure you want to clear Cookies?', '', '', 'No', 'Yes'):
        import os

        cookie_file = join(datapath, 'Cookies')
        ClearDir(xbmc.translatePath(cookie_file), True)
        xbmc.executebuiltin("XBMC.Notification(Clear Cookies,Successful,5000,"")")


def ClearDir(dir, clearNested=False):
    for the_file in os.listdir(dir):
        file_path = join(dir, the_file)
        if clearNested and os.path.isdir(file_path):
            ClearDir(file_path, clearNested)
            try:
                os.rmdir(file_path)
            except Exception, e:
                print str(e)
        else:
            try:
                os.unlink(file_path)
            except Exception, e:
                print str(e)


def PlayStream(url, iconimage):
    playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
    ok = True
    xbmc.Player().play(playback_url)


def Login():
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR red]Free Member Fix[/COLOR]', '- Open Addon Settings, set to Defauls, Then press OK',
              '- Click Login, Re-Enter credentials and Log In',
              "- If you're still shown as a free member, open a support ticket on sportsaccess.net")

def LISTCONTENT(murl, thumb):
    json = getNewCookie()
    if json:
        for server in json["server_list"]:
            server = json["server_list"][server]
            name = server["name"]
            host = server["host"]
            port = server["port"]
            addLink2(name, murl+"|"+host+"|"+port+"|"+name, 564, '',fanart)

def PLAYLINK(mname, murl, thumb):
    ok = True
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    listitem = xbmcgui.ListItem(mname, thumbnailImage=thumb)
    playlist.add(murl, listitem)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist)
    return ok


def addPlay(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage='', thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('fanart_image', art + "fanart.jpg")
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addLink2(name, url, mode, iconimage, fanart, description=''):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addLink(name, url, iconimage):
    liz = xbmcgui.ListItem(name, iconImage=art + '/empty.png', thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('fanart_image', art + "fanart.jpg")
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)


def addDir2(name, url, mode, iconimage, fanart, description=''):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&description=" + str(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addDir(name, url, mode, iconimage):
    u = sys.argv[0]

    u += "?url=" + urllib.quote_plus(url)
    u += "&mode=" + str(mode)
    u += "&name=" + urllib.quote_plus(name)
    u += "&iconimage=" + urllib.quote_plus(iconimage)

    liz = xbmcgui.ListItem(name, iconImage='', thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('fanart_image', art + "fanart.jpg")

    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param
# -------------------------------- New functions ----------------------------------------------------------------------


def htmlNoCookies(url):
    opener = urllib2.build_opener()
    response = opener.open(url, "", defaultTimeout)
    raw = response.read()
    opener.close()
    response.close()
    return raw

def ChangeCategories():
    html = OPENURL(scheduleUrl, cookie='sportsaccess')
    html = cleanHex(html)
    partial = html.split('<select id="list_cat">')[1]
    partial = partial.split('</select>')[0]
    matchlist = re.compile('value="([^"]+)">([^"]+)</').findall(partial)
    addLink2("All", 'All', 558, '',fanart)
    for input, name in matchlist:
        addLink2(name, name, 558, '',fanart)

def SetCategory(url):
    scheduleConfig['scheduleCategory'] = url
    # Need to persist to sustain it
    selfAddon.setSetting('scheduleCategory', url)
    xbmc.executebuiltin("Action(Back)")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def ChangeTimezone():
    html = OPENURL(scheduleUrl, cookie='sportsaccess')
    html = cleanHex(html)
    partial = html.split('id="timezone">')[1]
    partial = partial.split('</select>')[0]
    matchlist = re.compile('value="([^"]+)".*>([^"]+)</').findall(partial)
    for value, name in matchlist:
        addLink2(name, value+"|"+name, 560, '',fanart)

def SetTimezone(url):
    parts = url.split("|")
    scheduleConfig['scheduleTimezoneValue'] = parts[0]
    scheduleConfig['scheduleTimezoneName'] = parts[1]
    # Need to persist to sustain it
    selfAddon.setSetting('scheduleTimezoneValue', parts[0])
    selfAddon.setSetting('scheduleTimezoneName', parts[1])
    xbmc.executebuiltin("Action(Back)")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def ChangeDate():
    html = OPENURL(scheduleUrl, cookie='sportsaccess')
    html = cleanHex(html)
    partial = html.split('id="days"')[1]
    partial = partial.split('</div>')[0]
    matchlist = re.compile('data-day="([^"]+)".?>([^"]+)</li').findall(partial)
    for input, name in matchlist:
        addLink2(name, input+"|"+name, 562, '',fanart)

def SetDate(url):
    parts = url.split("|")
    scheduleConfig['scheduleTimestamp'] = parts[0]
    # Need to persist to sustain it
    selfAddon.setSetting('scheduleTimestamp', parts[0])
    xbmc.executebuiltin("Action(Back)")
    xbmc.executebuiltin("XBMC.Container.Refresh")


def ChangeServer(url):
    json = getNewCookie()
    if json:
        for server in json["server_list"]:
            server = json["server_list"][server]
            name = server["name"]
            host = server["host"]
            port = server["port"]
            addLink2(name, name+"|"+host+"|"+port, 564, '',fanart)

def SetServer(url):
    parts = url.split("|")
    name = parts[0]
    host = parts[1]
    port = parts[2]
    playConfig['defaultServerHost'] = host
    playConfig['defaultServerPort'] = port
    playConfig['defaultServerName'] = name
    # Need to persist to sustain it
    selfAddon.setSetting('defaultServerHost', host)
    selfAddon.setSetting('defaultServerPort', port)
    selfAddon.setSetting('defaultServerName', name)
    xbmc.executebuiltin("Action(Back)")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def UpdateConfig():
    if selfAddon.getSetting("scheduleCategory"):
        scheduleConfig['scheduleCategory'] = selfAddon.getSetting("scheduleCategory")
    if selfAddon.getSetting("scheduleTimezoneValue"):
        scheduleConfig['scheduleTimezoneValue'] = selfAddon.getSetting("scheduleTimezoneValue")
    if selfAddon.getSetting("scheduleTimezoneName"):
        scheduleConfig['scheduleTimezoneName'] = selfAddon.getSetting("scheduleTimezoneName")
    if selfAddon.getSetting("scheduleTimestamp"):
        scheduleConfig['scheduleTimestamp'] = selfAddon.getSetting("scheduleTimestamp")
        floatvar = float(scheduleConfig['scheduleTimestamp'])
        if floatvar < time.time():
            scheduleConfig['scheduleTimestamp'] = 0
            selfAddon.setSetting("scheduleTimestamp", '0')
    if selfAddon.getSetting("defaultServer"):
        playConfig['defaultServer'] = selfAddon.getSetting("defaultServer")
    if selfAddon.getSetting("defaultServerName"):
        playConfig['defaultServerName'] = selfAddon.getSetting("defaultServerName")


def PlayChannel(chNumber, thumb):
    json = getNewCookie()
    host = selfAddon.getSetting('defaultServerHost')
    port = selfAddon.getSetting('defaultServerPort')
    chList = json["channel_list"][str(int(chNumber))]
    chPad = '{0:02d}'.format(int(chNumber))
    playLink = "http://"+host+":"+port+"/"+chList+"/ch"+chPad+"q1/playlist.m3u8?wmsAuthSign="+json["hash"]
    PLAYLINK("CH - "+chNumber+" - "+selfAddon.getSetting("skyusername")+" - "+selfAddon.getSetting('defaultServerName'),playLink,thumb)

def PlayChannelCustom(murl, thumb):
    json = getNewCookie()
    data = murl.split("|")
    ch = data[0]
    host = data[1]
    port = data[2]
    sname = data[2]
    chList = json["channel_list"][str(int(ch))]
    chPad = '{0:02d}'.format(int(ch))
    playLink = "http://"+host+":"+port+"/"+chList+"/ch"+chPad+"q1/playlist.m3u8?wmsAuthSign="+json["hash"]
    PLAYLINK("CH - "+ch+" - "+selfAddon.getSetting("skyusername")+" - "+sname,playLink,thumb)

params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ', '%20')
except:
    pass

print "Mode: " + str(mode)
print "Name: " + str(name)
print "Thumb: " + str(iconimage)

if mode == None or url == None or len(url) < 1:

    MAINSA()


elif mode == 411:
    LISTCONTENT(url, iconimage)
elif mode == 413:
    PLAYLINK(name, url, iconimage)
elif mode == 477:
    FullChannel(url)
elif mode == 456:
    PlayStream(url, iconimage)
elif mode == 358:
    clearCookies()
elif mode == 259:
    Login()
elif mode == 239:
    Set()
elif mode == 555:
    Fresh()
elif mode == 557:
    ChangeCategories()
elif mode == 558:
    SetCategory(url)
elif mode == 559:
    ChangeTimezone()
elif mode == 560:
    SetTimezone(url)
elif mode == 561:
    ChangeDate()
elif mode == 562:
    SetDate(url)
elif mode == 563:
    ChangeServer(url)
elif mode == 564:
    SetServer(url)
elif mode == 565:
    PlayChannel(url, iconimage)
elif mode == 566:
    PlayChannelCustom(url, iconimage)
elif mode == 999:
    epg_path = xbmc.translatePath(
        join('special://home', 'addons', 'plugin.video.sportsaccess', 'addon.py'))
    xbmc.executebuiltin("RunScript(" + epg_path + ")")
elif mode == 240:
    if selfAddon.getSetting("server-location") == "true":
        selfAddon.setSetting('server-location', 'false')
        print 'false'
    else:
        selfAddon.setSetting('server-location', 'true')
        print 'true'
    xbmc.executebuiltin("XBMC.Container.Refresh")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
