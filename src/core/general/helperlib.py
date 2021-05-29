"""
  Author:
  Create date:
  Description:    helper library


  Version     Date                Description(of Changes)
  1.0                             Created
"""

import sys
import re
from datetime import datetime
from dateutil import tz

import jellyfish as jf
from django.contrib.humanize.templatetags.humanize import ordinal

import pdb


def find_word(old, string, startpos=0):
    """
        old: is the word to be searched
        string: string to perform the operation on
        startpos: starting position
        if not found then we return -1
    """
    resultdict = {}
    idx = 0
    for pos in re.finditer(r'(\b%s\b)' % word, string[startpos:]):
        resultdict[idx] = [pos.start(), pos.end() + 1]
        idx += 1
    return resultdict


def replace_word(old, new, string):
    """
        old: word to replace
        new: word to be replaced with
        string: string to perform the operation on
    """
    return re.sub(r'\b%s\b' % old, new, string)


def check_word(word, string):
    """
        function will check if the word exists in a string
        uses word boundary for search
        word: is the word to be searched
        string: string to perform the operation on
    """
    regexStr = re.search(r'(\b%s\b)' % word, string)
    if regexStr is not None:
        return True

    return False


def search_word(i_word, i_string, i_startpos=0):
    """
        function will check if the word exists in a string
        uses word boundary for search
        i_word: is the word to be searched
        i_string: string to perform the operation on
        i_startpos: starting position from where to search
        return value: its the position where we found the string
        if result is not found then we return -1
    """
    outputDict = {}
    idx = 0
    for pos in re.finditer(r'(\b%s\b)' % i_word, i_string[i_startpos:]):
        outputDict[idx] = [pos.start(), pos.end() + 1]
        idx += 1
    return outputDict


def search_word_fuzzy(word, string, startpos=0):
    """
        word: is the word to be searched
        string: string to perform the operation on
        return value: if not found then we return -1
    """
    newstartpos = startpos
    resultdict = {}
    idx = 0

    if len(word) < 3:
        return resultdict
    """
        first we check if a simple singular vs plural match
        works for e.g. match hill with hills
    """
    for word in string.split():
        if word + 's' == word:
            """
                to handle cases like
                word: hill
                street_name: hills
            """
            posEnd = newstartpos + len(word) + 1
            resultdict[idx] = [newstartpos, posEnd]
            idx += 1
        elif word == word + 's':
            posEnd = newstartpos + len(word) + 1
            resultdict[idx] = [newstartpos, posEnd]
            idx += 1

        newstartpos += len(word) + 1
    """
        if the match didnt work then try soundex()
    """
    idx = 0
    newstartpos = startpos
    if not resultdict and len(word) > 4:
        for word in string.split():
            if len(word) > 4 and word[:2] == word[:2]:
                if (jf.metaphone(word) == jf.metaphone(word) and
                    jf.levenshtein_distance(word, word) < 3) or \
                   (jf.match_rating_comparison(word, word) and
                        jf.levenshtein_distance(word, word) < 2):
                    posEnd = newstartpos + len(word) + 1
                    resultdict[idx] = [newstartpos, posEnd]
                    idx += 1
            newstartpos += len(word) + 1

    return resultdict


def clean_string(string):
    """
        custom clean function to clean unwanted
        characters
        string: string to clean
    """
    # unCharSet = {'\\': ' ', "'": '', '(': ' ', ')': ' ',
    #              '.': ' ', ',': ' ', '/': ' ', '&': ' and '}
    unCharSet = {'\\': ' ', "'": '', '(': ' ', ')': ' ',
                 '.': ' ', ',': ' ', '&': ' and ',
                 ';': '', ')': '', '(': '', '}': '',
                 '{': '', ']': '', '[': '', '/': '',
                 '\\': '', '>': '', '<': '', '=': '',
                 '|': '', '%': '', '\'': '', '*': '',
                 'undefined': ''}

    if string is None:
        return None

    for key, value in unCharSet.items():
        string = string.replace(key, value)

    """
        most character to be replaced is straight forward
        except '/'
        some words have '/' to short the long word
        e.g. south can be written as s/th
        but sometimes we have 2/49 which means
        unit 2 and street number 49
        we want to only handle the second case
        another e.g. is 1051a/b high st
    """
    o_string = string.split()
    """
        below code is moved to addressparser
    """
    # for idx, word in enumerate(o_string):
    #     if '/' in word:
    #         pos = word.index('/')
    #         """
    #             sometimes we have string ending with '/'
    #             for e.g.
    #             1st floor cnr north pde/
    #         """
    #         if pos > 0:
    #             leftchar = word[:pos][-1]
    #             try:
    #                 rightchar = word[pos + 1:][0]
    #             except:
    #                 rightchar = ''
    #             if leftchar.isdigit() or rightchar.isdigit() or \
    #                     remove_ordinal(word[:pos]).isdigit():
    #                 o_string[idx] = word.replace('/', ' ')

    o_string = " ".join(o_string)
    return o_string


def remove_ordinal(string):
    """
        remove ordinal words like 2nd, 3rd etc
        string: string on the operation to be performed
    """
    o_string = []
    for numWord in string.split():
        regexNum = re.search(r'^[0-9]+', numWord)
        if regexNum:
            num = regexNum.group()
            # ordinal = numWord[regexNum.end():]
            """
                django's ordinal method will return
                23 -> 23rd
                4 -> th
                15th - > 15th
            """
            if ordinal(num) == numWord:
                numWord = num
        o_string.append(numWord)

    o_string = " ".join(o_string)
    return o_string


def remove_words(i_list, string):
    """
        remove the input list of word from string
        i_list: list of words to be removed
        string: string on the operation to be performed
    """
    regexStr = re.compile(r'\b%s\b' %
                          r'\b|\b'.join(map(re.escape, i_list)))
    o_string = regexStr.sub("", string)

    return o_string


def get_number(word, i_type='S'):
    """
        function is used to get the street number
        with suffix details
        word: input word from which number and suffix
        details will be derived
        i_type: S - street number
                P - premises number
    """

    resultdict = {}
    if word is None:
        return resultdict

    word = str(word)
    regexStr = None
    if i_type == 'S':
        regexStr = re.search(r'^[0-9\-]+', word)
    else:
        regexStr = re.search(r'[0-9\-]+', word)

    if regexStr is not None:
        # pdb.set_trace()
        numList = []
        if '-' in word:
            numList = word.split('-')
        else:
            numList.append(word)

        for idx, numWord in enumerate(numList):
            if idx > 1:
                resultdict = {}
                break
            """
                Let's get number and suffix for number1
                and number2
            """
            # to get the number
            regexNum = re.search(r'[0-9]+', numWord)
            key = 'number_' + str(idx + 1)
            if regexNum is not None:
                try:
                    resultdict[key] = int(regexNum.group().split(' ')[0])
                except:
                    pass
                # resultdict[key] = regexNum.group().split(' ')[0]

            # to get suffix
            regexSuff = re.search(r'[a-zA-Z]+', numWord)
            key = key + '_suff'
            if regexSuff:
                # resultdict[key] = regexSuff.group().split(' ')[0]
                """
                    dont think we should have suffix more than 1
                    character
                    there are few cases but we are ignoring them...
                """
                suff = regexSuff.group().split(' ')[0]
                if i_type == 'S':
                    if len(suff) == 1:
                        resultdict[key] = suff
                    else:
                        resultdict = {}
                else:
                    if len(suff) < 3:
                        resultdict[key] = suff

    return resultdict


def word_count(i_source, i_dest):
    """
        count the number of words from i_source string
        which are in destination string.
        i_source: source string
        i_dest: destination string
        return: count of words, 0 to indicate no match
    """
    counter = 0
    if not i_source or not i_dest:
        return counter

    unCharSet = {'\\': '', "'": '', '(': '', ')': '',
                 '.': '', ',': '', '-': ''}

    for key, value in unCharSet.items():
        i_source = i_source.replace(key, value)

    for key, value in unCharSet.items():
        i_dest = i_dest.replace(key, value)

    sourceArr = i_source.split(' ')
    destArr = i_dest.split(' ')
    for word in sourceArr:
        if word in destArr:
            counter += 1

    return counter


def cleanfield(value):
    """
        remove spaces
    """
    if not value:
        return None
    value = str(value)
    value = value.strip()
    return value


def cleanfieldlower(value):
    """
        remove spaces and convert to lower case
        so flag error
    """
    if not value:
        return None
    value = str(value)
    value = value.strip()
    value = value.lower()
    return value


def compare_fields(field1, field2):
    """
        compare 2 fields if they are same then return true
    """
    if field1 is None and field2 is None:
        return True

    if (field1 is None and field2 is not None) or\
            (field2 is None and field1 is not None):
        return False

    if field1 == field2:
        return True

    return False


def convert_timezone(time):
    """
        matdatepicker returns a datetime object in UTC time.
        Need to convert this to local time as only date is stored in db
    """
    if time is None:
        return None
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    try:
        utc = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        utc = datetime.strptime(time, "%Y-%m-%d")
    utc = utc.replace(tzinfo=from_zone)
    local_date = utc.astimezone(to_zone).date()
    return local_date


def convert_to_int(number):
    """
        converts the input to an integer
    """
    try:
        return int(number)
    except:
        return None


def convert_to_float(number):
    """
        converts the input to a float
    """
    try:
        return float(number)
    except:
        return None


def validate_date(date_text):
    time = date_text.strip()
    try:
        datetime.strptime(time, '%Y-%m-%d')
        return True
    except:
        try:
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
            return True
        except:
            return False
