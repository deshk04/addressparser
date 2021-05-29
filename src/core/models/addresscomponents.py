"""
  Author:
  Create date:
  Description:     modules for django orm


  Version     Date                Description(of Changes)
  1.0                             Created
"""

from django.db import models


class AddressComponents():

    pobox_type = models.TextField(blank=True, null=True)
    pobox_number = models.TextField(blank=True, null=True)
    building_name = models.TextField(blank=True, null=True)
    business_name = models.TextField(blank=True, null=True)
    flat_number = models.TextField(blank=True, null=True)
    flat_type = models.TextField(blank=True, null=True)
    flat_number_suffix = models.TextField(blank=True, null=True)
    level_number = models.TextField(blank=True, null=True)
    level_type = models.TextField(blank=True, null=True)
    level_number_suffix = models.TextField(blank=True, null=True)
    number_first = models.TextField(blank=True, null=True)
    number_suffix = models.TextField(blank=True, null=True)
    number_last = models.TextField(blank=True, null=True)
    street_name = models.TextField(blank=True, null=True)
    street_type = models.TextField(blank=True, null=True)
    suburb = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=4, blank=True, null=True)
    state = models.CharField(max_length=4, blank=True, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    parcel_id = models.TextField(blank=True, null=True)
    premises_type = models.TextField(blank=True, null=True)
    postal_id = models.TextField(blank=True, null=True)
    confidence = models.DecimalField(
        max_digits=2, decimal_places=0, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)
