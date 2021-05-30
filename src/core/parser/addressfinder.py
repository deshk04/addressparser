"""
  Author:
  Create date:
  Description:    find address components like street name, street num etc


  Version     Date                Description(of Changes)
  1.0                             Created
"""

import logging
from core.parser.addressreference import AddressReference
from core.general.helperlib import *

import pdb


class AddressFinder():
    """
        Task of this class is to identify address component from
        Address line
        Mandatory fields are address_line, suburb, postcode and state
    """

    def __init__(self, *args, **kwargs):
        self.allowed_fields = set(['address_line', 'suburb',
                                   'postcode', 'state'])
        self.components = {}
        self.streetPos = {}
        for field in self.allowed_fields:
            """
                check to be added to make sure mandatory fields are populated
            """
            setattr(self, field, kwargs[field].strip())
        self.leftoverString = 'N'

    def find_street(self, fuzzy_search=False):
        """
            find the street name & street type from address line
            fuzzy_search: 'N' indicates normal match
            fuzzy_search: 'Y' indicates fuzzy match
        """
        addr_ref = AddressReference()
        streetdf = addr_ref.get_streets(
            self.suburb, self.postcode, self.state)
        """
            find street from gnaf data
        """
        for idx, streetdata in streetdf.iterrows():
            self.street_name = streetdata.street_name
            self.street_type = streetdata.street_type

            self.street_confidence = 0
            self.streetPos = {}

            """
                if the street name is common word
                and street type is null then try another streetname
            """
            if self.street_name in addr_ref.commonwords and \
               self.street_type is None:
                continue

            """
                first let's see if the street name exists in
                in address line
                streetStartPos: its the starting position of
                street_name in address_line
            """
            if not fuzzy_search:
                self.streetPos = search_word(self.street_name,
                                             self.address_line)
                if not self.streetPos and '-' in self.street_name:
                    temp_streetname = self.street_name.replace(
                        '-', ' ')
                    self.streetPos = search_word(temp_streetname,
                                                 self.address_line)
            else:

                self.streetPos = search_word_fuzzy(self.street_name,
                                                   self.address_line)
            """
                we might have streetname occurance in multiple type
                in the address line so we check all match
                if any of them is good
            """
            for posIdx, searchPos in sorted(self.streetPos.items()):
                self.street_confidence = 0
                """
                    in case if the address has Cornor of 2 street
                    like the below examples
                    'l5/ste/10 cnr gilmore/ho'
                    or
                    'cnr day & macquarie st'
                    'cnr shepperton & oats st'
                    then we need to find the street before cornor
                    for now we are not handling that case as
                    most of the examples i have seen doesnt
                    have street number when cornor is given
                """
                self.cornerFlag = 'N'
                if searchPos[0] > 1:
                    cornerString = self.address_line[:searchPos[0]].split()
                    # if cornerString[-1] == 'cnr':
                    if 'corner' in cornerString:
                        self.cornerFlag = 'Y'
                    """
                        if the input is like below
                        'su 42 wesley medical ctr'
                        then we find street as wesley which is not good
                        since the next word indicates its a business
                    """
                    # nextwords = self.address_line[searchPos[1]:].split()
                    # if nextwords and \
                    #         addr_ref.get_businesstype(nextwords[0]) is not None:
                    #     continue
                    """
                        found an issue with the above logic
                        for e.g. if we have address like
                        '4 yellow book cl' the we get the street
                        but 'cl' is close and also considered as clinic
                        so the above logic think its clinic
                    """
                    nextwords = self.address_line[searchPos[1]:].split()
                    if nextwords and \
                            addr_ref.get_businesstype(nextwords[0]) is not None and \
                            nextwords[0] not in addr_ref.suffixwords[self.street_type]:
                        continue

                # pdb.set_trace()
                street_type_dict = self.search_street_type(posIdx)
                """
                    sometimes we have address like
                    total eyecare t66 channel court
                    the street type is not court but highway
                    address is 66/29 channel highway
                """
                if not street_type_dict and self.street_confidence >= \
                        self.components.get('street_confidence', 0):
                    street_type_dict['street_name'] = self.street_name
                    street_type_dict['street_type'] = self.street_type
                    street_type_dict['street_name_pos'] = searchPos[0]
                    self.street_confidence = 1
                    street_type_dict['street_confidence'] = 1

                street_num_dict = {}
                if searchPos[0] > 0 and bool(street_type_dict):
                    street_num_dict = self.search_street_number(posIdx)

                if not self.components or \
                    self.components.get('street_confidence', 0) <= \
                        self.street_confidence:
                    if street_type_dict:
                        self.components = street_type_dict
                        self.components.update(street_num_dict)
                        self.components['street_confidence'] = \
                            self.street_confidence

                """
                    if we get a match confidence of 3 or more then
                    we accept this street name as good match
                """
                if self.street_confidence >= 3:
                    break

            if not fuzzy_search:
                """
                    we need street number and street type
                    else ignore the self.street_confidence
                """
                if self.street_confidence > 1 and self.components:
                    street_num1 = self.components.get('number_1', None)
                    if not street_num1 or not street_num1.isdigit():
                        self.street_confidence = 0
                else:
                    self.street_confidence = 0
                pass

            if self.street_confidence >= 3:
                break

    def search_street_type(self, posIdx):
        """
            function to get the street type from address line
        """
        addr_ref = AddressReference()
        street_type_dict = {}
        self.street_confidence = 1

        """
            now let's find street type starting at the point of
            streetEndPos
        """
        sub_address_line = self.address_line[self.streetPos[posIdx][1]:]
        currPos = self.streetPos[posIdx][1]
        for idx, word in enumerate(sub_address_line.split()):
            """
                check if the word is number
            """
            number = get_number(word, 'S')

            """
                if the first word after street name is a common
                business word like 'hospital', 'surgery', 'clinic'
                etc then we should ignore this street_type as the
                street_name is probably part of business name
            """
            # if idx == 0 and (
            #         addr_ref.get_businesstype(word) is not None or
            #         number):
            #     self.street_confidence -= 1
            #     break

            """
                found an issue with the above logic
                for e.g. if we have address like
                '4 yellow book cl' the we get the street
                but 'cl' is close and also considered as clinic
                so the above logic think its clinic
            """
            if idx == 0 and (
                    addr_ref.get_businesstype(word) is not None or
                    number) and \
                    word not in addr_ref.suffixwords[self.street_type]:
                self.street_confidence -= 1
                break

            """
                if its a corner of 2 street then
                street type can be further than 2 words
            """
            if idx > 1 and self.cornerFlag == 'N':
                break

            """
                if its a number then it cant be street type
                so skip to next word
            """
            if number:
                continue

            if word == self.street_type:
                """
                    found street type
                """
                self.street_confidence = 2
                street_type_dict['street_name'] = self.street_name
                street_type_dict['street_type'] = self.street_type
                street_type_dict['street_name_pos'] = self.streetPos[posIdx][0]
                street_type_dict['street_type_pos'] = currPos
                break
            elif word in addr_ref.suffixwords[self.street_type]:
                """
                    found street type
                """
                self.street_confidence = 2
                street_type_dict['street_name'] = self.street_name
                street_type_dict['street_name_pos'] = self.streetPos[posIdx][0]
                street_type_dict['street_type'] = self.street_type
                street_type_dict['street_type_orig'] = word
                street_type_dict['street_type_pos'] = currPos
                break
            # else:
            #     """
            #         No street type was found
            #     """
            #     self.street_confidence = 1
            currPos += len(word) + 1

        """
            if street name has multiple words then increase
            the confidence
        """
        if len(self.street_name.split()) > 1 and self.street_confidence > 1:
            self.street_confidence += 1

        return street_type_dict

    def search_street_number(self, posIdx):
        """
            function to get the street number from address line
        """
        """
            now let's find street number before at the point of
            streetStartPos
            we are only interested in last word and second last word
            so we will reverse the string
        """
        sub_address_line = self.address_line[:self.streetPos[posIdx][0]]
        streetnumlist = sub_address_line.split()
        # streetNumString = ' '.join(reversed(streetNumString.split()))
        addr_ref = AddressReference()
        """
            we are only interested in last word and second last word
        """
        lastword = streetnumlist[-1].strip()
        """
            this is logical begining of new line
            e.g 022677GW: SE 101 GREY ST ANAESTHETIC,176 WELLINGTON PDE'
        """
        street_num_dict = {}
        numList = get_number(lastword, 'S')
        if not numList:
            """
                sometimes we have detail like
                'denture clinics 37 a main st'
                in this case the street number will not be found
                in ideal world the address would be like
                'detail denture clinics 37a main st'
            """
            if len(streetnumlist) >= 2:
                if len(lastword) == 1 and lastword.isalpha() and \
                        streetnumlist[-2].isdigit():
                    """
                        check if there is word before number
                        and if the word is part of premises
                        if its then dont consider this as street number
                    """
                    if len(streetnumlist) > 2:
                        premisestype = addr_ref.get_suffixtype(
                            streetnumlist[-3])
                        if not premisestype:
                            numList['number_1'] = streetnumlist[-2]
                            numList['number_1_suff'] = lastword
                    else:
                        numList['number_1'] = streetnumlist[-2]
                        numList['number_1_suff'] = lastword
                    """
                        remove the suffix word such that rest of
                        below code could work
                    """
                    lastword = streetnumlist[-2] + ' ' + streetnumlist[-1]
                    del streetnumlist[-1]
                else:
                    return street_num_dict
            else:
                return street_num_dict

        number1 = numList.get('number_1', None)
        if number1:
            self.street_confidence += 1
            street_num_dict['street_num1'] = number1
            street_num_dict['street_num1_suff'] = \
                numList.get('number_1_suff', None)
            street_num_dict['street_num_orig'] = lastword
            street_num_dict['street_num_pos'] = \
                self.streetPos[posIdx][0] - len(lastword)

        number2 = numList.get('number_2', None)
        if number2:
            self.street_confidence += 1
            street_num_dict['street_num2'] = number2
            street_num_dict['street_num2_suff'] = \
                numList.get('number_2_suff', None)

        """
            lets handle cases like
            012403CW : ST10A/3RD FL 1 SOUTH ST

        """
        if len(streetnumlist) > 1:
            previousword = streetnumlist[-2].strip()
            if previousword in addr_ref.directions:
                self.street_confidence -= 1
                street_num_dict = {}
            else:
                premisestype = addr_ref.get_suffixtype(previousword)
                if premisestype is not None:
                    """
                        if the code reached hear means that
                        the word before the street number is premises
                        type
                        so let's make sure the street number is not part
                        of premises and it is actual street number
                        if there is any more words before  this word
                        then
                    """
                    if len(streetnumlist) == 2:
                        self.street_confidence -= 1
                        street_num_dict = {}
        else:
            self.street_confidence += 1

        # self.components['street_confidence'] = self.street_confidence
        return street_num_dict

    def search_premises(self):
        """
            method to identify premises like suite, shop, unit, floor etc
        """
        premises_dict = {}
        self.sub_address_line = self.address_line.strip()

        if self.components.get('street_confidence', 0) == 0 or \
                len(self.sub_address_line) == 0:
            return

        """
            we remove the street components from address the line
            and then we find the premises
            first let's remove substring from position of
            street name to street type
        """
        streetNumPos = self.components.get('street_num_pos', -1)
        streetNamePos = self.components.get('street_name_pos', -1)
        streetTypePos = self.components.get('street_type_pos', -1)
        startPos = -1
        endPos = -1
        if streetNumPos >= 0:
            startPos = streetNumPos
        elif streetNamePos >= 0:
            startPos = streetNamePos

        """
            the above code finds the street name/num position
            now we find the end of street_type position
            then we remove the words between the start and end
            position. this gives us a string without street
            components which will be used for searching the premises
            components
        """
        self.leftoverString = 'N'
        if startPos >= 0:
            if streetTypePos > startPos:
                """
                    calculate the end string with
                """
                streetType = self.components.get(
                    'street_type_orig', None)
                if streetType is None:
                    streetType = self.components.get(
                        'street_type', None)
                endPos = streetTypePos + len(streetType)
            else:
                endPos = streetNamePos + len(self.components.get(
                    'street_name', ''))
            if startPos == 0:
                self.sub_address_line = self.sub_address_line[:startPos] + \
                    self.sub_address_line[endPos + 1:]
                if len((self.sub_address_line[endPos + 1:]).strip()) > 2:
                    self.leftoverString = 'Y'
            else:
                self.sub_address_line = self.sub_address_line[:startPos - 1] + \
                    self.sub_address_line[endPos:]
                if len((self.sub_address_line[endPos:]).strip()) > 2:
                    self.leftoverString = 'Y'

        """
            premises can be written in multiple ways
            'S 1 LVL 9'
            'S108'
            'Level 5/STE5'
            'STE45'
            'SUITES 8', '9 LEVEL 3'
            'FL G' or 'FL GRD' or 'G'
        """
        addr_ref = AddressReference()
        prem_line = self.sub_address_line.split()
        """
            sometimes we have address like
            g 25 rocklands
            where g indicates ground floor
            so the logic will be there is only 1 word
            and its part of numberwords then consider it
            as floor or level
        """
        foundIdx = []
        idx = 0

        if len(prem_line) == 1 and prem_line[0] in addr_ref.numberwords:
            premises_dict['floor'] = addr_ref.numberwords[prem_line[0]]
            premises_dict['floor_orig'] = prem_line[0]
            foundIdx.append(0)
        else:
            """
                we are using while instead of for since we
                need to skip a word in logic
            """
            while idx < len(prem_line):
                """
                    let's if its word like STE45 or U43
                    word that has both prefix and number
                    if its just a normal number skip to next
                """
                suff_type = addr_ref.get_suffixtype(prem_line[idx])
                num_dict = get_number(prem_line[idx], 'P')
                if num_dict:
                    premsuff = num_dict.get('number_1_suff', None)
                    premnum = num_dict.get('number_1', None)
                    if premsuff:
                        suff_type = addr_ref.get_suffixtype(premsuff)
                        if suff_type and premnum:
                            premises_dict[suff_type] = premnum
                            # premises_dict[suff_type + '_suff'] = premsuff
                            premises_dict[suff_type + "_orig"] = prem_line[idx]

                            foundIdx.append(idx)
                elif suff_type:
                    """
                        now first let's check if the next word is number
                    """
                    foundNextNum = 'N'
                    if idx + 1 < len(prem_line):
                        """
                            need to handle lvl first or FL G
                        """
                        num_dict = get_number(prem_line[idx + 1], 'P')
                        if num_dict or \
                                prem_line[idx + 1] in addr_ref.numberwords:
                            if suff_type in ['floor', 'level'] and \
                                    prem_line[idx + 1] in addr_ref.numberwords:
                                # prem_line[idx + 1] = \
                                #     addr_ref.numberwords[prem_line[idx + 1]]
                                num_dict = get_number(prem_line[idx + 1], 'P')

                            premsuff = num_dict.get('number_1_suff', None)
                            premnum = num_dict.get('number_1', None)
                            premises_dict[suff_type] = premnum
                            premises_dict[suff_type + '_suff'] = premsuff
                            premises_dict[suff_type + "_orig"] = prem_line[idx]
                            premises_dict[suff_type +
                                          "_orig"] = prem_line[idx + 1]
                            foundIdx.append(idx)
                            foundIdx.append(idx + 1)
                            idx += 1
                            foundNextNum = 'Y'
                    if foundNextNum == 'N' and idx > 0:
                        num_dict = get_number(prem_line[idx - 1], 'P')
                        if num_dict or \
                                prem_line[idx - 1] in addr_ref.numberwords:
                            if suff_type in ['floor', 'level'] and \
                                    prem_line[idx - 1] in addr_ref.numberwords:
                                num_dict = get_number(prem_line[idx - 1], 'P')

                            """
                                if we already found premises then dont overwrite it
                            """
                            if premises_dict.get(suff_type, None) is None:
                                premsuff = num_dict.get('number_1_suff', None)
                                premnum = num_dict.get('number_1', None)
                                premises_dict[suff_type] = premnum
                                if premsuff:
                                    premises_dict[suff_type +
                                                  '_suff'] = premsuff
                                premises_dict[suff_type +
                                              "_orig"] = prem_line[idx]
                                premises_dict[suff_type +
                                              "_orig"] = prem_line[idx - 1]
                                foundIdx.append(idx)
                                foundIdx.append(idx - 1)

                idx += 1
        """
            the components we found earlier
        """
        self.sub_address_line = ''
        for idx, word in enumerate(prem_line):
            if idx not in foundIdx:
                self.sub_address_line += word + ' '

        self.components.update(premises_dict)
        self.sub_address_line = self.sub_address_line.strip()
        """
            sometimes we have unit or flat information as
            102a lvl 1 151-155 hawkesbury
            the code above should already find level but
            wont find unit and if there is only 1 word
            and it numeric then we should consider it as
            unit
        """
        unitword = self.sub_address_line.split()
        unit_dict = {}
        """
            check if we already have unit information in
            address component, if yes then ignore
            the logic
        """
        unitnum = self.components.get('unit', None)
        if unitnum is None:
            unitnum = self.components.get('suite', None)

        if len(unitword) == 1 and unitnum is None:
            unitnum = get_number(unitword[0], 'P')
            if unitnum:
                num_suff = unitnum.get('number_1_suff', None)
                if num_suff:
                    unit_dict['unit_suff'] = num_suff
                    unit_dict['unit'] = unitnum.get('number_1', None)
                else:
                    unit_dict['unit'] = unitnum.get('number_1', None)
                self.sub_address_line = ''

            self.components.update(unit_dict)

    def search_businessname(self):
        """
            method to identify business name from address
        """
        # pdb.set_trace()

        """
            if the street confidence is <= 1 then remove
            the premises line from else show sub_address_line
        """
        self.business_name = ''
        addr_ref = AddressReference()
        business_line = self.sub_address_line.split()
        streetconf = self.components.get('street_confidence', 0)
        if streetconf < 2:
            premisesWords = []
            for prem in addr_ref.premisestype:
                """
                    for every premises type we search
                    for _orig and _type in the dict
                """
                prem_orig = self.components.get(prem + "_orig", None)
                prem_type = self.components.get(prem + "_type", None)
                if prem_orig:
                    premisesWords.append(prem_orig)
                if prem_type:
                    premisesWords.append(prem_type)
                if (prem_orig or prem_type) and prem in self.address_line.split():
                    premisesWords.append(prem)
            if len(premisesWords) == 0:
                # self.sub_address_line = ''
                pass
            else:
                self.sub_address_line = remove_words(premisesWords,
                                                     self.address_line)
        else:
            for idx, word in enumerate(business_line):
                comWord = addr_ref.get_businesstype(word)
                if comWord is not None:
                    business_line[idx] = comWord
            self.sub_address_line = " ".join(business_line)

            """
                the above logic works in most cases but there are
                scenarios where we have leftover words after street name
                e.g. 'castle hill hospital 72-74 cecil ave'
                system found cecil street instead of cecil avenue
                so ave is leftover and business look like
                'castle hill hospital ave'
                so this is hack to fix this type of issues
            """
            """
                the fix was giving problem for e.g.
                if the business name = 'bates street dental' and
                street_names is 'bates' then business name becomes
                'street dental' hence i created a new variable
                self.leftoverString if it is 'Y' then perform the fix
            """

            numpos = self.components.get('street_num_pos', None)
            namepos = self.components.get('street_name_pos', None)
            typepos = self.components.get('street_type_pos', None)
            startpos = -1
            if numpos is not None:
                startpos = numpos
            elif namepos is not None:
                startpos = namepos + \
                    len(self.components.get('street_name'))
                if self.cornerFlag == 'Y':
                    # startpos -= 4
                    cordic = search_word('corner', self.address_line)
                    if cordic:
                        corpos = cordic[0]
                        if corpos[0] < startpos:
                            startpos = corpos[0]
            if startpos >= 0 and self.leftoverString == 'Y':
                streetComp = []
                streetname = self.components.get('street_name')
                streetComp.append(streetname)
                streettypeabb = self.components.get(
                    'street_type_orig', None)
                if streettypeabb:
                    streetComp.append(streettypeabb)
                for word in self.address_line[startpos:].split():
                    if streettypeabb and word not in streettypeabb:
                        self.sub_address_line = replace_word(
                            word, ' ', self.sub_address_line)

            self.sub_address_line = " ".join(self.sub_address_line.split())
            if len(self.sub_address_line) < 4:
                self.sub_address_line = ''
            self.sub_address_line = self.sub_address_line.strip()

        self.business_name = self.sub_address_line
        """
            need to write logic to derive department name
        """
        self.department_name = ''
