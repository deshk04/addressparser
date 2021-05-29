"""
  Author:
  Create date:
  Description:    enhence the data from gnaf and google


  Version     Date                Description(of Changes)
  1.0                             Created
"""

import requests
from datetime import datetime
import logging
import pandas as pd
from core.models.addresscomponents import AddressComponents
from core.parser.addressreference import AddressReference
from core.general.db import Database

from core.general.helperlib import *
from core.general import settings
from core.general.exceptions import *

import pdb


class AddressEnhencer():

    def __init__(self, *args, **kwargs):
        self.title = None
        self.firstname = None
        self.middlename = None
        self.lastname = None
        self.business_name = None
        self.addressdetails = None
        self.google_flag = 'Y'
        self.confidence = 0
        self.googleplaces = None
        self.dbobj = Database()
        self.base_url = settings.GOOGLE_URL
        self.api_key = settings.GOOGLE_API
        self.states = {
            'nsw': 'new south wales',
            'vic': 'victoria',
            'qld': 'queensland',
            'sa': 'south australia',
            'wa': 'western australia',
            'tas': 'tasmania',
            'nt': 'northern territory',
            'act': 'australian capital territory',
            'ot': 'other territories'
        }
        self.headers = settings.HTTP_HEADER
        self.pharmacy_flag = 'N'

        self.addrref = AddressReference()
        self.api_type = None
        self.invalid_business_name = ['theatre', 'the']

    def execute(self):
        """
          main function
        """
        if not self.addressdetails:
            logging.debug('Input data missing')
            return

        if not self.business_name:
            if self.addressdetails.business_name and \
                    len(self.addressdetails.business_name) > 2:
                self.business_name = self.addressdetails.business_name

        self.sanitize()

        """
            get gnaf geo location
            if address confidence is good and street number is populated
            we fetch the geo-codes from gnaf else from google
        """
        gnaf_status = False
        if self.addressdetails.confidence > 2 and \
                self.addressdetails.number_first and \
                self.addressdetails.street_name:
            gnaf_status = self.get_gnafdata()

        from core.models.googleplacesproxy import GooglePlacesProxy

        if self.business_name and len(self.business_name) > 2 and \
                self.addressdetails.postcode:
            self.business_name = self.business_name.strip()
            """
                we call google api
            """
            self.generate_query(self.business_name)
        elif self.addressdetails.business_name and \
                len(self.addressdetails.business_name) > 2:
            self.generate_query(self.addressdetails.business_name)
        else:
            self.generate_query(True)

        """
            let's search google
        """
        self.googleplaces = self.findplacefromtext()
        if not self.googleplaces or (self.googleplaces and
                                     len(self.googleplaces.place_id) < 5):
            self.googleplaces = self.autocomplete()

        if self.googleplaces and len(self.googleplaces.place_id) > 5:
            self.googleplaces = self.place_details(self.googleplaces.place_id)
            if self.googleplaces:
                self.set_confidence()
        if self.confidence > 0:
            return True

        return False

    def get_gnafdata(self):
        """
            fetch geo-codinates from gnaf data
        """
        logging.debug('processing get_gnafdata')

        query = """SELECT *
                    from dim_gnaf_address_details t1
                    where state_abbreviation='{0}'
                    and street_name='{1}'
                    and (postcode = '{2}' or locality_name = '{3}')
                    and number_first = '{4}'
                """
        query = query.format(self.addressdetails.state,
                             self.addressdetails.street_name,
                             self.addressdetails.postcode,
                             self.addressdetails.suburb,
                             self.addressdetails.number_first
                             )
        gnafdf = pd.read_sql_query(query, self.dbobj.connstring)
        # pdb.set_trace()
        if gnafdf.empty:
            return False
        record = gnafdf.iloc[0]
        """
            populate addressdetails with geo-codes
        """
        self.addressdetails.latitude = record.latitude
        self.addressdetails.longitude = record.longitude
        self.addressdetails.parcel_id = record.legal_parcel_id

        return True

    def sanitize(self):
        """
            clean the variables
        """

        if self.firstname and len(self.firstname) > 0:
            if self.firstname.lower() == 'none':
                self.firstname = ''

        if self.middlename and len(self.middlename) > 0:
            if self.middlename.lower() == 'none':
                self.middlename = ''

        if self.lastname and len(self.lastname) > 0:
            if self.lastname.lower() == 'none':
                self.lastname = ''

        if self.business_name and len(self.business_name) > 0:
            if self.business_name.lower() == 'none':
                self.business_name = ''

        if self.title and len(self.title) > 0:
            if self.title.lower() == 'none':
                self.title = ''

        """
            sometimes we have business name as
            'theatre','the' in that case we should remove it
            as they give bad result
        """
        if self.business_name:
            for inv_bus in self.invalid_business_name:
                if self.business_name == inv_bus:
                    self.business_name = ''

    def generate_query(self, nameflag=False):
        """
          generate query for api based on business name
        """
        self.query = ''
        if not nameflag:
            if self.business_name:
                self.query = self.business_name
        else:
            if self.firstname and len(self.firstname) > 0:
                self.query = str(self.title) + " " + str(self.firstname) + " " + str(self.lastname)
            else:
                self.query = str(self.title) + " " + str(self.middlename) + " " + str(self.lastname)

        if self.addressdetails.street_name and len(self.addressdetails.street_name) > 1:
            if not self.business_name and \
                    self.addressdetails and self.addressdetails.number_first:
                self.query += str(self.addressdetails.number_first)
            self.query += " " + str(self.addressdetails.street_name)
            self.query += " " + str(self.addressdetails.street_type)

        self.query += "," + str(self.addressdetails.postcode)
        self.query += "," + str(self.addressdetails.state)

    def findplacefromtext(self):
        """
          handles googles findplacefromtext api
        """
        self.api_type = 'F'
        from core.models.googleplacesproxy import GooglePlacesProxy

        url = self.base_url + "place/findplacefromtext/json"
        query = self.query
        query = ',australia'
        payload = {'input': self.query,
                   'key': self.api_key,
                   'inputtype': 'textquery',
                   'components': 'country:au',
                   'fields': 'name,place_id,formatted_address,geometry'
                   }

        api_response = requests.get(
            url, params=payload, headers=self.headers)
        results = api_response.json()
        googleplaces = GooglePlacesProxy()
        if results['status'] != 'OK':
            if results['status'] == 'OVER_QUERY_LIMIT':
                raise PDMOverQueryLimit
            if results['status'] == 'REQUEST_DENIED':
                raise PDMRequestDenied
            return None

        answer = self.find_response(results['candidates'])
        if not answer:
            return None

        googleplaces.place_id = answer.get("place_id", None)
        googleplaces.business_name = answer.get("main_text", '')
        googleplaces.address_string = answer.get(
            "secondary_text", '')
        googleplaces.types = answer.get("types", '')
        googleplaces.longitude = ''
        googleplaces.latitude = ''
        googleplaces.street_name = ''
        googleplaces.street_number = ''
        googleplaces.postcode = ''
        googleplaces.weekday_text = ''

        return googleplaces

    def autocomplete(self):
        """
          handles googles autocomplete api
        """
        self.api_type = 'A'
        from core.models.googleplacesproxy import GooglePlacesProxy

        url = self.base_url + "place/autocomplete/json"
        payload = {'input': self.query,
                   'key': self.api_key,
                   'rankby': 'distance',
                   'components': 'country:au',
                   'fields': 'name, place_id, formatted_address, geometry.location'
                   }

        api_response = requests.get(
            url, params=payload, headers=self.headers)
        results = api_response.json()
        googleplaces = GooglePlacesProxy()
        if results['status'] != 'OK':
            if results['status'] == 'OVER_QUERY_LIMIT':
                raise PDMOverQueryLimit
            if results['status'] == 'REQUEST_DENIED':
                raise PDMRequestDenied
            return None

        answer = self.find_response(results['predictions'])
        if not answer:
            return None

        googleplaces.place_id = answer.get("place_id", None)
        googleplaces.business_name = answer.get("main_text", '')
        googleplaces.address_string = answer.get(
            "secondary_text", '')
        googleplaces.types = answer.get("types", '')
        googleplaces.longitude = ''
        googleplaces.latitude = ''
        googleplaces.street_name = ''
        googleplaces.street_number = ''
        googleplaces.postcode = ''
        googleplaces.weekday_text = ''

        return googleplaces

    def textsearch(self):
        """
          handles googles textsearch api
        """
        self.api_type = 'T'
        from core.models.googleplacesproxy import GooglePlacesProxy

        url = self.base_url + "place/textsearch/json"
        payload = {'query': self.query,
                   'key': self.api_key,
                   'region': 'au'}

        api_response = requests.get(
            url, params=payload, headers=self.headers)
        results = api_response.json()

        googleplaces = GooglePlacesProxy()
        if results['status'] != 'OK':
            if results['status'] == 'OVER_QUERY_LIMIT':
                raise PDMOverQueryLimit
            if results['status'] == 'REQUEST_DENIED':
                raise PDMRequestDenied
            return None

        answer = self.find_response(results['results'])
        if not answer:
            return None
        googleplaces.place_id = answer.get("place_id", None)
        googleplaces.business_name = answer.get("name", '')
        googleplaces.address_string = answer.get(
            "formatted_address", '')
        googleplaces.types = answer.get("types", '')
        googleplaces.longitude = answer.get(
            "geometry").get("location").get("lng", None)
        googleplaces.latitude = answer.get(
            "geometry").get("location").get("lat", None)
        googleplaces.street_name = ''
        googleplaces.street_number = ''
        googleplaces.postcode = ''
        googleplaces.weekday_text = ''

        return googleplaces

    def place_details(self, google_place_id):
        """
          handles googles geo search api
          this method can be called independently if we have place_id
          and interested in populating the google_places
        """
        if google_place_id is None or len(google_place_id) < 5:
            return None

        from core.models.googleplacesproxy import GooglePlacesProxy

        googleplaces = GooglePlacesProxy.objects.get_or_none(
            place_id=google_place_id)
        if googleplaces:
            return googleplaces

        googleplaces = GooglePlacesProxy()
        url = self.base_url + "place/details/json"
        payload = {'placeid': google_place_id, 'key': self.api_key}
        response = None
        with requests.Session() as ses:
            response = ses.get(url, params=payload,
                               headers=self.headers, timeout=10)
        detail_results = response.json()
        """
        OK:         indicates that no errors occurred;
                    the place was successfully detected and
                    at least one result was returned.
        UNKNOWN_ERROR: indicates a server-side error;
                    trying again may be successful.
        ZERO_RESULTS: indicates that the reference was valid but
                    no longer refers to a valid result.
                    This may occur if the establishment is no longer
                    in business.
        OVER_QUERY_LIMIT: indicates that you are over your quota.
        REQUEST_DENIED: indicates that your request was denied,
                    generally because of lack of an invalid key parameter.
        INVALID_REQUEST: generally indicates that the query (reference) is
                        missing.
        NOT_FOUND: indicates that the referenced location was
                    not found in the Places database.
        """
        if detail_results['status'] != 'OK':
            if detail_results['status'] == 'OVER_QUERY_LIMIT':
                raise MitOverQueryLimit
            if detail_results['status'] == 'REQUEST_DENIED':
                raise MitRequestDenied

            return googleplaces

        result = detail_results['result']
        data = result
        for item in result['address_components']:
            for category in item['types']:
                data[category] = {}
                data[category] = item['long_name'].lower()

        googleplaces.street_number = data.get('street_number', '')
        if '/' in googleplaces.street_number:
            googleplaces.street_number = googleplaces.street_number.replace(
                '/', '-')

        googleplaces.street_name = str(data.get("route", ''))
        googleplaces.state = data.get("administrative_area_level_1", '')
        googleplaces.suburb = data.get("locality", '')
        googleplaces.county = data.get("administrative_area_level_2", '')
        googleplaces.country = data.get("country", '')
        googleplaces.postcode = data.get("postal_code", '')
        googleplaces.neighborhood = data.get("neighborhood", '')
        googleplaces.sublocality = data.get("sublocality", '')
        googleplaces.housenumber = data.get("housenumber", '')
        googleplaces.town = data.get("town", '')
        googleplaces.subpremise = data.get("subpremise", '')
        googleplaces.latitude = data.get("geometry", {}).get(
            "location", {}).get("lat", None)
        googleplaces.longitude = data.get("geometry", {}).get(
            "location", {}).get("lng", None)
        googleplaces.location_type = data.get(
            "geometry", {}).get("location_type", '')
        googleplaces.postal_code_suffix = data.get("postal_code_suffix", '')
        googleplaces.business_name = data.get("name", '')
        googleplaces.business_name = googleplaces.business_name.lower()

        googleplaces.formatted_phone_number = data.get(
            "formatted_phone_number", '')
        googleplaces.international_phone_number = data.get(
            "international_phone_number", '')

        weekday_text = data.get('opening_hours', {}).get("weekday_text", '')

        for day in weekday_text:
            if 'Monday' in day:
                googleplaces.opening_hours_mon = day.replace('Monday:', '')
            if 'Tuesday' in day:
                googleplaces.opening_hours_tue = day.replace('Tuesday:', '')
            if 'Wednesday' in day:
                googleplaces.opening_hours_wed = day.replace('Wednesday:', '')
            if 'Thursday' in day:
                googleplaces.opening_hours_thu = day.replace('Thursday:', '')
            if 'Friday' in day:
                googleplaces.opening_hours_fri = day.replace('Friday:', '')
            if 'Saturday' in day:
                googleplaces.opening_hours_sat = day.replace('Saturday:', '')
            if 'Sunday' in day:
                googleplaces.opening_hours_sun = day.replace('Sunday:', '')

        googleplaces.web_url = data.get('website', '')
        googleplaces.place_id = google_place_id
        googleplaces.rating = data.get('rating', -1)
        googleplaces.permanently_closed = data.get('permanently_closed', '')
        googleplaces.scope = data.get('scope', '')
        googleplaces.price_level = data.get('price_level', -1)
        googleplaces.types = data.get('types', [])

        googleplaces.sys_creation_date = datetime.now()
        googleplaces.user_id = 'system'
        """
            the above code had bug, in case of business_name is not
            populated then exception is set as 'N'
        """
        if self.addrref.valid_googletypeMed(googleplaces.types) or \
            word_count(self.business_name, googleplaces.business_name) > 0 or \
            (self.firstname in googleplaces.business_name and
             self.lastname in googleplaces.business_name):
            googleplaces.exception_flag = 'N'
        else:
            googleplaces.exception_flag = 'Y'

        googleplaces.save()

        return googleplaces

    def set_confidence(self):
        """
          set the confidence of the google result
        """
        self.confidence = 0
        """
            sometimes the postcode falls under 2 states
        """
        self.addrref.gnafpostcodes[self.addressdetails.postcode]
        if (self.googleplaces.state == self.addressdetails.states[self.addressdetails.state] or
                self.googleplaces.postcode == self.addressdetails.postcode):
            if self.googleplaces.postcode == self.addressdetails.postcode or \
                    self.googleplaces.suburb == self.addressdetails.suburb or \
                    self.googleplaces.suburb.find(self.addressdetails.suburb) >= 0:
                self.confidence = 1
                """
                    check if input business_name is populated
                """
                if self.business_name and len(self.business_name) > 2:
                    """
                        let's check if the business_name returned by
                        google match to iMed building name
                    """
                    if self.googleplaces.business_name:
                        wc = word_count(self.business_name,
                                        self.googleplaces.business_name,
                                        )
                        if wc > 0:
                            self.confidence = 2
                if self.addressdetails.number_first is not None and \
                        str(self.addressdetails.number_first) == \
                            str(self.googleplaces.street_number) and \
                            self.googleplaces.street_name.find(self.addressdetails.street_name) >= 0:  # noqa
                    self.confidence += 1
            elif self.googleplaces.postcode and \
                    self.googleplaces.postcode[:2] == self.addressdetails.postcode[:2]:
                """
                    match is closer to postcode
                """
                self.confidence = 1
                if self.searchType == 'N' and self.googleplaces.business_name:
                    """
                        if the provider name is part of search check
                        if the google result has provider last name
                    """
                    if self.googleplaces.business_name.find(self.lastname) >= 0:  # noqa
                        self.confidence += 1

    def find_response(self, results):
        """
          to find the correct google response
          results: the json array received from google
          resultKey: array index name
          businesskey: to key to identify business name
        """
        # if len(results) == 1:
        #     return results[0]

        if self.api_type == 'A':
            # resultKey = 'predictions'
            businessnamekey = 'main_text'
            addresskey = 'description'
            state = self.states[self.addressdetails.state]
        else:
            # resultKey = 'results'
            businessnamekey = 'name'
            addresskey = 'formatted_address'
            state = self.addressdetails.state
        """
            google might return multiple results, the rule to identify
            the best result is
            1) its within the same state
            2) its near to the postcode
            3) highest ranking confidence in business name (best match)
            4) valid google type
        """

        """
            first we filter valid types
        """
        newResults = []
        for idx, result in enumerate(results):
            gtypes = result.get("types", [])
            if self.addrref.valid_googletype(gtypes) and \
                    self.pharmacy_flag == 'N':
                newResults.append(result)
            # if we are searching for pharmacy then check if google
            # return pharmacy type
            elif self.pharmacy_flag == 'Y' and 'pharmacy' in gtypes:
                newResults.append(result)

        """
            sometimes google fetch's result that are not good FAP
            for e.g. 'emergency department' instead of hospital details
            so we are trying to ignore the result that not good
            self.addrref.excludewords will have list of words that needs
            to be excluded
        """
        for idx, result in enumerate(newResults):
            businessName = result.get(businessnamekey, None)
            if businessName is not None:
                for word in self.addrref.excludewords:
                    """
                        if we are searching for pharmacy then we
                        dont exclude pharmacy words else for all other
                        search we exclude pharmacy
                    """
                    if self.pharmacy_flag == 'Y' and word == 'pharmacy':
                        continue

                    if check_word(word, businessName.lower()):
                        """
                            remove this record
                        """
                        del newResults[idx]
                        break

        if len(newResults) == 1:
            return newResults[0]

        """
            second we filter based on street name
        """
        if self.addressdetails.street_name and len(self.addressdetails.street_name) > 1 and len(newResults) > 1:
            tempResults = []
            for idx, result in enumerate(newResults):
                addrString = result.get(addresskey, None)
                if addrString and len(addrString) > 2:
                    if not check_word(self.addressdetails.street_name, addrString.lower()):
                        continue
                    tempResults.append(result)

            if len(tempResults) > 0:
                newResults = tempResults

        """
            third filter is business name
            first we clean up the name, sometimes we get
            centre othertimes we center so its best to clean up
            the google name
            second based on highest matched words we pick up the best
            match name
        """
        tempResults = []
        if len(newResults) > 1 and self.business_name and \
                len(self.business_name) > 2:
            """
                let's see there is exact match of business name
            """
            for idx, result in enumerate(newResults):
                businessName = result.get(businessnamekey, None)
                if businessName and len(businessName) > 2:
                    businessName = businessName.lower()
                    businessNameList = businessName.split()
                    for idx, word in enumerate(businessNameList):
                        comWord = self.addrref.get_businesstype(word)
                        if comWord is not None:
                            businessNameList[idx] = comWord
                    businessName = " ".join(businessNameList)
                    if word_count(self.business_name, businessName) == \
                            len(self.business_name.split()):
                        tempResults.append(result)
            if len(tempResults) > 0:
                newResults = tempResults
            else:

                for idx, result in enumerate(newResults):
                    businessName = result.get(businessnamekey, None)
                    if businessName and len(businessName) > 2:
                        if word_count(self.business_name,
                                      businessName.lower()) == 0:
                            continue
                        tempResults.append(result)

                if len(tempResults) > 0:
                    newResults = tempResults

        """
            forth filter is street number
        """
        if self.street_number1 and len(str(self.street_number1)) > 0 \
                and len(newResults) > 1:
            tempResults = []
            streetnum = str(self.street_number1)
            for idx, result in enumerate(newResults):
                addrString = result.get(addresskey, None)
                if addrString and len(addrString) > 2:
                    if not check_word(streetnum, addrString.lower()):
                        continue
                    tempResults.append(result)

            if len(tempResults) > 0:
                newResults = tempResults

        if len(newResults) > 0:
            return newResults[0]
        else:
            return None
