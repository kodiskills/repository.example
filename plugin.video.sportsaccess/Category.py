# -*- coding: utf-8 -*-
#
#      Copyright (C) 2016 SportsAccess.se
#


class Category(object):
    category_mappings = {
        'FOOTBALL': '#E85F10',
        'NCAAF': '#E85F10',
        'NFL': '#E85F10',
        'BASEBALL': '#D49F24',
        'BASKETBALL': '#DE8512',
        'NBA': '#FC4F3D',
        'NCAAB': '#B0372A',
        'CRICKET': '#3DB800',
        'GOLF': '#1EBD06',
        'HOCKEY': '#1373D4',
        'MOTOR': '#D10404',
        'RUGBY': '#A5AB24',
        'TENNIS': '#00A658',
        'TV_SHOWS': '#111D87',
        'GENERAL': '#845191',
        'PPV': '#000000',
        'SOCCER': '#1E9C2A',
        'WRESTLING': '#9C793D',
        'NO_CATEGORY': ''
    }

    file_mappings = {
        'FOOTBALL': 'football',
        'NCAAF': 'football',
        'NFL': 'football',
        'BASEBALL': 'baseball',
        'BASKETBALL': 'basketball',
        'NBA': 'basketball',
        'NCAAB': 'basketball',
        'CRICKET': 'cricket',
        'GOLF': 'golf',
        'HOCKEY': 'hockey',
        'MOTOR': 'motor',
        'RUGBY': 'rugby',
        'TENNIS': 'tennis',
        'TV_SHOWS': 'general',
        'GENERAL': 'general',
        'PPV': 'general',
        'SOCCER': 'soccer',
        'WRESTLING': 'wrestling',
        'NO_CATEGORY': 'no-category'
    }

    labels = {
        'FOOTBALL': 'American Football',
        'NCAAF': 'NCAAF',
        'NFL': 'NFL',
        'BASEBALL': 'Baseball',
        'BASKETBALL': 'Basketball',
        'NBA': 'NBA',
        'NCAAB': 'NCAAB',
        'CRICKET': 'Cricket',
        'GOLF': 'Golf',
        'HOCKEY': 'Ice Hockey',
        'MOTOR': 'Motor Sports',
        'RUGBY': 'Rugby',
        'TENNIS': 'Tennis',
        'TV_SHOWS': 'TV Shows',
        'GENERAL': 'General TV',
        'PPV': 'PPV',
        'SOCCER': 'World Football',
        'WRESTLING': 'Wrestling',
        'NO_CATEGORY': ''
    }

    def __init__(self):
        pass

    def get_label(self, name):
        for cat, label in self.labels.iteritems():
            if cat == name:
                print ">>>>>>>>>>>>> NAME: " + str(name) + " -> " + str(label)
                return label
        return name

    def _get_file_mapping(self, name):
        for cat, m_name in self.file_mappings.iteritems():
            if cat == name:
                return m_name
        return 'grey'  # fallback to default!

    def get_focus_texture(self, name):
        return 'tvguide-program-%s-focus.png' % self._get_file_mapping(name)

    def get_no_focus_texture(self, name):
        return 'tvguide-program-%s.png' % self._get_file_mapping(name)
