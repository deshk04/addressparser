"""
#  Author:
#  Create date:
#  Description:    Address Mapper
#
#
#  Version     Date                Description(of Changes)
#  1.0                             Created
"""

from datetime import datetime
from django.utils.timezone import get_current_timezone
import logging

from core.general import *
from core.general import settings

from django.db.models import Q
from django.db import connection, transaction

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
import pdb


class AddressMapper():
    """
        Practice Mapper
    """

    def __init__(self, *args, **kwargs):
        self.user_id = settings.SYSTEM_USER
        # 0 for success and 1 for failure
        self.status = 0
        self.errorMessage = None
        self.staging_address = None

    def map(self):
        """
            let's map the output
        """
        from core.models.coreproxy import AddressDetailsProxy

        if not self.staging_address:
            self.seterror('Mandatory fields missing')
            return None

        if not self.staging_address.state or \
                not self.staging_address.postcode:
            self.seterror('Postcode or state is missing')
            return None


        if not self.staging_address.pobox_number:
            if not self.staging_address.street_name or \
                    not self.staging_address.number_first:
                self.seterror('street details is missing')
                return None

        """
            check if the address already exists
        """
        address_details_queryset = AddressDetailsProxy.objects.filter(
            pobox_type=self.staging_address.pobox_type,
            pobox_number=self.staging_address.pobox_number,
            building_name=self.staging_address.building_name,
            flat_number=self.staging_address.flat_number,
            flat_type=self.staging_address.flat_type,
            flat_number_suffix=self.staging_address.flat_number_suffix,
            level_number=self.staging_address.level_number,
            level_type=self.staging_address.level_type,
            level_number_suffix=self.staging_address.level_number_suffix,
            number_first=self.staging_address.number_first,
            number_suffix=self.staging_address.number_suffix,
            number_last=self.staging_address.number_last,
            street_name=self.staging_address.street_name,
            street_type=self.staging_address.street_type,
            suburb=self.staging_address.suburb,
            postcode=self.staging_address.postcode,
            state=self.staging_address.state
        )
        if len(address_details_queryset) > 0:
            address_details = address_details_queryset[0]
            if address_details.premises_type is None or \
                    address_details.premises_type == 'R':
                address_details.premises_type = self.staging_address.premises_type  # noqa
                address_details.save()

            if address_details.premises_type in ['R', 'C'] and\
                    self.staging_address.premises_type == 'S':
                address_details.premises_type = 'S'
                address_details.save()
            return address_details.address_id

        else:
            cursor = connection.cursor()
            cursor.execute("select nextval('address_details_address_id_seq')")
            result = cursor.fetchone()
            address_id = result[0]

            address_details = AddressDetailsProxy(
                address_id=address_id,
                record_creation_date=datetime.now(tz=get_current_timezone()),
                record_user=self.user_id,
                pobox_type=self.staging_address.pobox_type,
                pobox_number=self.staging_address.pobox_number,
                building_name=self.staging_address.building_name,
                flat_number=self.staging_address.flat_number,
                flat_type=self.staging_address.flat_type,
                flat_number_suffix=self.staging_address.flat_number_suffix,
                level_number=self.staging_address.level_number,
                level_type=self.staging_address.level_type,
                level_number_suffix=self.staging_address.level_number_suffix,
                number_first=self.staging_address.number_first,
                number_suffix=self.staging_address.number_suffix,
                number_last=self.staging_address.number_last,
                street_name=self.staging_address.street_name,
                street_type=self.staging_address.street_type,
                suburb=self.staging_address.suburb,
                postcode=self.staging_address.postcode,
                state=self.staging_address.state,
                latitude=self.staging_address.latitude,
                longitude=self.staging_address.longitude,
                parcel_id=self.staging_address.parcel_id,
                premises_type=self.staging_address.premises_type
            )
            try:
                address_details.save()
            except:
                self.seterror('Error storing address')
                return None

            return address_details.address_id


    def seterror(self, message):
        """
            set error message
        """
        self.status = 1
        self.errorMessage = message
        logging.error(message)
