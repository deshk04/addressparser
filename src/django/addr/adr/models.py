from django.db import models


class AddressDetails(models.Model):
    system_creation_date = models.DateTimeField(blank=True, null=True)
    system_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    address_id = models.BigIntegerField(unique=True)
    pobox_type = models.TextField(blank=True, null=True)
    pobox_number = models.TextField(blank=True, null=True)
    building_name = models.TextField(blank=True, null=True)
    department_name = models.TextField(blank=True, null=True)
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

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'address_details'


class DimAddrAbbrWords(models.Model):
    suffixword = models.CharField(primary_key=True, max_length=30)
    primaryword = models.CharField(max_length=60)
    typeflag = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_addr_abbr_words'
        unique_together = (('suffixword', 'primaryword'),)


class DimAddrCommonwords(models.Model):
    word = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_addr_commonwords'


class DimAddrPatch(models.Model):
    sourcestring = models.CharField(max_length=80, blank=True, null=True)
    destinationstring = models.CharField(max_length=80, blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_addr_patch'


class DimAddrPobox(models.Model):
    pobox = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_addr_pobox'


class DimAddressType(models.Model):
    address_type = models.CharField(primary_key=True, max_length=1)
    address_type_desc = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_address_type'


class DimCommonWords(models.Model):
    word = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_common_words'


class DimGnafPostcode(models.Model):
    postcode = models.CharField(max_length=4, blank=True, null=True)
    state = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_gnaf_postcode'


class DimGnafStreets(models.Model):
    street_name = models.CharField(max_length=100, blank=True, null=True)
    street_type = models.CharField(max_length=15, blank=True, null=True)
    suburb = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=4, blank=True, null=True)
    state = models.CharField(max_length=3, blank=True, null=True)
    street_length = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_gnaf_streets'


class DimNameAbbr(models.Model):
    name = models.CharField(max_length=60, blank=True, null=True)
    shortname = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_name_abbr'


class DimPobox(models.Model):
    pobox = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_pobox'


class DimWordDictionary(models.Model):
    mainword = models.TextField(blank=True, null=True)
    suffixword = models.TextField(blank=True, null=True)
    wordtype = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_word_dictionary'


class GooglePlaces(models.Model):
    place_id = models.TextField(unique=True, blank=True, null=True)
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    street_number = models.TextField(blank=True, null=True)
    street_name = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    suburb = models.TextField(blank=True, null=True)
    county = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    postcode = models.TextField(blank=True, null=True)
    neighborhood = models.TextField(blank=True, null=True)
    sublocality = models.TextField(blank=True, null=True)
    housenumber = models.TextField(blank=True, null=True)
    town = models.TextField(blank=True, null=True)
    subpremise = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    location_type = models.TextField(blank=True, null=True)
    postal_code_suffix = models.TextField(blank=True, null=True)
    business_name = models.TextField(blank=True, null=True)
    formatted_phone_number = models.TextField(blank=True, null=True)
    international_phone_number = models.TextField(blank=True, null=True)
    trading_hours_mon = models.TextField(blank=True, null=True)
    trading_hours_tue = models.TextField(blank=True, null=True)
    trading_hours_wed = models.TextField(blank=True, null=True)
    trading_hours_thu = models.TextField(blank=True, null=True)
    trading_hours_fri = models.TextField(blank=True, null=True)
    trading_hours_sat = models.TextField(blank=True, null=True)
    trading_hours_sun = models.TextField(blank=True, null=True)
    web_website = models.TextField(blank=True, null=True)
    permanently_closed = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    price_level = models.TextField(blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    types = models.TextField(blank=True, null=True)  # This field type is a guess.
    exception_flag = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'google_places'


class StagingInputData(models.Model):
    system_creation_date = models.DateTimeField(blank=True, null=True)
    system_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    system_type = models.TextField(blank=True, null=True)
    source_key = models.TextField(blank=True, null=True)
    address_type = models.TextField(blank=True, null=True)
    address_line1 = models.TextField(blank=True, null=True)
    address_line2 = models.TextField(blank=True, null=True)
    suburb = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=4, blank=True, null=True)
    state = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'staging_input_data'


class StagingProcessedAddress(models.Model):
    system_creation_date = models.DateTimeField(blank=True, null=True)
    system_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    source_input = models.ForeignKey(StagingInputData, models.DO_NOTHING, blank=True, null=True)
    pobox_type = models.TextField(blank=True, null=True)
    pobox_number = models.TextField(blank=True, null=True)
    building_name = models.TextField(blank=True, null=True)
    department_name = models.TextField(blank=True, null=True)
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
    rank = models.IntegerField(blank=True, null=True)
    exception_flag = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'staging_processed_address'
