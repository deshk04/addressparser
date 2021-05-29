import logging
from datetime import datetime
import pandas as pd
import numpy as np

from core.general.exceptions import *
from core.general import settings
from core.parser.addressreference import AddressReference

import pdb


class GnafHandler():
    """
        match against gnaf dataset
    """

    def __init__(self, *args, **kwargs):
        self.dbObj = None
        self.addressdetails = None
        self.gnafRecs = pd.DataFrame()
        self.confidence = 0
        self.gnafAddr = None
        self.distance_meters = None

    def execute(self):
        """
            for the time, we are fetching best matched record
        """
        from core.models import DimGnafAddressDetailsProxy

        if self.dbObj is None or not self.addressdetails:
            raise MandatoryFieldMissing

        self.confidence = 0
        self.distance_meters = None
        """
            comparison with gnaf database is time consuming
            gnaf has around 14.3 million records, so we have to find
            a way to optimise the comparison
        """
        # pdb.set_trace()

        if self.addressdetails.confidence > 1:
            self.streetnum_name()
            self.match_records()

    def street_name(self):
        """
          search based on the address details ignore google data
        """
        self.gnafRecs = pd.DataFrame()
        if self.addressdetails.street_name and self.addressdetails.state:

            """
                some postcode falls under 2 states
            """
            addrDim = AddressReference()
            tempStates = addrDim.gnafPostcode[self.addressdetails.postcode]
            sqlQuery = ''
            if tempStates and len(tempStates) == 2:
                sqlQuery = """SELECT t1.*, 0 distance_meters
                                from dim_gnaf_address_details t1
                                where (state_abbreviation='{0}'
                                or state_abbreviation='{3}')
                                and street_name='{1}'
                                and (postcode = '{4}'
                                   or locality_name = '{5}')
                                """
                sqlQuery = sqlQuery.format(tempStates[0],
                                           self.addressdetails.street_name,
                                           self.addressdetails.number_first,
                                           tempStates[1],
                                           self.addressdetails.postcode,
                                           self.addressdetails.suburb
                                           )

            else:
                sqlQuery = """SELECT t1.*, 0 distance_meters
                            from dim_gnaf_address_details t1
                            where state_abbreviation='{0}'
                            and street_name='{1}'
                            and (postcode = '{3}' or locality_name = '{4}')
                            """
                sqlQuery = sqlQuery.format(self.addressdetails.state,
                                           self.addressdetails.street_name,
                                           self.addressdetails.number_first,
                                           self.addressdetails.postcode,
                                           self.addressdetails.suburb
                                           )
            # print(sqlQuery)
            self.gnafRecs = pd.read_sql_query(
                sqlQuery,
                self.dbObj.dbConnStr
            )

    def streetnum_name(self):
        """
          search based on the address details ignore google data
        """
        self.gnafRecs = pd.DataFrame()
        if self.addressdetails.street_name and self.addressdetails.number_first and \
                self.addressdetails.state:

            """
                some postcode falls under 2 states
            """
            addrDim = AddressReference()
            tempStates = addrDim.gnafPostcode[self.addressdetails.postcode]
            sqlQuery = ''
            if tempStates and len(tempStates) == 2:
                sqlQuery = """SELECT t1.*, 0 distance_meters
                                from dim_gnaf_address_details t1
                                where (state_abbreviation='{0}'
                                or state_abbreviation='{3}')
                                and street_name='{1}'
                                and (postcode = '{4}'
                                   or locality_name = '{5}')
                                and (COALESCE(number_first,-1) = {2}
                                or ({2} between COALESCE(number_first,-1)
                                and COALESCE(number_last,-1))
                                )
                                """
                sqlQuery = sqlQuery.format(tempStates[0],
                                           self.addressdetails.street_name,
                                           self.addressdetails.number_first,
                                           tempStates[1],
                                           self.addressdetails.postcode,
                                           self.addressdetails.suburb
                                           )

            else:
                sqlQuery = """SELECT t1.*, 0 distance_meters
                            from dim_gnaf_address_details t1
                            where state_abbreviation='{0}'
                            and street_name='{1}'
                            and (postcode = '{3}' or locality_name = '{4}')
                            and (COALESCE(number_first,-1) = {2}
                            or ({2} between COALESCE(number_first,-1)
                            and COALESCE(number_last,-1))
                            )
                            """
                sqlQuery = sqlQuery.format(self.addressdetails.state,
                                           self.addressdetails.street_name,
                                           self.addressdetails.number_first,
                                           self.addressdetails.postcode,
                                           self.addressdetails.suburb
                                           )
            # print(sqlQuery)
            self.gnafRecs = pd.read_sql_query(
                sqlQuery,
                self.dbObj.dbConnStr
            )

    def match_records(self):
        """
          we try to find the best possible match
        """
        """
            first filter it based on number suffix
        """
        if self.gnafRecs.empty:
            return

        self.gnafRecsMatched = self.gnafRecs
        self.filter_street_suff()
        if len(self.gnafRecsMatched) > 1:
            self.filter_flat()
            if len(self.gnafRecsMatched) > 1:
                self.filter_level()

        """
            we still have more records we need to fetch
            only one record
        """
        if len(self.gnafRecsMatched) > 0:
            """
                order by confidence desc, legal_parcel_id
            """
            # pdb.set_trace()
            self.gnafRecsMatched = self.gnafRecsMatched.sort_values(
                ['distance_meters', 'confidence', 'legal_parcel_id'],
                ascending=[True, False, True]
            )
            self.final_record()

    def final_record(self):
        """
          find gnaf data based on street_num and geo cordinates
        """
        self.distance_meters = None
        # pdb.set_trace()
        from core.models import DimGnafAddressDetailsProxy
        if not self.gnafRecsMatched.empty:
            """
             we populate self.gnafAddr
            """
            record = self.gnafRecsMatched.iloc[0]
            self.gnafAddr = DimGnafAddressDetailsProxy(
                address_detail_pid=record.address_detail_pid,
                street_locality_pid=record.street_locality_pid,
                locality_pid=record.locality_pid,
                building_name=record.building_name,
                lot_number_prefix=record.lot_number_prefix,
                lot_number=record.lot_number,
                lot_number_suffix=record.lot_number_suffix,
                flat_type=record.flat_type,
                flat_number_prefix=record.flat_number_prefix,
                flat_number=record.flat_number,
                flat_number_suffix=record.flat_number_suffix,
                level_type=record.level_type,
                level_number_prefix=record.level_number_prefix,
                level_number=record.level_number,
                level_number_suffix=record.level_number_suffix,
                number_first_prefix=record.number_first_prefix,
                number_first=record.number_first,
                number_first_suffix=record.number_first_suffix,
                number_last_prefix=record.number_last_prefix,
                number_last=record.number_last,
                number_last_suffix=record.number_last_suffix,
                street_name=record.street_name,
                street_class_code=record.street_class_code,
                street_class_type=record.street_class_type,
                street_type_code=record.street_type_code,
                street_suffix_code=record.street_suffix_code,
                street_suffix_type=record.street_suffix_type,
                locality_name=record.locality_name,
                state_abbreviation=record.state_abbreviation,
                postcode=record.postcode,
                latitude=record.latitude,
                longitude=record.longitude,
                geocode_type=record.geocode_type,
                confidence=record.confidence,
                alias_principal=record.alias_principal,
                primary_secondary=record.primary_secondary,
                legal_parcel_id=record.legal_parcel_id,
                date_created=record.date_created
            )
            """
                pandas converts None to NaN
                which is not good for us to convert it to None
            """
            # pdb.set_trace()
            if self.gnafAddr.flat_number and \
                    np.isnan(self.gnafAddr.flat_number):
                self.gnafAddr.flat_number = None
            if self.gnafAddr.level_number and \
                    np.isnan(self.gnafAddr.level_number):
                self.gnafAddr.level_number = None
            if self.gnafAddr.number_first and \
                    np.isnan(self.gnafAddr.number_first):
                self.gnafAddr.number_first = None
            if self.gnafAddr.number_last and \
                    np.isnan(self.gnafAddr.number_last):
                self.gnafAddr.number_last = None

            self.distance_meters = record.distance_meters
            self.confidence += 1

    def filter_street_name(self):
        """
          filter records
        """
        # pdb.set_trace()
        emptyFrame = pd.DataFrame()
        recs = self.filter_field('street_name',
                                 self.addressdetails.street_name, emptyFrame)
        if not recs.empty:
            self.gnafRecsMatched = recs
            self.confidence += 1

    def filter_street_suff(self):
        """
          filter records
        """
        emptyFrame = pd.DataFrame()
        recs = self.filter_field('number_first_suffix',
                                 self.addressdetails.number_suffix, emptyFrame)
        if not recs.empty:
            self.gnafRecsMatched = recs
            self.confidence += 1

    def filter_flat(self):
        """
          filter records
        """
        # pdb.set_trace()
        emptyFrame = pd.DataFrame()
        if self.addressdetails.flat_type and self.addressdetails.flat_number:
            recs = self.filter_field('flat_type',
                                     self.addressdetails.flat_type, emptyFrame)
            if not recs.empty:
                recs = self.filter_field('flat_number',
                                         self.addressdetails.flat_number, recs)
                if not recs.empty:
                    self.gnafRecsMatched = recs
                    self.confidence += 1
                    if self.addressdetails.flat_number_suffix:
                        recs = self.filter_field('flat_number_suffix',
                                                 self.addressdetails.flat_number_suffix,
                                                 emptyFrame)
                        if not recs.empty:
                            self.gnafRecsMatched = recs

    def filter_level(self):
        """
          filter records
        """
        emptyFrame = pd.DataFrame()
        if self.addressdetails.level_type and self.addressdetails.level_number:
            recs = self.filter_field('level_type',
                                     self.addressdetails.level_type, emptyFrame)
            if not recs.empty:
                recs = self.filter_field('level_number',
                                         self.addressdetails.level_number, recs)
                if not recs.empty:
                    self.gnafRecsMatched = recs
                    self.confidence += 1
                    recs = self.filter_field('level_number_suffix',
                                             self.addressdetails.level_number_suffix,
                                             emptyFrame)
                    if not recs.empty:
                        self.gnafRecsMatched = recs

    def filter_field(self, gfield, addr_field, df):
        """
          filter records
        """
        # if len(self.gnafRecsMatched) <= 1:
        #     return
        if df.empty:
            df = self.gnafRecsMatched

        if addr_field and not df.empty:
            data = df[df[gfield] == addr_field]
            return data

        """
            we can not send null since the above send dataframe
            so let's send an empty dataframe
        """
        return pd.DataFrame()

