# -*- coding: utf-8 -*-
#
#      Copyright (C) 2017 SportsAccess.se
#
import ConfigParser
import json
import os
import urllib2
import xml . etree . ElementTree as Et
import datetime as d_t
from operator import itemgetter
import pytz
import xbmc
import time
import xbmcgui
from strings import ADDON
if 64 - 64: i11iIiiIii
OO0o = 'Default'
Oo0Ooo = 1
O0O0OO0O0O0 = 2
iiiii = 3
ooo0OO = 4
II1 = 9
O00ooooo00 = 92
if 32 - 32: ooOoO + iIiiiI1IiI1I1 * IIiIiII11i * o0oOOo0O0Ooo
if 2 - 2: o0 * i1 * ii1IiI1i % OOooOOo / I11i / Ii1I
class Scoreboard (xbmcgui . WindowXMLDialog) :
 C_CANCEL_BUTTON = 6004
 C_REFRESH_BUTTON = 6005
 C_BUTTON_MLB = 4000
 C_BUTTON_NBA = 4001
 C_BUTTON_NFL = 4002
 C_BUTTON_NHL = 4003
 C_BUTTON_EPL = 4004
 C_LABEL_NONE = 7000
 C_LABEL_LOAD = 7500
 if 34 - 34: iii1I1I / O00oOoOoO0o0O . O0oo0OO0 + Oo0ooO0oo0oO . I1i1iI1i - II
 time_zone = 'US/Eastern'
 url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.js.asp?jsonp=true&sport=%s&period=%d'
 if 100 - 100: i11Ii11I1Ii1i . ooO - OOoO / II * OOooOOo . o0
 def __new__ ( cls , database ) :
  return super (Scoreboard, cls) . __new__ (cls, 'script-tvguide-scoreboard.xml', ADDON . getAddonInfo ('path'), OO0o)
  if 1 - 1: o0 - iii1I1I % i11iIiiIii + i11Ii11I1Ii1i . ooO
 def __init__ ( self , database ) :
  super (Scoreboard, self) . __init__ ()
  if 55 - 55: iIiiiI1IiI1I1 - i1 . I1i1iI1i * i11Ii11I1Ii1i * o0oOOo0O0Ooo / iIiiiI1IiI1I1
  if 79 - 79: O00oOoOoO0o0O + ooO . OOoO * i11Ii11I1Ii1i % Oo0ooO0oo0oO . i1
  if 94 - 94: II * I1i1iI1i / i11Ii11I1Ii1i . o0oOOo0O0Ooo * II
  self . database = database
  self . selected_program = None
  self . is_future = False
  self . top_list = [ ]
  self . right_list = [ ]
  self . left_list = [ ]
  self . bottom_list = [ ]
  self . score_list = list ( )
  self . label_list = list ( )
  self . game_list = list ( )
  self . league = ''
  iiiii11iII1 = os . path . join ( xbmc . translatePath ( ADDON . getAddonInfo ( 'profile' ) ) , "5" )
  if os . path . isfile ( iiiii11iII1 ) :
   self . team_map = ConfigParser . ConfigParser ( )
   self . team_map . read ( iiiii11iII1 )
  else :
   self . team_map = None
   xbmc . log ( '[%s] Team-Map not found' % ADDON . getAddonInfo ( 'id' ) , xbmc . LOGERROR )
   if 54 - 54: OOoO . OOoO / iIiiiI1IiI1I1 / Oo0ooO0oo0oO + O00oOoOoO0o0O / Ii1I
 def onInit ( self ) :
  for I1i1I in range ( 4010 , 4015 ) :
   OOoOoo00oo = self . getControl ( I1i1I )
   OOoOoo00oo . setVisible ( False )
  self . setFocusId ( self . C_BUTTON_MLB )
  if 41 - 41: iIiiiI1IiI1I1 / ooO + O0oo0OO0
 def build_score_grid ( self ) :
  self . getControl ( self . C_LABEL_NONE ) . setVisible ( False )
  if len ( self . score_list ) > 0 :
   self . removeControls ( self . score_list )
   self . removeControls ( self . label_list )
   self . score_list = list ( )
   self . game_list = list ( )
   self . label_list = list ( )
   if 91 - 91: Ii1I / o0 . iii1I1I + O0oo0OO0
  self . getControl ( self . C_LABEL_LOAD ) . setVisible ( True )
  self . _add_scores ( )
  self . getControl ( self . C_LABEL_LOAD ) . setVisible ( False )
  if 47 - 47: I11i / I1i1iI1i * IIiIiII11i
  if len ( self . score_list ) == 0 :
   self . getControl ( self . C_LABEL_NONE ) . setVisible ( True )
  else :
   self . addControls ( self . score_list )
   self . addControls ( self . label_list )
  self . _update_bounds ( )
  if 9 - 9: i1 - I1i1iI1i % o0oOOo0O0Ooo % IIiIiII11i
 def _add_scores ( self ) :
  i1iIIi1 = self . query_data ( )
  if 50 - 50: i11iIiiIii - I1i1iI1i
  oo0Ooo0 = 0
  for I1i1I in range ( 160 , 640 , 80 ) :
   for I1I11I1I1I in range ( 150 , 1150 , 250 ) :
    if oo0Ooo0 < len ( i1iIIi1 ) :
     OooO0OO = i1iIIi1 [ oo0Ooo0 ]
     if self . league == OooO0OO [ 'league' ] :
      if OooO0OO [ 'status' ] == 'Pre-Game' :
       iiiIi = OooO0OO [ 'start' ]
       IiIIIiI1I1 = ''
      elif OooO0OO [ 'status' ] == 'Final' :
       iiiIi = OooO0OO [ 'clock' ]
       IiIIIiI1I1 = ''
      else :
       iiiIi = OooO0OO [ 'clock' ]
       IiIIIiI1I1 = OooO0OO [ 'clock-section' ]
       if 86 - 86: i11iIiiIii + I1i1iI1i + OOoO * Oo0ooO0oo0oO + Ii1I
       if 61 - 61: OOooOOo / i11iIiiIii
      OOoOoo00oo = xbmcgui . ControlButton (
 I1I11I1I1I ,
 I1i1I ,
 240 ,
 70 ,
 '' ,
 noFocusTexture = 'tvguide-program-grey.png' ,
 focusTexture = 'tvguide-program-grey-focus.png'
 )
      self . score_list . append ( OOoOoo00oo )
      self . game_list . append ( OooO0OO )
      if 34 - 34: IIiIiII11i + iIiiiI1IiI1I1 + i11iIiiIii - iii1I1I + i11iIiiIii
      if 65 - 65: I11i
      if 6 - 6: i1 / ii1IiI1i % I1i1iI1i
      if 84 - 84: i11iIiiIii . Ii1I
      self . label_list . append ( xbmcgui . ControlLabel (
 I1I11I1I1I + 10 , I1i1I + 5 , 80 , 25 , "[B]%s[/B]" % OooO0OO [ 'away-alias' ]
 ) )
      self . label_list . append ( xbmcgui . ControlLabel (
 I1I11I1I1I + 90 , I1i1I + 5 , 50 , 25 , OooO0OO [ 'away-score' ]
 ) )
      self . label_list . append ( xbmcgui . ControlLabel (
 I1I11I1I1I + 140 , I1i1I + 5 , 90 , 25 , iiiIi
 ) )
      if 100 - 100: I1i1iI1i - I1i1iI1i - ooO
      if 20 - 20: IIiIiII11i
      self . label_list . append ( xbmcgui . ControlLabel (
 I1I11I1I1I + 10 , I1i1I + 35 , 80 , 25 , "[B]%s[/B]" % OooO0OO [ 'home-alias' ]
 ) )
      self . label_list . append ( xbmcgui . ControlLabel (
 I1I11I1I1I + 90 , I1i1I + 35 , 50 , 25 , OooO0OO [ 'home-score' ]
 ) )
      self . label_list . append ( xbmcgui . ControlLabel (
 I1I11I1I1I + 140 , I1i1I + 35 , 90 , 25 , IiIIIiI1I1
 ) )
      if 13 - 13: o0oOOo0O0Ooo - I1i1iI1i % O00oOoOoO0o0O / iIiiiI1IiI1I1 % II
     oo0Ooo0 += 1
    else :
     return
     if 97 - 97: i11iIiiIii
 def _update_bounds ( self ) :
  II1i1Ii11Ii11 = len ( self . score_list )
  if II1i1Ii11Ii11 <= 4 :
   self . top_list = range ( 0 , II1i1Ii11Ii11 )
   self . bottom_list = range ( 0 , II1i1Ii11Ii11 )
   self . left_list = [ 0 ]
   self . right_list = [ II1i1Ii11Ii11 - 1 ]
  else :
   self . top_list = [ 0 , 1 , 2 , 3 ]
   if II1i1Ii11Ii11 <= 8 :
    self . bottom_list = range ( 4 , II1i1Ii11Ii11 )
    self . left_list = [ 0 , 4 ]
    self . right_list = [ 3 , II1i1Ii11Ii11 - 1 ]
   elif II1i1Ii11Ii11 <= 12 :
    self . bottom_list = range ( 8 , II1i1Ii11Ii11 )
    self . left_list = [ 0 , 4 , 8 ]
    self . right_list = [ 3 , 7 , II1i1Ii11Ii11 - 1 ]
   elif II1i1Ii11Ii11 <= 16 :
    self . bottom_list = range ( 12 , II1i1Ii11Ii11 )
    self . left_list = [ 0 , 4 , 8 , 12 ]
    self . right_list = [ 3 , 7 , 11 , II1i1Ii11Ii11 - 1 ]
   elif II1i1Ii11Ii11 <= 20 :
    self . bottom_list = range ( 16 , II1i1Ii11Ii11 )
    self . left_list = [ 0 , 4 , 8 , 12 , 16 ]
    self . right_list = [ 3 , 7 , 11 , 15 , II1i1Ii11Ii11 - 1 ]
   elif II1i1Ii11Ii11 <= 24 :
    self . bottom_list = range ( 20 , II1i1Ii11Ii11 )
    self . left_list = [ 0 , 4 , 8 , 12 , 16 , 20 ]
    self . right_list = [ 3 , 7 , 11 , 15 , 19 , II1i1Ii11Ii11 - 1 ]
   else :
    self . right_list = [ 3 , 7 , 11 , 15 , 19 , 23 ]
    self . left_list = [ 0 , 4 , 8 , 12 , 16 , 20 ]
    self . bottom_list = [ 20 , 21 , 22 , 23 ]
    if 35 - 35: Ii1I + II + II
 def get_control_for_current_league ( self ) :
  I11I11i1I = None
  if self . league == 'MLB' :
   I11I11i1I = self . C_BUTTON_MLB
  elif self . league == 'NBA' :
   I11I11i1I = self . C_BUTTON_NBA
  elif self . league == 'NFL' :
   I11I11i1I = self . C_BUTTON_NFL
  elif self . league == 'NHL' :
   I11I11i1I = self . C_BUTTON_NHL
  elif self . league == 'EPL' :
   I11I11i1I = self . C_BUTTON_EPL
  return self . getControl ( I11I11i1I )
  if 49 - 49: o0 % II * ooOoO
 def onFocus ( self , control_id ) :
  if control_id == self . C_BUTTON_MLB and self . league != 'MLB' :
   self . league = 'MLB'
   self . build_score_grid ( )
  elif control_id == self . C_BUTTON_NBA and self . league != 'NBA' :
   self . league = 'NBA'
   self . build_score_grid ( )
  elif control_id == self . C_BUTTON_NHL and self . league != 'NHL' :
   self . league = 'NHL'
   self . build_score_grid ( )
  elif control_id == self . C_BUTTON_NFL and self . league != 'NFL' :
   self . league = 'NFL'
   self . build_score_grid ( )
  elif control_id == self . C_BUTTON_EPL and self . league != 'EPL' :
   self . league = 'EPL'
   self . build_score_grid ( )
   if 89 - 89: O00oOoOoO0o0O + ii1IiI1i
 def onAction ( self , action ) :
  if action . getId ( ) in [ II1 , O00ooooo00 ] :
   self . close ( )
   return
   if 3 - 3: o0oOOo0O0Ooo / i1 % Oo0ooO0oo0oO * i11iIiiIii / ooOoO * Oo0ooO0oo0oO
  III1ii1iII = self . getFocus ( )
  if action . getId ( ) == Oo0Ooo :
   self . _left ( III1ii1iII )
  elif action . getId ( ) == O0O0OO0O0O0 :
   self . _right ( III1ii1iII )
  elif action . getId ( ) == iiiii :
   self . _up ( III1ii1iII )
  elif action . getId ( ) == ooo0OO :
   self . _down ( III1ii1iII )
   if 54 - 54: i1 % o0 % o0
 def onClick ( self , control_id ) :
  if control_id == self . C_CANCEL_BUTTON :
   self . close ( )
  elif control_id == self . C_REFRESH_BUTTON :
   self . build_score_grid ( )
   if 13 - 13: Ii1I . I1i1iI1i
  OooO0OO = self . _get_game_from_control ( self . getControl ( control_id ) )
  if OooO0OO is None :
   return
   if 19 - 19: Oo0ooO0oo0oO + OOoO
  ooo = self . database . search ( [ self . league , OooO0OO [ 'away-guide' ] , OooO0OO [ 'home-guide' ] ] , 2 )
  if len ( ooo [ 'ended' ] ) == 0 and len ( ooo [ 'now' ] ) == 0 and len ( ooo [ 'future' ] ) == 0 :
   xbmcgui . Dialog ( ) . ok ( 'Program not available' , 'We don\'t seem to have a stream for this game today.' )
  elif len ( ooo [ 'now' ] ) > 0 :
   ii1I1i1I = list ( )
   for OOoo0O0 in ooo [ 'now' ] :
    ii1I1i1I . append ( '[B]%3d:[/B] %s' % ( int ( OOoo0O0 . channel . id ) , self . format_title ( OOoo0O0 ) ) )
   iiiIi1i1I = xbmcgui . Dialog ( ) . select ( 'Watch Program' , ii1I1i1I )
   if iiiIi1i1I >= 0 :
    self . selected_program = ooo [ 'now' ] [ iiiIi1i1I ]
    self . close ( )
    return
  elif len ( ooo [ 'ended' ] ) > 0 :
   ii1I1i1I = list ( )
   for OOoo0O0 in ooo [ 'ended' ] :
    ii1I1i1I . append ( '[B]%3d:[/B] %s' % ( int ( OOoo0O0 . channel . id ) , self . format_title ( OOoo0O0 ) ) )
   iiiIi1i1I = xbmcgui . Dialog ( ) . select ( 'Recently Ended' , ii1I1i1I )
   if iiiIi1i1I >= 0 :
    self . selected_program = ooo [ 'ended' ] [ iiiIi1i1I ]
    self . close ( )
    return
  elif len ( ooo [ 'future' ] ) > 0 :
   ii1I1i1I = list ( )
   for OOoo0O0 in ooo [ 'future' ] :
    ii1I1i1I . append ( '[B]%3d:[/B] %s' % ( int ( OOoo0O0 . channel . id ) , self . format_title ( OOoo0O0 ) ) )
   iiiIi1i1I = xbmcgui . Dialog ( ) . select ( 'Set Reminder' , ii1I1i1I )
   if iiiIi1i1I >= 0 :
    self . selected_program = ooo [ 'future' ] [ iiiIi1i1I ]
    self . is_future = True
    self . close ( )
    return
    if 80 - 80: I11i - OOooOOo
 @ staticmethod
 def format_title ( program ) :
  OOO00 = program . title
  if '(' in OOO00 :
   OOO00 = OOO00 [ : OOO00 . find ( '(' ) ]
  return OOO00
  if 21 - 21: IIiIiII11i - IIiIiII11i
 def _get_game_from_control ( self , control ) :
  oo0Ooo0 = 0
  for iIii11I in self . score_list :
   if iIii11I == control :
    OooO0OO = self . game_list [ oo0Ooo0 ]
    return OooO0OO
   oo0Ooo0 += 1
  return None
  if 69 - 69: O00oOoOoO0o0O % ooO - Ii1I + ooO - ooOoO % IIiIiII11i
 def getControl ( self , control_id ) :
  try :
   return super (Scoreboard, self) . getControl (control_id)
  except :
   return None
   if 31 - 31: o0 - O0oo0OO0 . ooO % I11i - ooOoO
 def _left ( self , control_in_focus ) :
  for I1i1I , OOoOoo00oo in enumerate ( self . score_list ) :
   if OOoOoo00oo == control_in_focus :
    if I1i1I in self . left_list :
     oo0Ooo0 = self . left_list . index ( I1i1I )
     iii11 = self . score_list [ self . right_list [ oo0Ooo0 ] ]
    else :
     iii11 = self . score_list [ I1i1I - 1 ]
     if 58 - 58: O0oo0OO0 * i11iIiiIii / I11i % ooO - iii1I1I / O00oOoOoO0o0O
    self . setFocus ( iii11 )
    break
    if 50 - 50: i1
 def _right ( self , control_in_focus ) :
  for I1i1I , OOoOoo00oo in enumerate ( self . score_list ) :
   if OOoOoo00oo == control_in_focus :
    if I1i1I in self . right_list :
     oo0Ooo0 = self . right_list . index ( I1i1I )
     iii11 = self . score_list [ self . left_list [ oo0Ooo0 ] ]
    else :
     iii11 = self . score_list [ I1i1I + 1 ]
     if 34 - 34: i1 * o0 % II * I11i - i1
    self . setFocus ( iii11 )
    break
    if 33 - 33: Ii1I + O0oo0OO0 * OOooOOo - ii1IiI1i / O00oOoOoO0o0O % I1i1iI1i
 def _up ( self , control_in_focus ) :
  if control_in_focus . getId ( ) in [ self . C_BUTTON_NHL , self . C_BUTTON_NFL , self . C_BUTTON_NBA , self . C_BUTTON_MLB ,
 self . C_BUTTON_EPL ] :
   self . setFocus ( self . getControl ( self . C_REFRESH_BUTTON ) )
   self . _update_visibility ( False )
  elif control_in_focus . getId ( ) in [ self . C_REFRESH_BUTTON , self . C_CANCEL_BUTTON ] :
   if len ( self . score_list ) > 0 :
    self . setFocus ( self . score_list [ self . bottom_list [ 0 ] ] )
   else :
    self . _update_visibility ( True )
    self . setFocus ( self . get_control_for_current_league ( ) )
  else :
   for I1i1I , OOoOoo00oo in reversed ( list ( enumerate ( self . score_list ) ) ) :
    if OOoOoo00oo == control_in_focus :
     if I1i1I in self . top_list :
      iii11 = self . get_control_for_current_league ( )
      self . _update_visibility ( True )
     else :
      iii11 = self . score_list [ I1i1I - 4 ]
      if 21 - 21: OOooOOo * iIiiiI1IiI1I1 % O00oOoOoO0o0O * o0oOOo0O0Ooo
     self . setFocus ( iii11 )
     break
     if 16 - 16: ooOoO - ooO * iIiiiI1IiI1I1 + II
 def _down ( self , control_in_focus ) :
  if control_in_focus . getId ( ) in [ self . C_REFRESH_BUTTON , self . C_CANCEL_BUTTON ] :
   self . _update_visibility ( True )
   self . setFocus ( self . get_control_for_current_league ( ) )
  elif control_in_focus . getId ( ) in [ self . C_BUTTON_MLB , self . C_BUTTON_NBA , self . C_BUTTON_NFL , self . C_BUTTON_NHL ,
 self . C_BUTTON_EPL ] :
   if len ( self . score_list ) > 0 :
    self . setFocus ( self . score_list [ 0 ] )
   else :
    self . setFocus ( self . getControl ( self . C_REFRESH_BUTTON ) )
   self . _update_visibility ( False )
  else :
   for I1i1I , OOoOoo00oo in enumerate ( self . score_list ) :
    if OOoOoo00oo == control_in_focus :
     oo0Ooo0 = I1i1I + 4
     if I1i1I in self . bottom_list or oo0Ooo0 >= len ( self . score_list ) :
      iii11 = self . getControl ( self . C_REFRESH_BUTTON )
     else :
      iii11 = self . score_list [ oo0Ooo0 ]
      if 50 - 50: o0 - OOoO * iii1I1I / ooO + Ii1I
     self . setFocus ( iii11 )
     break
     if 88 - 88: I1i1iI1i / ooO + II - o0 / OOoO - I11i
 def _update_visibility ( self , show ) :
  OOoOoo00oo = self . get_control_for_current_league ( )
  IIIIii = self . getControl ( OOoOoo00oo . getId ( ) + 10 )
  if show :
   IIIIii . setVisible ( False )
   OOoOoo00oo . setVisible ( True )
  else :
   time . sleep ( 0.1 )
   OOoOoo00oo . setVisible ( False )
   IIIIii . setVisible ( True )
   if 70 - 70: I1i1iI1i / Oo0ooO0oo0oO . II % ii1IiI1i
 def query_data ( self ) :
  OOoOO00OOO0OO = d_t . datetime . now ( pytz . timezone ( self . time_zone ) )
  iI1I111Ii111i = int ( OOoOO00OOO0OO . strftime ( "%Y%m%d" ) )
  I11IiI1I11i1i = int ( OOoOO00OOO0OO . strftime ( "%H%M" ) )
  if I11IiI1I11i1i < 400 :
   if 38 - 38: Ii1I
   iI1I111Ii111i = int ( ( OOoOO00OOO0OO - d_t . timedelta ( days = 1 ) ) . strftime ( "%Y%m%d" ) )
   if 57 - 57: ooOoO / O00oOoOoO0o0O * ooO / I11i . o0
  i1iIIi1 = { 'in' : [ ] , 'pre' : [ ] , 'end' : [ ] }
  i11iIIIIIi1 = self . league
  try :
   iiII1i1 = urllib2 . urlopen ( self . url % ( i11iIIIIIi1 , iI1I111Ii111i ) )
   o00oOO0o = iiII1i1 . read ( )
   iiII1i1 . close ( )
   OOO00O = o00oOO0o . replace ( 'shsMSNBCTicker.loadGamesData(' , '' ) . replace ( ');' , '' )
   OOoOO0oo0ooO = json . loads ( OOO00O )
   for O0o0O00Oo0o0 in OOoOO0oo0ooO . get ( 'games' , [ ] ) :
    O00O0oOO00O00 = Et . XML ( O0o0O00Oo0o0 )
    if 11 - 11: i11Ii11I1Ii1i . iii1I1I
    if i11iIIIIIi1 == 'EPL' :
     o0oo0oOo = O00O0oOO00O00 . find ( 'home-team' )
     o000O0o = O00O0oOO00O00 . find ( 'visiting-team' )
    else :
     o0oo0oOo = O00O0oOO00O00 . find ( 'visiting-team' )
     o000O0o = O00O0oOO00O00 . find ( 'home-team' )
    iI1iII1 = O00O0oOO00O00 . find ( 'gamestate' )
    oO0OOoo0OO = o000O0o . get ( 'nickname' )
    O0 = o000O0o . get ( 'alias' )
    ii1ii1ii = o000O0o . get ( 'score' )
    oooooOoo0ooo = o0oo0oOo . get ( 'nickname' )
    I1I1IiI1 = o0oo0oOo . get ( 'alias' )
    III1iII1I1ii = o0oo0oOo . get ( 'score' )
    oOOo0 = iI1iII1 . get ( 'status' )
    oo00O00oO = int (
 time . mktime ( time . strptime ( '%s %d' % ( iI1iII1 . get ( 'gametime' ) , iI1I111Ii111i ) , '%I:%M %p %Y%m%d' ) ) )
    if 23 - 23: OOooOOo + OOooOOo . O0oo0OO0
    if oOOo0 == 'In-Progress' :
     ii1ii11IIIiiI = 'in'
    elif oOOo0 == 'Pre-Game' :
     ii1ii11IIIiiI = 'pre'
    else :
     ii1ii11IIIiiI = 'end'
    i1iIIi1 [ ii1ii11IIIiiI ] . append ( {
 'league' : i11iIIIIIi1 . upper ( ) ,
 'orig-start' : oo00O00oO ,
 'start' : self . _to_local_time ( oo00O00oO ) . strftime ( "%I:%M %p" ) . lstrip ( '0' ) ,
 'home' : oO0OOoo0OO ,
 'home-alias' : O0 . upper ( ) ,
 'home-guide' : self . _get_mapped_team ( i11iIIIIIi1 , O0 . upper ( ) ) ,
 'away' : oooooOoo0ooo ,
 'away-alias' : I1I1IiI1 . upper ( ) ,
 'away-guide' : self . _get_mapped_team ( i11iIIIIIi1 , I1I1IiI1 . upper ( ) ) ,
 'home-score' : ii1ii1ii ,
 'away-score' : III1iII1I1ii ,
 'status' : oOOo0 ,
 'clock' : iI1iII1 . get ( 'display_status1' ) ,
 'clock-section' : iI1iII1 . get ( 'display_status2' )
 } )
  except Exception , O00OOOoOoo0O :
   xbmc . log ( "[%s] ERROR: %s" % ( ADDON . getAddonInfo ( 'id' ) , O00OOOoOoo0O . message ) , xbmc . LOGERROR )
   if 77 - 77: II % II * O00oOoOoO0o0O - i11iIiiIii
  return self . _sort_games ( i1iIIi1 [ 'in' ] ) + self . _sort_games ( i1iIIi1 [ 'pre' ] ) + self . _sort_games ( i1iIIi1 [ 'end' ] )
  if 93 - 93: IIiIiII11i / i1 % i11iIiiIii + iii1I1I * OOooOOo
 def _get_mapped_team ( self , league , name ) :
  if self . team_map is not None :
   for I1 , iI11Ii in dict ( self . team_map . items ( league ) ) . iteritems ( ) :
    if iI11Ii . upper ( ) == name :
     return I1 . title ( )
  return ''
  if 6 - 6: O00oOoOoO0o0O
 @ staticmethod
 def _sort_games ( games ) :
  if len ( games ) > 0 :
   return sorted ( games , key = itemgetter ( 'orig-start' , 'away-alias' ) )
  return [ ]
  if 68 - 68: I11i - OOooOOo
 def _to_local_time ( self , dt ) :
  dt = d_t . datetime . fromtimestamp ( dt )
  IIi = pytz . utc
  ooOOoooooo = pytz . timezone ( self . time_zone )
  II1I = ooOOoooooo . localize ( dt )
  O0i1II1Iiii1I11 = II1I . astimezone ( IIi )
  IIII = O0i1II1Iiii1I11 . replace ( tzinfo = None ) - O0i1II1Iiii1I11 . utcoffset ( )
  if 32 - 32: IIiIiII11i / iIiiiI1IiI1I1 - Ii1I
  o00oooO0Oo = time . daylight and time . localtime ( ) . tm_isdst > 0
  o0O0OOO0Ooo = - ( time . altzone if o00oooO0Oo else time . timezone )
  iiIiI = d_t . timedelta ( seconds = o0O0OOO0Ooo )
  return IIII + iiIiI
