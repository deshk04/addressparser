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

    def execute(self):
        """
            for the time, we are fetching best matched record
        """
        if self.dbObj is None or not self.addressdetails:
            raise MandatoryFieldMissing

        self.confidence = 0
        """
            Gnaf is millions of records to best to filter the data
        """
        self.base_set()
        if self.gnafRecs.empty:
            return None

        if self.addressdetails.number_first:
            found = self.filter_records('number_first', self.addressdetails.number_first)
            if found:
                if self.addressdetails.flat_type and self.addressdetails.flat_number:
                    self.filter_records('flat_type', self.addressdetails.flat_type)
                    self.filter_records('flat_number', self.addressdetails.flat_number)
                if self.addressdetails.level_type and self.addressdetails.level_number:
                    self.filter_records('level_type', self.addressdetails.level_type)
                    self.filter_records('level_number', self.addressdetails.level_number)
        return self.final_record()


    def base_set(self):
        """
          fetch the baseset based on postcode / state
        """
        self.gnafRecs = pd.DataFrame()
        if self.addressdetails.street_name and self.addressdetails.state:

            """
                some postcode falls under 2 states
            """
            addrDim = AddressReference()
            tempStates = addrDim.gnafpostcodes[self.addressdetails.postcode]
            sqlQuery = ''
            if tempStates and len(tempStates) == 2:
                sqlQuery = """SELECT t1.*
                                from dim_gnaf_address_details t1
                                where (state_abbreviation='{0}'
                                or state_abbreviation='{1}')
                                and (postcode = '{2}'
                                   or locality_name = '{3}')
                                and street_name = '{4}'
                                """
                sqlQuery = sqlQuery.format(tempStates[0],
                                           tempStates[1],
                                           self.addressdetails.postcode,
                                           self.addressdetails.suburb,
                                           self.addressdetails.street_name
                                           )

            else:
                sqlQuery = """SELECT t1.*
                            from dim_gnaf_address_details t1
                            where state_abbreviation='{0}'
                            and (postcode = '{1}' or locality_name = '{2}')
                            and street_name = '{3}'
                            """
                sqlQuery = sqlQuery.format(self.addressdetails.state,
                                           self.addressdetails.postcode,
                                           self.addressdetails.suburb,
                                           self.addressdetails.street_name
                                           )
        else:
            sqlQuery = """SELECT t1.*
                            from dim_gnaf_address_details t1
                            where (state_abbreviation='{0}'
                            or state_abbreviation='{1}')
                            and (postcode = '{2}'
                                or locality_name = '{3}')
                            """
            sqlQuery = sqlQuery.format(tempStates[0],
                                        tempStates[1],
                                        self.addressdetails.postcode,
                                        self.addressdetails.suburb
                                        )

        self.gnafRecs = pd.read_sql_query(
            sqlQuery,
            self.dbObj.connstring
        )

    def filter_records(self, field_name, field_value):
        """
          filter records
        """
        recs = self.filter_field(field_name, field_value)
        if not recs.empty:
            self.confidence +=1
            self.gnafRecs = recs
            return True

        return False

    def filter_field(self, gfield, addr_field):
        """
          filter records
        """
        if addr_field and not self.gnafRecs.empty:
            data = self.gnafRecs[self.gnafRecs[gfield] == addr_field]
            return data

        """
            we can not send null since the above send dataframe
            so let's send an empty dataframe
        """
        return pd.DataFrame()


    def final_record(self):
        """
          consider first record as final record as
          we are more interested in geo-cordinates
        """
        from core.models.coreproxy import DimGnafAddressDetailsProxy
        record = self.gnafRecs.iloc[0]
        gnafAddr = DimGnafAddressDetailsProxy(
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
        if gnafAddr.flat_number and np.isnan(gnafAddr.flat_number):
            gnafAddr.flat_number = None
        if gnafAddr.level_number and np.isnan(gnafAddr.level_number):
            gnafAddr.level_number = None
        if gnafAddr.number_first and np.isnan(gnafAddr.number_first):
            gnafAddr.number_first = None
        if gnafAddr.number_last and np.isnan(gnafAddr.number_last):
            gnafAddr.number_last = None
        return gnafAddr


