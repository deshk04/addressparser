"""
  Author:
  Create date:
  Description:    fetch address reference data


  Version     Date                Description(of Changes)
  1.0                             Created
"""

import logging
from collections import defaultdict
import pandas as pd

from django.db import models
from django.db.models import Q

from core.pattern import Singleton

import pdb


class AddressReference(metaclass=Singleton):
    """
        reference data for address module
    """

    def __init__(self):
        self.suffixwords = defaultdict(list)
        self.premises = defaultdict(list)
        self.business = defaultdict(list)
        self.corner = defaultdict(list)
        self.names = defaultdict(list)
        self.commonwords = []
        self.excludewords = []
        self.pobox = None
        self.gnafstreets = {}
        self.gnafpostcodes = defaultdict(list)

        self.states = ['nt', 'qld', 'nsw', 'sa', 'tas',
                       'ot', 'vic', 'act', 'wa']

        self.numberwords = {'g': 0, 'grd': 0, 'lg': 0, 'ground': 0, 'first': 1,
                            'second': 2, 'third': 3, 'fourth': 4,
                            'fifth': 5, 'sixth': 6, 'seventh': 7,
                            'eigth': 8, 'nineth': 9, 'tenth': 10}

        self.premisestype = ['suite', 'unit', 'level', 'floor', 'shop']
        """
          direction can be written as
          e.g. SE: South East
               NW: North West
        """
        self.directions = ['se', 'ne', 'sw', 'nw']
        self.googletypes = defaultdict(list)

    def get_reference(self, i_dbobj):
        """
            fetch reference data
        """
        self.dbobj = i_dbobj

        """
            premises data
        """
        query = """select mainword, suffixword
                      from dim_word_dictionary
                      where mainword in (
                    'level', 'floor','suite', 'unit', 'shop')
                """
        cursor = self.dbobj.query(query)
        rows = cursor.fetchall()
        for row in rows:
            self.premises[row.mainword].append(row.suffixword)

        """
            we store suffix words in table such that it is flexible
            e.g. Street can be represented as st, strt, str etc
        """
        query = """select mainword, suffixword
                      from dim_word_dictionary
                      where wordtype = 'street'
                """
        cursor = self.dbobj.query(query)
        rows = cursor.fetchall()
        for row in rows:
            self.suffixwords[row.mainword].append(row.suffixword)

        """
            let's get corner words
        """
        query = """select mainword, suffixword
                      from dim_word_dictionary
                      where mainword = 'corner'
                    """
        cursor = self.dbobj.query(query)
        rows = cursor.fetchall()
        for row in rows:
            self.corner[row.mainword].append(row.suffixword)

        """
          abbrevation for business name
        """
        query = """select mainword, suffixword
                      from dim_word_dictionary
                      where mainword in (
                        'hospital', 'medical', 'private',
                        'public','community','service','health',
                        'surgery', 'clinic', 'centre',
                        'practice','specialist','coast')
                    """
        cursor = self.dbobj.query(query)
        rows = cursor.fetchall()
        for row in rows:
            self.business[row.mainword].append(row.suffixword)

        query = """select word from dim_common_words """
        cursor = self.dbobj.query(query)
        records = cursor.fetchall()
        for record in records:
            self.commonwords.append(record.word)

        query = """SELECT DISTINCT
                       street_name, street_type,
                       suburb, postcode, state, street_length
                       from dim_gnaf_streets
                    where street_length > 2
                    order by street_length desc,suburb
                    """
        gnafdf = pd.read_sql_query(query, self.dbobj.connstring)
        for state in self.states:
            self.gnafstreets[state] = gnafdf.loc[
                gnafdf['state'] == state, [
                    'street_name',
                    'street_type',
                    'suburb',
                    'postcode']]
        del gnafdf

        """
         let's fetch the list of POBOX strings
        """
        query = """select pobox from dim_pobox """
        cursor = self.dbobj.query(query)
        self.pobox = cursor.fetchall()

        """
         let's fetch the list of strings to patch
        """
        query = """select sourcestring, destinationstring, type
                     from dim_address_patch
                    """
        patchdf = pd.read_sql_query(
            query, self.dbobj.connstring)
        self.patchDataSuburb = patchdf.loc[
            patchdf['type'] == 'S', ['sourcestring', 'destinationstring']]
        self.patchDataAddr = patchdf.loc[
            patchdf['type'] != 'S', ['sourcestring', 'destinationstring']]
        del patchdf


        """
           let's fetch postcode which fells under 2 states
        """
        query = """
                    select t1.postcode, t1.state from dim_gnaf_postcode t1,(
                        select postcode,count(distinct state) s
                        from dim_gnaf_postcode
                        group by 1 having count(distinct state) > 1) t2
                    where t1.postcode = t2.postcode
                    order by t1.postcode
                      """
        cursor = self.dbobj.query(query)
        rows = cursor.fetchall()
        for row in rows:
            self.gnafpostcodes[row.postcode].append(row.state)


        """
          for names we pick up short names
        """
        query = """select distinct name, shortname
                      from dim_name_abbr
                    """
        cursor = self.dbobj.query(query)
        rows = cursor.fetchall()
        for row in rows:
            self.names[row.name].append(row.shortname)

    def get_streets(self, i_suburb, i_postcode, i_state):
        """
            return all the streets for a suburb or postcode
            first the street is searched based on suburb
            if not found then suburb condition is ignored
        """
        gnafstreetdata = self.gnafstreets[i_state]
        """
            some postcodes fall under 2 states in that case we
            have problem, so need to fetch the data
            the check can be done from self.gnafpostcodes
        """
        tempstates = self.gnafpostcodes[i_postcode]
        if tempstates:
            for state in tempstates:
                if state == i_state:
                    continue
                tempgnafstreetdata = self.gnafstreets[state]
                gnafstreetdata = gnafstreetdata.append(
                    tempgnafstreetdata, ignore_index=True)

        """
            first we look for street name closer to suburb or postcode
        """
        streetdata = None
        streetdata = gnafstreetdata.loc[
            (gnafstreetdata.suburb == i_suburb) |
            (gnafstreetdata.postcode == i_postcode),
            ['street_name', 'street_type']]

        """
            if not found then try without suburb /postcode match
        """
        if streetdata.empty:
            streetdata = gnafstreetdata.loc[
                ~(
                    (gnafstreetdata.suburb == i_suburb) |
                    (gnafstreetdata.postcode == i_postcode)
                ),
                ['street_name', 'street_type']]

        return streetdata

    def get_suffixtype(self, suffWord):
        for key, value in self.premises.items():
            if key == suffWord or suffWord in value:
                return key

        if suffWord in self.directions:
            return 'unit'

        return None

    def get_businesstype(self, suffWord):
        for key, value in self.business.items():
            if key == suffWord or suffWord in value:
                return key

        return None

