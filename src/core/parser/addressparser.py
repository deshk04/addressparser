"""
  Author:
  Create date:
  Description:    address parser module


  Version     Date                Description(of Changes)
  1.0                             Created
"""

import logging
from collections import defaultdict
import pandas as pd

from core.parser.addressreference import AddressReference
from core.parser.addressfinder import AddressFinder
from core.models.addresscomponents import AddressComponents
from core.general.helperlib import *

import pdb


class AddressParser():

    def __init__(self, *args, **kwargs):
        self.address_line = ''
        self.raw_addr_line = ''
        self.confidence = 0
        self.addressdetails = AddressComponents()
        self.pobox_flag = 'N'
        allowed_fields = set(['address_line1', 'address_line2',
                              'suburb', 'postcode', 'state'])
        for field in allowed_fields:
            """
              this will raise python exception if the field is missing
              in future this needs to raise PDMException
            """
            try:
                setattr(self, field, kwargs[field].lower().strip())
            except:
                setattr(self, field, '')

        if self.address_line1 is not None and len(self.address_line1) > 0:
            self.address_line = self.address_line1

        if self.address_line2 is not None and len(self.address_line2) > 0:
            self.address_line = self.address_line + ' ' + self.address_line2

        self.raw_addr_line = self.address_line

    def parse(self):
        """
          this function will try and interpret the address line
        """
        output = {}
        logging.debug("Input for address parser")
        logging.debug("address line: " + self.address_line)
        logging.debug("postcode: " + str(self.postcode))
        logging.debug("suburb: " + str(self.suburb))
        logging.debug("state: " + str(self.state))
        """
            first we check if its a pobox number
        """
        addrref = AddressReference()
        pobox_num = 0
        pobox_type = ''
        for record in addrref.pobox:

            if record.pobox in self.address_line and pobox_num == 0:
                """
                    lets try and fetch pobox_num
                """
                pobox_type = record.pobox
                line_after = self.address_line[self.address_line.index(
                    record.pobox) + len(record.pobox):]
                line_after = line_after.replace(',', ' ')
                for word in line_after.split():
                    if word.isdigit():
                        try:
                            pobox_num = int(word)
                        except:
                            continue
                        break
                if pobox_num == 0:
                    line_before = self.address_line[:self.address_line.index(
                        record.pobox)]
                    if line_before:
                        word = line_before.split()[-1]
                        if word.isdigit():
                            try:
                                pobox_num = int(word)
                            except:
                                pobox_num = -1
                        if pobox_num == 0:
                            pobox_num = -1
                        break

        if pobox_num != 0:
            self.pobox_flag = 'Y'
            self.addressdetails.pobox_number = str(pobox_num)
            self.addressdetails.pobox_type = pobox_type
            self.addressdetails.suburb = self.suburb
            self.addressdetails.postcode = self.postcode
            self.addressdetails.state = self.state
            self.addressdetails.confidence = 3
            """
                we still need to find pobox_type
            """
            return

        """
           sanitize the data
        """
        self.sanitize()
        addrfinder = AddressFinder(
            address_line=self.address_line,
            suburb=self.suburb,
            postcode=self.postcode,
            state=self.state
        )
        tempaddrfinder = addrfinder
        addrfinder.find_street()
        self.confidence = addrfinder.components.get(
            'street_confidence', 0)
        """
            only if confidence is not good than go for fuzzy match
        """
        if self.confidence < 2:
            """
                lets do fuzzy matching check
            """
            fuzzy_search = True
            tempaddrfinder.find_street(fuzzy_search)
            if tempaddrfinder.components.get(
                    'street_confidence', 0) > self.confidence:
                addrInt = tempaddrfinder
                self.confidence = addrfinder.components.get(
                    'street_confidence', 0)
            """
                area match or fuzzy match didnt work then lets try
                non area match
            """
            if self.confidence < 1:
                addrfinder.find_street(1, 0)
                self.confidence = addrfinder.components.get(
                    'street_confidence', 0)

        """
            let's search for premises details
        """
        addrfinder.search_premises()
        """
            let's search business name
        """
        addrfinder.search_businessname()
        """
            it's better to clean the business name before
            sending it out to google
        """

        if addrfinder.sub_address_line and len(addrfinder.sub_address_line) > 2:
            tempBuss = addrfinder.sub_address_line.split()
            addrref = AddressReference()
            for idx, word in enumerate(tempBuss):
                comWord = addrref.get_businesstype(word)
                if comWord is not None:
                    tempBuss[idx] = comWord
            addrfinder.sub_address_line = " ".join(tempBuss)
            """
                business name is shopping centre then
                move it to building name
            """
            if 'shopping' in addrfinder.sub_address_line:
                addrfinder.department_name = addrfinder.sub_address_line
                addrfinder.sub_address_line = ''
            """
                if business name is same as street name
                or suburb then make it empty
            """
            if addrfinder.sub_address_line == self.suburb or \
                    addrfinder.sub_address_line == addrfinder.street_name:
                addrfinder.sub_address_line = ''

        # print(self.address_line)
        # print(str(addrfinder.components))
        # print("Business name: " + str(addrfinder.sub_address_line))
        if self.confidence > 0:
            """
                Lets map to AddressComponent.
            """
            self.addressdetails.confidence = self.confidence
            self.addressdetails.business_name = addrfinder.sub_address_line
            self.addressdetails.building_name = addrfinder.department_name
            flat_num = None
            flat_type = None
            flat_suff = None
            for key in ['unit', 'suite', 'flat', 'shop']:
                flat_num = addrfinder.components.get(key, None)
                """
                    sometimes the number is zero
                    hence he condition 'is not None'
                """
                if flat_num is not None and (
                        type(flat_num) is int or flat_num.isdigit()):
                    flat_num = int(flat_num)
                    flat_type = key
                    suff = key + '_suff'
                    flat_suff = addrfinder.components.get(suff, None)
                    break

            level_num = None
            level_type = None
            level_suff = None
            for key in ['floor', 'level']:
                level_num = addrfinder.components.get(key, None)
                if level_num is not None:
                    level_type = key
                    suff = key + '_suff'
                    level_suff = addrfinder.components.get(suff, None)
                    break

            self.addressdetails.flat_number = flat_num
            self.addressdetails.flat_type = flat_type
            self.addressdetails.flat_number_suffix = flat_suff
            self.addressdetails.level_number = level_num
            self.addressdetails.level_type = level_type
            self.addressdetails.level_number_suffix = level_suff

            try:
                num = addrfinder.components.get('street_num1', None)
                if num:
                    self.addressdetails.number_first = int(num)
                self.addressdetails.number_suffix = \
                    addrfinder.components.get('street_num1_suff', None)
                num = addrfinder.components.get('street_num2', None)
                if num:
                    self.addressdetails.number_last = int(num)
            except:
                self.addressdetails.number_first = None
                self.addressdetails.number_suffix = None
                self.addressdetails.number_last = None

            self.addressdetails.street_name = \
                addrfinder.components.get('street_name', None)
            self.addressdetails.street_type = \
                addrfinder.components.get('street_type', None)

            self.addressdetails.suburb = self.suburb
            self.addressdetails.postcode = self.postcode
            self.addressdetails.state = self.state
            """
                derive premises_type
                check the valid values in dim_premises_type
            """
            self.addressdetails.premises_type = None
            if self.addressdetails.flat_type and \
                    self.addressdetails.flat_type == 'shop':
                self.addressdetails.premises_type = 'shoppingcenter'
            elif self.addressdetails.business_name:
                if 'hospital' in self.addressdetails.business_name:
                    self.addressdetails.premises_type = 'hospital'
                elif 'shop' in self.addressdetails.business_name or \
                   'shop' in self.addressdetails.building_name:
                    self.addressdetails.premises_type = 'shoppingcenter'
                else:
                    self.addressdetails.premises_type = 'clinic'
            else:
                self.addressdetails.premises_type = 'residential'

    def sanitize(self):
        """
          clean the address line
        """
        """
          patch suburb based on reference data
        """
        addrref = AddressReference()
        for idx, patchRec in addrref.patchDataSuburb.iterrows():
            self.suburb = replace_word(
                patchRec.sourcestring,
                patchRec.destinationstring,
                self.suburb)

        """
          let's clean the address line
        """
        for idx, patchRec in addrref.patchDataAddr.iterrows():
            self.address_line = replace_word(
                patchRec.sourcestring,
                patchRec.destinationstring,
                self.address_line)

        """
          if there 'mc' space then it means its one word
          so make mc donald to mcdonald
        """
        mcLoc = search_word('mc', self.address_line)
        for posIdx, searchPos in sorted(mcLoc.items()):
            currPos = mcLoc[posIdx]
            self.address_line = self.address_line[:currPos[1] - 1] + \
                self.address_line[currPos[1]:].strip()

        self.address_line = replace_word('n/a', '', self.address_line)
        """
            now let's replace all the abbrevation of corner word
            to 'corner'
        """
        for corword in addrref.corner['corner']:
            self.address_line = replace_word(corword, 'corner', self.address_line)

        self.address_line = clean_string(self.address_line)
        """
            below code is moved from pdmhelper as we require to check
            the previous word
        """
        temp_addr_line = self.address_line.split()
        for idx, word in enumerate(temp_addr_line):
            if '/' in word:
                pos = word.index('/')
                """
                    sometimes we have string ending with '/'
                    for e.g.
                    1st floor cnr north pde/
                """
                if pos > 0:
                    leftchar = word[:pos][-1]
                    try:
                        rightchar = word[pos + 1:][0]
                    except:
                        rightchar = ''
                    if leftchar.isdigit() or rightchar.isdigit() or \
                            remove_ordinal(word[:pos]).isdigit():
                        """
                            sometimes we have address like
                            'bmb dental clinic  2/4 bungan st'
                            so we need 2 to be unit
                        """
                        if leftchar.isdigit() and idx > 0 and \
                                addrref.get_suffixtype(temp_addr_line[idx - 1]) is None:  # noqa
                            temp_addr_line[idx] = 'u' + word.replace('/', ' ')
                        else:
                            temp_addr_line[idx] = word.replace('/', ' ')

        """
            sometimes we have address like
            '2a-1 manchester rd' in that case we need to seperate
            2a to be seperate, so the logic will be
            if number1 is greater than number 2  then replace '-' with
            space
            also we have address like '12 nerang-broadbeach rd'
            where as gnaf will have 'nerang broadbeach' so it wont match
            if both side of '-' is characters then we replace '-' with
            space
        """
        for idx, word in enumerate(temp_addr_line):
            if '-' not in word:
                continue

            numlist = get_number(word, 'S')
            if not numlist:
                temp_addr_line[idx] = word.replace('-', ' ')
                continue

            num1 = numlist.get('number_1', None)
            num2 = numlist.get('number_2', None)
            try:
                num1 = int(num1)
                num2 = int(num2)
            except:
                num1 = None
                num2 = None

            if num1 is not None and num2 is not None:
                if num1 > num2:
                    temp_addr_line[idx] = 'u ' + word.replace('-', ' ')

        self.address_line = " ".join(temp_addr_line)
        """
          number suffix like 2ND should be converted to 2
        """
        self.address_line = remove_ordinal(self.address_line)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)
